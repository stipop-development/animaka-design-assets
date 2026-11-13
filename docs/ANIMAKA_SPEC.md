# Animaka — 유저가 직접 만드는 AI 애니 (fan.stipop.ai) 개발 기획서 v1.0

작성 2026-11-13 · 작성 Claude (Tony 요청) · 구현 담당 Devin

> **Devin에게.** 이 문서 한 개로 기능 전체를 한 번에 구현하는 것이 목표야.
> - 시안과 이 문서가 다르면 **이 문서가 우선**이야.
> - 문서에 없는 세부는 같은 저장소의 기존 **AI 미니 망가(`/manga`)** 구현 방식을 그대로 따라줘.
> - **§13 "Devin이 직접 확인할 것"** 은 작성자가 코드를 못 본 부분이야. 확인하고 맞춰서 구현해줘.
> - **§14 "결정 필요"** 는 기본값으로 구현하되 서버 설정값으로 빼서 나중에 바꿀 수 있게 해줘.

---

## 0. 한눈에 보기

- **무엇:** 유저가 한 줄 아이디어로 대사·목소리·자막이 들어간 1~10분짜리 애니를 만들고, 공개해서 포인트로 판매하는 기능. Higgsfield Mangaka의 애니 버전이고, 이름은 **Animaka**.
- **위치:** fan.stipop.ai 좌측바 → 미디어 제작 → **Animaka** (NEW 배지). 경로는 `/animaka`.
- **포맷 문법 (경쟁작 무빙툰 역분석 결과):**
  - 러닝타임의 60~70%는 "정지 그림 + 천천히 움직이는 카메라(줌·팬)"로 채워요.
  - AI가 인물을 실제로 움직이는 영상(Atlas)은 고개 들기·표정 변화 같은 핵심 장면 20~30%에만 써요.
  - 자막은 영상 위에 따로 얹는 말풍선형이에요.
  - 씬 전환은 컷 또는 화이트 플래시예요.
- **원가 구조:** 비용은 그림 수가 아니라 **AI 모션 씬 수와 길이**에서 갈려요. 그래서 기본값은 "카메라 무빙", AI 모션은 유저가 씬마다 골라서 추가 결제해요.
- **소리 원칙:** 영상과 소리를 따로 만들어서 나중에 합쳐요. 목소리는 대사마다 기존 Gemini TTS 서버로 만들어요. 대사나 감정을 고쳐도 영상은 다시 만들지 않아요.
- **자막 원칙:** 스토리보드에서 쓴 대사가 곧 자막이에요. 목소리 길이에 맞춰 자동으로 타이밍이 잡혀요.

### 전체 흐름

| 단계 | 화면 | 유저가 하는 일 | 비용 |
|---|---|---|---|
| 0 | Animaka 홈 `/animaka` | 샘플 감상 → 아이디어 입력 또는 템플릿 선택 | 무료 |
| 1 | 스토리·캐스트 `/animaka/create?work=ID&step=story` | AI가 정리한 줄거리·막 구성 확인, 등장인물 얼굴·목소리 고정 | 무료 (하루 한도) |
| 2 | 스토리보드·결제 `…&step=board` | 씬마다 첫 장면 그림·대사·연출 확인 및 수정, 대사 목소리 미리듣기 → **결제** | **결제** |
| 3 | 영상 만들기·편집 `…&step=edit` | 첫 씬부터 만들어지는 대로 보며 구간 수정·삭제·순서 변경, 목소리·자막 조정 | 다시 만들기만 유료 |
| 4 | 저장·공개 `…&step=publish` | 하나의 영상으로 저장, 공개 범위·판매 가격 설정 | 무료 |
| — | 시청 `/animaka/[id]` | 다른 유저가 보고, 무료 맛보기 뒤 포인트로 잠금 해제 | 시청자 결제 |

---

## 1. 참고 자료

| 자료 | 위치 |
|---|---|
| 화면 시안 (Tony 확인용 캔버스) | https://claude.ai/artifact/NNP5NUGbn59criHpZV5moD |
| 시안 원본 마크업 (인라인 스타일 = 정확한 수치) | 이 저장소 `design/*.dc.html` (`Main`, `Story`, `Storyboard`, `Editor`, `Publish`, `Sidebar`) |
| 디자인 토큰 (색·글꼴·간격·둥글기) | `design/tokens.json`, 설명 `design/design-system.md` |
| 시안·샘플용 이미지 30장 | `images/` (캐릭터 시트 9, 장소 2, 씬 12, 템플릿 4, 표지 3) |
| 따라 할 기존 기능 (가장 비슷함) | fan.stipop.ai `pages/manga/*`, `utils/manga.js`, `utils/mangaActive.js`, `components/view/manga/*` 와 fanza-api 의 manga 라우트·서비스 |
| 영상 생성 (Atlas) | fan.stipop.ai `components/view/scene/studio/usePlanStudio.js` (`/v4.0.1/scene*`, `/scene/price`, 폴링) 와 fanza-api 의 scene 서비스 |
| 목소리 (Gemini TTS) | fan.stipop.ai `utils/chatVoice.js` (`VOICE_HOST` = voice.royalchat.ai, `/v1/anima/voice/catalog`, `/anima` 소켓, `/v4/message/voice/audio` 업로드), 단가 근거 `docs/voice-pricing-comparison.md` |
| 이미지 생성·캐릭터 일관성 | fanza-api studio 모듈 (`/v4.0.1/studio/image`, Seedream, 레퍼런스 이미지로 같은 얼굴 유지), 설계 `docs/create-studio.md` |
| 포인트 부족 처리 | `utils/pointShort.js` `openPointShort(source)`, `components/view/chat/PointShortPopup.js` |
| 앱 셸·좌측바 | `components/layout/AppShell.js` (`SHELL_TYPES`), `components/view/chat/SideMenu.js` |

---

## 2. 디자인 규칙 (모든 화면 공통)

`design/tokens.json` 값을 그대로 써줘. 기존 코드 기준값은 다음과 같아.

- **다크 기본:** `constants/darkPalette.js` `DARK` (bg `#0f0d17`, sidebar `#13111c`, surface `#1a1726`, surface2 `#231f33`, line `rgba(255,255,255,0.08)`, ink `#f3f1fa`, sub `#a19db3`). 라이트 모드는 `homeShared.palette(false)`를 따라가.
- **주 버튼:** `homeShared.PrimaryBtn` 재사용 (46px, 둥글기 12, `BRAND` 그라데이션, `shadow-cta`).
  - 한 화면에 주 버튼은 1개만 둬.
  - 보조 버튼은 `GhostBtn` 을 써.
- **선택 상태:** 배경 `#3a1428`, 테두리 `#ff3d7f`. 미디어 기능 톤은 `TONES.media` (`#8b5cf6`).
- **글꼴:** Poppins → Noto Sans JP → Noto Sans KR. 제목 800, 버튼 800, 라벨 500.
- **이미지:** 캐릭터·장면 그림은 카드를 꽉 채워 (`object-fit: cover`, 아래쪽 어두운 그라데이션 위에 글자). 캐릭터 대표 이미지는 최소 3:4 비율로, 작은 칸에 넣지 마.
- **아이콘:** `lucide-react` (16~20px). 이모지는 쓰지 마.
- **언어:** 일본어 기본, 한국어·영어 지원. `lang/{ja,ko,en}.json` 에 `animaka.*` 키를 추가해. 화면 문구의 일본어는 어려운 한자보다 가나 위주로 써줘.

