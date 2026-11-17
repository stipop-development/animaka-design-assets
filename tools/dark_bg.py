import re, sys
sys.path.insert(0, 'tools')
from build_light import homefix
ROLE = {'page': ['#0b0a10', '#0d0b13', '#0f0d17'], 'side': ['#13101c', '#13111c'],
        'surf': ['#17151f', '#16131f', '#1b1726', '#1d1928', '#1a1726', '#1c1828', '#15121e', '#13101b'],
        'surf2': ['#2a2236', '#231f33', '#221d2e', '#262033', '#2a2235', '#2a2536']}
VARIANTS = {
    'A_current': None,
    'B_black': dict(page='#000000', side='#000000', surf='#121212', surf2='#1e1e1e', glow=False, sideborder='rgba(255,255,255,0.10)'),
    'C_charcoal': dict(page='#0f0f10', side='#0f0f10', surf='#1a1a1c', surf2='#242427', glow=False, sideborder='rgba(255,255,255,0.08)'),
    'D_ink': dict(page='#0c0c10', side='#111116', surf='#18181f', surf2='#22222b', glow=False, sideborder='rgba(255,255,255,0.06)'),
    'E_black_side': dict(page='#000000', side='#111113', surf='#141416', surf2='#202024', glow=False, sideborder='rgba(255,255,255,0.0)'),
}
def recolor(s, p):
    head, sep, rest = s.partition('</helmet>')
    body, sep2, tail = rest.partition('</x-dc>')
    head = head.replace('background:#0b0a10', 'background:' + p['page'])
    def fix_decl(d):
        k, v = d.split(':', 1)
        if not k.strip().lower().startswith('background'):
            return d
        if not p['glow'] and 'radial-gradient' in v and 'rgba(192,77,255' in v:
            v = ' ' + p['page']
        for role in ('page', 'side', 'surf', 'surf2'):
            for hx in ROLE[role]:
                v = re.sub(re.escape(hx) + r'\b', p[role], v, flags=re.I)
        v = re.sub(r'linear-gradient\(180deg, (#[0-9a-f]{6}) 0%, \1 100%\)', r'\1', v)
        return k + ':' + v
    def fix_style(m):
        st = m.group(1)
        st = ';'.join(fix_decl(d) if ':' in d else d for d in st.split(';'))
        if 'aria-label' in m.group(0):
            pass
        return 'style="' + st + '"'
    body = re.sub(r'style="([^"]*)"', fix_style, body)
    # sidebar right border
    body = body.replace('border-right: 1px solid rgba(255,255,255,0.08)', 'border-right: 1px solid ' + p['sideborder'])
    return head + sep + body + sep2 + tail

if __name__ == '__main__':
    base = homefix(open('home-renewal/design/Main14.dc.html').read(), 'home')
    base = base.replace('min-height: 40px; padding: 4px 10px 4px 12px', 'min-height: 44px; padding: 4px 10px 4px 12px')
    for name, p in VARIANTS.items():
        s = base if p is None else recolor(base, p)
        s = re.sub(r'<title>(.*?)</title>', '<title>다크 배경 ' + name + '</title>', s, count=1)
        open(f'home-renewal/design/D_{name}.dc.html', 'w').write(s)
        print(name)
