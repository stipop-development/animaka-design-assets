FONT="font-family: Poppins, 'Noto Sans JP', 'Noto Sans KR', system-ui, sans-serif"
GRAD='linear-gradient(95deg, #ff3d7f 0%, #c04dff 55%, #6f5bff 100%)'
B={'c06':'7dcbe240edbc92204d0cbcef99df4979','u02':'defb7ebcc4725dc4963f7db0cf1a8576','c08':'01b33091e880a1cfe59d1e70eb724985','u04':'1b3214766389e78e33fd72453613e222',
   'c09':'8ee4bc03b8330856ccd4e8e0fc93bc81','u05':'c8fe7c11bd9f8d2198220c38817a7e0f','c01':'1ebdbff0d066a223b306e7dff07f6272','u01':'fea9ac5bf7af50ebbdf8e5fcd07c7bca'}
def I(k): return '/_blob/'+B[k]
SLIDES=[('c06','u02','ふりむいて、ほほえむ','髪がゆれる・5びょう'),('c08','u04','くるっと一回転','コスプレ・10びょう'),
        ('c09','u05','グラスをかたむける','夜のオフィス・8びょう'),('c01','u01','なみうちぎわで手をふる','ビーチ・15びょう')]
T={'dark':dict(card='#1a1a1c',ink='#f3f1fa',sub='#a19db3',s2='#242427',line='rgba(255,255,255,0.08)',page='#0f0f10',ok='#5eead4',pink='#ff9cc0'),
   'light':dict(card='#ffffff',ink='#17151f',sub='#6c6878',s2='#f1f0f6',line='rgba(20,16,40,0.08)',page='#f6f6f9',ok='#0f766e',pink='#e0336f')}
PLAY='<svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>'
X='<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>'
def media(h, radius):
    n=len(SLIDES); dur=n*3
    sl=''
    for i,(a,b,motion,meta) in enumerate(SLIDES):
        sl+=(f'<div class="vp-s" style="position: absolute; inset: 0; animation: vpfade {dur}s infinite; animation-delay: {i*3}s; opacity: 0">'
             f'<img class="vp-k" src="{I(b)}" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 50% 25%">'
             f'<div style="position: absolute; left: 0; right: 0; bottom: 0; height: 55%; background: linear-gradient(180deg, rgba(15,15,16,0) 0%, rgba(15,15,16,0.88) 100%)"></div>'
             f'<div style="position: absolute; right: 12px; top: 34px; width: 64px; height: 84px; border-radius: 10px; overflow: hidden; border: 2px solid #ffffff; box-shadow: 0 6px 18px rgba(0,0,0,.45); transform: rotate(4deg)"><img src="{I(a)}" style="width: 100%; height: 100%; object-fit: cover; filter: saturate(.7)"><span style="position: absolute; left: 0; right: 0; bottom: 0; padding: 2px 0; text-align: center; background: rgba(0,0,0,.6); color: #fff; font-size: 9px; font-weight: 800">もとの写真</span></div>'
             f'<div style="position: absolute; left: 14px; bottom: 12px; display: flex; flex-direction: column; gap: 4px; color: #ffffff"><span style="align-self: flex-start; display: inline-flex; align-items: center; gap: 4px; padding: 4px 9px; border-radius: 99px; background: rgba(255,255,255,0.18); backdrop-filter: blur(6px); font-size: 11px; font-weight: 800">{PLAY} {motion}</span><span style="font-size: 10px; opacity: .8">{meta}</span></div>'
             '</div>')
    bars=''.join(f'<span style="flex: 1; height: 3px; border-radius: 3px; background: rgba(255,255,255,0.3); overflow: hidden"><span style="display: block; height: 100%; background: #ffffff; transform-origin: 0 50%; animation: vpbar {dur}s infinite linear; animation-delay: {i*3}s; transform: scaleX(0)"></span></span>' for i in range(n))
    return (f'<div style="position: relative; height: {h}px; border-radius: {radius}; overflow: hidden; background: #121014">{sl}'
            f'<div style="position: absolute; left: 12px; right: 52px; top: 12px; display: flex; gap: 4px">{bars}</div>'
            f'<span style="position: absolute; right: 10px; top: 6px; width: 32px; height: 32px; border-radius: 99px; background: rgba(0,0,0,.45); display: flex; align-items: center; justify-content: center">{X}</span></div>')
