# Eval harness

> 휴리스틱 자동 검증 layer — humanized 결과가 SKILL.md 의 정량 룰을 실제로 지키는지 확인.

## 무엇을 검사하나

| Metric | 정의 | Pass 조건 |
|---|---|---|
| **M1** 수정 비율 | modified-sentence count / raw-sentence count | ≤ `cap` (기본 0.20) |
| **M2** 단락 cap | 단락 별 최대 modified-sentence count | ≤ `paragraph_cap` (기본 3) |
| **M3** 길이 비율 | `len(humanized) / len(raw)` | 0.5 ~ 1.05 (warn: 0.30~0.5 / 1.05~1.20, fail: <0.30 또는 >1.20) |
| **M4** 톤 보존 | 발화체 도메인에서 raw 에 없던 ~다체가 humanized 에 도입되면 fail | speech 도메인에서만 활성, 그 외 n/a |
| **M5** brand preserve *(v0.8)* | brand voice 의 `preserve` 단어가 humanized 에 모두 살아있어야 pass | `brand_voice:` frontmatter 있을 때만 활성, 그 외 n/a |

> **modified-sentence**: raw sentence 와 humanized 후보들 중 *최소* normalized edit distance 가 0.15 초과면 modified.

## Fixture 형식

`eval/fixtures/<domain>-<num>.md`:

```markdown
---
domain: blog
cap: 20
paragraph_cap: 3
expected_failures:
notes: 짧은 코멘트 (선택)
---

## Raw

[원문]

## Humanized

[다듬어진 텍스트]
```

### Frontmatter 필드

| 필드 | 필수 | 의미 |
|---|---|---|
| `domain` | ✓ | 12 도메인 중 하나 (`blog` `marketing` `email` `linkedin` `youtube` `newsletter` `wiki` `academic` `news` `chat` `review` `b2b-message`) |
| `cap` | | 수정 비율 임계 (% 단위, 기본 20) |
| `paragraph_cap` | | 단락 cap (기본 3) |
| `expected_failures` | | 의도적으로 실패해야 할 metric 목록 (예: `m4` — trap fixture). 콤마 구분 (`m1, m3`). 일반 품질 fixture 에는 쓰지 않는다. |
| `brand_voice` | | brand voice profile 파일 path (옵션, v0.8). 있으면 M5 활성 — preserve 단어가 humanized 에 모두 살아있는지 검증. 예: `examples/brand-voice-toss-style.md`. |
| `notes` | | fixture 가 검증하는 시나리오 한 줄 |

### Speech 도메인 (M4 활성)

`youtube` `podcast` `live` `lecture`. 그 외는 M4 = `n/a`.

## 실행

```bash
bash scripts/eval-harness.sh
# = python3 scripts/eval-harness.py --strict
```

`eval/scorecard.md` 가 자동 생성됨. CI 는 `--strict` 로 fail 일 때 exit 1.

## 회귀 시나리오 (개발용)

`scripts/eval-harness.py --no-strict` 로 단순 리포트만 생성. fixture 수정 → 점수 변화 확인 워크플로우에 사용.

Scorecard 의 `Clean pass` 는 실제 품질 통과, `Expected-failure pass` 는 trap / known-risk fixture 통과다. v1 안정화에서는 일반 품질 fixture 의 expected failure 를 줄이고, 남기는 항목은 파일명과 `notes` 에 trap 목적을 명시한다.

## Fixture 큐레이션 가이드

- 같은 도메인 fixture 가 너무 몰리지 않게 — 도메인 별 1-3 개.
- raw 는 모델 평소 출력 그대로 (humanizer 의식 X).
- humanized 는 SKILL 룰 안에서만 손댐 (통째로 새로 쓰지 않음).
- 짧은 fixture (1-2 문장) 와 장문 fixture (40+ 문장) 모두 포함.
- 톤 위반·과다 수정 등 의도적 trap 1-2 개 — `expected_failures` 명시. 실제 예시 품질을 보여주는 fixture 에는 expected failure 를 붙이지 않는다.
