FONT="font-family: Poppins, 'Noto Sans JP', 'Noto Sans KR', system-ui, sans-serif"
GRAD='linear-gradient(95deg, #ff3d7f 0%, #c04dff 55%, #6f5bff 100%)'
B={'c06':'7dcbe240edbc92204d0cbcef99df4979','u02':'defb7ebcc4725dc4963f7db0cf1a8576','c08':'01b33091e880a1cfe59d1e70eb724985',
   'u04':'1b3214766389e78e33fd72453613e222','c09':'8ee4bc03b8330856ccd4e8e0fc93bc81','u05':'c8fe7c11bd9f8d2198220c38817a7e0f'}
def img(k): return '/_blob/'+B[k]
COPY={
 5:dict(kicker='写真からどうが · さいだい30びょう', title='写真1枚が、うごきだす。', sub='えらぶだけ。しっぱいしたらポイントはぜんぶもどるよ', cta='どうがをつくる'),
 6:dict(kicker='AIミニマンガ', title='じぶんのキャラが、マンガの主役に', sub='1行かくだけで、8コマのオトナなマンガが完成', cta='マンガをつくる'),
 7:dict(kicker='ストーリーモード', title='えらぶたびに、ふたりの関係がかわる', sub='あなたの選択で、ラストがかわる大人のものがたり', cta='ストーリーをよむ'),
}
PLAY='<svg width="22" height="22" viewBox="0 0 24 24" fill="#ffffff"><path d="M8 5v14l11-7z"/></svg>'
TONE='background-image: radial-gradient(rgba(0,0,0,0.35) 1px, transparent 1.2px); background-size: 5px 5px'