def body(t, mobile=False):
    steps=[('1','写真をえらぶ','じぶんの写真・キャラ・サンプル'),('2','うごきをえらぶ','50しゅるい＋自由入力'),('3','長さをきめる','5〜30びょう')]
    st=''.join(f'<div style="flex: 1; display: flex; flex-direction: column; align-items: center; gap: 4px; text-align: center"><span style="width: 24px; height: 24px; border-radius: 99px; background: {GRAD}; color: #fff; font-size: 12px; font-weight: 800; display: flex; align-items: center; justify-content: center">{n}</span><span style="font-size: 12px; font-weight: 800">{a}</span><span style="font-size: 10px; color: {t["sub"]}">{b}</span></div>' for n,a,b in steps)
    return (f'<div style="padding: 16px 18px 18px; display: flex; flex-direction: column; gap: 14px; color: {t["ink"]}">'
      f'<div style="display: flex; flex-direction: column; gap: 6px"><span style="align-self: flex-start; padding: 3px 9px; border-radius: 99px; background: rgba(255,61,127,0.14); color: {t["pink"]}; font-size: 11px; font-weight: 800">はじめての動画 50%OFF</span>'
      f'<span style="font-size: 22px; font-weight: 800; line-height: 1.3">写真1枚が、うごく。</span>'
      f'<span style="font-size: 13px; color: {t["sub"]}">きのう {{n}} 本の動画がつくられました</span></div>'
      f'<div style="display: flex; gap: 8px; padding: 12px 8px; border-radius: 14px; background: {t["s2"]}">{st}</div>'
      f'<div style="display: flex; align-items: center; gap: 6px; font-size: 11.5px; color: {t["ok"]}; font-weight: 700"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>しっぱいしたら、ポイントはぜんぶボーナスでもどるよ</div>'
      f'<div style="display: flex; flex-direction: column; gap: 8px"><span style="height: 50px; border-radius: 14px; background: {GRAD}; color: #fff; font-size: 15px; font-weight: 800; display: flex; align-items: center; justify-content: center; gap: 8px; box-shadow: 0 8px 24px rgba(192,77,255,.35)">{PLAY} 動画をつくってみる</span>'
      f'<span style="display: flex; justify-content: space-between; font-size: 12px; color: {t["sub"]}"><span>あとで</span><span>今日は表示しない</span></span></div></div>')
def desktop(k):
    t=T[k]
    return (f'<div style="position: relative; width: 760px; height: 880px; background: {t["page"]}; border-radius: 20px; overflow: hidden; display: flex; align-items: center; justify-content: center">'
      f'<div style="position: absolute; inset: 0; background: rgba(0,0,0,0.55)"></div>'
      f'<div style="position: relative; width: 420px; border-radius: 22px; overflow: hidden; background: {t["card"]}; border: 1px solid {t["line"]}; box-shadow: 0 30px 80px rgba(0,0,0,.5)">{media(360,"0")}{body(t)}</div></div>')
def mobile(k):
    t=T[k]
    return (f'<div style="position: relative; width: 390px; height: 844px; background: {t["page"]}; border-radius: 28px; overflow: hidden">'
      f'<div style="position: absolute; inset: 0; background: rgba(0,0,0,0.55)"></div>'
      f'<div style="position: absolute; left: 0; right: 0; bottom: 0; border-radius: 22px 22px 0 0; overflow: hidden; background: {t["card"]}"><div style="padding: 8px 0 0; display: flex; justify-content: center; background: #121014"><span style="width: 40px; height: 4px; border-radius: 4px; background: rgba(255,255,255,.35)"></span></div>{media(360,"0")}{body(t,True)}</div></div>')
