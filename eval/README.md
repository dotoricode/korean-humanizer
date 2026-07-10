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

## v1.x metric 후보

Advanced humanize pipeline 은 아직 휴리스틱 문서/fixture 중심으로 검증한다. 다음 metric 은 v1.x 에서 별도 구현 후보로 둔다.

| Metric | 목적 | 초안 판정 |
|---|---|---|
| **M6** 첫 문장 delay | 첫 문장에 주제 명사구가 너무 늦게 나오는지 확인 | domain 이 `linkedin` `newsletter` `youtube` `marketing` 일 때만 warn |
| **M7** AI tell residue | `references/ko-ai-signals.md` high-frequency 표현이 humanized 에 남았는지 확인 | brand preserve / quoted text 는 제외 |
| **M8** voice DNA coverage | voice DNA 의 ban / prefer / anti-voice 가 지켜졌는지 확인 | `voice_dna:` frontmatter 있을 때만 활성 |
| **M9** reading load | 긴 문장, 중첩절, 어려운 한자어 후보를 warn | domain 별 threshold 분리 |

새 metric 을 구현하기 전까지는 advanced pass fixture 도 M1-M5 를 반드시 통과해야 한다. hook / story / dumbify 를 이유로 20% cap 과 90% 길이 보존을 깨면 실패로 본다.

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

## Expected-failure cleanup

현재 scorecard 에는 legacy 교육용 예시에서 온 `expected_failures` 가 많다. v1.x cleanup 목표:

1. trap 목적 fixture 만 `expected_failures` 를 유지한다.
2. 일반 품질 fixture 는 20% cap / 문단 cap / 길이 비율을 통과하도록 humanized 를 다시 작성한다.
3. `examples/before-after.md` 의 강한 교육용 rewrite 는 eval fixture 와 분리한다.
4. clean pass 비율을 80% 이상으로 올린 뒤 새 metric 을 켠다.
