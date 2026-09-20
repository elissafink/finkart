#!/usr/bin/env python3
"""
Download every image this site uses from finkart.com into an "images" folder
next to this script, and point every page at the local copies.

Run it once, while the original site (finkart.com) is still online:

    python3 localize-images.py

Needs Python 3.6+ and an internet connection. No extra packages.
Safe to re-run: files already downloaded are skipped, and pages that already
point at local copies are left alone.
"""
import os, re, sys, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor

BASE = os.environ.get("FINKART_BASE", "https://finkart.com")
PREFIX = BASE.rstrip("/") + "/wp-content/uploads/"
ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(ROOT, "images")
PATTERN = re.compile(re.escape(PREFIX) + r"[^\"'<>\s]+")

def html_files():
    for dp, _, fs in os.walk(ROOT):
        for f in fs:
            if f.endswith(".html"):
                yield os.path.join(dp, f)

def local_path(url):
    return os.path.join(IMG_DIR, urllib.parse.unquote(url[len(PREFIX):]).replace("/", os.sep))

def fetch(url):
    dest = local_path(url)
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return url, True, "already downloaded"
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (site-localizer)"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r, open(dest + ".part", "wb") as out:
            while True:
                chunk = r.read(65536)
                if not chunk:
                    break
                out.write(chunk)
        os.replace(dest + ".part", dest)
        return url, True, "ok"
    except Exception as e:
        if os.path.exists(dest + ".part"):
            os.remove(dest + ".part")
        return url, False, str(e)

def main():
    pages = list(html_files())
    urls = set()
    for p in pages:
        with open(p, encoding="utf-8") as f:
            urls.update(PATTERN.findall(f.read()))
    if not urls:
        print("No finkart.com image links found. Nothing to do.")
        return
    print(f"Downloading {len(urls)} images...")
    ok, failed = set(), []
    with ThreadPoolExecutor(max_workers=6) as ex:
        for n, (url, good, msg) in enumerate(ex.map(fetch, sorted(urls)), 1):
            if good:
                ok.add(url)
            else:
                failed.append((url, msg))
            if n % 25 == 0 or n == len(urls):
                print(f"  {n}/{len(urls)}")
    for p in pages:
        with open(p, encoding="utf-8") as f:
            text = f.read()
        page_dir = os.path.dirname(p)
        def swap(m):
            url = m.group(0)
            if url not in ok:
                return url  # keep the online link if the download failed
            rel = os.path.relpath(local_path(url), page_dir).replace(os.sep, "/")
            return urllib.parse.quote(rel, safe="/-._~")
        new = PATTERN.sub(swap, text)
        if new != text:
            with open(p, "w", encoding="utf-8") as f:
                f.write(new)
    print(f"\nDone. {len(ok)} images are now local, in: {IMG_DIR}")
    if failed:
        print(f"\n{len(failed)} could not be downloaded (those pages still use the online link):")
        for url, msg in failed:
            print(f"  {url}  ({msg})")
        sys.exit(1)

if __name__ == "__main__":
    main()