### 2.1 반응형

데스크톱 기준은 좌측바 296px + 본문이야. 브레이크포인트는 `constants/GlobalBreakPoint` 를 써.

| 화면 | 데스크톱 | 모바일 (≤ web 브레이크포인트) |
|---|---|---|
| 홈 | 샘플 플레이어 16:7.2, 아이디어 입력 4열 옵션 | 플레이어 16:9, 옵션 2열, 템플릿 가로 스크롤 |
| 스토리·캐스트 | 캐릭터 카드 3열(3:4) → 아래 작품정보·장소·AI도우미 3열 | 캐릭터 카드 가로 스와이프(카드 폭 78%), 나머지 세로 쌓기, AI 도우미는 하단 시트 |
| 스토리보드 | 씬 카드 4열 + 오른쪽 씬 상세 패널 | 씬 카드 2열, 씬을 누르면 상세가 하단 시트로 올라옴 |
| 편집 | 미리보기 + 오른쪽 구간 수정 패널, 아래 타임라인 | 미리보기 위 고정, 아래 탭 3개(씬 / 대사·목소리 / 소리), 타임라인은 가로 스크롤 |
| 하단 결제 바 | 화면 하단 고정 | 하단 고정, 내역은 접고 "내역 보기"로 펼침 |

---

## 3. 화면별 상세

> 시안 파일 이름을 괄호로 표시했어. 모든 단계 화면 상단에는 공통 헤더를 둬.
> - 헤더 구성: 로고 "ANIMAKA", 작품 제목(눌러서 수정), 4단계 진행 표시, 오른쪽 주 버튼.
> - 진행 표시의 단계 이름: 1 스토리·캐스트 / 2 스토리보드·결제 / 3 영상 만들기·편집 / 4 저장·공개.
> - 끝난 단계에는 ✓ 를 붙이고, 누르면 그 단계로 돌아가.
> - **결제 이후에는 1단계로 돌아가도 읽기 전용이야.** 수정하려면 "새 버전으로 복제" 버튼을 쓰게 해.

### 3.0 Animaka 홈 `/animaka` (`Main.dc.html`)

**1) 샘플 플레이어 (맨 위)**
- 공식 샘플 작품 3~5개의 실제 mp4를 자동재생해 (`muted`, `playsInline`, `loop`, 처음 30초 하이라이트 구간).
- 왼쪽 위에 글자를 얹어: "ANIMAKA", "한 줄 아이디어로, 목소리까지 들어간 나만의 애니를", "이 작품도 유저가 Animaka로 만들었어요".
- 버튼은 두 개야.
  - 주 버튼 "나도 만들어 보기": 아이디어 입력칸으로 스크롤하고 포커스해.
  - 보조 버튼 "이 템플릿으로": 그 샘플의 템플릿으로 1단계를 시작해.
- 하단 조작 요소:
  - 소리 켜기 버튼 (누르면 소리 재생, 다른 샘플로 넘어가도 유지)
  - 작품별 진행바 (작품 개수만큼 칸)
  - 작품 제목·길이 표시
  - 자막 말풍선 (WebVTT 를 오버레이로 표시)
- `prefers-reduced-motion` 이면 자동재생하지 말고 포스터 이미지만 보여줘.
- 샘플 데이터: 서버 `GET /v4.0.1/animaka/works?official=1` (망가의 `mangaOfficial` 과 같은 방식).
- 운영팀이 공식 작품을 올리기 전까지는 `images/s01~s12` 로 만든 카메라 무빙 영상 1개를 공식 샘플로 등록해서 써줘.

**2) 아이디어 입력 카드**
- 탭 3개: "아이디어로 시작" / "내 채팅에서 가져오기" / "대본 붙여넣기".
- **아이디어로 시작:**
  - 텍스트 영역 (최대 500자).
  - 빈 칸일 때 아래에 예시 칩 3개를 보여줘. 누르면 그 문장이 입력돼. 템플릿 데이터에서 무작위로 골라.
- **내 채팅에서 가져오기:**
  - 최근 채팅방 목록을 보여줘 (`/v4/message/room?isChat=Y`, AppShell 과 같은 방식).
  - 하나를 고르면 서버가 최근 대화 50턴을 요약해서 아이디어 문장으로 채워줘.
  - 그 방의 캐릭터가 자동으로 주연이 돼.
- **대본 붙여넣기:**
  - 최대 8,000자.
  - 서버가 대본을 씬으로 나눠. 대사와 화자를 추출해서 2단계에 그대로 써.
- **옵션 4칸:**
  - **주연 캐릭터:** "내 캐릭터에서 변경" 을 누르면 내가 만든 캐릭터·대화한 캐릭터 목록이 나와 (여러 명 선택, 최대 4명). 기존 캐릭터를 고르면 그 캐릭터 이미지를 얼굴 기준으로 써.
  - **길이:** 1분 / 3분 / 5분 / 10분. **처음 만드는 유저의 기본값은 1분**이야 (비용 부담과 대기 시간을 줄이기 위해). 고르면 예상 씬 수를 보여줘: 1분 5~6씬, 3분 10~12씬, 5분 18~22씬, 10분 40~45씬.
  - **화풍:** 소프트 셰이딩 애니(기본) / 셀 애니 / 수채 / 흑백 망가.
  - **목소리·자막:** 음성 언어 일본어(기본)·한국어, 자막 언어 끄기·일본어·한국어·영어. 화면비 16:9(기본)·9:16.
- 하단 안내문: "스토리와 스토리보드 그림까지는 무료예요. 영상은 씬 길이를 보고 스토리보드에서 결제해요."
- 주 버튼 "스토리 만들기 · 무료" → `POST /animaka/works` → 1단계로 이동.
- 로그인 안 했으면 `mangaLogin('/animaka')` 과 같은 방식으로 로그인시켜. 입력한 내용은 localStorage 에 보존해.

**3) 만드는 과정 4칸 안내:** 01 스토리 / 02 스토리보드·결제 / 03 영상 만들기·편집 / 04 저장·공개.

**4) 템플릿으로 바로 시작**
- 템플릿 카드 4~8개 (16:10 이미지, 길이 배지, 이름, 한 줄 설명).
- 누르면 아이디어·캐릭터·길이를 미리 채운 상태로 1단계를 시작해.
- 서버 템플릿 목록: `GET /animaka/templates`.

**5) 내 애니 / 커뮤니티 인기작 탭**
- 내 애니 카드: 3:4 표지, 제목, 상태 배지, 이어하기 링크.
- 상태 배지는 6가지야:
  - 스토리 작성 중
  - 스토리보드 수정 중 N/M씬
  - 결제 완료·영상 만드는 중 N/M
  - 편집 중
  - 저장됨
  - 공개 중 (조회수와 판매 수 표시)
- 이어하기는 각 상태에 맞는 단계로 연결해.

### 3.1 1단계 스토리·캐스트 (`Story.dc.html`)

