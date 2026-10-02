# korean-humanizer

한국어 AI 글에서 어색한 표현을 줄이는 스킬과 프롬프트입니다. 원문의 의미·정보·말투를 유지하며 필요한 부분만 다듬습니다.

[English](README.md) · [中文](README.zh-CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

마지막 출시 버전은 **v1.0.1**입니다. 이 문서는 main의 개선 사항을 설명하며 다음 버전 번호는 미정입니다. [버전 정책](docs/STABILITY-PROMISE.md)과 [변경 안내](docs/UPGRADE-NOTES.md)를 확인하세요.

![korean-humanizer preview](assets/translation-humanizer-card.svg)

## 바로 써보기

설치 없이 쓰려면 [짧은 프롬프트](PROMPT.short.md)를 사용하는 LLM의 지침 또는 첫 메시지에 붙여 넣고 아래처럼 요청하세요. 더 자세한 규칙은 [전체 프롬프트](PROMPT.md)에 있습니다.

```text
이거 AI 티 빼줘. 도메인=email:
안녕하세요. 다름이 아니오라 미팅 일정과 관련하여 말씀드리고자 연락드립니다. 부득이한 사정으로 인해 일정 변경이 불가피한 상황이 발생하여 양해를 구하고자 합니다.
```

`$korean-humanizer`를 실제로 호출한 Astra의 첫 최종 응답입니다. 요청에 지침 본문이나 정답을 넣지 않았고 응답 뒤 재교정하지 않았습니다.

````markdown
## Humanized

안녕하세요. 부득이한 사정으로 미팅 일정을 변경해야 해서 연락드립니다. 양해 부탁드립니다.

## 주요 변경 (최대 5개)

- “다름이 아니오라”를 덜고 연락 목적을 바로 전했습니다.
- “일정 변경이 불가피한 상황이 발생하여”를 “일정을 변경해야 해서”로 줄였습니다.
- “양해를 구하고자 합니다”를 “양해 부탁드립니다”로 다듬었습니다.

*마음에 안 드는 변경이 있으면 알려주세요 — 되돌리거나 다시 다듬겠습니다.*
````

[실제 스킬 호출·다른 예시 검토](eval/native-skill-2026-10-01.md) · [이전 지침 직접 전달 검사](eval/emoji-and-flow-2026-10-01.md)

## 설치

스킬을 사용할 프로젝트에서 아래 명령을 실행합니다. [Skills CLI](https://github.com/vercel-labs/skills)를 사용하며 Node.js/npm이 필요합니다.

```bash
npx skills add dotoricode/korean-humanizer --skill korean-humanizer --agent codex claude-code --copy
```

공개 저장소의 기본 브랜치를 Codex의 `.agents/skills/korean-humanizer/`와 Claude Code의 `.claude/skills/korean-humanizer/`에 파일로 설치합니다. 하나만 설치하려면 `--agent codex` 또는 `--agent claude-code`로 바꾸고, 모든 프로젝트에서 쓰려면 `--global`을 추가합니다. Codex·Claude 내장 명령이 아닌 외부 전용 설치 CLI입니다.

설치한 프로젝트에서 새 대화를 시작합니다. Codex에서는 `$korean-humanizer`, Claude Code에서는 `/korean-humanizer` 뒤에 교정할 원문을 전달합니다. 설치 목록은 `npx skills list`로 확인합니다.

PR #5는 머지되었습니다. 기본 브랜치는 v1.0.1 이후 개선을 포함하며 마지막 정식 태그는 v1.0.1입니다. 설치·첫 호출 검사와 출력 품질 검사는 구분합니다. 남은 출시 검사는 `ROADMAP.md`에 기록합니다.

## 어떻게 다듬나요?

- 사실·숫자·날짜·고유명사·링크·인용과 가능성·조건을 보존합니다.
- 원래의 존댓말과 종결어미를 유지합니다. 말로 읽을 글을 문어체로 바꾸지 않습니다.
- 수정량을 고정 비율로 제한하지 않고, 글 전체의 어색한 표현을 자연스럽게 고칩니다.
- 중복과 장식을 줄일 수 있습니다. 문자 수보다 핵심 정보·조건·확신의 보존을 확인합니다.
- 문맥상 자연스러운 표현은 그대로 둡니다. 카탈로그는 일괄 치환 목록이 아닙니다.
- 용도가 명확하면 바로 처리하고, 의미나 말투를 잘못 바꿀 위험이 있을 때 질문합니다.
- 기본 응답은 `main`과 같은 `Humanized`·`주요 변경 (최대 5개)`와 첫 응답 안내입니다. 전체 diff나 본문만 필요하면 요청하세요.

이는 편집 지침입니다. 모든 모델이 항상 지킨다는 보증은 아닙니다. [평가 안내](eval/README.md)의 자동 검사는 고정된 입력·출력 쌍을 확인하며, 자연스러움이나 의미 보존을 완전히 판단하지 못합니다.

## 내 말투와 금지어 적용

한 번만 적용할 설정은 요청에 적으세요.

```text
이거 AI 티 빼줘. 금지=활용,매우; 선호=유용하다→쓸만하다:
[원문]
```

반복 사용할 설정은 파일로 지정합니다.

```text
personal=내-설정.md
brand=내-브랜드.md
```

[개인 설정 양식](examples/personal-list.md)과 [Brand voice 양식](examples/brand-voice-template.md)을 복사해 수정하세요. 제공 예시 목록은 자동 적용하지 않습니다. 참고 글도 선택적으로 전달할 수 있습니다. 어떤 설정도 사실·의미·말투 보존 규칙을 앞설 수 없습니다.

## 문서와 기여

| 목적 | 문서 |
|---|---|
| 표현별 후보 확인 | [패턴 카탈로그](references/ko-ai-signals.md), [빠른 참고표](CHEATSHEET.md) |
| 도메인·Brand voice 예시 | [문서 안내](docs/README.md) |
| 검사 방법과 한계 | [평가 안내](eval/README.md), [평가표](eval/scorecard.md) |
| 변경·출시 준비 | [CHANGELOG](CHANGELOG.md), [ROADMAP](ROADMAP.md) |
| 기여·보안 | [CONTRIBUTING](CONTRIBUTING.md), [SECURITY](SECURITY.md) |

[Issue](https://github.com/dotoricode/korean-humanizer/issues)와 PR을 환영합니다. 도움이 됐다면 GitHub Star로 알려주세요. [MIT 라이선스](LICENSE)로 사용할 수 있습니다.

## 외부 체험 서비스

Socialistic/Tinkerland가 운영하는 제3자 체험 서비스입니다. 저장소의 공식 서비스가 아니며, 입력은 외부 운영자가 처리합니다.

[Socialistic에서 체험하기](https://socialistic.ai/ko/skill/writing-dotoricode-korean-humanizer-5d759b?utm_source=github&utm_medium=readme&utm_campaign=20260520-writing-koc-creators&utm_content=badge)