MEMO=('<div style="width: 480px; display: flex; flex-direction: column; gap: 14px; font-size: 13px; line-height: 1.7; color: #3d3a4a">'
 '<div style="font-size: 20px; font-weight: 800; color: #17151f">영상 만들기 유도 팝업 v2 — 기획</div>'
 '<div><b>뭐가 바뀌나</b><br>• 사진 1장 → <b>결과 영상 4편이 3초마다 넘어감</b>(인스타 스토리처럼 위 진행 막대). 오른쪽 위 작은 「もとの写真(원본 사진)」으로 비포·애프터를 바로 보여 줌<br>• 영상마다 모션 이름 칩(「ふりむいて、ほほえむ」 등) → 「이런 걸 고르면 되는구나」를 보여 줌<br>• 3단계 설명은 한 줄 아이콘 3개로 압축, 「실패하면 전액 반환」은 믿음 줄로 따로<br>• CTA 1개만 크게(브랜드 그라데이션). 「あとで(나중에)」·「今日は表示しない(오늘 안 보기)」는 작게</div>'
 '<div><b>영상 소스</b><br>• 실제 서비스로 만든 성인향 샘플 4~6편(노출은 썸네일 수위), 각 3~5초 무음 루프 mp4, 4:5, 720px, 1편 600KB 이하<br>• 첫 편은 포스터 이미지로 먼저 보여 주고 영상은 그다음 로드. 데이터 절약 모드·느린 회선이면 정지 이미지만<br>• 위 시안은 정지 이미지 + 확대 움직임으로 흉내 낸 것</div>'
 '<div><b>누구에게 언제</b><br>• 대상: 영상 만들기를 한 번도 안 쓴 유저만(navState untried에 video)<br>• 때: 홈 진입 3초 뒤, 또는 대화 5턴째 응답 뒤(둘 중 먼저). 하루 1번, 같은 유저 최대 3번(닫으면 다음 날)<br>• 첫 결제 직후·대화방 안에서는 안 띄움<br>• 「今日は表示しない」 누르면 그날은 끝</div>'
 '<div><b>문구</b> (ja / ko)<br>• はじめての動画 50%OFF / 첫 영상 50% 할인<br>• 写真1枚が、うごく。/ 사진 한 장이 움직여요<br>• きのう {n} 本の動画がつくられました / 어제 {n}편의 영상이 만들어졌어요 ← 실제 집계값, 100 미만이면 이 줄 숨김<br>• 写真をえらぶ・うごきをえらぶ・長さをきめる / 사진 고르기·움직임 고르기·길이 정하기<br>• しっぱいしたら、ポイントはぜんぶボーナスでもどるよ / 실패하면 포인트는 전부 보너스로 돌려줘요<br>• 動画をつくってみる / 영상 만들어 보기</div>'
 '<div><b>측정</b> (Mixpanel)<br>video_promo_view(slot, trigger) · video_promo_slide(idx) · video_promo_cta · video_promo_dismiss(type)<br>주 지표: 팝업 노출 → 7일 안 첫 영상 생성 완료율. 기존 팝업과 50:50 A/B 2주</div>'
 '</div>')
html=f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><title>영상 만들기 유도 팝업 v2</title><script src="./support.js"></script></head>
<body><x-dc><helmet>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700;800&family=Noto+Sans+JP:wght@400;500;700;800&family=Noto+Sans+KR:wght@400;500;700;800&display=swap" rel="stylesheet">
<style>body{{margin:0;background:#e9e7ef}}
@keyframes vpfade{{0%{{opacity:0}}3%{{opacity:1}}25%{{opacity:1}}28%{{opacity:0}}100%{{opacity:0}}}}
@keyframes vpbar{{0%{{transform:scaleX(0)}}25%{{transform:scaleX(1)}}25.01%{{transform:scaleX(0)}}100%{{transform:scaleX(0)}}}}
@keyframes vpken{{0%{{transform:scale(1.02) translateY(0)}}100%{{transform:scale(1.12) translateY(-2%)}}}}
.vp-k{{animation:vpken 3s ease-in-out infinite alternate}}</style>
</helmet>
<div style="width: 2000px; padding: 28px; box-sizing: border-box; display: flex; gap: 28px; background: #e9e7ef; {FONT}">
<div style="display: flex; flex-direction: column; gap: 24px">{desktop("dark")}{desktop("light")}</div>
<div style="display: flex; flex-direction: column; gap: 24px">{mobile("dark")}{mobile("light")}</div>
{MEMO}
</div></x-dc></body></html>'''
open('home-renewal/design/VP.dc.html','w').write(html)