들어오자마자 서버가 대본 초안을 만들어 (`POST /works/:id/script`, 망가의 `mangaScript` 와 같은 방식). 만드는 동안은 스켈레톤을 보여줘.

**1) 등장인물 (맨 위, 가로 꽉 채움, 3열)**
- 카드 구성:
  - 3:4 대표 이미지 (앞모습 전신, 위쪽 기준으로 잘라 보여줌)
  - 왼쪽 위 배지 "얼굴 고정"
  - 아래 그라데이션 위에 이름(24/800)과 한 줄 소개
  - 그 아래 앞/뒤/얼굴 썸네일 3개 (1:1). 누르면 대표 이미지가 그 그림으로 바뀌어.
  - 목소리 줄: "목소리 · 맑은 20대 여성", 재생 버튼
  - 버튼 2개: "다시 그리기", "내 캐릭터로 교체"
- **캐릭터 시트 생성:**
  - 기존 studio 이미지 생성(Seedream)으로 앞·뒤·얼굴 3장을 만들어.
  - 앞모습을 먼저 만들고, 뒤·얼굴은 앞모습을 레퍼런스로 넣어서 같은 얼굴을 유지해.
  - 기존 캐릭터를 골랐으면 그 캐릭터의 `aiImg` 를 레퍼런스로 써.
- **다시 그리기:**
  - 캐릭터당 하루 3회까지 무료, 넘으면 설정값 `ANIMAKA_SHEET_REDRAW_PT` 만큼 과금 (§14).
  - 이전 버전은 버전 칩으로 남겨서 되돌릴 수 있게 해.
- **목소리:**
  - 재생 버튼은 voice catalog 의 `previewUrl[lang]` 을 재생해.
  - 목소리 이름을 누르면 목소리 선택 시트가 열려. 기존 `ChatVoice` 의 picker UI 를 재사용하고, catalog 목록을 성별로 필터해.
  - 고르면 `PUT /works/:id/cast/:castId` 로 저장해.
- **인물 추가:** "+ 인물 추가" 카드로 직접 입력해. 최대 4명.
- **안전:** 나이는 20세 이상만 가능해 (studio 규칙과 동일). 미성년을 떠올리게 하는 단어는 막고 오류 코드 8003을 재사용해.

**2) 작품 정보 카드**
- AI가 정리한 로그라인을 보여주고, 눌러서 수정할 수 있어.
- 장르 / 분위기 / 길이·씬 수를 표시해.
- 이야기 흐름(막)은 5개 내외로, 각 막에 "제목 · 씬 범위 · 한 줄 설명"을 보여줘.
- 막 제목과 설명을 바로 고칠 수 있고, 순서는 드래그로 바꿔.

**3) 장소·소품 카드**
- 장소는 16:9 썸네일과 이름을 보여줘. 장소 그림은 씬 첫 장면을 만들 때 배경 레퍼런스로 써.
- 소품은 칩으로 보여주고, "+ 추가"로 늘릴 수 있어.

**4) AI 연출 도우미 (오른쪽)**
- 대화로 스토리를 고쳐: "렌을 더 무뚝뚝하게", "결말을 더 설레게", "씬 줄이기".
- 응답마다 무엇을 바꿨는지 요약해서 보여주고, 해당 칸을 1.5초 동안 하이라이트해.
- 제안 칩 3개를 보여줘.
- LLM 은 망가 대본 생성과 같은 모델과 경로를 써.

**5) 주 버튼 "스토리보드 그리기 · N장"**
- 누르면 씬마다 첫 장면 이미지를 한꺼번에 만들기 시작하고 2단계로 이동해.
- 2단계에서 씬 카드가 하나씩 채워지는 걸 보여줘.

### 3.2 2단계 스토리보드·결제 (`Storyboard.dc.html`)

**1) 씬 카드 격자 (4열)**
- 카드 구성:
  - 16:9 첫 장면 이미지 (만드는 중이면 스켈레톤과 "그리는 중")
  - 왼쪽 아래 `#번호`, 오른쪽 아래 길이
  - 움직임 표시 점과 이름 (카메라 무빙 `#7dd3fc` / AI 모션 `#ff3d7f` / 정지 `#a19db3`)
  - 대표 대사 1줄
- 위쪽 필터 칩: 전체 N / 막별. 오른쪽에 범례.
- 씬은 드래그로 순서를 바꿀 수 있어.
- "+ 씬 추가" 카드를 두고, 앞 씬 내용을 바탕으로 AI가 초안을 써.

**2) 씬 상세 패널 (오른쪽)**
- **헤더:** 씬 번호, 장소, 삭제 아이콘. 삭제하면 5초 동안 "되돌리기" 토스트를 보여줘.
- **큰 첫 장면:** 대표 대사를 말풍선 자막으로 얹어서 미리보기를 보여줘.
- **첫 장면 후보:**
  - 처음에는 2장을 만들어. 유저가 하나를 고르면 선택 테두리를 표시해.
  - "다시 뽑기"로 2장을 더 만들어. 씬당 3회까지 무료, 넘으면 `ANIMAKA_FRAME_REDRAW_PT`.
  - "이렇게 바꿔줘" 입력칸에 수정 요청을 넣으면 그 내용을 반영해서 다시 그려.
- **대사 목록:**
  - 각 줄: 화자 칩(캐릭터 색), 감정 칩, 대사 본문(눌러서 수정), 재생 버튼.
  - 감정 칩 7가지: 기본 / 설렘 / 놀람 / 울먹임 / 속삭임 / 화남 / 숨찬.
  - **재생 = 결제 전 목소리 미리듣기 (무료).** 같은 대사·감정·목소리 조합은 캐시해. 하루 한도 `ANIMAKA_PREVIEW_TTS_DAILY` (기본 200줄).
  - 대사 1줄은 최대 60자. 넘으면 "두 줄로 나누기"를 제안해.
  - "+ 대사 추가", 줄 순서는 드래그로 바꿔.
  - 지문(화자 없는 내레이션)도 줄로 넣을 수 있어. 내레이션 목소리는 옵션이야.
- **움직임 (라디오 3개):**
  - **카메라 무빙 (기본 포함):**
    - 프리셋 칩 7가지: 천천히 줌인(기본) / 줌아웃 / 좌→우 / 우→좌 / 위→아래 / 아래→위 / 흔들림 약하게.
    - 각 칩에 마우스를 올리면 첫 장면 이미지로 2초 미리보기 애니메이션을 보여줘.
  - **AI 모션 (+pt):**
    - "어떻게 움직일까요?" 입력칸이 있어. AI가 대사와 상황으로 기본 문장을 채워둬.
    - 씬 가격이 바로 다시 계산돼.
  - **정지:** 그대로 보여주기만 해.
  - AI 모션 씬 수에는 상한이 있어 (`ANIMAKA_AI_SCENE_MAX`, 기본: 1분 2씬, 3분 4씬, 5분 6씬, 10분 10씬). 넘으면 비활성화하고 이유를 툴팁으로 알려줘.
- **길이:**
  - 기본값은 "대사에 맞춤"이야. 대사 목소리 길이 합계 + 앞뒤 여백 0.6초, 최소 3초.
  - 직접 지정도 가능해 (3~20초 슬라이더).
  - AI 모션 씬은 Atlas 지원 길이(`/scene/price` 의 `durations`) 중 가장 가까운 값으로 맞춰.
