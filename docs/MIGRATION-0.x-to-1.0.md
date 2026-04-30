# Migration Guide — v0.x → v1.0

> v0.5 부터 v1.0 까지 4 sprint 동안 누적된 변경 사항을 단일 문서로 통합. 어떤 사용자가 어떤 작업을 해야 하는지 영향 매트릭스 + step-by-step.

---

## TL;DR — 일반 사용자 (90 % 케이스)

**SKILL.md / PROMPT.md 만 사용** 하는 일반 사용자는:

```bash
cd ~/.claude/skills/korean-humanizer  # 또는 자기 환경 path
git pull
```

이게 끝. 영향 0. 12 카테고리 / 정량 룰 / 출력 포맷 모두 동일하다.

**아래는** 카탈로그 / lint / eval-harness 를 직접 fork 했거나 inline 한 사용자용.

---

## 영향 매트릭스

| 환경 | 0.5 → 1.0 영향 | 작업 |
|---|---|---|
| Claude Code / OpenCode / Codex (skill 사용) | 0 | `git pull` |
| Claude.ai (Cowork — SKILL.md 업로드) | 0 | 새 SKILL.md 다시 업로드 |
| ChatGPT / Cursor / Gemini (PROMPT.md 시스템 프롬프트) | 0 | 새 PROMPT.md 로 갱신 |
| 카탈로그 fork / inline (외부 도구) | **큼** | 카탈로그 표 4 컬럼 마이그레이션 (S3 §1) |
| 외부 lint 도구 fork | 중간 | lint-patterns.sh v2 갱신 또는 본 스크립트 사용 |
| 외부 eval-harness fork | 중간 | M5 metric 추가 (옵션) |
| Brand voice 사용 (신규) | n/a | 0.8 부터 사용 가능, 안 쓰면 영향 없음 |

---

## 버전별 변경 요약

### 0.5 → 0.6 (S1 — Eval Foundation)

#### Added

- `scripts/eval-harness.py` (4 metric 자동 검증).
- 20 fixture (`eval/fixtures/`).
- `eval/scorecard.md` (auto-gen).
- 5 번째 CI hard-fail job.

#### 외부 영향

- **카탈로그 fork**: 0.
- **lint fork**: 0.
- **eval-harness fork**: 4 metric 가정 — 기존이 있으면 그대로, 신규는 본 script 사용 권장.

---

### 0.6 → 0.7 (S2 — Domain Coverage v2)

#### Added

- 5 신규 도메인 사례 (`examples/domain-academic.md` / `domain-news.md` / `domain-chat.md` / `domain-review.md` / `domain-b2b-message.md`).
- 카탈로그 부록 E (도메인별 카테고리 우선순위 매트릭스).

#### 외부 영향

- **카탈로그 fork**: 부록 E 가 새로 추가됨. fork 가 부록을 통째로 가져왔다면 부록 E 추가 cherry-pick.
- **lint fork**: 0.
- **eval-harness fork**: 5 신규 도메인 fixture 추가 — 기존 12 도메인 가정에 새 코드 (`academic` / `news` / `chat` / `review` / `b2b-message`) 추가 필요.

---

### 0.7 → 0.8 (S3 — Brand Voice + Catalog v2) — **BREAKING for fork**

#### Added

- Brand voice profile (4 번째 customization mode) — `examples/brand-voice-template.md`, `brand-voice-toss-style.md`, `brand-voice-essayist.md`.
- 부록 F (도메인 코드 표준).
- M5 (brand voice preserve coverage) 옵션 metric.
- `eval/frequency-data/` 스캐폴딩.

#### Changed (BREAKING for fork)

- **카탈로그 9 패턴 표** → 4 컬럼 (`나쁨 / 자연스러움 / 빈도 / 적용 도메인`).
- `lint-patterns.sh` v2 — 4 컬럼 의무 + 도메인 코드 valid 검증.
- `lint-cross-file.sh` — 4 번째 mode + brand voice 파일 + 부록 F sync 검증 추가.
- SKILL.md / PROMPT.md — 4 번째 mode (방식 D / 형식 D) 섹션 추가.

#### 외부 영향

- **카탈로그 fork**: **마이그레이션 의무**. 9 표 헤더에 `| 적용 도메인 |` 컬럼 추가, 정렬 줄 (`|---|`) 한 칸 추가, 모든 데이터 행 끝에 도메인 값 (`all` 안전 디폴트). 자세한 절차: [`roadmap/S3-migration-notes.md`](../roadmap/S3-migration-notes.md).
- **lint fork**: lint-patterns.sh v2 갱신 또는 본 스크립트 사용.
- **eval-harness fork**: M5 옵션 metric 추가. `brand_voice` frontmatter 없는 fixture 는 `n/a` (기존 동작 유지).

#### 자동 마이그레이션 sed 한 줄

자기 fork 의 카탈로그가 v0.7 헤더라면:

```bash
# Dry-run (실제 수정 안 함, diff 만 확인)
sed -E '/^\|.*\|.*\|.*\|.*\|$/!{ /^\|.*\| (high|med|low) \|$/s/$/ all |/ }' references/ko-ai-signals.md > /tmp/diff.md
diff references/ko-ai-signals.md /tmp/diff.md

# 적용
sed -i.bak -E '/^\|.*\|.*\|.*\|.*\|$/!{ /^\|.*\| (high|med|low) \|$/s/$/ all |/ }' references/ko-ai-signals.md
```

