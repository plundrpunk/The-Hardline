#!/usr/bin/env python3
"""Build the GitHub Pages copy of THE HARDLINE from the artifact's HTML.

  python3 build.py ARTIFACT.html        # writes index.html next to this script

ARTIFACT.html is the file the Artifact tool saves on a read (wrapped or not).
Exits non-zero, writing nothing, if the page doesn't look whole.
"""
import os, re, sys

HEAD = """<!doctype html><html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="THE HARDLINE — seven-city live-music zine. Punk, hardcore, rock'n'roll, ska, reggae, funk, jazz, blues, bluegrass across NFK, RVA, DC, CLT, RDU, CHS, CAE.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 100 100%27%3E%3Ctext y=%27.9em%27 font-size=%2790%27%3E🤘%3C/text%3E%3C/svg%3E">
"""

src = open(sys.argv[1], encoding="utf8").read()
a, b, c = src.find("<title>"), src.find('<div class="wrap">'), src.rfind("</script>")
if not 0 <= a < b < c:
    sys.exit("build: page markers missing")
top, body = src[a:b].rstrip(), src[b:c + len("</script>")]
out = HEAD + top + "\n</head><body>\n" + body + "\n</body></html>\n"
m = re.search(r'const DATA_UPDATED="(\d{4}-\d\d-\d\d)"', out)
ok = m and all(s in out for s in ("const CITIES=", "const VENUES=", "const WIRE=", "const IMGS=")) and len(out) > 1_000_000
if not ok:
    sys.exit("build: page incomplete (%d bytes)" % len(out))
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html"), "w", encoding="utf8").write(out)
print("built index.html: data %s, %d bytes" % (m.group(1), len(out)))