- **다음 씬 전환:** 바로 컷(기본) / 화이트 플래시 / 페이드 / 암전.
- **배경음·효과음 (씬 단위, 선택):** 효과음 프리셋 칩 6가지: 빗소리 / 카페 소음 / 발소리 / 문 종소리 / 심장 소리 / 없음.

**3) 하단 결제 바 (고정)**
- **왼쪽:**
  - "총 N씬 · M분 SS초 영상"
  - 내역 칩: "카메라 무빙·정지 a씬 · x초", "AI 모션 b씬 · y초", "목소리·자막 N씬 포함"
  - 화질: 720p(기본) / 1080p
  - 작은 안내: "생성에 실패한 씬은 자동 환불"
- **오른쪽:**
  - "결제 금액 ○○pt" (26/800, 포인트 노란색)
  - 보유 포인트·보너스 포인트
  - 첫 작품 할인이 있으면 원가에 취소선을 긋고 할인가를 보여줘. `useFirstUseDiscount`, `campaign/first-use` 와 연동.
  - 주 버튼 "결제하고 영상 만들기".
- **가격은 서버 견적으로 보여줘.** 화면에서 바뀌는 즉시 `POST /works/:id/quote` 를 다시 불러 (300ms 디바운스). 계산 규칙은 §7.
- **결제 버튼을 누르면 확인 모달을 띄워:**
  - 내용: 총액, 씬 수, 길이, 화질, 안내 문구 2줄.
  - 안내 문구: "결제 후에는 스토리·캐릭터를 바꿀 수 없어요(대사·목소리·자막은 편집에서 수정 가능)", "실패한 씬은 자동 환불".
  - 버튼: "결제하기" / "취소".
- **포인트가 부족하면** `openPointShort('animaka_pay')` 를 열어. 충전하고 돌아오면 이 화면으로 복귀해 (`mangaCharge` 와 같은 방식, `back_url`).
- **결제가 성공하면** 3단계로 이동하고 생성 작업을 시작해.

### 3.3 3단계 영상 만들기·편집 (`Editor.dc.html`)

**1) 상단 생성 상태 바 (`role="status"`)**
- 표시 내용: "영상 만드는 중 · 9 / 22씬 완성", 그라데이션 진행바, "약 N분 남음".
- 안내: "첫 씬부터 순서대로 만들어요. 완성된 씬은 바로 보고 고칠 수 있어요. 창을 닫아도 계속 만들어요."
- 다 끝나면 "모든 씬 완성"과 함께 사라지고, 토스트와 알림벨 알림을 띄워.
- 실패한 씬이 있으면 빨간 배지 "N씬 실패 · 자동 환불됨"과 "다시 만들기(무료 1회)" 버튼을 보여줘.
- **생성 순서 (중요):**
  - 카메라 무빙·정지 씬은 서버 ffmpeg 로 수 초 안에 끝나. 그래서 결제 직후 1~2분 안에 앞부분을 볼 수 있어.
  - AI 모션 씬은 Atlas 큐에 넣고, 끝나는 대로 갈아 끼워.
  - AI 모션 씬이 아직 안 끝났으면 그 자리에 카메라 무빙 임시본을 넣고 "AI 모션 만드는 중" 배지를 붙여.
  - 이렇게 하면 미리보기가 끊기지 않아.

**2) 미리보기 플레이어 (왼쪽 큰 영역)**
- 씬별 영상을 순서대로 이어서 재생해. 서버가 합친 파일이 아니라 클라이언트가 이어 붙이는 플레이리스트야.
- 목소리 트랙, 효과음, 배경음악을 Web Audio 로 동시에 재생해.
- 자막은 HTML 오버레이로 그려.
- 왼쪽 위 배지 "미리보기", 오른쪽 위 "씬 #5 · 카메라 천천히 줌인".
- 조작 요소:
  - 이전 씬 / 재생·정지 / 다음 씬
  - 현재 시간 / 전체 시간
  - 자막 켜기·끄기
  - 목소리 언어 표시
  - 전체화면
- 단축키: 스페이스(재생·정지), ←→(5초 이동), ↑↓(이전·다음 씬). 입력칸에 포커스가 있을 때는 동작하지 않아.

**3) 구간 수정 패널 (오른쪽, 선택한 씬 기준)**
- 헤더: "씬 #5 · 0:38 – 0:54".
- **버튼 4개:**
  - "이 구간 다시 만들기": 가격을 버튼 안에 표시해. 카메라 무빙은 `ANIMAKA_SCENE_REGEN_CAM_PT`, AI 모션은 견적가.
  - "여기서 자르기": 재생 위치에서 씬을 둘로 나눠. 대사도 시간 기준으로 나눠.
  - "순서 옮기기": 타임라인 드래그와 같은 동작이야.
  - "구간 삭제": 확인한 뒤 삭제하고, 5초 동안 되돌리기를 보여줘. 환불은 없어.
- **대사·목소리:**
  - 줄마다 본문 수정, 감정 칩, "다시 읽기"(무료), 목소리 바꾸기.
  - 본문을 고치면 그 줄 목소리를 자동으로 다시 만들고, 자막 타이밍도 다시 잡아.
  - 대사가 길어져 씬 길이를 넘으면 씬 길이를 자동으로 늘려. 카메라 무빙 씬만 해당이고, AI 모션 씬은 마지막 프레임을 멈춰서 늘려.
- **자막:**
  - 위치: 하단 가운데(기본) / 하단 왼쪽 / 상단.
  - 스타일 3종: 말풍선(기본, 검은 반투명 둥근 박스 + 흰 굵은 글씨) / 외곽선 / 화자 이름 표시.
  - 위치·스타일은 작품 전체 적용과 이 씬만 적용을 고를 수 있어.
- **다음 씬 전환:** 바로 컷 / 화이트 플래시 / 페이드 / 암전.
- **AI에게 말로 고치기:** 입력칸에 "이 장면 조금 더 길게", "비 소리 크게" 처럼 쓰면 서버가 위 설정값으로 바꿔 적용해. 그림을 다시 그리는 요청이면 비용 확인 모달을 띄워.
- **되돌리기·다시하기:** 헤더 오른쪽 아이콘, Ctrl+Z / Ctrl+Shift+Z. 편집 기록은 최근 50개까지 보관해.

**4) 타임라인 (하단, 가로 스크롤)**
- 트랙 4줄: 영상 / 대사·자막 / 목소리 / 배경음악·효과음.
- **영상 트랙:** 씬 블록 폭 = 길이. 썸네일, 위쪽 3px 움직임 색 띠, `#번호`.
  - 상태별 표시: 완성(밝게) / 만드는 중(흐리게 + "만드는 중 62%") / 대기(흐리게 + "대기") / 실패(빨간 테두리).
  - 블록 끝을 드래그해서 길이를 조절해 (카메라 무빙·정지만).
