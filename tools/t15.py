FONT="font-family: Poppins, 'Noto Sans JP', 'Noto Sans KR', system-ui, sans-serif"
T = {
 'dark': dict(bg='#0f0f10', surf='#1a1a1c', surf2='#242427', line='rgba(255,255,255,0.08)', ink='#f3f1fa', sub='#a19db3',
              r1='linear-gradient(160deg, #2e1426 0%, #1c1530 100%)', h14='linear-gradient(160deg, #2e1a2c 0%, #1a1720 100%)',
              rank=('#ffc847','#d1d5db','#f0a46b'), fb='#1f1f22', fbicon='#3a3a3f', shim='rgba(255,255,255,0.06)',
              cs_tile='rgba(124,92,255,0.18)', cs_icon='#b9a8ff', shadow='0 8px 24px rgba(192,77,255,0.35)', tab='#0f0f10', label='다크 · 차콜 #0f0f10'),
 'light': dict(bg='#f6f6f9', surf='#ffffff', surf2='#f1f0f6', line='rgba(20,16,40,0.08)', ink='#17151f', sub='#6c6878',
              r1='linear-gradient(160deg, #fde4ee 0%, #ece5fd 100%)', h14='linear-gradient(160deg, #fbe7f1 0%, #f1edf7 100%)',
              rank=('#b45309','#64748b','#c2410c'), fb='#e4e2ec', fbicon='#b8b4c6', shim='rgba(20,16,40,0.06)',
              cs_tile='#efeaff', cs_icon='#6d4fe0', shadow='0 8px 24px rgba(192,77,255,0.25)', tab='#ffffff', label='라이트 #f6f6f9'),
}
GRAD='linear-gradient(95deg, #ff3d7f 0%, #c04dff 55%, #6f5bff 100%)'
HEAD='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 14h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a9 9 0 0 1 18 0v7a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3"/></svg>'
MENU='<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
IMG='<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="9" cy="9" r="2"/><path d="M21 15l-5-5L5 21"/></svg>'

def h(t, c): return f'<div style="font-size: 13px; font-weight: 800; color: {c}; margin: 0 0 10px">{t}</div>'

def col(k):
    t=T[k]; ink=t['ink']; sub=t['sub']
    out=[f'<div style="flex: 1; background: {t["bg"]}; color: {ink}; padding: 24px; border-radius: 20px; display: flex; flex-direction: column; gap: 28px; {FONT}">',
         f'<div style="font-size: 18px; font-weight: 800">{t["label"]}</div>']
    # 1 gradient cards
    out.append('<div>'+h('① 그라데이션 강조 카드', sub)+'<div style="display: flex; gap: 12px">'
      f'<div style="flex: 1; height: 120px; border-radius: 16px; background: {t["r1"]}; border: 1px solid {t["line"]}; padding: 14px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between"><span style="font-size: 30px; font-weight: 800; color: {t["rank"][0]}">1</span><span style="font-size: 13px; font-weight: 800">ランキング 1位カード</span></div>'
      f'<div style="flex: 1; height: 120px; border-radius: 16px; background: {t["h14"]}; border: 1px solid {t["line"]}; padding: 14px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: flex-end"><span style="font-size: 13px; font-weight: 800">ホーム v1.4 カード</span><span style="font-size: 11px; color: {sub}">글자는 ink·sub 토큰</span></div>'
      '</div></div>')
    # 2 coach mark
    out.append('<div>'+h('② ☰ 첫 방문 안내 (6초)', sub)+
      f'<div style="position: relative; height: 130px; background: {t["tab"]}; border: 1px solid {t["line"]}; border-radius: 16px; overflow: visible">'
      f'<div style="height: 56px; display: flex; align-items: center; gap: 12px; padding: 0 12px; border-bottom: 1px solid {t["line"]}">'
      f'<span style="position: relative; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; color: {ink}">'
      '<span class="ring" style="position: absolute; inset: 2px; border-radius: 12px; border: 2px solid #ff3d7f"></span>'
      '<span class="ring r2" style="position: absolute; inset: 2px; border-radius: 12px; border: 2px solid #ff3d7f"></span>'
      f'{MENU}<span style="position: absolute; top: 6px; right: 6px; width: 8px; height: 8px; border-radius: 99px; background: #ff3b5c"></span></span>'
      f'<span style="font-size: 16px; font-weight: 800">キャラ</span></div>'
      f'<div style="position: absolute; left: 10px; top: 64px; padding: 10px 14px; border-radius: 12px; background: {GRAD}; color: #ffffff; font-size: 13px; font-weight: 800; box-shadow: {t["shadow"]}; white-space: nowrap">'
      '<span style="position: absolute; left: 18px; top: -6px; width: 12px; height: 12px; background: #ff3d7f; transform: rotate(45deg); border-radius: 2px"></span>'
      'すべてのメニューはここ <span style="opacity: .8; font-weight: 700">✕</span></div></div></div>')
    # 3 CS card
    out.append('<div>'+h('③ カスタマーサポート 카드 (하단 줄 바로 위 고정)', sub)+
      f'<div style="background: {t["surf"]}; border: 1px solid {t["line"]}; border-radius: 14px; padding: 12px; display: flex; flex-direction: column; gap: 10px; width: 272px">'
      f'<div style="display: flex; align-items: center; gap: 10px"><span style="width: 34px; height: 34px; border-radius: 10px; background: {t["cs_tile"]}; color: {t["cs_icon"]}; display: flex; align-items: center; justify-content: center">{HEAD}</span>'
      f'<span style="flex: 1; display: flex; flex-direction: column"><span style="font-size: 13px; font-weight: 800">カスタマーサポート</span><span style="font-size: 11px; color: {sub}">24時間・すぐ返事</span></span><span style="width: 7px; height: 7px; border-radius: 99px; background: #34d399"></span></div>'
      '<div style="display: flex; gap: 6px">'+''.join(f'<span style="flex: 1; height: 30px; border-radius: 8px; background: {t["surf2"]}; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700">{x}</span>' for x in ['ガイド','みんなの声','ご意見'])+'</div></div></div>')
    # 4 rank numbers
    out.append('<div>'+h('④ 랭킹 1·2·3위 숫자', sub)+'<div style="display: flex; gap: 12px">'+''.join(
      f'<div style="width: 90px; height: 70px; border-radius: 14px; background: {t["surf"]}; border: 1px solid {t["line"]}; display: flex; flex-direction: column; align-items: center; justify-content: center"><span style="font-size: 28px; font-weight: 800; color: {c}">{n}</span><span style="font-size: 10px; color: {sub}">{c}</span></div>'
      for n,c in zip('123',t['rank']))+'</div></div>')
    # 5 fallback
    out.append('<div>'+h('⑤ 사진 없음(로드 실패)·로딩 중 카드', sub)+'<div style="display: flex; gap: 12px">'
      f'<div style="position: relative; width: 150px; height: 200px; border-radius: 16px; overflow: hidden; background: {t["fb"]}; display: flex; align-items: center; justify-content: center; color: {t["fbicon"]}">{IMG}'
      '<div style="position: absolute; left: 0; right: 0; bottom: 0; height: 90px; background: linear-gradient(180deg, rgba(15,15,16,0) 0%, rgba(15,15,16,0.85) 100%)"></div>'
      '<div style="position: absolute; left: 12px; bottom: 12px; color: #ffffff; display: flex; flex-direction: column"><span style="font-size: 13px; font-weight: 800">彼氏持ちの先輩</span><span style="font-size: 10px; opacity: .85">#NTR #先輩</span></div></div>'
      f'<div style="width: 150px; height: 200px; border-radius: 16px; background: {t["fb"]}; position: relative; overflow: hidden"><div class="shim" style="position: absolute; inset: 0; background: linear-gradient(100deg, transparent 20%, {t["shim"]} 50%, transparent 80%)"></div></div>'
      '</div></div>')
    out.append('</div>')
    return ''.join(out)

