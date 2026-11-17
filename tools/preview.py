"""Static preview of a .dc.html board: resolves sc-if with hint/placeholder or given vars, fills {{holes}}, screenshots with Chrome.
usage: preview.py board.dc.html out.png width height [var=value ...]
"""
import re, sys, os, asyncio
from playwright.async_api import async_playwright

BLOBMAP = {}
mp = os.path.join(os.path.dirname(__file__), 'blobmap.txt')
if os.path.exists(mp):
    for line in open(mp):
        if line.strip():
            k, v = line.split()
            BLOBMAP['/_blob/' + k] = 'file://' + v


def render(src, vars):
    s = open(src).read()
    head = re.search(r'<helmet>(.*?)</helmet>', s, re.S)
    head = head.group(1) if head else ''
    body = s.split('</helmet>', 1)[1].split('</x-dc>', 1)[0] if '</helmet>' in s else s
    def ev(expr):
        expr = expr.strip()
        if expr in vars: return vars[expr]
        return None
    # resolve sc-if (innermost first)
    pat = re.compile(r'<sc-if value="\{\{\s*([^}]*?)\s*\}\}"(?: hint-placeholder-val="\{\{\s*([^}]*?)\s*\}\}")?>((?:(?!<sc-if).)*?)</sc-if>', re.S)
    while True:
        m = pat.search(body)
        if not m: break
        v = ev(m.group(1))
        if v is None: v = (m.group(2) or 'false').strip() == 'true'
        body = body[:m.start()] + (m.group(3) if v in (True, 'true') else '') + body[m.end():]
    body = re.sub(r'\{\{\s*([^}]*?)\s*\}\}', lambda m: str(vars.get(m.group(1).strip(), '')), body)
    for k, v in BLOBMAP.items():
        body = body.replace(k, v)
    return '<!doctype html><html><head><meta charset="utf-8">' + head + '</head><body>' + body + '</body></html>'


async def shot(html, out, w, h):
    p = out + '.html'
    open(p, 'w').write(html)
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files'])
        pg = await b.new_page(viewport={'width': w, 'height': h})
        await pg.goto('file://' + p)
        await pg.wait_for_timeout(1500)
        await pg.screenshot(path=out, full_page=False)
        await b.close()


if __name__ == '__main__':
    src, out, w, h = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    vars = {}
    for a in sys.argv[5:]:
        k, v = a.split('=', 1)
        vars[k] = True if v == 'true' else False if v == 'false' else v
    asyncio.run(shot(render(src, vars), out, w, h))
