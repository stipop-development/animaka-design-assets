FONT="font-family: Poppins, 'Noto Sans JP', 'Noto Sans KR', system-ui, sans-serif"
GRAD='linear-gradient(95deg, #ff3d7f 0%, #c04dff 55%, #6f5bff 100%)'
B={'c01':'1ebdbff0d066a223b306e7dff07f6272','c02':'3f70b5c0882b3b44c3272fb6b8f0691d','c03':'0db405bd3e41a5c08379f0c28c046cda','c04':'ce6764cc314a1f59cb0065cac6f350c7',
   'c05':'86aa6fe5fc680ef962f3fe14a53fe207','c06':'7dcbe240edbc92204d0cbcef99df4979','c07':'ecaa5854cef2a6c42b1713075758bfed','c08':'01b33091e880a1cfe59d1e70eb724985',
   'c09':'8ee4bc03b8330856ccd4e8e0fc93bc81','c10':'0c7c69ab24b578199d4749fde14b1d52'}
def I(k): return '/_blob/'+B[k]
DMM="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'%3E%3Crect width='20' height='20' rx='5' fill='white'/%3E%3Ctext x='10' y='13.6' text-anchor='middle' font-family='Arial' font-weight='900' font-size='7.4' fill='%23111'%3EDMM%3C/text%3E%3C/svg%3E"
T={'dark':dict(card='#1a1a1c',ink='#f3f1fa',sub='#a19db3',s2='#242427',line='rgba(255,255,255,0.08)',page='#0f0f10',ok='#5eead4',pink='#ff9cc0',gift='rgba(255,61,127,0.12)'),
   'light':dict(card='#ffffff',ink='#17151f',sub='#6c6878',s2='#f1f0f6',line='rgba(20,16,40,0.08)',page='#f6f6f9',ok='#0f766e',pink='#e0336f',gift='#fdeaf2')}
X='<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>'
BUB=[('c06','…やっと来た。まってたんだから'),('c08','ねぇ、きょうは何はなす？'),('c09','おそかったな。こっちにおいで')]
def row(keys, dirn, w):
    cards=''.join(f'<img src="{I(k)}" style="width: {w}px; height: {int(w*1.33)}px; border-radius: 14px; object-fit: cover; object-position: 50% 20%; flex: none">' for k in keys*2)
    return f'<div style="display: flex; gap: 10px; width: max-content; animation: lg{dirn} 28s linear infinite">{cards}</div>'
def media(t, h):
    bub=''.join(f'<div style="position: absolute; left: 50%; bottom: 16px; transform: translateX(-50%); display: flex; align-items: center; gap: 8px; padding: 7px 14px 7px 7px; border-radius: 99px; background: rgba(15,15,16,0.72); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.14); color: #fff; font-size: 13px; font-weight: 700; white-space: nowrap; opacity: 0; animation: lgbub 9s infinite; animation-delay: {i*3}s"><img src="{I(k)}" style="width: 30px; height: 30px; border-radius: 99px; object-fit: cover; object-position: 50% 15%; border: 2px solid #ff3d7f">{s}</div>' for i,(k,s) in enumerate(BUB))
    return (f'<div style="position: relative; height: {h}px; overflow: hidden; background: {t["page"]}">'
      f'<div style="position: absolute; left: 0; top: 14px; display: flex; flex-direction: column; gap: 10px; transform: rotate(-6deg) translateX(-30px)">'
      f'{row(["c06","c01","c08","c03","c09"],"l",104)}{row(["c02","c10","c07","c04","c05"],"r",104)}</div>'
      f'<div style="position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,0) 35%, {t["card"]} 100%)"></div>'
      f'{bub}<span style="position: absolute; right: 10px; top: 10px; width: 32px; height: 32px; border-radius: 99px; background: rgba(0,0,0,.45); display: flex; align-items: center; justify-content: center">{X}</span></div>')
IC={'chat':'<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    'make':'<path d="M12 3l2.5 5.5L20 9l-4 4 1 6-5-3-5 3 1-6-4-4 5.5-.5z"/>',
    'gift':'<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13M19 12v9H5v-9M7.5 8a2.5 2.5 0 0 1 0-5C11 3 12 8 12 8s1-5 4.5-5a2.5 2.5 0 0 1 0 5"/>',
    'lock':'<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>'}
