# Eval harness

> 휴리스틱 자동 검증 layer — humanized 결과가 SKILL.md 의 정량 룰을 실제로 지키는지 확인.

## 무엇을 검사하나

| Metric | 정의 | Pass 조건 |
|---|---|---|
| **M1** 수정 비율 | modified-sentence count / raw-sentence count | ≤ `cap` (기본 0.20) |
| **M2** 단락 cap | 단락 별 최대 modified-sentence count | ≤ `paragraph_cap` (기본 3) |
| **M3** 길이 비율 | `len(humanized) / len(raw)` | 0.90 ~ 1.05 (warn: 0.50~0.90 / 1.05~1.20, fail: <0.50 또는 >1.20) |
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

항상 wrapper 로 실행한다. wrapper 는 실행 가능한 Python 3.8+만 선택한 뒤 harness 를 호출한다.

```bash
bash scripts/eval-harness.sh
# strict 검증 (기본값)

bash scripts/eval-harness.sh --no-strict
# 로컬 점수 확인
```

`eval/scorecard.md` 가 자동 생성됨. CI 는 strict 모드에서 fail 이면 exit 1.

### Python 선택과 override

`PYTHON` 이 비어 있거나 설정되지 않으면 wrapper 는 순서대로 `python3`, `python`, `py -3`를 검사한다. Windows Store `python3` alias 처럼 PATH 에 있지만 실행할 수 없는 후보는 거부하고 다음 후보로 진행한다.

비어 있지 않은 `PYTHON` 은 fallback 하지 않는다. 정확히 `PYTHON='py -3'`만 `py`와 `-3`의 두 argv 요소로 해석한다. 그 밖의 값은 공백을 포함해 하나의 실행 파일 pathname 이다.

```bash
PYTHON='py -3' bash scripts/eval-harness.sh
PYTHON='/path with spaces/python' bash scripts/eval-harness.sh
```

flags, quoting, command line, shell syntax은 지원하지 않으며 parsing/eval하지 않는다.

각 후보는 Python 3.8+ sentinel, exit 0, stderr 없음만 통과한다. 기본 선택은 `eval-harness: candidate=... rejected: ...`와 `eval-harness: selected candidate=... version=...`를 순서대로 stderr에 출력한다. 명시 override 실패는 fallback 없이 `eval-harness: PYTHON override candidate=... rejected: ...; set PYTHON to an executable pathname or unset it`를 출력한다. 거부 이유는 probe exit, invalid sentinel, Python 3.8 미만, probe stderr 중 하나다.

## Fixture 큐레이션 가이드

- 같은 도메인 fixture 가 너무 몰리지 않게 — 도메인 별 1-3 개.
- raw 는 모델 평소 출력 그대로 (humanizer 의식 X).
- humanized 는 SKILL 룰 안에서만 손댐 (통째로 새로 쓰지 않음).
- 짧은 fixture (1-2 문장) 와 장문 fixture (40+ 문장) 모두 포함.
- 톤 위반·과다 수정 등 의도적 trap 1-2 개 — `expected_failures` 명시. 실제 예시 품질을 보여주는 fixture 에는 expected failure 를 붙이지 않는다.
