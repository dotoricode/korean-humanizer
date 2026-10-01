# 과거 보수적 지침의 README 예시 모델 비교

이 문서는 수정량·길이 제한이 있던 이전 실행 기록입니다. [현재 지침의 비교](model-comparison.md)를 먼저 읽으세요.

같은 원문을 Claude Code + Opus 5.5와 Codex CLI + GPT-6 Astra에서 각각 한 번씩 교정했습니다. 아래 결과 6개는 실제 출력이며 앞뒤 공백만 제거했으며 수동으로 다시 고치지 않았습니다. 서로 다른 표현을 선택했지만, 이번 사례에서는 모두 원문 길이의 90% 이상과 원래의 격식 어미를 유지했습니다.

## 실행 조건

| 항목 | 기록 |
|---|---|
| 실행일 | 2026-10-01, 입력별 새 대화, 모델별 1회 |
| 스킬·카탈로그 버전 | `4c5a02fb428eac7ff14f62a81881a3cd1c0f8652` |
| Claude | Claude Code 2.1.286, `claude-opus-5-5`, `--effort medium` |
| Codex | Codex CLI 0.159.3, `gpt-6-astra`, `model_reasoning_effort="medium"` |
| 공통 입력 | `SKILL.md`·카탈로그 전체 본문 + 도메인·README 원문 |
| 답안 노출 | README의 수동 편집 답안·이전 실행 결과는 전달하지 않음 |
| 외부 설정 | Claude safe mode, Codex ignore-user-config; CLI별 기본 지침은 다를 수 있음 |
| 도구 | Claude 도구 비활성화, Codex 사용 금지 요청; Codex 로그에서도 도구 실행 없음 |

