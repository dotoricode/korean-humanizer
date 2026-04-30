# 베타 모집 — v1.0 안정화 검증

> **이 문서는 메인테이너용**. 사용자 (`@dotoricode`) 가 X / GeekNews / Disquiet / 브런치·뉴스레터 채널 / 개인 네트워크에 그대로 붙여넣을 수 있는 모집 글 + 운영 체크리스트를 담는다.

---

## 모집 한 줄 요약

> **한국어로 매주 글 쓰는 분 3-5 명**, **1-2 주 간 humanizer 사용 후 5 분 폼**. README contributor 로 표기 (선택). 신청은 [GitHub Issue](https://github.com/dotoricode/korean-humanizer/issues/new) 또는 X DM.

---

## 모집 글 — 채널별

### 1. X / Threads (한국어, 280 자)

```
한국어 AI 글쓰기에서 "AI 티" 걷어내는 작은 skill 만들고 있어요.
v1.0 안정화 전 베타 사용자 3-5 명 찾습니다.

조건: 한국어 글쓰기 주 2 회+ / 1-2 주 사용 / 5 분 폼
보상: README contributor 표기 (선택)
환경: Claude Code / Claude.ai / ChatGPT / Cursor / Gemini 어디든

DM 주세요 🙏
github.com/dotoricode/korean-humanizer
```

### 2. X / Threads (영어, 280 자)

```
Korean-only humanizer skill — strips "AI smell" from Korean text.
Looking for 3-5 beta users before v1.0.

Need: Write Korean weekly / use 1-2 weeks / fill 5-min form
Reward: README contributor (optional)
Works in Claude Code, Claude.ai, ChatGPT, Cursor, Gemini

DM me 🙏
github.com/dotoricode/korean-humanizer
```

### 3. IndieHackers KR Slack / 한국어 작가 디스코드

```
안녕하세요! 한국어 AI 글쓰기에서 "AI 티" 걷어내는 작은 skill (`korean-humanizer`) 을 만들고 있어요.

v0.8 까지 12 카테고리 / 137+ 패턴 / 12 도메인 / 4 customization mode (Personal list + Brand voice) 갖춰졌고, v1.0 안정화 release 전 외부 검증을 받고 싶습니다.

**찾는 분**:
- 한국어 글쓰기 주 2 회 이상 (블로그 / 마케팅 / 이메일 / 뉴스레터 / LinkedIn / 학술 / 채팅 등 어떤 도메인이든)
- 1-2 주간 humanizer 를 실제로 사용해보고 5 분 정도 짧은 피드백 폼 응답

**환경**: Claude Code / Claude.ai (Cowork) / OpenCode / Codex / ChatGPT / Cursor / Gemini 중 평소 쓰는 거 그대로.

**보상** (선택):
- v1.0 release 시 README contributor 섹션 이름 표기
- v1.x 의 패턴 / 도메인 추가 PR 우선 검토

**일정**: 주차 1 모집 → 주차 2-3 사용 + 주간 피드백 → 주차 4 v1.0 release.

신청은 GitHub Issue (https://github.com/dotoricode/korean-humanizer/issues/new) 에 `[beta]` prefix 또는 X DM (@dotoricode) 으로.

자세한 사용 가이드: docs/beta-guide.md (확정 후 안내).

감사합니다!
```

### 4. GeekNews (한국 개발자 커뮤니티 — ★★★★★)

> https://news.hada.io/ — 한국 개발자 / IT 종사자 집결지. "쇼 GeekNews" 섹션이 사이드 프로젝트 쇼케이스 공간.

**제목**: `한국어 AI 글쓰기에서 "AI 티" 걷어내는 skill 만들었습니다 (korean-humanizer v0.8)`

**본문** (800-1200 자 — GeekNews 는 긴 소개 OK):

```
한국어로 AI 글 쓰고 다듬으시는 분들께 공유합니다.

claude-code / claude.ai / chatgpt / cursor / gemini 어디서든 붙여 쓸 수 있는 한국어 전용 humanizer skill 을 만들고 있습니다 (korean-humanizer). AI 가 생성한 한국어 텍스트에서 "AI 티"를 걷어내고 의미는 그대로 두는 게 목표예요.

**왜 만들었나**

영어용 humanizer (blader/humanizer, jalaalrd/anti-ai-slop-writing 등) 는 여럿 있는데 한국어 전용은 비어 있더라구요.

한국어 AI 글에는 영어와 다른 패턴이 있어요:
- 번역체: "~에 있어서", "~의 경우에는", "~하게 된다"
- 격식체 남용: "~인 것이다", "~하고 있다"
- AI 고빈도 어휘: "활용하다", "극대화하다", "시사하다", "구현하다"
- 과도한 나열·병렬구

KatFish / XDAC 같은 한국어 AI 탐지 연구도 비슷한 신호를 지적해요.

**현재 상태 (v0.8 → v1.0-rc)**

- 12 카테고리 / 137+ 패턴
- 12 도메인 (블로그 / 마케팅 / 이메일 / LinkedIn / YouTube / 뉴스레터 / 위키 / 학술 / 뉴스 / 카톡·DM / 리뷰 / B2B)
- 4 customization mode — 인라인 한 줄 / 자연어 / 파일 / Brand voice profile
- 자동 검증: 5 metric eval-harness, 25/25 fixture pass

**v1.0 안정화 전 베타 사용자 3-5 명 찾습니다**

- 한국어 글쓰기 주 2 회 이상
- 1-2 주 평소 글에 적용 후 짧은 폼 (5 분)
- 보상: README contributor 표기 (선택)

GitHub: https://github.com/dotoricode/korean-humanizer
신청: GitHub Issue `[beta]` prefix 또는 X DM (@dotoricode)
```

---

### 5. Disquiet (한국 인디 메이커 커뮤니티 — ★★★★★)

> https://disquiet.io/ — 한국 인디 메이커 / 사이드 프로젝트 전용 커뮤니티. "메이커로그" 형식으로 개인 프로젝트 소개 활성.

**제목**: `한국어 AI 글쓰기에서 "AI 티" 걷어내는 skill — korean-humanizer`

**본문**:

```
안녕하세요, 인디 메이커 여러분.

AI 글쓰기 많이들 쓰시죠. 저도 그러다가 "AI 티"가 너무 신경 쓰여서 직접 만들었습니다.

**korean-humanizer** — AI 가 생성한 한국어 텍스트를 사람 말투로 다듬는 skill. Claude Code / claude.ai / ChatGPT / Cursor 어디서든 사용 가능.

번역체 ("~에 있어서"), 격식체 남용 ("~인 것이다"), AI 고빈도 어휘 ("활용 / 극대화 / 시사한다") 같은 한국어 특유 AI 신호 137+ 패턴 → 12 카테고리로 정리했어요. Brand voice 설정으로 "Toss 스타일", "에세이스트 톤" 같은 영구 브랜드 톤도 잡아줍니다.

v1.0 안정화 전 실제 글 쓰시는 분 3-5 명과 함께 검증하고 싶어요. 뉴스레터 / 블로그 / 마케팅 / LinkedIn 등 어떤 도메인이든. 1-2 주 사용 + 5 분 폼이면 충분합니다.

→ https://github.com/dotoricode/korean-humanizer
→ 신청: GitHub Issue `[beta]` 또는 X DM (@dotoricode)
```

---

### 6. 브런치 작가 채널 / 뉴스레터 운영자 (Stibee Slack 등 — ★★★★)

> 브런치 작가 오픈 카톡방 / Stibee 사용자 Slack / 뉴스레터 운영자 모임 — 한국어 글쓰기 정기성이 가장 보장되는 그룹.

**DM / 오픈 채팅 메시지**:

```
안녕하세요! 뉴스레터 / 브런치 정기 발행하시는 분들께 부탁 하나 드려요.

제가 AI 생성 한국어 텍스트에서 "AI 티" 걷어내는 skill 을 만들고 있는데, 실제로 정기 글 쓰시는 분들의 피드백이 가장 필요합니다.

1-2 주 동안 발행하시는 글에 한 번씩 적용해보시고 짧은 폼 (5 분) 응답해 주시면 돼요. 환경은 Claude Code / claude.ai / ChatGPT / Cursor 평소 쓰시는 거 그대로.

번역체 / 격식체 / AI 어휘 같은 패턴 137+ 개가 있고, 뉴스레터 / 브런치 도메인에 맞는 톤으로 Brand voice 설정도 할 수 있어요.

→ https://github.com/dotoricode/korean-humanizer
보상: README contributor 표기 (선택)
```

---

### 7. 개인 네트워크 (DM / 이메일 1:1)

```
안녕하세요 [이름]님,

한국어 글쓰기 자주 쓰시는 거 알아서 부탁 한 가지 드려요. 제가 한국어 AI 글쓰기에서 "AI 티" 걷어내는 작은 skill 을 만들고 있는데, v1.0 release 전 외부 검증이 필요해요. 1-2 주간 평소 쓰시는 글에 가끔 적용해보시고 짧은 폼 (5 분) 응답이면 충분합니다.

현재 12 카테고리 / 137+ 패턴 / 12 도메인 / 4 customization mode 까지 만들어진 상태고, 평소 [이름]님이 쓰는 [도메인 — 마케팅 / 블로그 등] 에 잘 맞는지 보고 싶어요.

레포: https://github.com/dotoricode/korean-humanizer
docs/beta-guide.md — 사용 가이드

도와주실 수 있으시면 평소 쓰시는 환경 (Claude Code / ChatGPT / Cursor 등) 알려주세요. 설치부터 같이 도와드릴게요.

감사합니다!
```

---

## 베타 운영 — 메인테이너 체크리스트

### Week 1 — 모집

- [ ] X / Threads 모집 트윗 게시 (한국어 280 자)
- [ ] GeekNews "쇼 GeekNews" 섹션 게시
- [ ] Disquiet 메이커로그 게시
- [ ] 브런치 작가 오픈 채팅 / Stibee Slack 게시 (접근 가능한 채널)
- [ ] 개인 네트워크 1-2 명 DM
- [ ] 신청 GitHub Issue 모니터링 + X DM 모니터링
- [ ] 신청자 명단 (`docs/beta-applicants.md` — gitignore) 정리: 이름, 환경, 주력 도메인, 신청일

**목표**: 3-5 명 confirmed. 1 명만 confirmed 면 진행하되 RC 기간 1 주 연장.

### Week 2 — 사용 시작

- [ ] 각 베타 사용자에게 환영 메시지 (`docs/beta-guide.md` 링크 + 피드백 폼 링크 + 일정 안내)
- [ ] 환경별 설치 도움 (막히는 분 1:1)
- [ ] Day 3 시점 first check-in — 첫 humanize 해본 인상
- [ ] Day 7 시점 mid check-in — 사용 빈도 / 막힌 부분

### Week 3 — 사용 + 피드백 수집

- [ ] 매일 피드백 폼 응답 체크
- [ ] `docs/beta-feedback.md` 에 누적 정리 (익명화 — 사용자 이름 / 텍스트 일부만)
- [ ] 심각한 룰 위반 (의미 변경 / 카탈로그 false positive) 발견 시 hot-fix PR
- [ ] 마지막 wrap-up 메시지 — "이번 주말까지 마지막 폼 응답 부탁"

### Week 4 — 피드백 반영 + release

- [ ] 피드백 분석 (누락 패턴 / 과교정 / 도메인 톤 위반 / brand voice 한계)
- [ ] 룰 미세 조정 PR 1-3 개 (12 카테고리 freeze 안에서)
- [ ] v1.0.0-rc tag → 1 주 RC 검증 (베타 사용자에게 confirmation 요청)
- [ ] 문제 없으면 v1.0.0 GA tag
- [ ] GitHub release notes (`CHANGELOG.md` 1.0.0 섹션 + MIGRATION 링크)
- [ ] 베타 사용자 README contributor 섹션 추가 (동의자만)
- [ ] 감사 메시지 (참여한 모든 분께)

---

## 신청자 / 응답자 익명화 룰

- 베타 사용자 GitHub username / 한국어 닉네임 → README contributor 섹션에 본인 동의 시만 표기.
- `docs/beta-feedback.md` — 사용 텍스트 일부 인용 시 **공개 동의 받은 텍스트만**, 회사명 / 인물명 / 내부 도메인 마스킹.
- `docs/beta-applicants.md` — gitignore (개인 정보).
- 피드백 폼 응답 raw — Google Drive 비공개 폴더, 외부 공유 금지.

---

## 분기 시나리오

### Plan A: 3 명 이상 모집 성공

→ 정규 일정 (3 주) 진행 후 v1.0 GA.

### Plan B: 1-2 명만 모집

→ RC 기간 1 주 연장 (1.0.0-rc.2 / rc.3). 충분한 사용량 확보 후 GA.

### Plan C: 0 명 모집 (가장 큰 위험)

→ **메인테이너 본인 + 1 명 (지인 부탁)** 으로 1 주 사용 → v1.0.0-rc 분리 publish → 6-8 주 RC 기간 → 공개 사용자 자연 유입 후 GA.

---

## 모집 글 / 베타 자료 PR 환영

이 문서 자체에 대한 PR 도 환영 — 더 좋은 모집 표현 / 채널 / 보상 구조 제안.

신청 GitHub Issue 템플릿: [`.github/ISSUE_TEMPLATE/beta_signup.md`](../.github/ISSUE_TEMPLATE/beta_signup.md) (S4 작업 중 추가 예정).
