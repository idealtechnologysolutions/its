/* Full-page screenshots of every built page at 375, 768 and 1280px.

   node tools/screenshots.cjs <puppeteer-core install dir>

   Serves site/ on a free local port, finds every page that is not a stub,
   and saves docs/screenshots/<name>-<width>.png, where <name> is "home" for
   the homepage and the last slug segment otherwise. Old screenshots are
   deleted first, so the folder always matches the current build.

   puppeteer-core is installed outside the repo (see tools/README.md), so no
   package files or node_modules land in the repo. Chrome is found at
   CHROME_PATH, or the default Windows install path. */

const fs = require("fs");
const http = require("http");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const SITE = path.join(ROOT, "site");
const OUT = path.join(ROOT, "docs", "screenshots");
const WIDTHS = [375, 768, 1280];
const CHROME = process.env.CHROME_PATH || "C:/Program Files/Google/Chrome/Application/chrome.exe";
const TYPES = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml", ".png": "image/png", ".txt": "text/plain" };

const installDir = process.argv[2];
if (!installDir) {
  console.error("usage: node tools/screenshots.cjs <puppeteer-core install dir>");
  process.exit(2);
}
const puppeteer = require(require.resolve("puppeteer-core", { paths: [path.resolve(installDir)] }));

function builtPages(dir = SITE) {
  let pages = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory() && entry.name !== "assets") pages = pages.concat(builtPages(full));
    if (entry.isFile() && entry.name === "index.html" && !fs.readFileSync(full, "utf8").includes('<main id="main" class="stub">')) {
      const rel = path.relative(SITE, dir).split(path.sep).join("/");
      pages.push({ url: rel ? `/${rel}/` : "/", name: rel ? rel.split("/").pop() : "home" });
    }
  }
  return pages;
}

function serve() {
  const server = http.createServer((req, res) => {
    let file = path.join(SITE, decodeURIComponent(req.url.split("?")[0]));
    if (!file.startsWith(SITE)) { res.writeHead(403).end(); return; }
    if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, "index.html");
    if (!fs.existsSync(file)) { res.writeHead(404).end(); return; }
    res.writeHead(200, { "Content-Type": TYPES[path.extname(file)] || "application/octet-stream" });
    fs.createReadStream(file).pipe(res);
  });
  return new Promise(resolve => server.listen(0, "127.0.0.1", () => resolve(server)));
}

(async () => {
  const pages = builtPages();
  fs.mkdirSync(OUT, { recursive: true });
  for (const old of fs.readdirSync(OUT).filter(f => f.endsWith(".png"))) fs.unlinkSync(path.join(OUT, old));

  const server = await serve();
  const base = `http://127.0.0.1:${server.address().port}`;
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: true });
  try {
    for (const { url, name } of pages) {
      for (const width of WIDTHS) {
        const page = await browser.newPage();
        await page.setViewport({ width, height: 900 });
        await page.goto(base + url, { waitUntil: "networkidle0" });
        await page.evaluate(() => document.fonts.ready);
        await new Promise(r => setTimeout(r, 2000)); // let the hero animation finish
        const file = path.join(OUT, `${name}-${width}.png`);
        await page.screenshot({ path: file, fullPage: true });
        console.log("saved", path.relative(ROOT, file).split(path.sep).join("/"));
        await page.close();
      }
    }
  } finally {
    await browser.close();
    server.close();
  }
})().catch(err => { console.error(err); process.exit(1); });
