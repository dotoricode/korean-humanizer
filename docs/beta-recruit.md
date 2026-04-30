# 베타 모집 — v1.0 안정화 검증

> **이 문서는 메인테이너용**. 사용자 (`@dotoricode`) 가 X / Slack / 디스코드 / 개인 네트워크에 그대로 붙여넣을 수 있는 모집 글 + 운영 체크리스트를 담는다.

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

### 4. 개인 네트워크 (DM / 이메일 1:1)

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

- [ ] X / Threads 모집 트윗 게시
- [ ] IndieHackers KR Slack 게시
- [ ] 한국어 작가 디스코드 게시 (있는 경우)
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
