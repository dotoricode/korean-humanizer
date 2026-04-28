---
name: 새 도메인 비교 사례 제안
about: examples/agent-vs-skill.md에 추가할 새 도메인의 raw vs skill 적용 사례를 제안합니다
title: "[Domain Case] "
labels: example, enhancement
---

## 도메인

(예: 학술 논문 인트로 / 정부 보도자료 / 게임 리뷰 / 의료 컨퍼런스 abstract / ...)

## 프롬프트

```
(모델에게 던진 프롬프트 — 한 줄~3줄)
```

## Raw 출력 (humanizer 의식 없이)

```
(모델이 평소처럼 출력한 한국어 결과물)
```

- 모델: (예: Claude Opus 4.7 / GPT-5 / Gemini 2.5)
- 시점: YYYY-MM-DD
- 문장 수: ___ 문장 / 약 ___ 자

## Humanized (룰 적용 결과)

```
(SKILL.md 또는 PROMPT.md를 적용한 결과)
```

- 문장 수: ___ 문장 / 약 ___ 자 (-__%)

## 변경 표

| # | 카테고리 | Before → After |
|---|---|---|
| 1 |  |  |
| 2 |  |  |

## 개선 포인트

- (3~5줄)

## 한계

- (이 도메인에서 humanizer가 닿지 못한 부분 / personality 보호가 필요한 부분)

## 룰 한도 체크

- [ ] 한 문단 3곳 룰 적용 결과 명시 (위반 시 logical paragraph 해석 사용 명시)
- [ ] 전체 문장 수의 20% 한도 체크
- [ ] 의미 불변 — 팩트 / 숫자 / 고유명사 / 인용문 / 링크 그대로
- [ ] 카테고리 라벨이 카탈로그와 1:1 매칭됨