(헤더 / 정렬 줄도 손으로 수정 필요. 본 레포의 `references/ko-ai-signals.md` 가 reference.)

---

### 0.8 → 1.0 (S4 — Stabilization)

#### Added

- `docs/STABILITY-PROMISE.md` — v1.0 freeze 영역 명문화.
- `CHANGELOG.md` — 0.1 ~ 1.0 종합.
- `SECURITY.md` — 보안 정책.
- `docs/beta-recruit.md` / `docs/beta-guide.md` / `docs/beta-feedback-form-spec.md` — 베타 운영 자료.
- README v1.0 hero + 안정화 배지.

#### Changed

- **변경 없음** — 1.0 은 0.8 의 surface freeze 약속. 코드 / 카탈로그 동작 동일.
- 베타 피드백 반영으로 **카탈로그 패턴 행 추가 / 자연스러움 컬럼 개선** 발생 시 — minor (1.0.x or 1.1) 로 분리 release.

#### 외부 영향

- **모든 사용자**: 0 (freeze 의 의미).
- 1.x 동안 minor / patch 룰: [`docs/STABILITY-PROMISE.md`](STABILITY-PROMISE.md).

---

## v1.0 이후 — 1.x 트랙 가이드

v1.0 이후 minor / patch / major 의 의미:

| 버전 | 변경 가능 영역 | 사용자 영향 |
|---|---|---|
| **1.0.x** (patch) | 오탈자 / lint 미세 조정 / CI 인프라 / 케이스 스터디 본문 개선 | 0 |
| **1.x.0** (minor) | 카탈로그 패턴 행 추가 / 자연스러움 개선 / 빈도 재라벨링 / 새 도메인 추가 / 새 옵션 metric / 새 examples / brand voice 보조 필드 추가 | 0 (freeze 영역 안 깨짐) |
| **2.0** (major) | freeze 영역 변경 (카테고리 #13 / 정량 룰 cap / 카탈로그 컬럼 변경 등) | 마이그레이션 가이드 동봉, 12 개월 N-1 보안 패치 지원 |

자세한 freeze 영역: [`docs/STABILITY-PROMISE.md`](STABILITY-PROMISE.md).

---

## FAQ

### Q. v0.5 부터 사용 중인데 어떻게 v1.0 으로 올라가요?

A. SKILL.md / PROMPT.md 만 쓰면 `git pull` 한 번. 카탈로그 / lint / eval 직접 건드리지 않으면 추가 작업 없음.

### Q. 자체 fork 한 카탈로그 표가 3 컬럼 (v0.5-0.7) 인데 v1.0 표 형식은 4 컬럼이라 lint 가 fail 해요.

A. v0.7 → v0.8 마이그레이션 [`roadmap/S3-migration-notes.md`](../roadmap/S3-migration-notes.md) 의 sed 스니펫 + 헤더 수동 수정. 모든 행 `all` 부여가 안전 디폴트.

### Q. Brand voice 안 쓰는데 4 번째 mode 가 영향을 주나요?

A. 0. Brand voice 는 *덧붙임* 으로만 동작. fixture 에 `brand_voice:` 명시 안 하면 M5 = `n/a` 로 무시.

### Q. 외부 LLM (ChatGPT 등) 에서 PROMPT.md 만 쓰는데 새로운 형식 D 추가가 의무인가요?

A. 아니오. 형식 D 섹션은 *옵션*. 사용 안 하면 기존 형식 A/B/C 와 12 카테고리만 동작 — v0.5-0.8 와 동일.

### Q. v1.0 이후 카테고리 #13 이 추가되면 어떻게 되나요?

A. 카테고리 추가 = 2.0 major bump. v1.x 동안은 12 카테고리 freeze. 새 패턴 군이 발견돼도 12 카테고리 안에서 행 추가 (minor) 또는 카테고리 라벨 미세 조정 (patch) 으로만 처리. #13 이 정말 필요해진 시점에 v2 RFC → community 협의.

### Q. 빈도 라벨이 v0.7 / v0.8 에서 다른가요?

A. 동일. v0.8 에서 4 번째 컬럼 (적용 도메인) 만 추가됐고 빈도 라벨은 v0.7 의 휴리스틱 그대로 carry over. 데이터 기반 재라벨링은 v1.0.x 또는 v1.1 sub-PR 트랙 (`eval/frequency-data/`).

### Q. v0.5 시절의 자체 personal list 가 v1.0 에서도 동작하나요?

A. ✓. Mode A / B / C 입력 형식 (`금지=...; 선호=A→B; 유지=...` / 자연어 한 줄 / `examples/personal-list.md` 파일) 은 v0.3 부터 v1.x 까지 freeze.

---

## 도움이 필요하면

- 마이그레이션이 막히면 [GitHub Issue](https://github.com/dotoricode/korean-humanizer/issues/new) 에 `[migration]` prefix 로.
- 외부 fork 가 카탈로그 v2 마이그레이션을 자동화한 스크립트가 있다면 PR 환영 (`scripts/migrate-catalog-v2.sh` 같은 자리).
- 보안 영향 있는 마이그레이션 이슈는 [SECURITY.md](../SECURITY.md) 절차로 비공개 보고.