def ic(k,c,s=16): return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{IC[k]}</svg>'
def body(t, m=False):
    ben=[('chat','会話がずっとのこる','つづきはいつでも、どの端末からでも',False),('make','じぶんだけのキャラがつくれる','見た目もせいかくも、すきなように',False),('gift','最大105ptボーナス','登録後、公式SNSフォローでもらえる',True)]
    rows=''.join(f'<div style="display: flex; align-items: center; gap: 12px; padding: 10px 12px; border-radius: 14px; background: {t["gift"] if g else t["s2"]}"><span style="width: 34px; height: 34px; border-radius: 10px; flex: none; display: flex; align-items: center; justify-content: center; background: {GRAD if g else t["card"]}">{ic(k,"#fff" if g else t["pink"],17)}</span><span style="display: flex; flex-direction: column; gap: 1px"><span style="font-size: 13.5px; font-weight: 800; color: {t["pink"] if g else t["ink"]}">{a}</span><span style="font-size: 11px; color: {t["sub"]}">{b}</span></span></div>' for k,a,b,g in ben)
    return (f'<div style="padding: 4px 20px 18px; display: flex; flex-direction: column; gap: 14px; color: {t["ink"]}">'
      f'<div style="display: flex; flex-direction: column; align-items: center; gap: 6px; text-align: center">'
      f'<span style="padding: 3px 10px; border-radius: 99px; border: 1px solid {t["line"]}; background: {t["s2"]}; color: {t["sub"]}; font-size: 11px; font-weight: 700">♡ お気に入りに入れるには、ログインが必要です</span>'
      f'<span style="font-size: {21 if m else 24}px; font-weight: 800; line-height: 1.3; letter-spacing: -0.01em">ログインで、<span style="background: {GRAD}; -webkit-background-clip: text; background-clip: text; color: transparent">ぜんぶ無料</span>でひらく。</span></div>'
      f'<div style="display: flex; flex-direction: column; gap: 8px">{rows}</div>'
      f'<div style="display: flex; flex-direction: column; gap: 8px; align-items: stretch">'
      f'<span style="height: 52px; border-radius: 14px; background: {GRAD}; color: #fff; font-size: 16px; font-weight: 800; display: flex; align-items: center; justify-content: center; gap: 10px; box-shadow: 0 10px 28px rgba(192,77,255,.38)"><img src="{DMM}" style="width: 26px; height: 26px; border-radius: 6px">DMMで無料ログイン</span>'
      f'<span style="text-align: center; font-size: 11.5px; color: {t["sub"]}">DMMアカウントで10びょう・はじめてでも無料で登録OK</span></div>'
      f'<div style="display: flex; align-items: center; justify-content: center; gap: 6px; font-size: 11px; color: {t["ok"]}; font-weight: 700">{ic("lock",t["ok"],13)}ほかのユーザーに、登録情報が見えることはありません</div>'
      f'<span style="text-align: center; font-size: 12px; color: {t["sub"]}">あとで</span></div>')
def desktop(k):
    t=T[k]
    return (f'<div style="position: relative; width: 760px; height: 880px; background: {t["page"]}; border-radius: 20px; overflow: hidden; display: flex; align-items: center; justify-content: center">'
      f'<div style="position: absolute; inset: 0; background: rgba(0,0,0,0.55)"></div>'
      f'<div style="position: relative; width: 420px; border-radius: 22px; overflow: hidden; background: {t["card"]}; border: 1px solid {t["line"]}; box-shadow: 0 30px 80px rgba(0,0,0,.5)">{media(t,270)}{body(t)}</div></div>')
def mobile(k):
    t=T[k]
    return (f'<div style="position: relative; width: 390px; height: 844px; background: {t["page"]}; border-radius: 28px; overflow: hidden">'
      f'<div style="position: absolute; inset: 0; background: rgba(0,0,0,0.55)"></div>'
      f'<div style="position: absolute; left: 0; right: 0; bottom: 0; border-radius: 22px 22px 0 0; overflow: hidden; background: {t["card"]}"><div style="position: absolute; z-index: 2; top: 8px; left: 50%; transform: translateX(-50%); width: 40px; height: 4px; border-radius: 4px; background: rgba(255,255,255,.5)"></div>{media(t,230)}{body(t,True)}</div></div>')
TRG=[('お気に入り ♡','♡ お気に入りに入れるには、ログインが必要です','즐겨찾기하려면 로그인이 필요해요'),
     ('대화 시작(비로그인 무료 턴 소진)','💬 この会話のつづきは、ログインで','이 대화의 다음은 로그인하면 이어져요'),
     ('이미지·영상 만들기','🎬 つくった作品を保存するには、ログインで','만든 작품을 저장하려면 로그인'),
     ('캐릭터 만들기','✨ キャラづくりは、ログインではじめられます','캐릭터 만들기는 로그인하면 시작돼요'),
     ('포인트 충전','🎁 ポイントの購入には、ログインが必要です','포인트 구매는 로그인이 필요해요'),
     ('그 외(헤더 로그인 버튼 등)','🔓 ログインすると、ぜんぶ使えます','로그인하면 전부 쓸 수 있어요')]
