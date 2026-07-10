# Voice DNA 추출 가이드

사용자가 자기 글 10-20개나 영상 transcript 를 주면, 내용을 요약하지 말고 **어떻게 말하는지**만 추출한다.

## 입력으로 좋은 자료

- 최근 게시물 10-20개
- 영상 / 팟캐스트 transcript
- 뉴스레터 원문
- 직접 쓴 이메일 / LinkedIn / 블로그 글

## 추출 절차

1. 모든 샘플을 먼저 읽고 도메인을 나눈다.
2. 내용 주제는 요약하지 않는다.
3. 문장 길이, 종결어미, 줄바꿈, 쉼표, 괄호, 강조 방식만 본다.
4. 반복되는 실제 표현과 절대 쓰지 않을 표현을 분리한다.
5. hook / closing 패턴을 따로 뽑는다.
6. `examples/voice-dna-template.md` 형식으로 profile 을 만든다.

## 추출 프롬프트

```text
아래 글 샘플에서 내 Voice DNA 를 추출해줘.
내용을 요약하지 말고, 내가 어떻게 쓰고 말하는지만 분석해줘.

출력은 다음 섹션으로 정리해줘:
- How I sound
- Sentence shapes
- Signature phrases & tics
- How I open
- How I close
- Anti-voice
- Application notes

규칙:
- 모든 판단은 실제 샘플 문장에 근거해.
- 내가 쓰지 않은 표현을 "추천"하지 마.
- 원문에 없는 사실 / 경험 / 수치를 만들지 마.
- 너무 일반적인 말("친근하고 명확함") 대신 문장 길이, 어미, 전환어, 리듬을 구체적으로 적어.

[여기에 샘플 10-20개 붙여넣기]
```

## 적용 예

```markdown
---
name: founder-note-voice
domain_default: linkedin
ending_default: ~합니다
emoji_policy: none
length_bias: concise
preserve:
  - "작게 시작"
ban:
  - "혁신적인"
  - "압도적인"
prefer:
  - "활용 → 쓰기"
---

## How I sound

- 짧은 문장으로 시작하고, 두 번째 문장에서 이유를 붙인다.
- 과한 감탄보다 담담한 단정을 선호한다.
- "~라고 봅니다" 보다 "~입니다" 를 더 자주 쓴다.

## Anti-voice

- "여러분도 함께해요" 같은 단체 호응형 마무리는 쓰지 않는다.
- 이모지와 느낌표를 쓰지 않는다.
```

## 주의

Voice DNA 는 "그 사람처럼 보이게 꾸미는" 장치가 아니다. 사용자가 직접 준 자기 글을 기준으로, 같은 사람이 후속 글을 다듬을 때 말투 drift 를 줄이는 장치다. 타인의 voice 를 무단으로 모방하거나 사칭하는 용도로 쓰지 않는다.