- **대사·자막 트랙:** 말풍선 블록. 드래그해서 시작 시간을 미세하게 옮겨.
- **목소리 트랙:** 파형을 보여줘.
- **배경음악 트랙:**
  - "음악 고르기"를 누르면 무료 음원 라이브러리 시트가 열려. 8~12곡: 잔잔한 피아노 / 설렘 / 긴장 / 슬픔 / 밝음 등.
  - 전체 볼륨 슬라이더. 대사가 나올 때는 자동으로 음악 볼륨을 줄여 (-12dB).
- 재생 위치 선은 흰색이야. 블록을 누르면 그 씬을 선택하고 재생 위치를 이동해.

**5) 주 버튼 "저장하기"** → 4단계로 이동. 아직 만드는 중인 씬이 있으면 버튼을 비활성화하고 "N씬 남음"을 표시해.

### 3.4 4단계 저장·공개 (`Publish.dc.html`)

**1) 저장 카드**
- 길이 / 씬 / 수정한 구간 수를 보여줘.
- 저장 화질은 결제한 화질 이하에서 골라.
- 진행 표시: "씬을 하나로 합치는 중 78%".
- 주 버튼 "저장하기".
- 저장하면 하나의 mp4로 합쳐 (영상 + 목소리·음악·효과음 믹스 + 자막 레이어). 자막 처리는 두 가지로 나눠:
  - **시청 페이지용:** 자막을 영상에 굽지 않고 WebVTT 로 따로 저장해서 켜고 끌 수 있게 해.
  - **다운로드용:** 자막을 영상에 구운 버전을 따로 만들어.
- 저장된 영상은 내 미디어(`/media`)에도 들어가.
- 안내: "결제는 스토리보드 단계에서 끝났어요 · 저장한 영상은 내 미디어에 들어가요".

**2) 공개·판매 카드**
- **표지 (3:4):** "장면에서 표지 고르기"를 누르면 씬 첫 장면 중에서 고르고, 제목 글자를 넣어 표지를 만들어 (이미지 생성 1회 무료).
- **제목·소개·태그:** 태그는 최대 5개.
- **공개 범위:** 전체 공개 / 링크로만 / 나만 보기. 망가 `mangaVisibility` 와 같은 방식이야.
- **판매 가격:** 무료 / 설정값 목록 중 선택 (§14). 무료 맛보기는 처음 30초 / 1분 / 없음.
- **수익 안내:** "구매 1건마다 판매가의 ○%가 크리에이터 포인트로 쌓여요. ○○마다 정산돼요." 숫자는 설정값으로 둬 (§14).
- **버튼:** 주 버튼 "공개하기" (저장이 끝나기 전에 누르면 "완성되면 바로 공개"로 예약), 보조 버튼 "2화 이어 만들기"(같은 캐릭터·세계관으로 1단계 시작).
- **공개 전 검수:**
  - 기존 이미지 검수 파이프라인(Hive + Google Vision + Sonnet 종합)을 표지와 씬 첫 장면 전체에 돌려.
  - 통과하면 바로 공개해.
  - 의심 판정이면 "검수 중" 상태로 두고 운영 확인 큐에 넣어.
  - FANZA 전체 공개(Y) 정책이 정해지기 전까지는 "전체 공개"를 fan.stipop.ai 안의 공개로만 처리해 (studio 와 같은 이유).

### 3.5 시청 페이지 `/animaka/[id]` (시안 없음, 망가 `pages/manga/[id].js` 구조를 따라줘)

- 16:9 플레이어:
  - 자막 켜기·끄기, 자막 언어 선택 (작품에 있는 언어만), 전체화면, 화질 선택.
  - 무료 맛보기 구간이 끝나면 정지하고 잠금 카드를 보여줘. `MangaUnlock` 과 같은 패턴이고, 가격과 "○○pt로 끝까지 보기" 버튼이 있어.
  - 해제는 `POST /animaka/works/:id/unlock` 으로 해.
- 아래 정보: 제목, 크리에이터(팔로우), 소개, 태그, 좋아요, 조회수, 길이, 같은 시리즈의 다음 화·이전 화.
- "이 작품처럼 만들기": 같은 템플릿으로 1단계를 시작해. 대본은 비공개라서 줄거리 구조만 복제해.
- 신고 버튼은 기존 `report` 페이지로 연결해.

---

## 4. 유저 시점 리뷰에서 나온 개선점 (시안 대비 변경 요약)

작성자가 첫 방문 유저 입장에서 처음부터 끝까지 써본다고 가정하고 막힌 지점을 고친 것들이야. 시안에는 아직 반영 안 된 것도 있으니 아래가 기준이야.

1. **샘플이 정지 이미지 슬라이드였음** → 실제 mp4 자동재생 + 자막 + 소리 버튼. "만들고 싶다"는 동기가 여기서 생겨.
2. **빈 아이디어 칸이 부담스러움** → 예시 칩 3개, 템플릿, 내 채팅 가져오기.
3. **첫 작품 비용·대기 부담** → 첫 작품 기본 길이 1분, 첫 작품 할인 연동, 예상 씬 수 즉시 표시.
4. **캐릭터 이미지 칸이 너무 작았음** → 3:4 큰 카드 + 앞/뒤/얼굴 전환.
5. **결제 전에 목소리를 들을 수 없었음** → 캐스트 목소리 샘플 + 대사별 무료 미리듣기.
6. **가격이 마지막에 나와서 놀람** → 스토리보드에서 씬 단위로 실시간 견적, 확인 모달, 실패 자동 환불.
7. **결제 후 한참 기다림** → 카메라 무빙 씬부터 빨리 완성해서 1~2분 안에 앞부분 미리보기, AI 모션 씬은 임시본으로 채운 뒤 교체, 창을 닫아도 진행, 완료 알림.
8. **"다시 만들기"가 얼마인지 몰랐음** → 버튼 안에 가격 표시, 목소리 다시 읽기는 무료.
9. **편집 실수 복구 불가** → 되돌리기·다시하기, 삭제 후 5초 되돌리기.
10. **소리 편집 수단이 부족** → 감정 칩, 효과음 프리셋, 배경음악 라이브러리, 대사 나올 때 음악 자동 줄임.
11. **시청 페이지가 없었음** → 시청·잠금 해제·시리즈 페이지 추가 (§3.5).
12. **모바일 미고려** → §2.1 반응형 표.
13. **결제 후 스토리 변경 요청** → 결제 후 1~2단계는 읽기 전용, "새 버전으로 복제"로 처리.

---

## 5. 생성 파이프라인 (서버, fanza-api)

