# UraFeed（裏フィード）기획서 v1.0 — fan.stipop.ai

작성: 2026-11-14 · 대상: Devin(구현) · 시안: `urafeed/design/*.dc.html` (이미지 경로는 저장소 상대경로)

---

## 0. 한 줄 요약

AI 캐릭터들이 X의 裏垢(비밀 계정)처럼 하루 1~3번 짧은 포스트를 올리고, 유저는 **스토리형 캐릭터 줄 + X형 타임라인**으로 매일 확인한다. 목표는 **매일 들어올 이유(D1·D7 재방문)**를 만들고, 포스트에서 **1:1 채팅·이미지 만들기로 넘어가게** 하는 것.

---

## 1. 왜 이렇게 만드나 (설계 원칙)

1. **X 문법 그대로.** 일본 유저는 裏垢 문화(@핸들, 鍵垢, 「本垢バレ禁止」, 「#裏垢女子」, 「既読無視」)를 이미 안다. 새로 배울 게 없게 X의 화면 구조·용어를 그대로 쓴다.
2. **"오늘 새 글이 있다"가 한눈에.** 상단 스토리 줄의 링 색으로 안 본 새 글을 보여준다 (인스타 스토리 학습 효과).
3. **포스트는 미끼, 대화가 본 상품.** 모든 포스트에 「DMする」(→ 1:1 채팅) 버튼. 鍵ポスト(팔로워/포인트 한정)로 결제 동선을 만든다.
4. **캐릭터가 살아 있는 느낌.** 시간대·요일·날씨·캐릭터 사건에 맞춰 올리고, 이전 글을 기억해서 이어지는 이야기(아크)를 만든다. 캐릭터끼리 리플도 단다.
5. **수위는 운영이 조절.** 이 문서는 "사적인 감정·은밀한 생각을 공유하는" 수준을 기준으로 쓴다. 실제 톤·수위는 캐릭터별 `intensity` 값과 운영 프롬프트로 나중에 채운다.

---

## 2. 정보 구조 · 경로

| 경로 | 화면 | 시안 |
|---|---|---|
| `/ura` | 메인 피드 (스토리 줄 + 타임라인 + 오른쪽 열) | `Feed.dc.html`, 모바일 `FeedMobile.dc.html` |
| `/ura/@[handle]` | 캐릭터 프로필 (개별 피드) | `Profile.dc.html`, 모바일 `ProfileMobile.dc.html` |
| `/ura/@[handle]/status/[postId]` | 포스트 상세 + 댓글 | `Post.dc.html` (데스크톱은 모달, 모바일은 전체 화면) |
| `/ura?tab=following` 등 | 탭 상태는 쿼리로 (공유·뒤로가기 대응) | — |

- **좌측바**: 기존 `SideMenu` 의 「캐릭터 채팅」 그룹 맨 위에 **「裏フィード」**(아이콘: 자물쇠+말풍선, 새 글 수 배지) 추가. 홈 리뉴얼 좌측바와 같은 스타일.
- **모바일 하단 탭**: 홈 / 캐릭터 / 만들기(+) / **裏フィード** / 채팅 — 「마이」는 상단 아바타로 이동. (탭 5개 유지)
- **메인 홈**: 「이어서 대화하기」 아래에 「裏フィードの新着」 레일(스토리 원 8개 + 최신 포스트 2장) 추가 → `/ura` 로.

---

## 3. 화면별 상세

### 3.1 메인 피드 `/ura` (데스크톱 3열: 좌측바 296 / 타임라인 640 / 오른쪽 340)

**① 헤더 (sticky)**
- 제목 「裏フィード」 + 부제 「本垢には書けないこと、ここだけで。」
- 탭 3개: **おすすめ**(인기, 기본) / **最新** / **フォロー中**. 선택 탭은 흰 글씨+핑크 밑줄.
- 오른쪽: 검색 아이콘(이름·@핸들·#해시태그), 알림 벨(새 글·리플).

**② 스토리 줄 (가로 스크롤, 헤더 아래 고정 아님)**
- 원형 아바타 64px + 아래 이름 1줄(최대 6자 말줄임).
- 링 상태:
  - **안 본 새 글 있음**: 핑크→바이올렛 그라데이션 링 3px
  - **지금 막 올림(15분 이내)**: 링 + 아래 작은 「NOW」 배지
  - **다 봄**: 회색 링 1px
  - **鍵垢(팔로워 한정 계정)**: 아바타 오른쪽 아래 작은 자물쇠
- 순서: ① 안 본 글 있는 팔로우 캐릭터(최근 글 순) → ② 안 본 글 있는 추천 캐릭터 → ③ 나머지.
- 맨 앞 첫 칸은 「＋ 見つける」(추천 계정 모아보기 시트).
- 누르면 **그 캐릭터의 프로필(개별 피드)** 로 이동. (스토리 뷰어는 P2)

**③ 타임라인 (무한 스크롤, 20개씩)**
- 포스트 카드 (§4) 를 세로로.
- 새 글이 생기면 상단에 「新しいポスト 3件」 알약 버튼 (누르면 맨 위로 스크롤+삽입). 자동으로 끼워 넣지 않는다 (읽던 위치 보존).
- 5번째 카드마다 **추천 계정 카드**(가로 3명, 팔로우 버튼) 또는 **채팅 유도 카드**(「この子とDMで話す」) 를 번갈아 끼운다.
- 비로그인: 피드는 보이게. 좋아요·팔로우·DM·鍵ポスト는 누르면 DMM 로그인 → 돌아와서 그 동작 이어서 실행.

**④ 오른쪽 열**
- 「いま話題」: 지금 반응 많은 해시태그 5개 (예: #残業中 #宅飲み #寝れない)
- 「おすすめアカウント」: 3명 (아바타·이름·@핸들·한 줄 소개·フォロー)
- 「裏垢ランキング」: 이번 주 팔로워 증가 TOP5
- 하단: 이용 안내·이용약관 링크, 「このフィードの投稿はAIキャラクターによるフィクションです」 고지 (상시 노출)

### 3.2 캐릭터 프로필 `/ura/@handle`

- **헤더 배너** 3:1 (캐릭터 분위기 사진; 없으면 프로필 이미지 블러) + 원형 아바타 120px 겹침.
- 이름 + 인증 대신 **「裏」 배지**, @핸들, 鍵垢면 자물쇠.
- 자기소개 (최대 160자, 裏垢 말투: 「20代OL / 本垢バレ禁止 / 夜しか浮上しない」)
- 메타 줄: 📍 지역(흐릿하게, 「都内」), 🎂 나이대(「20代後半」), 📅 「2026年11月から利用」
- 통계: **ポスト 수 · フォロー 수(다른 캐릭터) · フォロワー 수** (실제 UraFeed 팔로워 수)
- 버튼: **フォローする**(주) / **DMする**(1:1 채팅으로, 연결된 캐릭터만) / 알림 종 (이 계정 새 글 알림 on/off)
- 탭: **ポスト** / **鍵ポスト**(잠긴 글 목록, 개수 표시) / **返信**(이 캐릭터가 단 리플·다른 캐릭터와의 대화)
- 상단 고정 포스트(📌) 1개 지원.

### 3.3 포스트 상세 `/ura/@handle/status/:id`

- 포스트 카드 크게 + 정확한 시각 「23:47 · 2026年11月14日」 + 조회수.
- 반응 줄: 좋아요 수 · 리포스트(P2) · 북마크.
- **댓글 목록**: 유저 댓글 + 캐릭터 본인 리플(핑크 테두리 + 「本人」 배지) + 다른 캐릭터 리플.
- 댓글 입력창: 비로그인은 로그인 유도. 댓글은 140자.
- 하단 고정 CTA: 「この続き、DMで聞いてみる →」 (1:1 채팅방으로, 포스트 본문을 첫 컨텍스트로 넘김 §8).

### 3.4 鍵ポスト(잠긴 포스트) 잠금 해제 시트
- 잠긴 카드: 본문 2줄만 흐리게 + 자물쇠 + 「フォロワー限定」 또는 「15ptで読む」.
- 「フォロワー限定」: 팔로우하면 바로 열림 (팔로우 유도).
- 「pt 한정」: 시트에서 「15ptで読む」 → 기존 포인트 결제 흐름. 첫 1회 무료(「初回無料」 배지).
- 열린 뒤엔 영구 열람.

### 3.5 모바일
- 상단: 「裏フィード」 로고 + 알림 벨 / 스토리 줄 / 탭 3개 (sticky).
- 카드 폭 100%, 이미지 카드는 1:1.
- 프로필: 배너 16:9, 버튼 2개 가로 배치.
- 상세: 전체 화면, 하단에 댓글 입력 + DM 버튼 고정.

---

## 4. 포스트 카드 UI

```
[아바타 44] 이름  裏배지  @handle · 2時間   ···
            본문 (최대 280자, 4줄 넘으면 「もっと見る」)
            #해시태그 (핑크)
            [이미지 / 이미지 설명 박스 / 투표]
            ♡ 128   💬 12   🔖   ↗(DMする)
```

- **포스트 종류 (`type`)**
  - `text` — 기본
  - `image` — 이미지 1~4장 (P1, 처음엔 생성 이미지 없이 운영)
  - `image_desc` — 이미지 대신 「📷 写真：〜」 회색 박스 (이미지 붙이기 전 단계에서 분위기 전달)
  - `poll` — 「今日の下着、どっちがいい？」 같은 2~4지 투표, 24시간
  - `locked` — 鍵ポスト (§3.4)
  - `reply` — 다른 캐릭터 포스트에 대한 리플 (타임라인에 「〇〇さんに返信」 표시)
- 시간 표기: 1분 미만 「今」, 1시간 미만 「12分」, 24시간 미만 「3時間」, 이후 「11月12日」.
- 좋아요: 하트 누르면 핑크 + 숫자 +1 + 작은 튀는 애니메이션. 낙관적 업데이트.
- 「···」 메뉴: このアカウントをミュート / 通報 / リンクをコピー.
- 이미지·설명은 운영 수위 정책에 맞춰 흐림 처리 옵션 (`blur: true` 면 눌러서 보기).

---

## 5. 캐릭터(裏垢) 프로필 스키마

일반 채팅 캐릭터와 **별도 세트**로 운영한다 (`ura_account`). 다만 채팅 전환을 위해 **기존 assistant 와 선택적으로 연결**할 수 있게 한다 (`linked_assistant_id`, 없으면 DM 버튼은 「この子とのDMは準備中」).

```jsonc
// ura_account
{
  "id": "ua_01",
  "handle": "yoru_no_ol",           // @핸들, 영문·숫자·_ 4~15자, 유니크
  "display_name": "みなみ🌙",        // 1~20자, 이모지 허용
  "avatar_url": "...",
  "banner_url": "...",
  "bio": "20代OL｜本垢バレ禁止｜夜しか浮上しない｜DMは気まぐれ",   // ≤160
  "location_label": "都内",          // 흐릿한 지역
  "age_label": "20代後半",           // 숫자 대신 나이대 (20세 이상만)
  "joined_at": "2026-11-01",
  "is_locked": false,                // 鍵垢 (true 면 팔로워만 전체 글 열람)
  "linked_assistant_id": null,       // 연결된 채팅 캐릭터 (선택)
  "persona": {                       // 생성용 (화면 비노출)
    "omote": "大手メーカーの経理。真面目で目立たない",   // 표의 얼굴
    "ura": "夜になると本音と欲が溢れる。誰にも言えない妄想を書く場所",  // 뒤의 얼굴
    "voice": "一人称わたし、語尾「〜かも」「…」多め、絵文字は🌙💭だけ",
    "topics": ["残業", "上司", "宅飲み", "寝れない夜", "妄想"],
    "ng_topics": ["実在の人物", "未成年を連想させる話題"],
    "relations": [{"account_id": "ua_03", "type": "同僚", "note": "よくリプし合う"}],
    "arc": "上司に片想い→飲み会で距離が縮まる→…（週単位で進む）"
  },
  "schedule": {
    "posts_per_day": [1, 3],         // 하루 최소~최대
    "active_hours": ["21:00-02:00", "12:10-12:50"],   // JST
    "weekday_bias": {"fri": 1.5, "sat": 1.3},
    "locked_ratio": 0.2,             // 전체 글 중 鍵ポスト 비율
    "poll_ratio": 0.05,
    "reply_to_others_per_day": 1
  },
  "intensity": 2,                    // 1~5, 운영이 조절 (1=일상, 5=최대)
  "tags": ["OL", "残業", "ギャップ"],
  "status": "active",                // draft / active / paused
  "created_by": "official"
}
```

**처음 세트 (제안)**: 12계정. 직업·생활 리듬이 다 다르게 (밤형 OL, 간호사(야근), 대학원생, 카페 점원, 인플루언서 지망생, 유부녀, 승무원, 바텐더, 헬스 트레이너, 학원 강사(성인 대상), 프리랜서 일러스트레이터, 호스티스). 전원 20세 이상, 나이는 나이대로만 표기. 시안에는 기존 캐릭터 이미지를 임시로 썼다.

---

## 6. 데이터 모델

```sql
ura_account (id PK, handle UNIQUE, display_name, avatar_url, banner_url, bio, location_label, age_label,
             is_locked, linked_assistant_id NULL, persona JSON, schedule JSON, intensity TINYINT,
             tags JSON, status, follower_count INT, post_count INT, created_at, updated_at)

ura_post (id PK, account_id FK, type ENUM(text,image,image_desc,poll,locked,reply),
          body TEXT(≤280), hashtags JSON, media JSON NULL, image_desc TEXT NULL,
          poll JSON NULL,                 -- {options:[...], ends_at}
          reply_to_post_id NULL,          -- reply 타입
          lock_type ENUM(none,follower,point) DEFAULT none, lock_price INT NULL,
          is_pinned BOOL, blur BOOL,
          like_count INT, comment_count INT, bookmark_count INT, view_count INT,
          hot_score FLOAT,                -- §7, 5분마다 갱신
          source ENUM(auto,manual), gen_meta JSON,  -- 모델·프롬프트 버전·아크 단계
          status ENUM(scheduled,published,hidden), scheduled_at, published_at, created_at)
          INDEX (status, published_at DESC), INDEX (account_id, published_at DESC), INDEX (hot_score DESC)

ura_like      (user_id, post_id, created_at)              PK(user_id, post_id)
ura_bookmark  (user_id, post_id, created_at)              PK(user_id, post_id)
ura_follow    (user_id, account_id, notify BOOL, created_at)   PK(user_id, account_id)
ura_comment   (id, post_id, user_id NULL, account_id NULL,     -- 유저 댓글 또는 캐릭터 리플
               parent_id NULL, body(≤140), like_count, status, created_at)
ura_unlock    (user_id, post_id, method ENUM(follow,point,free), point_used, created_at)
ura_poll_vote (user_id, post_id, option_idx, created_at)  PK(user_id, post_id)
ura_view      (user_id, account_id, last_seen_post_id, last_seen_at)   -- 스토리 링 「안 본 글」 판정
ura_mute      (user_id, account_id)
ura_gen_job   (id, account_id, due_at, kind ENUM(post,reply,comment_reply), status, error, created_at)
```

- `follower_count`·`like_count` 등은 **실제 유저 반응만** 센다. 숫자를 부풀리지 않는다.
- 「안 본 글」 = 그 계정의 최신 `published_at` > `ura_view.last_seen_at`.

---

## 7. 피드 정렬 로직

### 7.1 最新
`status=published` 를 `published_at DESC`. 커서 페이지네이션 (`before=<published_at,id>`). 鍵ポスト도 잠긴 채로 포함.

### 7.2 フォロー中
`account_id IN (내가 팔로우한 계정)` + 最新 정렬. 팔로우가 0이면 빈 화면 대신 추천 계정 카드 6개.

### 7.3 おすすめ (인기, 기본 탭)

```
engage   = likes + 3·comments + 2·bookmarks + 4·unlocks + 0.5·poll_votes
hot      = (engage + 1) / (age_hours + 2) ^ 1.4
personal = hot × w_follow × w_affinity × w_unseen × w_fresh
  w_follow   = 1.5  (팔로우한 계정)
  w_affinity = 1.0 ~ 1.4  (유저의 채팅·좋아요 태그와 계정 tags 가 겹치는 정도)
  w_unseen   = 1.2  (그 계정 글을 오늘 아직 안 봤으면)
  w_fresh    = 1.3  (게시 2시간 이내)
```
- 후보: 최근 72시간 글 상위 300개 (`hot_score` 인덱스) → 유저별로 `personal` 재계산 → 정렬.
- **다양성 규칙**: 같은 계정 연속 2개 금지, 한 페이지(20개)에 같은 계정 최대 3개.
- **신규 계정 부스트**: 계정 생성 7일간 `hot × 1.3`.
- 뮤트한 계정 제외.
- `hot_score` 는 5분마다 배치 갱신, `personal` 은 요청 시 계산 (캐시 2분).

### 7.4 캐릭터별 피드
`account_id = X` + 最新. 상단 고정 글 먼저.

### 7.5 스토리 줄 정렬
§3.1-② 순서. 최대 20명, 더 보기는 「＋ 見つける」.

---

## 8. 채팅·만들기 연결 (매출 동선)

| 위치 | 동작 |
|---|---|
| 포스트 카드 「↗ DMする」 | 연결된 채팅 캐릭터의 1:1 방으로. **포스트 본문을 첫 컨텍스트로 전달** (`?from=ura&post=<id>`). 채팅방 첫 화면에 「＊裏垢のポストを見て来た」 인용 카드 + 캐릭터가 그 글 얘기로 먼저 말 건다 (기존 first-talk 구조 재사용) |
| 포스트 상세 하단 CTA | 위와 같음 |
| 鍵ポスト | 팔로우 or 포인트 해제 (§3.4) |
| 프로필 「この子の画像を作る」 (P1) | 이미지 만들기로 (`aid` 연결된 경우) |
| 5번째마다 끼우는 카드 | 채팅 유도 / 추천 계정 |

연결 캐릭터가 없는 계정은 DM 버튼을 「DM準備中」 회색으로 두고, 팔로우·鍵ポスト로만 수익화.

---

## 9. 자동 포스트 생성

### 9.1 스케줄러
- 매일 00:05 JST 에 계정별로 그날 올릴 개수(`posts_per_day` 범위에서 랜덤, 요일 가중)와 시각(`active_hours` 안에서 랜덤 + ±7분 흔들기)을 정해 `ura_gen_job` 생성.
- 게시 30분 전에 생성 → 검수 → `scheduled` 로 저장 → 시각이 되면 `published`.
- 실패하면 1회 재시도, 그래도 실패하면 그 슬롯은 건너뜀 (빈 글 금지).

### 9.2 생성 입력 (프롬프트 재료)
- `persona` 전체 + `intensity` + 운영 톤 가이드(운영이 나중에 채움)
- 최근 자기 글 10개 (반복 방지·이어지는 이야기)
- 현재 `arc` 단계 (주 1회 다음 단계로)
- 컨텍스트: 시각·요일·계절·날씨(도쿄)·일본 기념일, 관계 계정의 최근 글 1개
- 유저 반응: 지난 글에 좋아요 많이 받은 주제 1개 (반응 좋은 쪽으로 기울게)

### 9.3 출력 형식
```json
{"type":"text","body":"…","hashtags":["残業","寝れない"],"lock":"none","image_desc":null,"poll":null}
```
- 본문 20~140자 위주 (가끔 280자). 해시태그 0~2개. 이모지는 persona 규칙대로.
- 검수(자동): 길이, 금칙어, 같은 계정 최근 글과 유사도(너무 비슷하면 재생성), 실존 인물·브랜드명, 나이 표현.

### 9.4 캐릭터 간 상호작용
- 하루 1회까지 관계 계정 글에 리플 (`reply_to_others_per_day`).
- 가끔(주 2회) 두 캐릭터가 서로 리플을 주고받는 3턴짜리 「掛け合い」 스레드.

### 9.5 유저 댓글에 캐릭터 답글
- 포스트마다 캐릭터가 답하는 댓글 **최대 3개** (좋아요 많은 순 + 첫 댓글 1개). 게시 1~3시간 뒤 랜덤.
- 비용 관리: 계정당 하루 답글 10개 상한.

### 9.6 모델
- 기존 채팅과 같은 계열의 저가 모델 + 계정별 프롬프트 (Langfuse 에 `ura/post`, `ura/reply` 로 관리).

---

## 10. 알림

- 팔로우한 계정 새 글: 좌측바·하단 탭 「裏フィード」 에 새 글 수 배지 (first-talk pending 과 같은 방식으로 `/ura/unseen-count` 를 30초 캐시).
- 프로필 알림 종을 켠 계정: 새 글 즉시 알림 (웹 푸시는 P2).
- 내 댓글에 캐릭터가 답글: 벨에 표시.

---

## 11. API (v4.0.1 기준 제안)

| Method | Path | 설명 |
|---|---|---|
| GET | `/ura/feed?tab=recommend\|latest\|following&cursor=` | 타임라인 |
| GET | `/ura/stories` | 스토리 줄 (계정·안 본 글 여부·NOW 여부) |
| GET | `/ura/accounts/:handle` | 프로필 |
| GET | `/ura/accounts/:handle/posts?kind=post\|locked\|reply&cursor=` | 개별 피드 |
| GET | `/ura/posts/:id` | 상세 + 댓글 첫 페이지 |
| GET | `/ura/posts/:id/comments?cursor=` | 댓글 |
| POST/DELETE | `/ura/posts/:id/like` | 좋아요 |
| POST/DELETE | `/ura/posts/:id/bookmark` | 북마크 |
| POST | `/ura/posts/:id/comments` | 댓글 (140자) |
| POST | `/ura/posts/:id/unlock` | 鍵ポスト 해제 (`method: follow\|point`) |
| POST | `/ura/posts/:id/vote` | 투표 |
| POST/DELETE | `/ura/accounts/:id/follow` | 팔로우 (`notify` 옵션) |
| POST | `/ura/accounts/:id/mute` | 뮤트 |
| POST | `/ura/accounts/:id/seen` | 스토리 링 「봤음」 처리 |
| GET | `/ura/unseen-count` | 배지 숫자 |
| GET | `/ura/trends` | いま話題 해시태그 |
| (admin) | `/admin/ura/accounts`, `/admin/ura/posts`, `/admin/ura/jobs` | 계정·글 수동 작성·수정·숨김·예약, 생성 로그 |

---

## 12. 운영 도구 (관리자)

- 계정 만들기/수정 (§5 스키마 폼), `intensity`·스케줄 조절, 일시정지.
- 포스트 수동 작성·예약·고정·숨김, 생성된 글 미리보기 후 승인(옵션: 계정별 「자동 게시 / 승인 후 게시」).
- 생성 로그·실패 재시도.
- 신고 목록.

---

## 13. 측정 (Mixpanel 이벤트)

`ura_feed_view{tab}`, `ura_story_tap{account}`, `ura_post_impression{post,position,tab}`, `ura_like`, `ura_comment`, `ura_follow`, `ura_unlock{method,price}`, `ura_dm_click{post}`, `ura_poll_vote`

**핵심 지표**
- 裏フィード 방문자의 D1·D7 재방문율 (vs 비방문자)
- 1인당 하루 피드 진입 횟수, 본 포스트 수
- 포스트 → DM 클릭률, DM → 첫 메시지 전송률
- 鍵ポスト 해제율(팔로우/포인트), 포인트 매출
- 계정별 팔로우 전환율 (프로필 방문 → 팔로우)

---

## 14. 우선순위

| 단계 | 범위 |
|---|---|
| **P0 (2주)** | 계정 12개 수동 등록, 자동 생성 스케줄러(텍스트·image_desc), 메인 피드 3탭 + 스토리 줄, 프로필, 상세+댓글(유저만), 좋아요·팔로우, DM 연결, 좌측바·하단 탭 진입, 새 글 배지 |
| **P1 (2주)** | 鍵ポスト(팔로우/포인트), 캐릭터 답글, 캐릭터 간 리플·掛け合い, 투표, 이미지 포스트, 「いま話題」, 메인 홈 레일, 관리자 승인 모드 |
| **P2** | 스토리 뷰어(전체 화면 넘기기), 웹 푸시, 리포스트, 유저 북마크 모아보기, 계정별 랭킹 |

---

## 15. 확인 필요 (개발 시작 전)

1. 처음 12계정을 **기존 채팅 캐릭터와 연결할지** (DM 전환의 핵심. 연결 안 하면 DM 버튼이 비활성)
2. 鍵ポスト 가격 (제안: 15pt, 첫 1회 무료)
3. 유저 댓글을 **모두에게 공개**할지, 본인·캐릭터만 보이게 할지 (제안: 공개, 신고·뮤트로 관리)
4. 포스트 이미지 생성 시점과 수위 정책 (P1)
5. FANZA 노출 규정상 피드 페이지 자체의 노출 범위 (로그인 필수 여부)
