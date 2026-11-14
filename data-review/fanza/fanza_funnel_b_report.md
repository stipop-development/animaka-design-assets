# fanza-stipop 추가 분석 B1–B8 (2026-11-15 기준, 읽기 전용)

- 기준 시점 2026-11-15 00:00 JST. 프로덕션 DB SELECT만 사용 + Mixpanel(4030771, 11/14까지). QA·테스트 계정(qa-agent-*, 762614, 공식 캐릭터 계정 723711) 제외.
- pt는 DMM 포인트 사용량(현금 매출 아님). "12주 가입자" = 2026-08-17 ~ 11-08 가입 11,949명.
- 모든 숫자는 `fanza_funnel_b_numbers.json`, 표별 CSV는 `csv/b*.csv`. 유저 단위 원본은 포함하지 않음.

## 결론

1. **S1→S2 이탈의 대부분은 결제 벽이 아니다.** 20회 전에 이탈한 6,729명 중 68.1%는 마지막 메시지 때 무료분이나 보너스가 남아 있었다. 무료·보너스가 0이고 포인트 부족 이벤트까지 본 유저는 8.5%다. 메시지 1회 이탈자는 100% 무료분이 남아 있었다. 즉 첫 몇 턴에서 대화 자체에 흥미를 잃고 나가는 쪽이 크다.
2. 첫 7일 메시지 수: 0회 35.5%, 1회 9.6%, 2~5회 28.3%, 6~10회 13.0%, 11~19회 6.9%, 20회+ 6.8%. **보낸 유저 기준 59%가 5회 이하에서 멈춘다.** 무료분이 상대 캐릭터 기준 5회이므로 "무료 5회 소진 지점"과 겹치지만, 위 1번처럼 잔액이 있는 채로 나간 비율이 더 크다.
3. 첫 캐릭터별 20회 도달률(누적): 공식 1:1 15.9% > 유저 제작 1:1 13.0% > NTR 11.8% > 그룹 5.0%(20명) / 스토리 7.7%(13명). 차이는 있지만 크지 않다. 첫 답장 응답 시간·에러는 이탈과 뚜렷한 관계가 없다(실패율 1% 미만, 구간별 차이 비단조).
4. **결제 벽:** 상대 캐릭터 무료 5회를 다 쓴 3,241명 중 DMM 결제는 1시간 23.2% / 24시간 26.0% / 7일 29.4%. 결제가 일어나면 대부분 1시간 안이다. 완전 부족(포인트 부족 팝업·에러) 이후 7일 결제는 12.3%. 첫 결제는 중앙값 20pt(=대화 1~2회)로 작고, 결제 직전 기능은 1:1 대화 37%·무드샷 31%·NTR 룸 16%·영상 6%.
5. **LTV:** 가입자 1명당 D30 누적 pt는 8~9월 코호트 256~712pt, 10/5 주 1,101pt. 다만 코호트마다 상위 1명이 크게 좌우한다(10/5 주는 1명이 45%, 빼면 601pt; 9/7 주는 1명이 56%, 빼면 313pt). 최근 30일 pt 중 최근 30일 가입자 비중은 20.5%, 그 이전 가입자 79.5%. S7을 빼면 41.5% vs 58.5%.
6. **S7 623명:** 10월 가입이 23.8%(pt 35.1%). 가입→S7 중앙값 4.6일(60%가 7일 안). 첫 기능 1:1 대화 69.5%. pt는 영상 44.7%·대화 32.7%·씬 이미지 10.4%. 제작자 53.6%. 30일 중 활동일 중앙값 6일. 상위 10명 중 8명이 영상 중심.
7. **영상:** 12주 가입자 중 7일 안 영상 생성 4.6%(보낸 유저 기준 6.0%, 7일 내 결제자 기준 20.7%). 첫 영상 후 2번째까지 47.9%(중앙 23분 뒤). 영상 사용자 D30 4.5% vs 미사용 0.6%, 가입 후 30일 pt 7,356 vs 224(자기선택 효과 포함, 인과 아님).
8. **S0(메시지 0회) 4,187명:** Mixpanel 매칭 92.6%. 처음 페이지는 연령 확인 팝업 51%·chat_room 37%. chat_room 페이지 도달은 79.5%(랜딩 포함 추정, 상한값)이고, 1:1 `Chat Room View` 이벤트 기준 실제 방 진입은 5.4%다. 즉 대부분 방에 들어가기 전, 연령 확인·첫 화면에서 끝난다. 캐릭터 상세 대용인 Artist 페이지는 6.2%. 본 페이지 수 중앙값 6.
9. **D1 차이:** PC/모바일 차이 없음(12.9% vs 12.4%, 보낸 유저). 공식/유저 제작 첫 캐릭터도 거의 같음(11.8% vs 12.6%). 선톡 받은 유저 D1 23.0% vs 15.4%, 선톡을 연 유저 55.6%(열람 자체가 재방문이라 인과 아님). 웰컴 7일 보너스는 11/13 시작이라 D7 판단 불가.
10. **10/5 주 D1 상승의 1순위 후보는 10/7 19:00 라이브된 "재방문 보상(복귀일 무료 3회 × 3일)"이다**(API #246 + 웹 #302). 일별 D1은 10/7 가입자부터 계단식으로 올랐고, 10/7 이후 D1 활동 유저의 거의 전원이 그날 재방문 보상을 받았다. Mixpanel 페이지뷰 기준 D1 방문율은 14.0%→16.4~18.2%로 소폭 올랐고, "D1에 들어왔지만 메시지·기능 0"인 비율이 10.1%→5.7%로 줄었다. **재방문자 수가 늘었다기보다, 돌아온 유저가 무료 3회로 실제 대화를 하게 된 효과가 크다.** 10/2 선톡(First Talk, #234/#235/#296) 단독 기간(10/2~10/6)에는 D1 변화가 없었다.

## B1. S1→S2 이탈 원인

### 1-1 첫 7일 메시지 수 분포 (12주 가입자 11,949명)

| 버킷 | 유저 | 전체 대비 | 보낸 유저 대비 |
|---|---|---|---|
| 0 | 4,240 | 35.5% | - |
| 1 | 1,144 | 9.6% | 14.8% |
| 2-5 | 3,381 | 28.3% | 43.9% |
| 6-10 | 1,549 | 13.0% | 20.1% |
| 11-19 | 826 | 6.9% | 10.7% |
| 20+ | 809 | 6.8% | 10.5% |


주별 분포는 `csv/b1_first7d_msg_dist_by_week.csv`.

### 1-2 무료분·보너스 지급 구조

| 항목 | 지급량 | 근거 |
|---|---|---|
| 상대 캐릭터 무료 메시지 | 5회 (OWNER=N 1행/유저, 내 캐릭터 대화는 별도 5회) | T_USER_CHAT_FREE, API ROOM_FREE_LIMIT=5 |
| 재방문 보상 | 복귀일마다 무료 3회, 최대 3일 (가입일 제외) | T_RETURN_REWARD, 시작 2026-10-07 18:25:52 |
| 가입 보너스 | 300pt (225명) | T_SIGNUP_BONUS, 시작 2026-11-13 11:11:55 |
| SNS 팔로우/웰컴 보너스 | 캠페인별 30~45pt 내외 | T_BONUS_LEDGER (기록 시작 2026-11-02 18:59:33) |
| 캠페인 크레딧 autumn2026 | 중앙값 100pt (2,320명) | T_CAMPAIGN_CREDIT, 시작 2026-10-23 17:37:31 |
| 대화 1회 가격 | 15pt (모델별 상이) | T_DMM_POINT 관측 중앙값 |


12주 가입자 상대 캐릭터 무료분 사용량(0~5): 0회 4,097명, 1회 959명, 2회 501명, 3회 441명, 4회 392명, 5회 3,386명.

| 캠페인 | 유저 | 지급 pt |
|---|---|---|
| instagram_follow_v1 | 466 | 13,980 |
| none | 2 | 2,000 |
| signup_v1 | 225 | 67,500 |
| welcome_v1 | 113 | 4,575 |
| welcome_v1_test | 3 | 195 |
| x_follow_v1 | 582 | 26,190 |
| youtube_follow_v1 | 552 | 16,560 |


### 1-3 이탈자의 마지막 메시지 시점 잔액

정의: 12w signups (8/17-11/07) with >=1 msg, <20 msgs ever, no activity in last 7d; balances at last message: room free (OWNER=N row), today return reward, bonus ledger BALANCE_AFTER, campaign credit; shortage event = Mixpanel Send Fail Point / Popup point_short / Error point_shortage within -10min..+24h of last msg


| 총 메시지 | 이탈자 | 무료·보너스 남음 | 0 + 부족 이벤트 | 0 + 기결제자 | 0 + 이벤트 없음 | 무료·보너스 0 합 |
|---|---|---|---|---|---|---|
| 1 | 1,073 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 2-5 | 3,209 | 70.9% | 8.7% | 1.0% | 19.3% | 29.1% |
| 6-10 | 1,567 | 49.9% | 13.4% | 13.3% | 23.4% | 50.1% |
| 11-19 | 880 | 50.9% | 9.4% | 26.2% | 13.4% | 49.1% |
| 합계 | 6,729 | 68.0% | 8.5% | 7.0% | 16.4% | 31.9% |


### 1-4 첫 대화 캐릭터 유형별 20회 도달률 (S1 유저)

| 첫 캐릭터 | 유저 | 7일 내 20회 | 30일 내 20회 | 누적 20회 | 7일 내 결제 |
|---|---|---|---|---|---|
| direct_official | 769 | 12.2% | 13.3% | 15.9% | 27.7% |
| direct_ugc | 6,187 | 10.1% | 10.9% | 13.0% | 30.3% |
| group | 20 | 0.0% | 7.1% | 5.0% | 30.0% |
| ntr | 1,047 | 8.9% | 10.8% | 11.8% | 35.0% |
| story | 13 | 0.0% | 0.0% | 7.7% | 7.7% |


### 1-5 첫 답장 응답 시간·에러

DB(T_AI_CHAT_MESSAGE query→answer REG_DATE 차이, 1:1 첫 메시지) 중앙값 2.0초.


| 첫 답장 지연(DB) | 유저 | 2회+ 전송 | 누적 20회 |
|---|---|---|---|
| 10-20s | 274 | 85.4% | 15.0% |
| 20-40s | 16 | 87.5% | 12.5% |
| 40s+ | 2 | 0.0% | 0.0% |
| 5-10s | 1,614 | 84.7% | 13.4% |
| <5s | 5,009 | 89.8% | 13.2% |
| no_answer | 42 | 85.7% | 14.3% |


| 첫 답장 실패(DB ERROR_TYPE/STATUS) | 유저 | 2회+ 전송 | 누적 20회 |
|---|---|---|---|
| False | 6,891 | 88.5% | 13.3% |
| True | 66 | 72.7% | 15.2% |


Mixpanel 서버 이벤트(Claude/Gemini Response Details) 첫 응답: 6,573명, 중앙 3.3초, 실패율 0.9%.


| 응답 시간(MP) | 유저 | 2회+ 전송 | 누적 20회 |
|---|---|---|---|
| 10-20s | 338 | 89.6% | 24.0% |
| 2-5s | 2,631 | 85.3% | 10.3% |
| 20s+ | 24 | 83.3% | 16.7% |
| 5-10s | 1,522 | 86.9% | 12.8% |
| <2s | 2,054 | 95.1% | 21.6% |
| na | 4 | 50.0% | 0.0% |


해석: 지연 구간별 차이가 단조롭지 않다(<2초와 10~20초가 모두 높음). 모델·캐릭터 종류가 섞인 영향으로 보이며, 응답 시간·에러가 이탈의 주원인이라는 신호는 없다. 첫 답장 실패 표본은 60~66명뿐이다.

## B2. 결제 벽

| 기준 | 대상 | 1시간 | 24시간 | 7일 | 이후 누적 |
|---|---|---|---|---|---|
| room_free_exhausted | 3,241 | 23.2% | 25.9% | 29.4% | 31.9% |
| point_shortage_event | 2,274 | 7.5% | 9.4% | 12.3% | 14.5% |


- room_free_exhausted: 상대 캐릭터 무료 5회 소진 시점(T_USER_CHAT_FREE.UPDATE_DATE). 이 시점에 보너스·재방문 보상이 남아 있을 수 있음.
- point_shortage_event: Mixpanel Send Fail Point / point_short 팝업 / point_shortage 에러 첫 발생 = 무료·보너스·DMM 모두 부족. 직전 DMM 결제자 제외.


### 첫 DMM 결제 금액 (12주 가입자 2,946명, 첫 차감 1건 기준: 중앙 20pt, 평균 72.5pt; 첫 24시간 누적 중앙 160pt)


| 금액 | 유저 | 비중 |
|---|---|---|
| <=10 | 1,123 | 38.1% |
| 11-15 | 154 | 5.2% |
| 16-50 | 1,206 | 40.9% |
| 51-100 | 272 | 9.2% |
| 101-300 | 16 | 0.5% |
| 301-1000 | 160 | 5.4% |
| 1000+ | 15 | 0.5% |


| 첫 결제 기능(차감 항목) | 유저 | 비중 | 중앙 pt |
|---|---|---|---|
| chat | 1,616 | 54.9% | 10 |
| manga | 7 | 0.2% | 80 |
| other | 93 | 3.2% | 40 |
| other_moodshot | 926 | 31.4% | 50 |
| scene_image | 56 | 1.9% | 40 |
| video | 174 | 5.9% | 650 |
| voice | 74 | 2.5% | 20 |


### 첫 결제 직전에 쓰던 기능 (첫 결제 시각 -30분~+2분, 가장 가까운 사용 이벤트; 결제·보너스 이벤트 제외)


| 기능 | 유저 | 비중 |
|---|---|---|
| chat_1to1 | 1,099 | 37.3% |
| moodshot | 909 | 30.9% |
| ntr_room | 478 | 16.2% |
| video | 177 | 6.0% |
| none_within_30min | 101 | 3.4% |
| voice | 77 | 2.6% |
| scene_image | 56 | 1.9% |
| creation | 25 | 0.9% |
| group_room | 14 | 0.5% |
| manga | 7 | 0.2% |
| story_room | 3 | 0.1% |


## B3. 가입 묶음별 LTV (가입자 1명당 DMM pt 누적)

| 가입 주 | 가입자 | D1 pt/인 | D7 pt/인 | D30 pt/인 | D30 결제 유저율 |
|---|---|---|---|---|---|
| 2026-08-17 | 1,478 | 92 | 175 | 256 | 20.5% |
| 2026-08-24 | 1,286 | 156 | 347 | 570 | 23.9% |
| 2026-08-31 | 1,065 | 127 | 245 | 389 | 22.7% |
| 2026-09-07 | 1,108 | 103 | 273 | 712 | 20.5% |
| 2026-09-14 | 981 | 139 | 251 | 483 | 21.9% |
| 2026-09-21 | 847 | 168 | 376 | 578 | 23.0% |
| 2026-09-28 | 821 | 172 | 279 | 376 | 28.4% |
| 2026-10-05 | 988 | 101 | 204 | 1,101 | 26.8% |
| 2026-10-12 | 952 | 249 | 426 | 960* | 26.3% |
| 2026-10-19 | 900 | 178 | 382 | - | - |
| 2026-10-26 | 777 | 190 | 327 | - | - |
| 2026-11-02 | 746 | 212 | 405* | - | - |


\* 관측 기간이 덜 찬 가입자를 뺀 부분 값(경과 가입자만). 평균은 소수 대형 유저 영향이 큼: D30 기준 10/5 주는 상위 1명이 45.4%(제외 시 601pt/인), 9/7 주는 56.0%(제외 시 313pt/인).


| 최근 30일 pt | 결제 유저 | pt | 비중 | 결제 유저당 pt |
|---|---|---|---|---|
| signed_up_before | 1,503 | 6,555,812 | 79.5% | 4,362 |
| signed_up_last30d | 822 | 1,688,549 | 20.5% | 2,054 |


S7 제외 시: signed_up_before 426,932pt (58.5%), signed_up_last30d 302,438pt (41.5%). 가입 월별은 `csv/b3_last30d_pt_by_signup_month.csv`.


## B4. S7 헤비 623명 프로필

| 가입 월 | 유저 | 비중 | 최근 30일 pt 비중 |
|---|---|---|---|
| 2025-09 | 6 | 1.0% | 0.3% |
| 2025-10 | 55 | 8.8% | 7.5% |
| 2025-11 | 40 | 6.4% | 4.0% |
| 2025-12 | 21 | 3.4% | 4.1% |
| 2026-01 | 29 | 4.7% | 2.4% |
| 2026-02 | 28 | 4.5% | 1.9% |
| 2026-03 | 38 | 6.1% | 3.7% |
| 2026-04 | 25 | 4.0% | 3.6% |
| 2026-05 | 25 | 4.0% | 4.4% |
| 2026-06 | 26 | 4.2% | 4.7% |
| 2026-07 | 34 | 5.5% | 3.7% |
| 2026-08 | 50 | 8.0% | 9.6% |
| 2026-09 | 53 | 8.5% | 10.1% |
| 2026-10 | 148 | 23.8% | 35.1% |
| 2026-11 | 45 | 7.2% | 5.0% |


가입→S7 첫 충족: 중앙 4.6일 (p25 1.8, p75 21.6). S7 시점 = 과거 DMM 이력으로 '직전 30일 결제일 3일+ 또는 상위10% 기준 pt' 조건을 처음 만족한 날.


| 가입→S7 | 유저 |
|---|---|
| same_day(<1d) | 62 |
| 1-7d | 311 |
| 7-30d | 113 |
| 30-90d | 60 |
| 90d+ | 77 |


| 첫 기능 | 유저 | 비중 |
|---|---|---|
| chat_1to1 | 433 | 69.5% |
| creation | 72 | 11.6% |
| moodshot | 42 | 6.7% |
| video | 32 | 5.1% |
| ntr_room | 26 | 4.2% |
| scene_image | 15 | 2.4% |
| group_room | 2 | 0.3% |
| voice | 1 | 0.2% |


| 기능 | S7 최근 30일 pt | 비중 |
|---|---|---|
| video | 3,361,760 | 44.7% |
| chat | 2,460,666 | 32.7% |
| scene_image | 779,615 | 10.4% |
| other_moodshot | 602,120 | 8.0% |
| manga | 181,350 | 2.4% |
| other | 87,855 | 1.2% |
| voice | 41,625 | 0.5% |


제작자(캐릭터 1개+ 저장) 비율 53.6%. 최근 30일 활동일 중앙 6일(평균 8.2), 결제일 중앙 5일.


| 활동일(30일 중) | 유저 |
|---|---|
| 0 | 0 |
| 1-2 | 25 |
| 3-6 | 331 |
| 7-14 | 168 |
| 15-29 | 92 |
| 30 | 7 |


### 상위 10명 (순번, ID 없음)


| 순번 | 30일 pt | 전체 비중 | 활동일 | 결제일 | 제작자 | 가입 월 | 대화 | 영상 | 씬 이미지 | 무드샷 | 망가 | 목소리 | 기타 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 775,503 | 9.4% | 10 | 10 | Y | 2026-10 | 863 | 751,460 | 17,160 | 1,440 | 3,800 | 0 | 780 |
| 2 | 430,840 | 5.2% | 8 | 8 | N | 2026-08 | 0 | 425,590 | 5,250 | 0 | 0 | 0 | 0 |
| 3 | 209,660 | 2.5% | 25 | 25 | Y | 2026-09 | 2,090 | 176,080 | 25,710 | 5,220 | 0 | 20 | 540 |
| 4 | 151,795 | 1.8% | 9 | 9 | Y | 2026-10 | 125 | 149,630 | 1,680 | 360 | 0 | 0 | 0 |
| 5 | 134,335 | 1.6% | 27 | 26 | Y | 2026-05 | 11,815 | 95,690 | 23,880 | 2,250 | 0 | 400 | 300 |
| 6 | 133,150 | 1.6% | 21 | 20 | N | 2026-06 | 0 | 90,720 | 42,430 | 0 | 0 | 0 | 0 |
| 7 | 130,615 | 1.6% | 22 | 22 | Y | 2026-10 | 91,895 | 2,400 | 300 | 30,780 | 0 | 140 | 5,100 |
| 8 | 104,425 | 1.3% | 23 | 23 | Y | 2026-10 | 1,245 | 72,110 | 16,800 | 0 | 13,570 | 0 | 700 |
| 9 | 98,610 | 1.2% | 13 | 13 | Y | 2025-10 | 59,100 | 0 | 0 | 35,910 | 0 | 900 | 2,700 |
| 10 | 93,020 | 1.1% | 23 | 23 | N | 2026-09 | 220 | 60,400 | 32,400 | 0 | 0 | 0 | 0 |


## B5. 영상 퍼널 (12주 가입자)

정의: video = non-failed T_SCENE video generation row or DMM charge with feature ntr_video/char-video; events within 2 min of the previous one for the same user merged as one video (dedupe gen row vs charge) (원본 14,355건 → 13,345건)


| 지표 | 값 |
|---|---|
| 7일 안 영상 1회+ (전체 가입자) | 4.6% (555명) |
|   보낸 유저 기준 | 6.0% |
|   7일 내 결제자 기준 | 20.7% |
| 첫 영상 → 2번째 영상 (누적) | 47.9% |
|   24시간 안 | 40.9% |
|   7일 안 | 45.6% |
| 첫→2번째 중앙 시간 | 23분 |
| 가입→첫 영상 중앙 시간 | 24분 |


| 구분 | 7일 내 영상 | 유저 | D7 | D30 | 가입 후 30일 pt/인 | 영상 제외 pt/인 | pt 중앙값 |
|---|---|---|---|---|---|---|---|
| all_signups | Y | 555 | 10.8% | 4.5% | 7,356 | 2,843 | 1,295 |
| all_signups | N | 11,394 | 1.9% | 0.6% | 224 | 152 | 0 |
| paid_within_7d | Y | 541 | 11.0% | 4.7% | 7,595 | 2,935 | 1,365 |
| paid_within_7d | N | 2,068 | 6.4% | 1.3% | 1,155 | 800 | 140 |


D30은 가입 후 30일이 지난 유저만(d30_eligible). 영상 사용자는 원래 결제 의향이 큰 유저라 차이는 인과가 아니다. 7일 내 결제자끼리 비교해도 D30 4.7% vs 1.3%.


## B6. S0(메시지 0회) 유저 — Mixpanel

정의: signups 8/17-11/14 with 0 messages ever (1:1+group/NTR/story). Mixpanel Page View/Button Click/Chat Room View 8/10-11/14, $insert_id dedupe, distinct_id = user id (includes merged pre-signup guest events). no dedicated character-detail page_name exists; character detail = Artist (creator profile) page; chat room = chat_room / n-group_room / story_room Page View or Chat Room View event

대상 4,187명, Mixpanel 이벤트 있음 3,877명(92.6%), 기능 사용도 0인 유저 3,751명. 페이지뷰 중앙 6, 버튼 클릭 중앙 8.


| 처음 본 페이지 | 유저 | 비중 |
|---|---|---|
| fan_18_agree_popup | 1,990 | 51.3% |
| chat_room | 1,436 | 37.0% |
| (none) | 356 | 9.2% |
| (no page view) | 56 | 1.4% |
| n-group_lobby | 20 | 0.5% |
| home_icon_tip | 5 | 0.1% |
| discover_bots | 5 | 0.1% |
| motion_create_page | 3 | 0.1% |
| create_bots | 2 | 0.1% |
| chat_ai_model_intro | 1 | 0.0% |
| createV2_step1 | 1 | 0.0% |
| story_list | 1 | 0.0% |


| 마지막 본 페이지 | 유저 | 비중 |
|---|---|---|
| chat_room | 1,957 | 50.5% |
| (none) | 310 | 8.0% |
| motion_create_page | 242 | 6.2% |
| n-group_lobby | 238 | 6.1% |
| create_bots | 210 | 5.4% |
| chat_ai_model_intro | 166 | 4.3% |
| ntr_home_promo | 107 | 2.8% |
| discover_bots | 107 | 2.8% |
| n-group_room | 96 | 2.5% |
| home_c | 76 | 2.0% |
| (no page view) | 56 | 1.4% |
| Artist | 45 | 1.2% |


| 페이지뷰 수 | 유저 | 비중 |
|---|---|---|
| 0 | 56 | 1.4% |
| 1 | 120 | 3.1% |
| 2-3 | 962 | 24.8% |
| 4-10 | 1,788 | 46.1% |
| 11-30 | 786 | 20.3% |
| 31+ | 165 | 4.3% |


| 도달 | 비율 |
|---|---|
| chat_room_page_or_view | 79.5% |
| chat_room_1to1_view_event | 5.4% |
| artist_profile_page | 6.2% |
| discover_bots | 15.4% |
| home_c | 10.9% |
| group_or_ntr_lobby | 20.8% |
| create_pages | 30.5% |
| motion_or_scene_pages | 23.6% |


주의: S0의 37%가 첫 페이지부터 chat_room이라, chat_room page_name은 랜딩/채팅 목록 화면에도 붙는 것으로 보인다(추정). 따라서 79.5%는 "방에 들어갔다"의 상한값이다. 1:1 전용 `Chat Room View` 이벤트 기준으로는 5.4%. 전용 캐릭터 상세 페이지 이벤트는 없다.


## B7. D1/D7 리텐션 차이

재방문 = 그날(JST) 메시지 1회+ 또는 기능 사용 1회+ (원 리포트와 동일). 12주 가입자.


| 분할 | 값 | 유저 | D1 | D7 | D7 경과 유저 |
|---|---|---|---|---|---|
| first_char_type(senders) | direct_official | 769 | 11.8% | 3.3% | 761 |
| first_char_type(senders) | direct_ugc | 6,187 | 12.6% | 3.1% | 6,143 |
| first_char_type(senders) | group | 20 | 0.0% | 0.0% | 19 |
| first_char_type(senders) | ntr | 1,047 | 11.6% | 5.0% | 1,031 |
| first_char_type(senders) | story | 13 | 23.1% | 0.0% | 11 |
| platform(all_signups) | mobile | 9,127 | 8.7% | 2.4% | 9,052 |
| platform(all_signups) | pc | 2,018 | 8.8% | 2.3% | 1,991 |
| platform(all_signups) | unknown(no_mixpanel) | 804 | 7.2% | 2.0% | 796 |
| platform(senders) | mobile | 6,224 | 12.4% | 3.4% | 6,175 |
| platform(senders) | pc | 1,290 | 13.0% | 3.2% | 1,274 |
| platform(senders) | unknown(no_mixpanel) | 522 | 11.1% | 3.1% | 516 |
| first_talk_received_by_d1(senders, signups>=10/03) | False | 2,558 | 15.4% | 4.7% | 2,502 |
| first_talk_received_by_d1(senders, signups>=10/03) | True | 640 | 23.0% | 5.1% | 625 |
| first_talk_opened(receivers) | False | 442 | 8.4% | 2.5% | 433 |
| first_talk_opened(receivers) | True | 198 | 55.6% | 10.9% | 192 |
| welcome_7day_bonus_enrolled(signups>=11/13) | False | 33 | 9.1% | - | 0 |
| welcome_7day_bonus_enrolled(signups>=11/13) | True | 225 | 18.4% | - | 0 |


- 선톡: 10/3 이후 가입 보낸 유저 3,198명 중 D1까지 선톡 수신 20.0%. 선톡 수신은 무작위 배정이 아니라 발송 조건(대화 이력 등)을 충족한 유저에게만 가므로 선택 편향이 있다. '열람' 유저 D1 55.6%는 열람=재방문이라 인과가 아니다.
- PC/모바일: Mixpanel 첫 이벤트의 $device/$os 기준(iPhone/Android/iPad = 모바일, Windows/Mac/Linux = PC).
- 웰컴 7일 보너스: 11/13 시작. D1 경과 49명뿐, D7 판단 불가.


## B8. 10/5 주부터 D1이 오른 이유

| 기간(가입일) | 가입자 | D1(활동) | D1(페이지뷰) | D1 방문했지만 활동 0 | 첫 메시지 비율 |
|---|---|---|---|---|---|
| a_0914-0928 | 1,949 | 6.4% | 14.0% | 8.2% | 65.8% |
| b_0929-1001 | 318 | 9.1% | 19.2% | 10.7% | 70.8% |
| c_1002-1006(first_talk) | 672 | 7.0% | 16.1% | 10.1% | 72.3% |
| d_1007-1013(+return_reward) | 998 | 11.5% | 16.4% | 5.7% | 73.2% |
| e_1014-1113 | 3,586 | 13.0% | 18.1% | 6.4% | 65.8% |


| 가입일 | 가입자 | D1 | D1 유저 | 그중 그날 재방문 보상 받음 | 그중 D1까지 선톡 수신 |
|---|---|---|---|---|---|
| 2026-09-28 | 121 | 6.6% | 8 | 0 | 0 |
| 2026-09-29 | 109 | 8.3% | 9 | 0 | 0 |
| 2026-09-30 | 113 | 8.0% | 9 | 0 | 0 |
| 2026-10-01 | 96 | 11.5% | 11 | 0 | 0 |
| 2026-10-02 | 115 | 7.8% | 9 | 0 | 2 |
| 2026-10-03 | 128 | 7.8% | 10 | 0 | 4 |
| 2026-10-04 | 139 | 4.3% | 6 | 0 | 2 |
| 2026-10-05 | 139 | 8.6% | 12 | 0 | 5 |
| 2026-10-06 | 151 | 6.6% | 10 | 4 | 4 |
| 2026-10-07 | 136 | 14.0% | 19 | 19 | 4 |
| 2026-10-08 | 122 | 8.2% | 10 | 10 | 1 |
| 2026-10-09 | 136 | 17.6% | 24 | 24 | 8 |
| 2026-10-10 | 150 | 15.3% | 23 | 22 | 4 |
| 2026-10-11 | 154 | 9.1% | 14 | 14 | 3 |
| 2026-10-12 | 153 | 7.8% | 12 | 11 | 2 |
| 2026-10-13 | 147 | 8.8% | 13 | 13 | 2 |
| 2026-10-14 | 137 | 19.0% | 26 | 24 | 8 |


### 9/28~10/12 main 머지 후보 (라이브 반영은 머지 직후~수십 분 뒤일 수 있음. T_RETURN_REWARD 첫 행 10/07 18:25은 라이브 DB를 쓰는 테스트 서버 기록으로 추정)

| 머지 시각(KST) | 레포 / PR | 내용 | D1 영향 판단 |
|---|---|---|---|
| 10/07 19:00 | fanza-api #246, fan.stipop.ai #302 (10/07 19:01) | **재방문 보상 추가**(복귀일 무료 3회 × 3일, `returnReward.claim`), 선톡 수정 | **1순위.** D1 계단 상승 시점(10/7 가입자부터)과 일치. 10/7 이후 D1 활동 유저 거의 전원이 그날 보상 수령. D1 방문 대비 활동 전환이 크게 개선 |
| 10/02 17:01~17:20 | fanza-api #234/#235, fan.stipop.ai #296 | 웹 푸시 + 선톡(First Talk) 추가 | 2순위(보조). 10/2~10/6 가입자 D1 7.0%로 변화 없음. 이후 재방문 보상과 결합(선톡이 보상 수령 가능 여부를 참조) |
| 09/29 15:14~18:54 | fanza-api #222/#224, fan.stipop.ai #285/#286 | premium v4 / ultra v2 모델, 씬 라이브러리·소재 스튜디오 | 낮음. 9/29~10/1 D1 9.1%로 소폭 상승했지만 표본 318명. #224 직후 Claude 경로 답장 오류(#226, 9/29 23:14 수정)도 있었음 |
| 09/30 22:05~10/03 | fanza-api #227/#238, fan.stipop.ai #291 | 영상 공급자 체인·실패 폴링, 영상 UX | 낮음. 영상은 신규 7일 4.6%만 사용 |
| 09/28 17:08 | fanza-api #213, fan.stipop.ai #278 | NTR 메이커 | 낮음. 이후 D1 변화 없음 |
| 10/12 21:36~21:44 | fanza-api #245/#247/#248, fan.stipop.ai #301 | release-live(미디어 가격·망가·채팅 내비 등) | 상승 이후라 원인 아님(유지에는 기여 가능) |

한계: 전면 반영(before/after)이라 A/B 비교가 아니며, 같은 기간 유입 채널 변화는 통제하지 못했다. 재방문 보상 수령은 재방문해야 생기므로 "수령자 ≈ D1 유저"는 구조상 당연하고, 근거는 시점 일치와 "방문했지만 활동 0" 비율 감소다.


## 정의·한계
- 무료·보너스 잔액은 과거 지갑 스냅샷이 없어 재구성한 근사값: 상대 캐릭터 무료분(T_USER_CHAT_FREE OWNER=N, CHAT<5면 남음), 그날 재방문 보상 잔여(GRANTED-USED), 마지막 메시지 시점 이전 마지막 T_BONUS_LEDGER.BALANCE_AFTER, 캠페인 크레딧(지급-사용). 보너스 원장은 11/2부터, 캠페인 크레딧은 10/23부터라 그 이전 이탈자는 무료분 기준만 판정.
- 이탈자 = 12주 가입자 중 메시지 1회+, 누적 20회 미만, 최근 7일 활동 없음.
- 메시지 = 1:1 `MESSAGE_TYPE='query'` + 그룹/NTR/스토리 `USER_TYPE='user' AND CONTENTS_TYPE='msg'`. 채팅 삭제 시 메시지도 삭제되어 과소 집계.
- Mixpanel은 `$insert_id` 중복 제거, 유저 = distinct_id(가입 전 게스트 이벤트 병합 포함). 11/14까지.
- MP 응답 이벤트 첫 응답은 JQL 집계 특성상 유저별 앞부분 일부만 보존된 근사값.
- 영상 = 실패 제외 T_SCENE 생성 또는 ntr_video/char-video DMM 차감, 같은 유저 2분 이내 이벤트는 1건으로 병합.
- pt는 DMM 포인트 사용량. 정산·환불 반영 매출 아님.

## 쿼리·스크립트
원 리포트 부록의 쿼리에 더해, 이번 추가 추출은 모두 SELECT: T_DMM_POINT(첫 차감, 전체 차감), T_USER_CHAT_FREE, T_RETURN_REWARD, T_BONUS_LEDGER, T_CAMPAIGN_CREDIT(+사용), T_FIRST_TALK, T_SIGNUP_BONUS, T_AI_CHAT_MESSAGE(첫 query/answer), T_SCENE. Mixpanel JQL: Page View/Button Click/Chat Room View 사용자별 집계, Claude/Gemini Response Details, Send Fail Point/Popup View/Error View, Page View 일자 집합.


### 추출 스크립트 원문 (extract_b.py, SELECT만)

```python
import pandas as pd, warnings; warnings.filterwarnings('ignore')
from db import q
Q={
'b_firstdmm':"""select USER_ID user_id,REG_DATE ts,-POINT pt,STATUS type,FEATURE feature from (
  select USER_ID,REG_DATE,POINT,STATUS,FEATURE,row_number() over (partition by USER_ID order by REG_DATE,SEQ) rn from T_DMM_POINT where POINT<0) x where rn=1""",
'b_dmm2':"""select USER_ID user_id,REG_DATE ts,-POINT pt,STATUS type,FEATURE feature from T_DMM_POINT where POINT<0 and REG_DATE>='2026-08-10'""",
'b_chatfree':"select USER_ID user_id,CHAT_ID chat_id,ASSISTANT_ID assistant_id,OWNER owner,CHAT chat,STATUS status,REG_DATE ts,UPDATE_DATE upd from T_USER_CHAT_FREE",
'b_retrew':"select USER_ID user_id,REWARD_DATE d,DAY_INDEX day_index,GRANTED granted,USED used,REG_DATE ts,UPDATE_DATE upd from T_RETURN_REWARD",
'b_bledger':"select USER_ID user_id,TYPE type,AMOUNT amount,BALANCE_AFTER bal,CAMPAIGN_ID campaign,FEATURE feature,REG_DATE ts from T_BONUS_LEDGER",
'b_credit':"select USER_ID user_id,CAMPAIGN campaign,GRANTED_POINT granted,BALANCE bal,REG_DATE ts from T_CAMPAIGN_CREDIT",
'b_credituse':"select USER_ID user_id,AMOUNT amount,FEATURE feature,REG_DATE ts from T_CAMPAIGN_CREDIT_USE",
'b_firsttalk':"select USER_ID user_id,ASSISTANT_ID assistant_id,SEND_DATE d,STATUS status,PUSH_STATUS push,OPENED_YN opened,REG_DATE ts from T_FIRST_TALK",
'b_ftoptin':"select USER_ID user_id,ASSISTANT_ID assistant_id,STATUS status,REG_DATE ts from T_FIRST_TALK_OPTIN",
'b_signupbonus':"select USER_ID user_id,AMOUNT amount,STATUS status,GRANTED_AT granted_at,REG_DATE ts from T_SIGNUP_BONUS",
# first 5 1:1 queries per user (signups since 8/17) and the next answer in the same chat
'b_firstreplies':"""with u as (select u_id from user where u_date>='2026-08-17'),
qq as (select c.USER_ID user_id,m.CHAT_ID,m.MESSAGE_ID,m.REG_DATE,row_number() over (partition by c.USER_ID order by m.MESSAGE_ID) rn
  from T_AI_CHAT_MESSAGE m join T_AI_CHAT c on c.CHAT_ID=m.CHAT_ID join u on u.u_id=c.USER_ID where m.MESSAGE_TYPE='query')
select qq.user_id,qq.rn,qq.REG_DATE q_ts,(select min(a.REG_DATE) from T_AI_CHAT_MESSAGE a where a.CHAT_ID=qq.CHAT_ID and a.MESSAGE_ID>qq.MESSAGE_ID and a.MESSAGE_TYPE='answer'
   and a.MESSAGE_ID<coalesce((select min(n.MESSAGE_ID) from T_AI_CHAT_MESSAGE n where n.CHAT_ID=qq.CHAT_ID and n.MESSAGE_ID>qq.MESSAGE_ID and n.MESSAGE_TYPE='query'),9e18)) a_ts,
  (select max(a.ERROR_TYPE) from T_AI_CHAT_MESSAGE a where a.CHAT_ID=qq.CHAT_ID and a.MESSAGE_ID>qq.MESSAGE_ID and a.MESSAGE_TYPE='answer'
   and a.MESSAGE_ID<coalesce((select min(n.MESSAGE_ID) from T_AI_CHAT_MESSAGE n where n.CHAT_ID=qq.CHAT_ID and n.MESSAGE_ID>qq.MESSAGE_ID and n.MESSAGE_TYPE='query'),9e18)) err
from qq where qq.rn<=5""",
'b_first11room':"""select user_id,ts,assistant_id,chat_id from (select c.USER_ID user_id,m.REG_DATE ts,c.ASSISTANT_ID assistant_id,c.CHAT_ID chat_id,row_number() over (partition by c.USER_ID order by m.MESSAGE_ID) rn
  from T_AI_CHAT_MESSAGE m join T_AI_CHAT c on c.CHAT_ID=m.CHAT_ID where m.MESSAGE_TYPE='query' and c.USER_ID in (select u_id from user where u_date>='2026-08-10')) x where rn=1""",
'b_grpfirst':"""select USER_ID user_id,ROOM_ID room_id,min(REG_DATE) ts from T_AI_CHAT_GROUP_MESSAGE where USER_TYPE='user' and CONTENTS_TYPE='msg' group by 1,2""",
}
import sys
for k,s in Q.items():
    if len(sys.argv)>1 and k not in sys.argv[1:]: continue
    d=q(s); d.to_pickle(f'data/{k}.pkl'); print(k,d.shape,flush=True)

```