```
[1] 대본         LLM (망가 대본과 같은 모델·경로)
                 → 막(act) 5개 내외, 씬 N개, 씬마다 {장소, 상황, 인물, 대사[], 연출 제안}
[2] 캐릭터 시트   studio 이미지 생성 (Seedream). 앞 → 뒤·얼굴(앞모습 레퍼런스)
[3] 씬 첫 장면    Seedream + 레퍼런스(등장인물 시트 + 장소 그림)
                 화면비 16:9 1536x864 (9:16 이면 864x1536), 후보 2장
[4] 목소리        voice.royalchat.ai Gemini TTS, 대사 1줄 = 파일 1개 (24kHz mono PCM → WAV → S3)
                 감정 칩 → TTS 톤 지시문으로 매핑
[5] 씬 영상
    카메라 무빙   서버 ffmpeg zoompan (30fps, 720p/1080p), 씬 길이 = §3.2 규칙
    AI 모션       기존 Atlas scene 파이프라인 img2video. 첫 장면 = 시작 프레임, 모션 문장 = 프롬프트
                 길이는 Atlas 지원 길이. 대사가 더 길면 마지막 프레임을 멈춰서 연장
    정지         ffmpeg 로 정지 프레임 영상
[6] 미리보기      클라이언트 플레이리스트 (씬 mp4 + 목소리 WAV + 효과음 + 자막 JSON)
[7] 저장          ffmpeg concat + 전환 효과 + 오디오 믹스(목소리 0dB, 효과음 -10dB, 음악 -18dB, 대사 중 음악 -12dB 더 줄임)
                 → mp4 (자막 없음) + WebVTT (언어별) + 자막 구운 mp4 (다운로드용)
```

**처리 방식**
- 모든 생성은 비동기 작업 큐로 처리하고, 클라이언트는 `utils/pollAsync.js` 와 같은 방식으로 상태를 받아.
- 작업 상태: `queued | running | done | failed | refunded`.
- 동시 처리 한도:
  - 유저당 Atlas 동시 작업 2개 (기존 scene 쿼터와 합산)
  - ffmpeg 작업은 서버 전체에서 CPU 수만큼
- ffmpeg 를 돌릴 서버 위치는 §13 를 확인해줘.

**자막 생성 규칙**
- 줄마다 시작 시간 = 그 줄 목소리 시작, 끝 시간 = 목소리 끝 + 0.3초.
- 한 줄은 최대 2행이고, 20자(일본어)·24자(한국어) 기준으로 자동 줄바꿈해.
- 번역 자막은 LLM 으로 만들고, 원문 대사가 바뀌면 다시 번역해.

**안전**
- 대본, 이미지 프롬프트, 모션 문장에 미성년을 떠올리게 하는 단어나 실존 인물·기존 IP 캐릭터 이름이 있으면 막아.
- 첫 장면과 표지는 기존 검수 파이프라인을 거쳐.
- 등장인물 나이는 20세 미만이면 20세로 보정해 (studio 와 동일).

---

## 6. 데이터 모델 (새 테이블, 기존 테이블 ALTER 금지)

`sql/animaka.sql` 에 `CREATE TABLE IF NOT EXISTS` 로 작성해서 다시 실행해도 안전하게 해줘. 컬럼 이름은 기존 망가 테이블 규칙(T_ 접두사, 대문자)을 따라줘.

| 테이블 | 주요 컬럼 |
|---|---|
| `T_ANIMAKA_WORK` | WORK_ID, USER_ID, TITLE, LOGLINE, STYLE, ASPECT, LENGTH_MIN, VOICE_LANG, SUB_LANGS(json), STATUS(draft/board/paid/generating/editing/saved/published), VISIBILITY(P/U/Y), PRICE_PT, FREE_SEC, COVER_URL, TEMPLATE_ID, PARENT_WORK_ID(시리즈·복제), QUALITY, PAID_PT, VIDEO_URL, VTT_URLS(json), DOWNLOAD_URL, DURATION_SEC, VIEW_CNT, LIKE_CNT, SALE_CNT, REVIEW_STATUS, CREATED_AT, UPDATED_AT |
| `T_ANIMAKA_ACT` | ACT_ID, WORK_ID, NO, TITLE, SUMMARY |
| `T_ANIMAKA_CAST` | CAST_ID, WORK_ID, ASSISTANT_ID(기존 캐릭터면), NAME, AGE, DESC, GENDER, VOICE_ID, FRONT_URL, BACK_URL, FACE_URL, SHEET_VER, COLOR |
| `T_ANIMAKA_PLACE` | PLACE_ID, WORK_ID, NAME, IMG_URL |
| `T_ANIMAKA_SCENE` | SCENE_ID, WORK_ID, ACT_ID, NO, PLACE_ID, SITUATION, MOTION(cam/ai/still), CAM_PRESET, AI_PROMPT, DURATION_MODE(auto/manual), DURATION_SEC, TRANSITION, SFX, FRAME_URL, FRAME_CANDIDATES(json), FRAME_REDRAW_CNT, VIDEO_URL, TEMP_VIDEO_URL, GEN_STATUS, ATLAS_ID, PRICE_PT, SUB_POS, SUB_STYLE |
| `T_ANIMAKA_LINE` | LINE_ID, SCENE_ID, NO, CAST_ID(null=내레이션), TEXT, EMOTION, VOICE_URL, VOICE_SEC, START_MS, TRANSLATIONS(json) |
| `T_ANIMAKA_JOB` | JOB_ID, WORK_ID, SCENE_ID, KIND(script/sheet/frame/voice/cam/ai/merge), STATUS, PT, ERROR, CREATED_AT, DONE_AT |
| `T_ANIMAKA_HISTORY` | 편집 기록 (WORK_ID, SEQ, PATCH json) — 되돌리기용, 최근 50개 |
| `T_ANIMAKA_UNLOCK` | WORK_ID, USER_ID, PT, CREATED_AT — 시청자 잠금 해제 |
| `T_ANIMAKA_TEMPLATE` | TEMPLATE_ID, TITLE_{JA,KO,EN}, IDEA, LENGTH_MIN, THUMB_URL, CAST_PRESET(json), SORT |

---

## 7. 과금 규칙 (서버 견적 = 진실)

견적 API `POST /animaka/works/:id/quote` 는 `{ lines: [{sceneId, motion, sec, pt}], camSec, aiSec, total, discounted, have }` 를 돌려줘. 계산 규칙은 다음과 같아.

- **카메라 무빙·정지 씬:** `sec × ANIMAKA_CAM_PT_PER_SEC`. 이미지, 목소리, 합치기 비용이 포함된 가격이야.
- **AI 모션 씬:** 기존 `GET /v4.0.1/scene/price` 의 `ratePerSec.create[quality]` × Atlas 길이. 기존 씬 영상 가격표와 같은 기준을 써줘.
- **화질 1080p:** 카메라 무빙 단가 × `ANIMAKA_1080_MULT`. AI 모션은 가격표의 1080p 값을 써.
- **첫 작품 할인:** `campaign/first-use` 와 연동해.
- **결제 처리:**
  - 기존 DMM 포인트 차감 경로를 써 (§13 확인).
  - 결제 기록에는 `feature = "animaka"` 를 남겨. `lang/*.json` 의 `feature` 목록에 "AI 애니"(ko) / "AIアニメ"(ja) / "AI Anime"(en) 를 추가해.
- **실패 환불:** 씬 작업이 최종 실패(재시도 2회 후)하면 그 씬 가격을 자동 환불하고 `refunded` 로 표시해. 유저는 "다시 만들기(무료 1회)"를 쓸 수 있어.
- **편집 중 다시 만들기:**
  - 카메라 무빙 씬은 `ANIMAKA_SCENE_REGEN_CAM_PT`.
  - AI 모션 씬은 견적가.
  - 목소리 다시 읽기는 무료 (하루 한도 `ANIMAKA_VOICE_REGEN_DAILY` 기본 300줄).
