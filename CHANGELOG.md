# Changelog

> 모든 변경은 [Keep a Changelog](https://keepachangelog.com/) 형식, 버전은 [SemVer](https://semver.org/) 규칙. v1.0 부터 freeze 영역은 [`docs/STABILITY-PROMISE.md`](docs/STABILITY-PROMISE.md) 참조.

## [Unreleased]

### Fixed

- Windows Store `python3` alias failure now falls back only to a proven runnable Python interpreter.

## [1.0.1] — 2026-06-02

### Changed

- `SKILL.md` / `PROMPT.md` / `PROMPT.short.md` / `references/ko-ai-signals.md` 에 "humanizer 는 요약기가 아니다" 원칙을 명시.
- 사용자가 "짧게"를 요청하지 않은 경우 결과를 원문 대비 90% 미만으로 줄이지 않는 길이 floor 추가.
- 문장 / 문단 통째 삭제보다 약화 / 치환을 우선하도록 개시·마무리·연결어·3항 나열 가이드를 조정.
- README 예시를 과압축 사례에서 정보량 보존형 예시로 교체.
- Codex 설치 안내를 `scripts/install-codex-skill.sh` 기준으로 최신화.

### Fixed

- README.ko 의 `v1.0-rc` 상태 배지를 stable `v1.0.1` 표기로 수정.
- `CHEATSHEET.md` 의 "삭제" 중심 표현을 최신 치환 중심 규칙에 맞게 수정.

### Validation

- `scripts/lint-cross-file.sh` 가 90% 길이 floor 동기화도 검사하도록 갱신.

## [1.0.0] — 2026-05-21

### Added

- README 첫 화면에 30초 체험 섹션 + 정적 preview card 추가.
- `PROMPT.short.md` — ChatGPT / Claude / Cursor / Gemini 에 바로 붙여 넣는 짧은 system prompt.
- `CHEATSHEET.md` — 한국어 AI 티 30개 빠른 표 + 도메인별 기본 방향.
- `docs/LAUNCH.md` — v1.0 공개 / 커뮤니티 공유용 한국어·영어 문구.
- `docs/GITHUB-TOPICS.md` — GitHub topic 추천 목록.
- `assets/translation-humanizer-card.svg` — README / GitHub social preview 용 정적 이미지.
- README 번역 정책 정리 — `README.md` 를 영어 메인으로 전환, 기존 한국어판은 `README.ko.md` 로 보존, 중국어 간결판 `README.zh-CN.md` 추가.
- AI 도구 포지셔닝을 Codex / Claude Code 중심으로 정리하고, 기타 LLM 은 portable prompt 호환으로 낮춰 표기.
- GitHub Issue / PR 도메인 지원 추가 (SKILL.md 사용 대상 명시, 감사 표현 가이드 카탈로그 추가).
- 워크플로우 1.5단계 신설 — 도메인 번호 선택지 확인 + 블로그/SNS/뉴스레터 참고 글(세션 범위 Brand voice) 요청.
- 발화체 도메인(YouTube/팟캐스트/강의) 종결어미 이중 잠금 — 2단계 사전 지시 + 5단계 사후 체크.
- 조건부 문장 병합 허용 — 의미 중복 인접 문장, 짧아지는 방향만.
- 보존 대상 명시 — 존칭 수식어("보내주신"), 주격 조사("은/는"), 대조 연결어("다만"), 격식 이메일 주어 대명사("저희").
- 카탈로그 패턴 추가: `일정상` → `일정이 생겨 / 일정 때문에` (chat, email 도메인).
- `docs/STABILITY-PROMISE.md` — v1.0 freeze 영역 SemVer 정책 명문화.
- `docs/MIGRATION-0.x-to-1.0.md` — v0.5 → v1.0 호환성 가이드.

### Changed

- CHANGELOG `[Unreleased]` → `[1.0.0]` 확정.

### Migration

- 일반 사용자: `git pull` 만으로 완료. 영향 없음.
- 외부 fork 사용자: [`docs/MIGRATION-0.x-to-1.0.md`](docs/MIGRATION-0.x-to-1.0.md) 참조.

---

## [0.8.0] — 2026-04-30

### Added

- **Brand voice profile (4 번째 customization mode)** — 단어 리스트 위주의 Personal list (Mode A/B/C) 위에 얹히는 영구 brand 톤. frontmatter 7 핵심 필드 (`name`, `domain_default`, `ending_default`, `preserve`, `ban`, `prefer`, `length_bias`) + 자유 형식 톤 가이드. 적용 순서: brand voice → personal list → 카탈로그.
- 템플릿 + 케이스 스터디: `examples/brand-voice-template.md`, `examples/brand-voice-toss-style.md` (가상 핀테크, concise / ~해요체), `examples/brand-voice-essayist.md` (가상 에세이스트, verbose / ~다체).
- 카탈로그 부록 F (도메인 코드 표준) — 12 개별 도메인 + shorthand (`all` / `informal` = chat,review / `formal` = email,b2b-message,academic) + 컬럼 값 작성 룰 + 신규 도메인 추가 절차.
- eval-harness M5 (brand voice preserve coverage) — 옵션 metric, fixture frontmatter `brand_voice:` 있을 때만 활성. preserve 단어가 humanized 에 모두 살아있는지 검증.
- `eval/frequency-data/` 스캐폴딩 — 90 LLM 샘플 (3 모델 × 6 도메인 × 5 prompt) 기반 빈도 재라벨링 방법론. 실 데이터 수집은 1.x sub-PR 트랙 분리.
- `roadmap/S3-migration-notes.md` — v0.7 → v0.8 호환성 매트릭스 + sed 스니펫 + v1.0 freeze 약속 관계.

### Changed

- **BREAKING (외부 fork 한정)**: 카탈로그 9 패턴 표 (#1, #2, #3, #4, #6, #7, #8, #11, #12) ~110 행 모두 4 컬럼 (`나쁨 / 자연스러움 / 빈도 / 적용 도메인`) 으로 확장. ~50 행 specific 도메인 부여, 나머지 `all`. 일반 사용자 / SKILL.md / PROMPT.md 사용자 영향 없음.
- `scripts/lint-patterns.sh` v2 — 4 컬럼 의무 + 도메인 코드 valid 검증 + `all` 단독 사용 룰.
- `scripts/lint-cross-file.sh` — 4 번째 mode (방식 D / 형식 D), brand voice 3 파일 존재, 부록 F 헤더 sync 검증 추가.
- SKILL.md / PROMPT.md — 4 번째 mode (방식 D / 형식 D) 추가, 적용 순서 brand → personal → 카탈로그 명시.
- README — hero 에 brand voice 한 줄, "Personal List" 섹션 → "Personal List + Brand Voice 캘리브레이션" 4 방식 확장, File Structure 갱신.

### Migration

- 외부 fork 사용자: [`roadmap/S3-migration-notes.md`](roadmap/S3-migration-notes.md) — 표 헤더 4 컬럼 + 도메인 코드 부여 절차.
- 일반 사용자 (SKILL.md / PROMPT.md 사용): clone / pull 만 — 영향 없음.

---

## [0.7.0] — 2026-04-29

### Added

- **5 신규 도메인 사례** (7 도메인 → 12 도메인): `examples/domain-academic.md` (학술 abstract, 정형 문구 보존), `examples/domain-news.md` (뉴스 단신, 인용문 글자 단위 동일), `examples/domain-chat.md` (카톡·DM, ~해요체 strict), `examples/domain-review.md` (제품 리뷰, 별점·구매일 strict), `examples/domain-b2b-message.md` (B2B 메시지, ad-hoc 격식).
- 카탈로그 부록 E — 12 도메인 × 카테고리 우선순위 매트릭스 (1-3 순위 + 톤 디폴트). S3 카탈로그 v2 의 도메인 컬럼 prereq.
- README hero "12 도메인" 명시 + 도메인별 사례 빠른 링크.

### Changed

- CONTRIBUTING — 도메인 사례 PR 체크리스트 (메타데이터 / Raw / Humanized / 변경 ≤ 5 / 보존 / 한계 / 적용 가이드 통일).
- ROADMAP S2 status ✓.

---

## [0.6.0] — 2026-04-29

### Added

- **eval-harness** (`scripts/eval-harness.py` + `eval-harness.sh`): 4 metric 자동 검증 — M1 수정 비율, M2 단락 cap, M3 길이 비율, M4 발화체 ~다체 보존.
- 20 fixture (`eval/fixtures/`) — 12 도메인 + edge / trap. M1-M4 회귀 4 종 (cap 초과 / 단락 4곳 / 30 % 팽창 / 발화체 ~다체 도입) 모두 catch.
- `eval/scorecard.md` — auto-gen, 매 머지마다 갱신.
- 5 번째 CI hard-fail job.
- `eval/README.md` — fixture 형식 가이드 + frontmatter spec.

### Calibration

- modified-sentence threshold = 0.20 (long-form.md 17.3 % reference 와 calibration).

---

## [0.5.0] — 2026-04 (이전)

### Added

- 자동 검증 layer 3 종: `scripts/lint-cross-file.sh` (SKILL/PROMPT/카탈로그 정량 규칙·카테고리 sync), `scripts/lint-examples.sh` ("주요 변경 5개" 룰 + 카테고리 범위 검증).
- 카탈로그 9 패턴 표에 빈도 컬럼 (`high` / `med` / `low`) 추가.
- 장문 사례 `examples/long-form.md` (52 문장 회고 블로그, 17.3 % 수정 — 20 % cap 시연).
- README Troubleshooting 섹션 5 항목 (스타일 차이 / 변경 부족 / 변경 과다 / 발화체 ~다체 / 한영 혼용).
- lint CI 4 jobs (1 markdownlint warning + 3 hard-fail).

---

## [0.4.0]

### Added

- README 최상단 hero (5 초 요약 + Before/After 표).
- 구조 재정렬 — Overview / Categories / Full Example → Installation 위로 이동.
- Wiki 배지 + 빠른 링크.
- lint CI (markdownlint warning + 표 형식 검증 fail).

---

## [0.3.1]

### Changed

- Full Example 을 위키 발췌 (raw vs humanized) 비교로 교체.
- 위키 humanized 본 추가 (`korean-humanizer-research-humanized.md`).
- 단락별 상세 비교 문서 (`examples/wiki-humanized-comparison.md`).

---

## [0.3.0]

### Added

- OpenCode / Codex / Cursor 설치 가이드 분리.
- Personal list 인라인 한 줄 입력 지원 (방식 A — `/korean-humanizer 금지=...; 선호=A→B; 유지=...`).
- Full Example 5 문단으로 확장.
- 연구 근거 문서 `korean-humanizer-research.md`.
- 카탈로그 부록 A (KatFish/XDAC 정량 근거) + 부록 B (한국어 전용 feature schema) + 부록 C (LREAD 사람 평가 루브릭) + 부록 D (윤리·한계).

---

## [0.2.0]

### Added

- 에이전트 raw 출력 vs skill 적용 비교 자료 (`examples/agent-vs-skill.md`, 6 도메인 정량·정성 비교).

---

## [0.1.0]

### Added

- 초기 공개. 12 카테고리 / 100+ 한국어 AI 패턴 카탈로그 (`references/ko-ai-signals.md`).
- SKILL.md (Claude Code / Cowork / OpenCode / Codex 진입점).
- PROMPT.md (ChatGPT / Cursor / Gemini 시스템 프롬프트).
- before-after / personal-list 예제.

---

## 비교 / 관련 링크

- v1.0 freeze 영역 정의: [`docs/STABILITY-PROMISE.md`](docs/STABILITY-PROMISE.md)
- v0.x → v1.0 전체 마이그레이션: [`docs/MIGRATION-0.x-to-1.0.md`](docs/MIGRATION-0.x-to-1.0.md)
- 4 sprint 로드맵: [`ROADMAP.md`](ROADMAP.md)
