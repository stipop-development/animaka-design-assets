import sys, re, os
sys.path.insert(0, 'tools')
from light import convert
B = {'c01_idol':'1ebdbff0d066a223b306e7dff07f6272','c02_idol_secret':'3f70b5c0882b3b44c3272fb6b8f0691d','c03_sharehouse':'0db405bd3e41a5c08379f0c28c046cda','c04_dorm':'ce6764cc314a1f59cb0065cac6f350c7','c05_ntr':'86aa6fe5fc680ef962f3fe14a53fe207','c06_tsundere':'7dcbe240edbc92204d0cbcef99df4979','c07_konbini':'ecaa5854cef2a6c42b1713075758bfed','c08_streamer':'01b33091e880a1cfe59d1e70eb724985','c09_boss':'8ee4bc03b8330856ccd4e8e0fc93bc81','c10_library':'0c7c69ab24b578199d4749fde14b1d52','u01_c01_beach':'fea9ac5bf7af50ebbdf8e5fcd07c7bca','u02_c06_yukata':'defb7ebcc4725dc4963f7db0cf1a8576','u04_c08_cosplay':'1b3214766389e78e33fd72453613e222','u05_c09_office_night':'c8fe7c11bd9f8d2198220c38817a7e0f'}
DMM = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'%3E%3Ccircle cx='10' cy='10' r='10' fill='%23ff6a00'/%3E%3Ctext x='10' y='14.5' text-anchor='middle' font-family='Arial' font-weight='900' font-size='13' fill='white'%3EP%3C/text%3E%3C/svg%3E"
nav = open('nav-redesign/design/Main.dc.html').read()
i = nav.find('<sc-if value="{{is_none}}"'); i = nav.find('>', i) + 1; j = nav.find('</sc-if>', i)
SIDE = nav[i:j].replace('min-height: 1500px', 'min-height: 100%')
SEL = 'background: rgba(255,61,127,0.14); color: #ffffff;'
UNSEL = 'background: transparent; color: #c9c4da;'
BAR = '<span style="position: absolute; left: 0; top: 10px; bottom: 10px; width: 3px; border-radius: 3px; background: #ff3d7f"></span>'

def side(active):
    s = SIDE
    if active == 'chars':
        k = s.find('キャラをさがす</'); a = s.rfind('<a ', 0, k)
        h = s.find('ホーム</'); ha = s.rfind('<a ', 0, h)
        seg_h = s[ha:h].replace(SEL, UNSEL, 1).replace(BAR, '', 1)
        seg_c = s[a:k].replace(UNSEL, SEL, 1)
        seg_c = seg_c.replace('"><span style="flex: none; display: flex">', '">' + BAR + '<span style="flex: none; display: flex">', 1)
        s = s[:ha] + seg_h + s[h:a] + seg_c + s[k:]
    return s

def homefix(s, active):
    old = re.search(r'<div style="flex: 0 0 296px"><dc-import name="Sidebar"[^>]*></dc-import></div>', s)
    if old:
        s = s.replace(old.group(0), '<div style="flex: 0 0 296px; display: flex">' + side(active) + '</div>')
    for k, v in B.items():
        s = s.replace('../../home/%s.png' % k, '/_blob/' + v)
    s = s.replace('/_blob/7a8f8f7b21cd262a51fd796f0f796c85', '/_blob/b430972ff8c29777df2b8c4abad50213').replace('/_blob/7bbbc7ec9d7302a7cc3b7a4fd2bb58ee', DMM)
    return s

def post(s):
    # sidebar rows: spec v1.1 = 44px
    s = s.replace('min-height: 40px; padding: 4px 10px 4px 12px', 'min-height: 44px; padding: 4px 10px 4px 12px')
    # toggle pills in DCLogic scripts: selected white pill -> ink pill; light grey labels -> sub
    s = re.sub(r"'#ffffff' : 'transparent'(, fg_[\w]+: [^?]+\? )'#17151f' : '#c9c4da'", r"'#17151f' : 'transparent'\1'#ffffff' : '#6c6878'", s)
    a, b = s.rsplit('class Component', 1) if 'class Component' in s else (s, '')
    for o, n in [("'#16131f'", "'#ffffff'"), ("'#3a1428'", "'#fde8f0'"), ("'#1f3b2e'", "'#e6f6ee'"), ("'#7d7891'", "'#8a8698'"),
                 ("'rgba(255,255,255,0.10)'", "'rgba(20,16,40,0.10)'"), ("'rgba(255,255,255,0.12)'", "'rgba(20,16,40,0.10)'"), ("'rgba(255,255,255,0.14)'", "'rgba(20,16,40,0.12)'")]:
        b = b.replace(o, n)
    s = a + ('class Component' + b if b else '')
    s = s.replace("'#c9c4da'", "'#6c6878'").replace("'#a19db3'", "'#6c6878'").replace("'#a7a2b8'", "'#6c6878'")
    return s

def title(s, suffix=' · 라이트'):
    return re.sub(r'<title>(.*?)</title>', lambda m: '<title>' + m.group(1) + suffix + '</title>', s, 1)

jobs = [('home-renewal/design', n, a) for n, a in [('Main14', 'home'), ('Chars14', 'chars'), ('Remix', None), ('Perks', None), ('Nudge', None)]] + \
       [('nav-redesign/design', n, None) for n in ['Main', 'MHome', 'MDrawer', 'MSheet', 'DSheet', 'MHelp', 'C1', 'C2', 'C3', 'C4', 'States', 'ChatRules', 'Help']]
for d, n, a in jobs:
    s = open(f'{d}/{n}.dc.html').read()
    if d.startswith('home'):
        s = homefix(s, a)
    s = post(convert(title(s)))
    open(f'{d}/L_{n}.dc.html', 'w').write(s)
    print(n, len(s), 'leftover ../:', s.count('src="../'))
