# fanza-stipop 유저 깊이 단계 리뷰 (2026-11-15 기준)

읽기 전용 조회 결과 (프로덕션 DB SELECT + Mixpanel 4030771). 유저 단위 원본 없음, 집계만.

- `fanza_funnel_report.md` — 단계·퍼널·리텐션·매출·기능·첫 캐릭터·데이터 품질 + 쿼리 부록
- `fanza_funnel_numbers.json` — 리포트의 모든 숫자
- `csv/` — 표별 집계 CSV (JSON 섹션 이름 = 파일 이름, `scalars.csv` = 단일 값)

## 추가 분석 B1–B8
- `fanza_funnel_b_report.md` — S1→S2 이탈 원인, 결제 벽, 코호트 LTV, S7 프로필, 영상 퍼널, S0 경로, D1 분할, 10/5 주 D1 상승 원인 후보 + 추출 쿼리
- `fanza_funnel_b_numbers.json` — B 리포트의 모든 숫자
- `csv/b*.csv` — B 표별 집계 CSV (상위 10명은 순번만, ID 없음)