def art(n, w, h):
    """right-side art (placeholder from existing character images)"""
    if n == 5:
        fw = int(h*0.52); fh = int(h*0.78)
        return (f'<div style="position: absolute; right: {int(w*0.04)}px; top: {int(h*0.09)}px; display: flex; align-items: center; gap: {int(h*0.04)}px">'
          f'<div style="position: relative; width: {int(fw*0.8)}px; height: {int(fh*0.8)}px; border-radius: 14px; overflow: hidden; transform: rotate(-4deg); box-shadow: 0 10px 30px rgba(0,0,0,.5)"><img src="{img("c06")}" style="width: 100%; height: 100%; object-fit: cover; filter: saturate(.75)"><span style="position: absolute; left: 8px; top: 8px; padding: 3px 8px; border-radius: 99px; background: rgba(0,0,0,.55); color: #fff; font-size: 11px; font-weight: 800">しゃしん</span></div>'
          f'<svg width="{int(h*0.1)}" height="{int(h*0.1)}" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.4" stroke-linecap="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
          f'<div style="position: relative; width: {fw}px; height: {fh}px; border-radius: 16px; overflow: hidden; box-shadow: 0 14px 40px rgba(192,77,255,.45); border: 2px solid rgba(255,255,255,.7)"><img src="{img("u02")}" style="width: 100%; height: 100%; object-fit: cover; object-position: 50% 30%">'
          f'<span style="position: absolute; left: 50%; top: 50%; width: 46px; height: 46px; margin: -23px 0 0 -23px; border-radius: 99px; background: rgba(0,0,0,.45); display: flex; align-items: center; justify-content: center">{PLAY}</span>'
          '<span style="position: absolute; left: 8px; right: 8px; bottom: 8px; height: 4px; border-radius: 4px; background: rgba(255,255,255,.3)"><span style="display: block; width: 62%; height: 100%; border-radius: 4px; background: #ffffff"></span></span>'
          '<span style="position: absolute; right: 8px; top: 8px; padding: 3px 8px; border-radius: 99px; background: rgba(0,0,0,.55); color: #fff; font-size: 11px; font-weight: 800">0:12 / 0:30</span></div>'
          f'<div style="display: flex; flex-direction: column; gap: 8px"><div style="width: {int(fw*0.42)}px; height: {int(fh*0.38)}px; border-radius: 10px; overflow: hidden; opacity: .9"><img src="{img("u02")}" style="width: 100%; height: 100%; object-fit: cover; object-position: 30% 40%"></div><div style="width: {int(fw*0.42)}px; height: {int(fh*0.38)}px; border-radius: 10px; overflow: hidden; opacity: .75"><img src="{img("u02")}" style="width: 100%; height: 100%; object-fit: cover; object-position: 70% 20%"></div></div>'
          '</div>')
    if n == 6:
        pw = int(h*0.5); ph = int(h*0.66)
        def panel(k, pos, rot, left, top, bubble, bx, by):
            return (f'<div style="position: absolute; left: {left}px; top: {top}px; width: {pw}px; height: {ph}px; background: #ffffff; padding: 6px; box-sizing: border-box; transform: rotate({rot}deg); box-shadow: 0 12px 30px rgba(0,0,0,.45)">'
              f'<div style="position: relative; width: 100%; height: 100%; overflow: hidden; border: 2px solid #111"><img src="{img(k)}" style="width: 100%; height: 100%; object-fit: cover; object-position: {pos}; filter: grayscale(1) contrast(1.35)"><div style="position: absolute; inset: 0; {TONE}; mix-blend-mode: multiply; opacity: .5"></div></div>'
              f'<div style="position: absolute; left: {bx}px; top: {by}px; padding: 8px 12px; background: #ffffff; border: 2px solid #111; border-radius: 50%; font-size: 13px; font-weight: 800; color: #111; white-space: nowrap">{bubble}</div></div>')
        x0 = int(w*0.44)
        return (f'<div style="position: absolute; inset: 0">'
          + panel('c08', '50% 20%', -6, x0, int(h*0.12), 'ねぇ、みてて…', -20, 14)
          + panel('u04', '50% 30%', 3, x0+int(pw*0.85), int(h*0.2), 'もっとちかくで', 40, ph-60)
          + panel('c08', '60% 60%', -2, x0+int(pw*1.7), int(h*0.08), 'ドキッ', 20, 20)
          + '</div>')
    if n == 7:
        return (f'<div style="position: absolute; right: 0; top: 0; bottom: 0; width: {int(w*0.62)}px; overflow: hidden"><img src="{img("u05")}" style="width: 100%; height: 100%; object-fit: cover; object-position: 50% 30%"></div>'
          f'<div style="position: absolute; right: {int(w*0.06)}px; top: {int(h*0.3)}px; display: flex; flex-direction: column; gap: 12px">'
          + ''.join(f'<div style="padding: 12px 22px; border-radius: 14px; background: rgba(255,255,255,0.16); border: 1px solid rgba(255,255,255,.6); color: #ffffff; font-size: {max(13,int(h*0.045))}px; font-weight: 800; backdrop-filter: blur(6px); box-shadow: 0 6px 20px rgba(0,0,0,.35)">{t}</div>' for t in ['▶ そばにいて、と言う', '▶ きょうはかえる'])
          + '</div>')

