# korean-humanizer

한국어 AI 글의 어색한 격식·번역체·반복을 줄이는 무료 스킬입니다. 원문의 정보·조건·말투를 유지하며 문장을 다듬습니다. 이 패키지는 다음 릴리스를 위한 개선을 포함하며, 마지막 정식 릴리스는 v1.0.1입니다.

## 설치와 첫 실행

공개 GitHub 버전을 전용 설치 명령으로 받으려면 사용할 프로젝트에서 아래 명령을 실행합니다. [Skills CLI](https://github.com/vercel-labs/skills)를 사용하며 설치할 때 Node.js/npm이 필요합니다. 스킬 실행 자체에는 Node.js가 필요하지 않습니다.

```bash
npx skills add dotoricode/korean-humanizer --skill korean-humanizer --agent codex claude-code --copy
```

이 명령은 공개 기본 브랜치를 설치합니다. Agensi에서 내려받은 이 ZIP과 버전이 다를 수 있습니다. 하나만 설치하려면 `--agent codex` 또는 `--agent claude-code`로 바꾸고, 모든 프로젝트에서 쓰려면 `--global`을 추가합니다.

내려받은 ZIP의 버전을 사용하려면 ZIP의 파일을 아래 디렉토리에 압축 해제합니다. 기존 설치가 있으면 먼저 별도 폴더에 보관하세요. `SKILL.md`가 해당 디렉토리에 바로 있어야 합니다.

| 환경 | 프로젝트 설치 경로 | 호출 |
|---|---|---|
| Codex | `.agents/skills/korean-humanizer/` | `$korean-humanizer` |
| Claude Code | `.claude/skills/korean-humanizer/` | `/korean-humanizer` |

프로젝트 밖에서 ZIP을 풀었다면 `korean-humanizer` 디렉토리 전체를 위 경로로 옮깁니다. 파일 하나만 옮기면 참조 파일을 읽을 수 없습니다. 설치한 프로젝트에서 새 대화를 시작해 아래처럼 요청하세요.

```text
$korean-humanizer 이거 AI 티 빼줘. 도메인=email:
안녕하세요. 다름이 아니오라 미팅 일정과 관련하여 말씀드리고자 연락드립니다. 부득이한 사정으로 인해 일정 변경이 불가피한 상황이 발생하여 양해를 구하고자 합니다.
```

Claude Code에서는 첫 줄의 `$korean-humanizer`를 `/korean-humanizer`로 바꿉니다. 기본 응답은 `Humanized` 본문과 최대 5개의 주요 변경 설명입니다. 설치 없이 사용하려면 `PROMPT.short.md`를 모델의 지침이나 첫 메시지에 붙여 넣습니다.

## 내 문체와 금지어

`examples/personal-list.md` 또는 `examples/brand-voice-template.md`를 복사해 수정하고 `personal=파일경로` 또는 `brand=파일경로`로 지정합니다. 설정은 선택 사항이며 지정하지 않은 예시는 자동 적용하지 않습니다. 스킬 루트 기준 상대 경로나 절대 경로를 사용합니다.

## 포함 파일과 동작

실행 지침·표현 카탈로그·선택 설정·예시·프롬프트·MIT 라이선스를 포함합니다. 개발 설정·설치 스크립트·평가 도구는 포함하지 않습니다. 포함된 파일은 텍스트뿐이며 별도 의존성이나 API 키가 필요하지 않습니다. 모델을 제공하는 앱이나 서비스는 별도로 필요합니다.

지침과 예시의 내부 참조는 패키지 안에 있으며, 평가 기록·연구·과거 자료 링크는 공개 GitHub 문서로 이어집니다. 선택한 모델과 서비스가 입력 텍스트를 처리합니다.

## 사용 범위와 한계

이메일·SNS·블로그·제품 소개·GitHub 답변 등 외부 한국어 글을 다듬습니다. 영어, 단순 오탈자 교정, 법률 문서와 내부 기술 문서에는 적용하지 않습니다. 편집 지침이므로 모든 실행에서 동일한 결과나 완전한 정보 보존을 보장하지 않습니다. 중요한 날짜·금액·조건은 결과에서 확인하세요.

## 소스와 라이선스

MIT 라이선스이며 `LICENSE`의 저작권 고지와 조건을 유지합니다. 무료 배포입니다.

업데이트·전체 실행 기록·Issue·PR은 [GitHub 저장소](https://github.com/dotoricode/korean-humanizer)에서 확인할 수 있습니다. 도움이 됐다면 Star로 알려주세요. Star는 사용 조건이 아닙니다.