- **시청자 잠금 해제:** 판매가를 차감하고, 크리에이터 몫은 `ANIMAKA_CREATOR_SHARE` 로 계산해서 크리에이터 포인트로 적립해. 정산 방식은 §14.

> ⚠️ **기존 씬 영상 가격표 기준으로 AI 모션은 1초당 단가가 커.** 그래서 AI 모션 씬 상한과 첫 작품 1분 기본값이 중요해. 견적에 항상 "AI 모션 b씬 · y초 = ○pt"를 따로 보여줘서 유저가 스스로 줄일 수 있게 해줘.

---

## 8. API (fanza-api, `/v4.0.1/animaka`, 응답 형식은 망가와 동일 `{header:{code}, body}`)

| 메서드·경로 | 용도 |
|---|---|
| GET `/templates` | 템플릿 목록 |
| GET `/works?official=1` / GET `/works/mine` / GET `/works/:id` | 공식·내 작품·상세 (시청자는 공개 정보 + 잠금 상태) |
| POST `/works` | 작품 생성 {idea \| roomId \| script, castAssistantIds[], lengthMin, style, aspect, voiceLang, subLangs, templateId} |
| PUT `/works/:id` / DELETE `/works/:id` | 제목·옵션 수정 / 삭제 |
| POST `/works/:id/clone` | 새 버전 복제 (결제 후 스토리 변경용) |
| POST `/works/:id/script` {force} | 대본 생성·재생성 (비동기) |
| PUT `/works/:id/script` | 막·로그라인 수정 |
| POST `/works/:id/assist` {message} | AI 연출 도우미 → {reply, changes[], chips[]} |
| POST/PUT/DELETE `/works/:id/cast[/:castId]` | 인물 추가·수정·삭제 (목소리 포함) |
| POST `/cast/:castId/sheet` {redraw} | 캐릭터 시트 생성·다시 그리기 |
| POST `/works/:id/frames` {sceneIds?} | 첫 장면 일괄·부분 생성 |
| POST `/scenes/:sceneId/frame` {prompt?} / PUT `/scenes/:sceneId/frame` {url} | 다시 뽑기 / 후보 선택 |
| POST/PUT/DELETE `/works/:id/scenes[/:sceneId]` · PUT `/works/:id/scenes/order` | 씬 추가·수정·삭제·순서 |
| POST/PUT/DELETE `/scenes/:sceneId/lines[/:lineId]` · PUT `/scenes/:sceneId/lines/order` | 대사 |
| POST `/lines/:lineId/preview` | 대사 목소리 미리듣기 → {voiceUrl, sec} (캐시) |
| POST `/works/:id/quote` | 견적 (§7) |
| POST `/works/:id/pay` {quality} | 결제 + 생성 시작 → {jobs[]} (부족하면 code·need·have, 기존 scene 과 같은 형식) |
| GET `/works/:id/progress` | 씬별 생성 상태 (폴링 4초) |
| POST `/scenes/:sceneId/regen` | 구간 다시 만들기 (과금) |
| POST `/scenes/:sceneId/split` {atMs} | 자르기 |
| POST `/lines/:lineId/voice` | 다시 읽기 |
| PUT `/works/:id/audio` {bgmId, bgmVol} · GET `/bgm` | 배경음악 |
| POST `/works/:id/edit` {instruction} | AI에게 말로 고치기 → 적용된 patch |
| POST `/works/:id/undo` · POST `/works/:id/redo` | 편집 기록 |
| POST `/works/:id/save` {quality} | 합치기 (비동기) |
| POST `/works/:id/cover` {sceneId} | 표지 만들기 |
| PUT `/works/:id/publish` {visibility, pricePt, freeSec, title, intro, tags} | 공개 설정 |
| POST `/works/:id/unlock` | 시청자 잠금 해제 |
| POST `/works/:id/like` · POST `/works/:id/view` | 좋아요·조회 |

**오류 코드:** 망가 오류 코드 체계를 재사용하고, 새 코드는 `9xxx` 대역을 써. 프론트에는 `mangaErrorText` 같은 매핑 함수 `animakaErrorText` 를 만들어줘.

---

## 9. 프론트 구현 지도 (fan.stipop.ai)

| 파일 | 내용 |
|---|---|
| `pages/animaka/index.js` | 홈 |
| `pages/animaka/create.js` | 1~4단계 한 페이지. 쿼리 `work`, `step`. 진행 중 작품은 `utils/animakaActive.js` 로 기억 (`mangaActive` 와 같은 방식) |
| `pages/animaka/[id].js` | 시청 |
| `pages/animaka/mine.js` | 내 애니 전체 |
| `utils/animaka.js` | API 묶음 + `animakaTrack` + `animakaErrorText` (`utils/manga.js` 구조 복제) |
| `components/view/animaka/*` | `AnimakaShell`, `StepHeader`, `SamplePlayer`, `IdeaCard`, `CastCard`, `StoryInfo`, `AssistPanel`, `SceneGrid`, `SceneDetail`, `PayBar`, `PayConfirmModal`, `GenStatusBar`, `PreviewPlayer`(플레이리스트+WebAudio), `EditPanel`, `Timeline`, `BgmSheet`, `VoicePicker`(ChatVoice 재사용), `SaveCard`, `PublishCard`, `WatchPlayer`, `AnimakaUnlock` |
| `components/layout/AppShell.js` | `SHELL_TYPES` 에 `/animaka`, `/animaka/create`, `/animaka/[id]`, `/animaka/mine` 추가 |
| `components/view/chat/SideMenu.js` | 미디어 제작 그룹의 "AI 미니 망가" 아래에 "Animaka" + NEW 배지, 경로 `/animaka` |
| 홈 진입 | 홈의 "만들기" 카드 하위 문구와 AI 미니 망가 배너 옆에 Animaka 배너 1개 추가 (기존 배너 스타일) |
| `lang/{ja,ko,en}.json` | `animaka.*` 키 |

**트래킹 (Mixpanel, `animakaTrack`)**
- `animaka_home_view`
- `animaka_sample_play` {workId, unmuted}
- `animaka_idea_submit` {source: idea|chat|script|template, lengthMin}
- `animaka_script_done` {ms}
- `animaka_sheet_redraw`
- `animaka_board_view` {scenes}
- `animaka_frame_redraw`
- `animaka_motion_change` {from, to}
- `animaka_line_preview`
- `animaka_quote` {total, aiScenes, camSec, aiSec}
- `animaka_pay_click`
- `animaka_pay_result` {ok, code, total}
- `animaka_point_short` {need, have}
- `animaka_gen_first_ready` {ms}
- `animaka_gen_done` {ms, failed}
- `animaka_edit_action` {type}
- `animaka_regen` {motion, pt}
- `animaka_save` {quality}
- `animaka_publish` {visibility, pricePt}
- `animaka_watch` {workId, sec}
- `animaka_unlock` {workId, pt}

주요 퍼널은 아이디어 제출 → 결제 클릭 → 결제 성공 → 저장 → 공개 → 첫 판매야.

---

## 10. 비동기·이탈 대응

