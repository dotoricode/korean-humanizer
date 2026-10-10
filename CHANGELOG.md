# Changelog

> 변경 기록은 [Keep a Changelog](https://keepachangelog.com/) 형식을 따릅니다. 현재 버전 기준과 과거 호환성 기록은 [버전 정책](docs/STABILITY-PROMISE.md)을 참고하세요.

## [Unreleased]

## [1.1.0] — 2026-10-10

### Changed

- `있다·것·수·접속사`를 조건부 검토 대상으로 명시하고, 진행 상태·능력·허용·논리 관계를 보존하는 간결화 기준을 추가합니다. 문장 삭제·결론 축소에도 정보와 글의 기능 보존 조건을 적용합니다.

- 교정 범위를 고정 비율·표현 수로 제한하지 않고, 정보·조건·말투 보존과 자연스러움으로 검수합니다.
- 개인 설정은 `personal=파일경로`로 명시한 파일만 사용합니다.
- 카탈로그 표 헤더를 `검토할 표현` / `치환 후보`로 변경합니다.
- 기본 교정의 20%·문단 3곳·짧은 글 1–2표현·길이 90% 제한을 제거합니다. 기존 평가 fixture는 과거 계약의 회귀 검사로 구분합니다.
- 명확한 용도는 바로 처리하며 참고 글은 선택 사항으로 둡니다.
- 기존 동작과 달라지는 부분을 [변경 안내](docs/UPGRADE-NOTES.md)를 추가했습니다. v1.1.0 릴리스에 이 차이와 전환 방법을 함께 안내합니다.

### Fixed

- 배포 ZIP은 깨끗한 저장소의 커밋 파일로만 생성하며, 구매자용 README도 원본 해시 기록에 포함합니다. 최상위 파일 구조에 맞춰 ZIP 압축 해제 안내를 수정했습니다.

- 출력 직전에 출력 계약을 다시 읽고, 비교 우위·조사·정도 부사 결합을 검토하도록 보완했습니다. 반환 결과를 Markdown 교정 문서로 정의하고 스킬 설명에도 고정 섹션 형식을 명시했습니다.

- 실제 스킬 호출에서도 참조 파일을 읽고 기본 응답 형식을 지키도록 지침 순서와 완료 조건을 보완했습니다.
- 변경 설명의 근거, 문장 흐름, 확신과 평가 강도의 보존을 스킬 내부 최종 검토에 명시했습니다.

- 이모지는 개수 대신 역할로 판단하며, 문장 간 같은 사건·요청의 반복을 마지막 검토에서 정리합니다.

- 설치 경로 재실행 시 자기 참조 링크, ripgrep 없는 검사 실패를 수정했습니다.
- 길이 하한·보존어·부정 테스트·빈 fixture·CLI 경로와 옵션 검사를 보완했습니다.
- 원문에 없는 정보를 추가하던 실행 참조 예시를 교체하고 지침 우선순위를 통일했습니다.
- Markdown 코드 블록 앞뒤 빈 줄 경고를 해결했습니다.

### Documentation

- 기본 표시를 main의 `Humanized`·`주요 변경 (최대 5개)`·첫 응답 안내로 복원합니다.

- README를 설치·사용·현재 예시 중심으로 정리하고 [문서 안내](docs/README.md)를 추가했습니다.
- 과거 베타·완료 개발 계획·비교 사례를 `docs/archive/`에 보관했습니다.
- 빈 피드백 scaffold·중복 장문 연구 교정본·적용 완료 Topics 메모를 제거하고 용어를 `AGENTS.md`에 통합했습니다.
- 연구 배경·빈도 측정 계획·QA·홍보 기록은 목적별 디렉토리로 옮겼습니다.

### Validation

- 수정 전 main `9358056`과 간결화 기준 추가본에 동일 입력 8개를 각각 새 Codex 세션에서 실행했습니다. 전체 응답 16개·실행 조건과 원문 대비 검토를 `eval/six-rules-2026-10-10.md` 및 원본 JSON에 기록했습니다. 이번 표본에서는 이전 지침도 주요 의미를 보존했으므로 일반적인 품질 향상을 주장하지 않습니다.

- 2026-10-02 최신 배포 ZIP을 스킬 이름으로 호출한 9응답에서 Claude 3/3회, Codex 6/6회가 고정 제목·최대 5개 변경 설명·첫 응답 안내를 지켰습니다. 이전 후보의 제목 누락은 실패 이력으로 유지합니다. 출력 형식 힌트와 생성 후 교정은 없었으며, 이 작은 표본으로 일반적인 성공률을 주장하지 않습니다.

- 입력 12개를 두 CLI에서 스킬 이름으로 직접 호출했습니다. 최종 기록은 최신 지침의 6응답과 직전 지침의 18응답으로 구분하며, 원본·해시·실패 이력은 [실행 기록](eval/native-skill-2026-10-01.md)에 남겼습니다. 응답 후 재교정은 하지 않았습니다.

- 이모지·문장 흐름 보완 후 입력 8개를 두 모델에서 실행한 실제 응답 16개를 [별도 기록](eval/emoji-and-flow-2026-10-01.md)했습니다.

- 최종 지침으로 README 원문 3개와 보존 입력 2개를 Opus 5.5·Astra에서 실행한 결과 10개와 [조건·한계](eval/model-comparison.md)를 기록했습니다. 스킬·카탈로그를 직접 전달한 실행이며 설치 검증이나 모델 순위 평가가 아닙니다.
- 회귀 검사 15개, 고정 입력·출력 fixture 25개를 확인했습니다. 모델 품질 성공률을 뜻하지 않습니다.
- 검사 범위·한계와 작은 실행 사례는 [QA 기록](docs/reviews/2026-10-01-qa.md)에 남겼습니다.

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
- 외부 fork 사용자: [`docs/MIGRATION-0.x-to-1.0.md`](docs/archive/migrations/MIGRATION-0.x-to-1.0.md) 참조.

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

- 외부 fork 사용자: [`roadmap/S3-migration-notes.md`](docs/archive/roadmap/S3-migration-notes.md) — 표 헤더 4 컬럼 + 도메인 코드 부여 절차.
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
- v0.x → v1.0 전체 마이그레이션: [`docs/MIGRATION-0.x-to-1.0.md`](docs/archive/migrations/MIGRATION-0.x-to-1.0.md)
- 4 sprint 로드맵: [`ROADMAP.md`](ROADMAP.md)