NOTE = ('<div style="background: #fff8e6; border: 1px dashed #b45309; border-radius: 16px; padding: 18px 22px; color: #3d3a4a; font-size: 13px; line-height: 1.7; '+FONT+'">'
 '<b style="color: #b45309">개발 피드백 반영 메모</b><br>'
 '① 보라·자주 그라데이션 카드는 다크(차콜)에서 한 단계 어둡게 #2e1426→#1c1530으로 낮춤(차콜 위에서 뜨지 않게). 라이트는 연분홍→연보라 #fde4ee→#ece5fd, 글자는 ink. 홈 v1.4 카드 다크 #2e1a2c→#1a1720, 라이트 #fbe7f1→#f1edf7.<br>'
 '② 링: 2px #ff3d7f, 1.6초마다 바깥으로 퍼지며 사라짐(2겹, 0.8초 차이). 말풍선: 브랜드 그라데이션 + 흰 글자, 두 테마 같음. 그림자만 다크 .35 / 라이트 .25. 6초 뒤 또는 ✕·☰ 누르면 사라지고 다시 안 뜸.<br>'
 '④ 1위 #ffc847→라이트 #b45309, 2위 은색 #e5e7eb(다크는 #d1d5db로 살짝 낮춤)→라이트 #64748b, 3위 #f0a46b→라이트 #c2410c.<br>'
 '⑤ 사진 실패 카드: 다크 #1f1f22 / 라이트 #e4e2ec + 가운데 이미지 아이콘. 사진 카드와 같은 아래쪽 어두운 그라데이션을 깔아서 흰 글자를 두 테마 모두 그대로 씀. 로딩 중은 같은 바탕 + 쉬머.'
 '</div>')

html = f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><title>T 라이트·다크 보완 (개발 피드백)</title><script src="./support.js"></script></head>
<body><x-dc><helmet>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700;800&family=Noto+Sans+JP:wght@400;500;700;800&family=Noto+Sans+KR:wght@400;500;700;800&display=swap" rel="stylesheet">
<style>body{{margin:0;background:#9a98a3}}
@keyframes pulse{{0%{{transform:scale(1);opacity:.7}}100%{{transform:scale(1.55);opacity:0}}}}
.ring{{animation:pulse 1.6s ease-out infinite}}.r2{{animation-delay:.8s}}
@keyframes sh{{0%{{transform:translateX(-100%)}}100%{{transform:translateX(100%)}}}}.shim{{animation:sh 1.2s linear infinite}}</style>
</helmet>
<div style="width: 1400px; padding: 24px; box-sizing: border-box; display: flex; flex-direction: column; gap: 20px; background: #9a98a3">
<div style="display: flex; gap: 20px">{col("dark")}{col("light")}</div>
{NOTE}
</div></x-dc></body></html>'''
open('nav-redesign/design/T15.dc.html','w').write(html)