- 진행 중인 작품과 단계는 서버 상태가 기준이야. 클라이언트는 `animakaActive` 로 재진입 위치만 기억해.
- 생성 중에 창을 닫아도 서버 큐는 계속 돌아. 완료되면 기존 알림벨(`NoticeBell`)에 "애니가 완성됐어요" 알림을 넣어.
- 폴링: 4초 간격. 탭이 숨겨져 있으면 15초 간격으로 늘려.
- 네트워크 오류가 나면 재시도 버튼을 보여줘. 결제 요청은 멱등 키(`Idempotency-Key`)를 붙여서 중복 결제를 막아.

---

## 11. 완료 기준 (Devin 자체 점검)

1. 로그인 → 아이디어 입력 → 1분 길이 → 스토리 → 시트 3명 → 스토리보드 6씬(AI 모션 1, 카메라 무빙 5) → 대사 미리듣기 → 견적 확인 → 결제 → 2분 안에 첫 씬 재생 → 모든 씬 완성 → 대사 1줄 수정(목소리·자막 자동 갱신) → 저장 → 공개. 이 흐름이 끊김 없이 동작해야 해.
2. 포인트가 부족할 때 PointShort 가 열리고, 충전 후 복귀해.
3. AI 모션 씬 실패를 강제로 일으키면 자동 환불되고, 무료 다시 만들기가 동작해.
4. 다른 계정으로 시청 페이지에 들어가면 무료 맛보기 → 잠금 → 해제 → 끝까지 재생돼. 크리에이터 몫이 적립돼.
5. 모바일 375px 에서 전 단계를 사용할 수 있어 (§2.1).
6. ja/ko/en 전환 시 문구가 빠짐없이 나와.
7. 결제 후 스토리 단계는 읽기 전용이고, 복제가 동작해.
8. 검수 의심 판정이 나오면 공개가 "검수 중"으로 멈춰.

---

## 12. 화면 문구 기준 (ko, ja는 가나 위주로 번역)

| 키 | ko |
|---|---|
| animaka.hero.title | 한 줄 아이디어로, 목소리까지 들어간 나만의 애니를 |
| animaka.hero.made | 이 작품도 유저가 Animaka로 만들었어요 |
| animaka.hero.cta | 나도 만들어 보기 |
| animaka.idea.free | 스토리와 스토리보드 그림까지는 무료예요. 영상은 씬 길이를 보고 스토리보드에서 결제해요. |
| animaka.story.cta | 스토리보드 그리기 · {{n}}장 |
| animaka.cast.lock | 얼굴·의상을 한 번 고정하면 모든 씬에서 같은 모습으로 나와요 |
| animaka.board.pay | 결제하고 영상 만들기 |
| animaka.board.refund | 생성에 실패한 씬은 자동 환불 |
| animaka.board.confirm1 | 결제 후에는 스토리·캐릭터를 바꿀 수 없어요. 대사·목소리·자막은 편집에서 고칠 수 있어요. |
| animaka.edit.status | 영상 만드는 중 · {{done}} / {{total}}씬 완성 |
| animaka.edit.statusDesc | 첫 씬부터 순서대로 만들어요. 완성된 씬은 바로 보고 고칠 수 있어요. 창을 닫아도 계속 만들어요. |
| animaka.edit.save | 저장하기 |
| animaka.publish.paid | 결제는 스토리보드 단계에서 끝났어요 · 저장한 영상은 내 미디어에 들어가요 |
| animaka.notice.done | 애니가 완성됐어요 |

---

## 13. Devin이 직접 확인할 것 (작성자가 못 본 부분)

1. **fanza-api:** manga·scene·studio 라우트·서비스의 실제 구조. 위 API 는 그 구조에 맞춰 같은 방식으로 만들어줘. 기존 모듈은 수정하지 말고 새 모듈로 만들어 (studio 원칙과 동일).
2. **목소리 서버 (voice.royalchat.ai):** 서버 간 호출로 대사 1줄을 WAV 로 받는 REST 경로가 있는지 확인해.
   - 없으면 소켓 `/anima` 서버의 TTS 함수를 재사용하는 배치용 REST 를 추가해. 예: `POST /v1/anima/tts {text, voiceId, lang, emotion} → wav`.
   - 모델과 목소리 catalog 는 기존 것을 그대로 써.
3. **Atlas:** 기존 scene 파이프라인을 "시작 이미지 URL + 프롬프트 + 길이"로 서버 안에서 호출할 수 있는지 확인해. 기존 scene 레코드를 쓰지 않고 Animaka 작업으로 분리해야 해.
4. **ffmpeg 실행 위치:** fanza-api 배포 환경(Railway/nixpacks 등)에 ffmpeg 가 있는지, CPU 여유가 있는지 확인해. 없으면 별도 워커(같은 저장소의 worker 프로세스)를 만들어.
5. **DMM 포인트 차감·환불 API:** 기존 scene·manga 결제가 쓰는 함수를 재사용해. 환불 경로도 같은 곳에 있는지 확인해.
6. **S3 저장 경로와 CDN:** 기존 manga·scene 과 같은 버킷 규칙을 써.
7. **알림벨에 알림 넣는 방법:** `NoticeBell` 의 데이터 소스를 확인해.
8. **공식 샘플 등록 방법:** 운영자가 공식 작품을 지정하는 방식. 망가 `official` 과 같은 방식을 써.

---

## 14. 결정 필요 (Tony) — 아래 기본값으로 구현하고, 서버 설정값으로 빼줘

| 설정 키 | 기본값 | 설명 |
|---|---|---|
| ANIMAKA_CAM_PT_PER_SEC | 3 | 카메라 무빙·정지 씬 1초당 pt (이미지·목소리·합치기 포함) |
| ANIMAKA_1080_MULT | 1.5 | 1080p 배수 |
| ANIMAKA_AI_SCENE_MAX | 1분 2, 3분 4, 5분 6, 10분 10 | AI 모션 씬 상한 |
| ANIMAKA_SHEET_REDRAW_PT | 20 | 캐릭터 시트 다시 그리기 (하루 3회 무료 후) |
| ANIMAKA_FRAME_REDRAW_PT | 20 | 첫 장면 다시 뽑기 (씬당 3회 무료 후) |
| ANIMAKA_SCENE_REGEN_CAM_PT | 10 | 편집 중 카메라 무빙 씬 다시 만들기 |
| ANIMAKA_PREVIEW_TTS_DAILY | 200 | 결제 전 대사 미리듣기 하루 한도 |
| ANIMAKA_VOICE_REGEN_DAILY | 300 | 편집 중 다시 읽기 하루 한도 |
| ANIMAKA_PRICE_OPTIONS | 0, 100, 300, 500, 1000 | 판매 가격 선택지(pt) |
| ANIMAKA_CREATOR_SHARE | 0.3 | 판매가 중 크리에이터 몫 (FANZA 6 : stipop 4 배분 이후 stipop 몫 기준으로 계산할지 확인 필요) |
| ANIMAKA_SETTLE | 크리에이터 포인트 적립만 (현금 정산 없음) | 정산 방식 |
| 스토리보드 첫 장면 비용 | 무료 (하루 작품 3개까지) | 이미지 원가가 들지만 결제 전환을 위해 무료로 둠 |
| FANZA 전체 공개 | 보류 (fan.stipop.ai 안 공개만) | FANZA 등록 정책 결정 후 |