모델명은 [Anthropic Opus 안내](https://www.anthropic.com/claude/opus)와 [OpenAI Astra 안내](https://developers.openai.com/api/docs/models/gpt-6-astra)에서 확인했습니다. Claude의 응답 `modelUsage`는 `claude-opus-5-5`를 기록했습니다. Codex는 CLI의 `--model gpt-6-astra` 선택을 기록했으며, 반환 이벤트에는 서버의 별도 모델·스냅샷 식별자가 없었습니다. 두 CLI의 `medium`이 같은 연산량을 뜻하지는 않습니다.

## 실제 출력

### Linkedin

| 구분 | 원문·실제 출력 |
|---|---|
| 원문 | 이번 프로젝트를 통해 다양한 기술적 도전을 경험하고 성장할 수 있었습니다. 이러한 경험은 앞으로의 커리어에 있어서 매우 소중한 자산이 될 것이라 확신합니다. 🚀 |
| Claude Code + Opus 5.5 | 이번 프로젝트를 통해 다양한 기술적 도전을 경험하고 성장할 수 있었습니다. 이런 경험은 앞으로의 커리어에서 매우 소중한 자산이 될 것이라 확신합니다. 🚀 |
| Codex CLI + GPT-6 Astra | 이번 프로젝트를 통해 다양한 기술적 도전을 경험하고 성장할 수 있었습니다. 이번 경험은 앞으로의 커리어에서 매우 소중한 자산이 될 것이라 확신합니다. 🚀 |

### Email

| 구분 | 원문·실제 출력 |
|---|---|
| 원문 | 안녕하세요. 다름이 아니오라 미팅 일정과 관련하여 말씀드리고자 연락드립니다. 부득이한 사정으로 인해 일정 변경이 불가피한 상황이 발생하여 양해를 구하고자 합니다. |
| Claude Code + Opus 5.5 | 안녕하세요. 다름이 아니오라 미팅 일정과 관련하여 말씀드리고자 연락드립니다. 부득이한 사정으로 일정을 변경할 수밖에 없게 되어 양해를 구하고자 합니다. |
| Codex CLI + GPT-6 Astra | 안녕하세요. 다름이 아니오라 미팅 일정과 관련하여 말씀드리고자 연락드립니다. 부득이한 사정으로 인해 일정을 변경해야 하는 상황이라 양해를 구하고자 합니다. |

### Marketing

| 구분 | 원문·실제 출력 |
|---|---|
| 원문 | 🚀 혁신적인 솔루션을 활용하여 다양한 비즈니스 가치를 극대화하고, 이러한 접근을 통해 사용자 경험을 한층 더 고도화할 수 있습니다. ✨ |
| Claude Code + Opus 5.5 | 🚀 혁신적인 솔루션을 활용하여 다양한 비즈니스 가치를 극대화하고, 이 방식으로 사용자 경험을 더 고도화할 수 있습니다. ✨ |
| Codex CLI + GPT-6 Astra | 🚀 혁신적인 솔루션을 사용하여 다양한 비즈니스 가치를 극대화하고, 이런 접근으로 사용자 경험을 한층 더 고도화할 수 있습니다. ✨ |

## 길이와 편집 범위

문자 수는 앞뒤 공백을 제거한 텍스트에 Python `len()`을 적용했습니다. 공백·문장부호·이모지도 포함하는 Unicode 코드 포인트 수입니다. 토큰 수나 눈에 보이는 글자 묶음의 수와는 다를 수 있습니다.

| 입력 | 모델 | 원문 → 결과 문자 수 | 길이 비율 |
|---|---|---|---|
| linkedin | Opus 5.5 | 89 → 85 | 95.5% |
| linkedin | Astra | 89 → 85 | 95.5% |
| email | Opus 5.5 | 90 → 84 | 93.3% |
| email | Astra | 90 → 86 | 95.6% |
| marketing | Opus 5.5 | 75 → 68 | 90.7% |
| marketing | Astra | 75 → 72 | 96.0% |

수정 문장은 원문과 결과를 문장별로 직접 비교했습니다. LinkedIn은 두 문장 중 두 번째, 이메일은 세 문장 중 세 번째, 마케팅은 한 문장만 수정했습니다. 모두 `max(1, floor(문장 수 × 0.20))` 안에서 수정했으며 문장 순서를 유지했습니다. 자동 평가의 M1 근사값을 정확한 수정 문장 수로 소개하지 않습니다.

| 입력 | 관찰한 차이 |
|---|---|
| LinkedIn | `이러한 경험`을 Opus는 `이런 경험`, Astra는 `이번 경험`으로 변경. 두 모델 모두 `커리어에 있어서`를 `커리어에서`로 변경 |
| 이메일 | 두 모델 모두 마지막 문장의 일정 변경 상황을 다듬음. 앞의 인사와 연락 목적은 유지 |
| 마케팅 | Opus는 `이러한 접근을 통해`와 `한층 더`를 다듬음. Astra는 `활용하여`와 `이러한 접근을 통해`를 다듬음 |

문맥상 원문에 있던 주장·가능성·양해 요청·격식 어미를 유지했으며, LinkedIn과 마케팅의 이모지도 보존했습니다. 이메일의 `다름이 아니오라`, 마케팅의 `혁신적인` 등 일부 후보는 남아 있습니다. 수정 한도 안에서 후보를 선택한 결과이므로 모든 후보를 없앤 예시로 읽지 마세요.

## 재현 방법

소스 커밋 `4c5a02fb428eac7ff14f62a81881a3cd1c0f8652`의 `SKILL.md`와 `references/ko-ai-signals.md`를 아래 위치에 **그대로** 넣고, 각 예시마다 새 대화로 요청합니다. 원문은 [실행 기록](model-runs/readme-2026-10-01.json)의 `input`을 사용합니다. 전체 요청의 SHA-256도 같은 기록에 있습니다.

```text
아래는 korean-humanizer 스킬 지침과 참조 카탈로그입니다. 이를 적용해 마지막 사용자 요청을 처리하세요. 파일·도구·다른 스킬은 사용하지 마세요. 아래 지침에 따라 교정한 본문만 응답하세요.

<skill>
[SKILL.md 전체 본문]
</skill>

<catalog>
[references/ko-ai-signals.md 전체 본문]
</catalog>

<request>
이거 AI 티 빼줘. 도메인=[해당 도메인]:
[해당 원문]
</request>
```

공통 요청을 `prompt.txt`로 저장한 경우 사용한 CLI 옵션은 다음과 같습니다. 이미 로그인된 CLI를 사용했고, 모델 자동 대체 옵션은 지정하지 않았습니다.

```bash
claude --print --model claude-opus-5-5 --effort medium --safe-mode \
  --no-session-persistence --strict-mcp-config \
  --mcp-config '{"mcpServers":{}}' --tools "" --output-format json < prompt.txt

codex exec --model gpt-6-astra -c 'model_reasoning_effort="medium"' \
  --ignore-user-config --ephemeral --sandbox read-only \
  --skip-git-repo-check --json --output-last-message output.txt - < prompt.txt
```

실행은 저장소 밖의 임시 디렉토리에서 수행했습니다. Claude는 JSON의 `result`, Codex는 마지막 응답 파일을 보존했습니다. 세션 ID·개인 설정·전체 CLI 로그는 저장소 기록에 넣지 않았습니다.

## 해석의 한계

- 각 입력을 한 번만 실행함. 재실행에서 다른 표현을 선택할 수 있음
- 기본 에이전트 지침과 처리 경로가 다름. 모델 자체의 능력 차이만 분리한 실험은 아님
- 설치·스킬 자동 발견·참조 파일 로딩 검증은 아님. 지침과 카탈로그를 직접 전달한 실행
- 짧은 예시 3개이며, 숫자·날짜·링크·인용 보존을 평가할 입력은 포함하지 않음
- 자연스러움은 사람의 선호에 따라 다름. 이 결과로 성공률·우열·품질 향상률을 주장하지 않음

고정 fixture 회귀 검사는 [평가 안내](README.md)에 있습니다. 이번 실제 모델 실행과 별도로 관리하며, 기존 fixture 수와 scorecard에 합산하지 않습니다.
