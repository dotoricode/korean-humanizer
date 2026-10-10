# Eval harness — 과거 보수적 편집 계약

> 과거 보수적 편집 계약에 따른 저장된 Raw / Humanized 쌍의 회귀 검사입니다. 모델을 실행하지 않으며, 자연스러움이나 의미 보존의 성공률을 측정하지 않습니다.

[스킬 직접 호출·다른 예시 검토](native-skill-2026-10-01.md)는 별도 기록입니다. 아래 고정 fixture 검사에 합산하지 않습니다.

간결화 규칙의 이전·수정 지침 비교는 `eval/six-rules-2026-10-10.md`에, 동일 입력 8개와 전체 응답 16개는 `eval/model-runs/six-rules-2026-10-10.json`에 기록했습니다.

현재 기본 교정은 수정량과 길이를 고정 비율로 제한하지 않습니다. 아래 M1/M2/M3의 기준은 과거 fixture·평가 도구의 동작을 검증하기 위한 값입니다. 현재 스킬 출력의 제품 품질이나 출시 조건으로 사용하지 않습니다.

## 무엇을 검사하나

| Metric | 정의 | Pass 조건 |
|---|---|---|
| **M1** 수정 비율 | 큰 수정으로 추정한 문장 수 / 원문 문장 수 | 수정 문장 수 ≤ `max(1, floor(원문 문장 수 × cap))`, 기본 `cap` 0.20 |
| **M2** 단락 cap | 단락별 큰 수정으로 추정한 문장 수 | ≤ `paragraph_cap` (기본 3) |
| **M3** 길이 비율 | `len(humanized) / len(raw)` | pass: 0.90–1.05, warn: >1.05–1.20, fail: <0.90 또는 >1.20 |
| **M4** 톤 보존 | 발화체 도메인에서 raw 에 없던 ~다체가 humanized 에 도입되면 fail | speech 도메인에서만 활성, 그 외 n/a |
| **M5** brand preserve *(v0.8)* | 원문에 있는 `preserve` 단어의 등장 횟수 보존 | `brand_voice:` frontmatter 있을 때만 활성, 그 외 n/a |

> **큰 수정으로 추정한 문장**: 원문 문장과 결과 문장 후보 사이의 최소 정규화 편집 거리가 0.20을 초과한 문장입니다. 작은 단어 치환은 세지 않을 수 있습니다. M1/M2는 정확한 수정 문장 수·표현 수를 보장하지 않으며, 문장 순서나 삭제도 완전히 검증하지 않습니다.

M3는 문자 수를 직접 계산하지만 M4는 일부 어미 패턴만 검사합니다. 숫자·날짜·고유명사·인용·링크·조건·말투 보존은 실제 모델 출력에서 별도로 확인해야 합니다. `Clean pass`도 이 검사 범위 안의 통과만 뜻합니다.

## Fixture 형식

`eval/fixtures/<domain>-<num>.md`:

```markdown
---
domain: blog
cap: 20
paragraph_cap: 3
expected_failures:
required_failures:
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
| `expected_failures` | | 허용할 기존 실패 목록. 콤마 구분 (`m1, m3`). 정상 사례에는 사용하지 않음. |
| `required_failures` | | trap이 반드시 탐지해야 할 실패 목록. `expected_failures`의 일부여야 하며 누락 시 전체 실패 처리. |
| `brand_voice` | | 저장소 기준 상대 경로 또는 절대 경로. 원문에 있던 preserve 단어만 M5로 검사. block 목록과 inline 문자열 목록 지원. |
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

`python3 scripts/eval-harness.py --no-strict`로 단순 리포트를 생성합니다. wrapper도 `--fixtures-dir`, `--scorecard`, `--no-scorecard`를 전달합니다. 기본 경로는 실행 위치와 관계없이 저장소의 `eval/`입니다.

Scorecard의 `Clean pass`는 고정 사례의 검사 통과, `Expected-failure pass`는 기존 과교정 사례 또는 trap의 허용된 실패입니다. 실제 모델 품질의 성공률이 아닙니다. 기존 과교정 결과는 그대로 남겨 검사 경계를 확인하며, `notes`로 정상 예시와 구분합니다. trap에는 `required_failures`를 함께 지정합니다.

회귀 검사 추가 실행:

```bash
python3 scripts/test-regressions.py
```

설치 검사는 임시 복사본의 home 경로만 격리합니다. 실제 사용자 설치 경로는 변경하지 않습니다. Claude Code·Codex가 스킬을 읽고 모델 출력을 생성하는 검증은 이 테스트에 포함되지 않습니다.

## Fixture 큐레이션 가이드

- 같은 도메인 fixture 가 너무 몰리지 않게 — 도메인 별 1-3 개.
- raw 는 모델 평소 출력 그대로 (humanizer 의식 X).
- humanized 는 SKILL 룰 안에서만 손댐 (통째로 새로 쓰지 않음).
- 짧은 fixture (1-2 문장) 와 장문 fixture (40+ 문장) 모두 포함.
- 톤 위반·과다 수정 등 의도적 trap 1-2 개 — `expected_failures` 명시. 실제 예시 품질을 보여주는 fixture 에는 expected failure 를 붙이지 않는다.
