# korean-humanizer

한국어 AI 글에서 어색한 표현을 줄이는 스킬과 프롬프트입니다. 원문의 의미·정보·말투를 유지하며 필요한 부분만 다듬습니다.

[English](README.md) · [中文](README.zh-CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Next release](https://img.shields.io/badge/next-2.0_unreleased-orange.svg)](docs/MIGRATION-1.x-to-2.x.md)

마지막 출시 버전은 **v1.0.1**입니다. 이 문서는 **미출시 2.0 준비 변경**을 설명합니다. 1.x 사용자는 [호환성 약속](docs/STABILITY-PROMISE.md)과 [마이그레이션 안내](docs/MIGRATION-1.x-to-2.x.md)를 확인하세요.

![korean-humanizer preview](assets/translation-humanizer-card.svg)

## 바로 써보기

설치 없이 쓰려면 [짧은 프롬프트](PROMPT.short.md)를 사용하는 LLM의 지침 또는 첫 메시지에 붙여 넣고 아래처럼 요청하세요. 더 자세한 규칙은 [전체 프롬프트](PROMPT.md)에 있습니다.

```text
이거 AI 티 빼줘. 도메인=email:
안녕하세요. 다름이 아니오라 미팅 일정과 관련하여 말씀드리고자 연락드립니다. 부득이한 사정으로 인해 일정 변경이 불가피한 상황이 발생하여 양해를 구하고자 합니다.
```

이모지·문장 흐름 지침을 보완한 뒤 Codex CLI + GPT-6 Astra에 직접 전달한 실제 출력입니다. main과 같은 표시를 사용합니다.

````markdown
## Humanized

안녕하세요. 부득이한 사정으로 미팅 일정을 변경해야 해서 연락드립니다. 양해 부탁드립니다.

## 주요 변경 (최대 5개)

- “다름이 아니오라” 삭제 (불필요한 도입 표현)
- “미팅 일정과 관련하여 말씀드리고자 연락드립니다”와 일정 변경 사유를 한 문장으로 정리 (연락 목적과 사유 보존)
- “일정 변경이 불가피한 상황이 발생하여” → “일정을 변경해야 해서” (겹치는 표현 정리)
- “양해를 구하고자 합니다” → “양해 부탁드립니다” (정중한 말투를 유지하며 간결하게 수정)

*마음에 안 드는 변경이 있으면 알려주세요 — 되돌리거나 다시 다듬겠습니다.*
````

[Opus 5.5·Astra 최신 결과 비교](eval/emoji-and-flow-2026-10-01.md) · [이전 실행 기록](eval/model-comparison.md) · [과거 수동 예시](examples/before-after.md)

## 설치

### Codex

```bash
git clone https://github.com/dotoricode/korean-humanizer.git
cd korean-humanizer
bash scripts/install-codex-skill.sh
bash scripts/check-codex-skill.sh
```

설치 스크립트는 저장소를 스킬 경로에 연결합니다. 설치 후 저장소를 옮기면 링크를 다시 설치해야 합니다.

### Claude Code

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/dotoricode/korean-humanizer.git ~/.claude/skills/korean-humanizer
```

설치 후 `이거 AI 티 빼줘:`와 함께 원문을 전달하세요. 이번 작업에서는 Codex 설치와 작은 실행 사례를 검사했으며, Claude Code 설치부터 첫 실행까지는 검사하지 않았습니다.

위 명령은 기본 브랜치를 설치합니다. 미출시 변경은 [PR #5](https://github.com/dotoricode/korean-humanizer/pull/5)에서 확인할 수 있습니다. 출시된 1.x를 고정하려면 복제한 저장소에서 `git checkout v1.0.1`을 실행하세요.

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