trg=''.join(f'<tr><td style="padding: 4px 8px 4px 0; vertical-align: top; white-space: nowrap">{a}</td><td style="padding: 4px 0">{b}<br><span style="color:#8a8698">{c}</span></td></tr>' for a,b,c in TRG)
MEMO=('<div style="width: 520px; display: flex; flex-direction: column; gap: 14px; font-size: 13px; line-height: 1.7; color: #3d3a4a">'
 '<div style="font-size: 20px; font-weight: 800; color: #17151f">일반 로그인 유도 팝업(DMM 로그인) — 기획</div>'
 '<div><b>왜 이렇게</b><br>• 위: 인기 캐릭터 카드 2줄이 반대 방향으로 천천히 흘러감 → 「여기 이런 애들이 있다」를 1초에 보여 줌<br>• 카드 위에 캐릭터 말풍선이 3초마다 바뀜(「…やっと来た。まってたんだから」 = 드디어 왔네, 기다렸잖아) → 감정 훅<br>• 맨 위 작은 줄은 <b>무엇을 하다가 막혔는지</b>를 그대로 말해 줌(아래 표). 「왜 로그인?」을 없애는 게 전환율 핵심<br>• 혜택 3줄: 대화 저장 / 캐릭터 만들기 / <b>최대 105pt</b>(지금 실제 있는 혜택)<br>• CTA는 하나만: 「DMMで無料ログイン」(DMM으로 무료 로그인) + 「DMM 계정 있으면 10초·처음이어도 무료 가입」<br>• 안심 줄: 「다른 유저에게 가입 정보가 보이지 않아요」</div>'
 f'<div><b>막힌 행동별 맨 위 문구</b> (ja / ko)<table style="border-collapse: collapse; font-size: 12px; margin-top: 4px">{trg}</table></div>'
 '<div><b>규칙</b><br>• <b>로그인 끝나면 원래 하던 행동으로 바로 복귀</b>(즐겨찾기면 자동으로 ♡ 처리, 대화면 그 방으로). 홈으로 튕기면 안 됨<br>• 행동으로 뜬 팝업은 매번 뜸. 자동으로 뜨는 팝업(체류 시간 등)은 「あとで」 누르면 그 세션 동안 안 뜸<br>• 캐릭터 대화방에서 뜨는 기존 캐릭터 전용 팝업은 그대로 두고, 그 외 모든 곳은 이 팝업으로 통일</div>'
 '<div><b>측정</b> (Mixpanel)<br>login_prompt_view(trigger) · login_prompt_cta(trigger) · login_prompt_dismiss(trigger) · login_complete(trigger, is_new)<br>주 지표: trigger별 노출 → 로그인 완료율, 그리고 로그인 후 원래 행동 완료율. 기존 팝업과 50:50 2주</div>'
 '</div>')
html=f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><title>일반 로그인 유도 팝업</title><script src="./support.js"></script></head>
<body><x-dc><helmet>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700;800&family=Noto+Sans+JP:wght@400;500;700;800&family=Noto+Sans+KR:wght@400;500;700;800&display=swap" rel="stylesheet">
<style>body{{margin:0;background:#e9e7ef}}
@keyframes lgl{{0%{{transform:translateX(0)}}100%{{transform:translateX(-50%)}}}}
@keyframes lgr{{0%{{transform:translateX(-50%)}}100%{{transform:translateX(0)}}}}
@keyframes lgbub{{0%{{opacity:0;transform:translate(-50%,8px)}}5%{{opacity:1;transform:translate(-50%,0)}}30%{{opacity:1;transform:translate(-50%,0)}}35%{{opacity:0;transform:translate(-50%,-6px)}}100%{{opacity:0}}}}</style>
</helmet>
<div style="width: 2040px; padding: 28px; box-sizing: border-box; display: flex; gap: 28px; background: #e9e7ef; {FONT}">
<div style="display: flex; flex-direction: column; gap: 24px">{desktop("dark")}{desktop("light")}</div>
<div style="display: flex; flex-direction: column; gap: 24px">{mobile("dark")}{mobile("light")}</div>
{MEMO}
</div></x-dc></body></html>'''
open('home-renewal/design/Login.dc.html','w').write(html)
