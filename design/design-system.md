# Stipop FANZA

The look of Stipop on FANZA キャラチャット (fan.stipop.ai): a dark, night-time app for adult AI character chat, image, video and manga creation. Built from `stipop-development/fan.stipop.ai` at `95e6189`.

## Voice

- Short, warm, direct. Menu labels are nouns ("캐릭터 채팅", "영상 제작"); buttons are verbs ("만들어 보기", "대화 이어가기").
- Shipped in Japanese first, also Korean and English. Prefer kana over hard kanji in display copy.
- Money is always in points: `7 pt`, `보너스 4,510pt`. Never show yen or won in the UI.
- Badges are one word, upper case Latin or short Korean: `NEW`, `HOT`, `리뉴얼`, `준비중`.

## Visual foundations

- **Dark first.** `bg` behind everything, `sidebar` for the 296px left menu (`sidebar-width`), `surface` for cards, `surface-2` for anything nested inside a card. Borders are `line`, never a solid grey.
- **One brand gradient.** `linear-gradient(95deg, brand-pink 0%, brand-violet 55%, brand-indigo 100%)`. It is reserved for the single primary action on a screen (`PrimaryBtn`), rank chips and brand moments. Everywhere else, selected states use solid `brand-pink`.
- **Points are yellow.** `point-yellow` with `on-point` text is only for buying DMM points and bonus figures.
- **Feature tones.** Each product area has a tone used on its home card and icons: chat `tone-chat`, NTR `tone-ntr`, group `tone-group`, create `tone-create`, media `tone-media`. New media features (video, image, AI manga, Animaka) use `tone-media`.
- **Shapes.** Buttons and inputs are 46px tall with `radius-md`; list cards and banners `radius-lg`; home hero cards `radius-xl`; chips and badges `radius-pill`.
- **Imagery carries the page.** Character art fills cards edge to edge (`object-fit: cover`), with text on a dark bottom fade. Do not put character art in small boxes; give it at least a 3:4 card.

## Type

Poppins for Latin and numbers, falling back to Noto Sans JP / Noto Sans KR. Weights are heavy: titles 800, buttons 800, labels 500. Scale: `display` 44, `h1` 32, `h2` 24, `title` 16, `button` 15, `body` 14, `label` 13, `caption` 12, `micro` 11.

## Components (in code)

- `PrimaryBtn`: 46px, padding 0 22px, `radius-md`, brand gradient, `on-brand` 15/800, `shadow-cta`.
- `GhostBtn`: 46px, `radius-md`, 1px `line` border on `surface`, `ink` 15/700.
- Side menu (`components/view/chat/SideMenu.js`): logo, account row, point pill + yellow DMM purchase button, grouped sections (캐릭터 채팅, 미디어 제작) with HOT/NEW badges, chat list, light/dark toggle at the bottom.
- Home feature cards (`components/view/home/HomeC.js`): three large image cards with a tone-coloured bottom fade, title, sub-label and a "보러 가기" pill.

## Iconography

Line icons from `lucide-react` at 16–20px, stroke 2, coloured `ink` or `sub`. Some legacy icons are PNGs on `img.stipop.io`. Never emoji.

## Logos

`assets/Logos/fanza-app-icon-c4.png` is the app icon shown in the side menu. `assets/Logos/fanza-logo-coral.png` is the coral double speech-bubble mark.

## Not synced

- Fonts are Google-hosted (Poppins, Noto Sans JP/KR), so no font files are copied.
- Components were not built into a live bundle; the list above is reference only.
- The NTR screen palette (`utils/ntrTheme.js`) is reduced to `ntr-accent`.