def banner(n, w, h, mobile=False):
    c = COPY[n]
    leftfade = (f'<div style="position: absolute; inset: 0; background: linear-gradient(90deg, #0f0f10 0%, rgba(15,15,16,0.92) 30%, rgba(15,15,16,0.0) 58%)"></div>' if not mobile else '')
    bottom = '<div style="position: absolute; left: 0; right: 0; bottom: 0; height: %s; background: linear-gradient(180deg, rgba(15,15,16,0) 0%%, rgba(15,15,16,0.85) 55%%, rgba(15,15,16,0.85) 100%%)"></div>' % ('60%' if mobile else '45%')
    base_bg = {5: 'radial-gradient(80% 120% at 75% 40%, #3a1d3f 0%, #121014 70%)', 6: 'radial-gradient(80% 120% at 75% 40%, #3b2a3a 0%, #121014 70%)', 7: '#121014'}[n]
    if mobile:
        txt = (f'<div style="position: absolute; left: 14px; right: 14px; bottom: 12px; color: #ffffff; display: flex; flex-direction: column; gap: 3px">'
          f'<span style="font-size: 16px; font-weight: 800; line-height: 1.3">{c["title"]}</span>'
          f'<span style="display: flex; justify-content: space-between; align-items: flex-end; gap: 8px"><span style="font-size: 10.5px; opacity: .85">{c["sub"]}</span>'
          f'<span style="flex: none; padding: 7px 12px; border-radius: 10px; background: {GRAD}; font-size: 11.5px; font-weight: 800">{c["cta"]}</span></span></div>')
        # mobile = crop of desktop art: render desktop art at desktop size then shift
        dw, dh = int(h*16/6), h
        artwrap = f'<div style="position: absolute; top: -6px; height: {dh}px; width: {dw}px; right: -10px; transform: scale(.78); transform-origin: 100% 0">{art(n, dw, dh)}</div>'
    else:
        txt = (f'<div style="position: absolute; left: {int(w*0.05)}px; top: 0; bottom: 0; width: {int(w*0.38)}px; display: flex; flex-direction: column; justify-content: center; gap: 10px; color: #ffffff">'
          f'<span style="align-self: flex-start; padding: 4px 10px; border-radius: 99px; background: rgba(255,255,255,0.14); font-size: 12px; font-weight: 800">{c["kicker"]}</span>'
          f'<span style="font-size: {int(h*0.07)}px; font-weight: 800; line-height: 1.3">{c["title"]}</span>'
          f'<span style="font-size: 14px; opacity: .85">{c["sub"]}</span>'
          f'<span style="align-self: flex-start; margin-top: 8px; padding: 12px 22px; border-radius: 12px; background: {GRAD}; font-size: 15px; font-weight: 800; box-shadow: 0 8px 24px rgba(192,77,255,.35)">{c["cta"]} →</span></div>')
        artwrap = art(n, w, h)
    return (f'<div style="position: relative; width: {w}px; height: {h}px; border-radius: {16 if mobile else 20}px; overflow: hidden; background: {base_bg}; flex: none">'
            f'{artwrap}{leftfade}{bottom}{txt}</div>')

def page(bg, ink, label, content):
    return f'<div style="background: {bg}; color: {ink}; padding: 18px; border-radius: 18px; display: flex; flex-direction: column; gap: 10px"><span style="font-size: 12px; font-weight: 800; opacity: .7">{label}</span>{content}</div>'

rows=[]
for n,name in [(5,'⑤ video → /scene?from=home-banner'),(6,'⑥ manga → /manga'),(7,'⑦ story → /story')]:
    rows.append(f'<div style="display: flex; flex-direction: column; gap: 12px"><div style="font-size: 20px; font-weight: 800; color: #17151f">{name}</div>'
      '<div style="display: flex; gap: 16px; align-items: flex-start">'
      + page('#0f0f10', '#f3f1fa', '데스크톱 16:6 · 다크', banner(n, 1120, 420))
      + '<div style="display: flex; flex-direction: column; gap: 16px">'
      + page('#0f0f10', '#f3f1fa', '모바일 4:3 · 다크', banner(n, 330, 248, True))
      + page('#f6f6f9', '#17151f', '모바일 4:3 · 라이트(이미지 같음)', banner(n, 330, 248, True))
      + '</div></div>'
      + page('#f6f6f9', '#17151f', '데스크톱 · 라이트(이미지 같음, 50% 축소)', f'<div style="width: 560px; height: 210px"><div style="transform: scale(.5); transform-origin: 0 0">{banner(n,1120,420)}</div></div>')
      + '</div>')
html=f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><title>홈 상단 배너 5·6·7</title><script src="./support.js"></script></head>
<body><x-dc><helmet>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700;800&family=Noto+Sans+JP:wght@400;500;700;800&family=Noto+Sans+KR:wght@400;500;700;800&display=swap" rel="stylesheet">
<style>body{{margin:0;background:#e9e7ef}}</style></helmet>
<div style="width: 1560px; padding: 28px; box-sizing: border-box; display: flex; flex-direction: column; gap: 40px; background: #e9e7ef; {FONT}">
<div style="font-size: 13px; color: #6c6878">시안 이미지는 기존 캐릭터 그림으로 만든 자리 표시예요. 실제 배너는 Seedream 프롬프트로 생성해 같은 구도로 교체합니다. 글자·버튼은 코드로 얹음.</div>
{"".join(rows)}
</div></x-dc></body></html>'''
open('home-renewal/design/BN567.dc.html','w').write(html)
