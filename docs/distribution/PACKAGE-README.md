# korean-humanizer

한국어 AI 글의 어색한 격식·번역체·반복을 줄이는 무료 스킬입니다. 원문의 정보·조건·말투를 유지하며 문장을 다듬습니다. Agensi에서는 파일을 내려받지 않고 Agensi MCP로 연결한 에이전트가 사용할 때마다 최신 버전을 불러옵니다.

## Agensi MCP 연결과 첫 실행

에이전트를 Agensi MCP 서버 `https://mcp.agensi.io/mcp`에 한 번 연결합니다. 스킬 파일은 컴퓨터에 저장되지 않습니다.

| 환경 | 연결 방법 |
|---|---|
| Claude Code | `claude mcp add --transport http agensi https://mcp.agensi.io/mcp` |
| Codex CLI | `codex mcp add agensi --url https://mcp.agensi.io/mcp` |
| 그 밖의 환경 | [Agensi 연결 안내](https://www.agensi.io/docs/mcp-setup) |

연결한 에이전트에게 아래처럼 요청합니다. 에이전트가 Agensi에서 `korean-humanizer`를 불러와 바로 교정합니다. Agensi 로그인을 요청하면 안내에 따라 승인합니다.

```text
korean-humanizer 스킬로 이거 AI 티 빼줘. 도메인=email:
안녕하세요. 다름이 아니오라 미팅 일정과 관련하여 말씀드리고자 연락드립니다. 부득이한 사정으로 인해 일정 변경이 불가피한 상황이 발생하여 양해를 구하고자 합니다.
```

기본 응답은 `Humanized` 본문과 최대 5개의 주요 변경 설명입니다.

## 내 문체와 금지어

가장 간단한 방법은 요청 첫 줄에 `금지=활용,매우; 선호=유용하다→쓸만하다`처럼 적는 것입니다. 파일로 관리하려면 내 컴퓨터에 설정 파일을 만들고 `personal=/절대/경로.md` 또는 `brand=/절대/경로.md`로 지정합니다. MCP로 불러온 스킬에는 스킬 폴더가 없으므로 상대 경로는 함께 전달된 예시 파일(`brand=examples/brand-voice-toss-style.md` 등)에만 씁니다. 설정 파일의 틀은 [GitHub의 examples 폴더](https://github.com/dotoricode/korean-humanizer/tree/main/examples)에서 복사합니다.

## 직접 설치

스킬 폴더에 설치하려면 [Skills CLI](https://github.com/vercel-labs/skills)로 공개 GitHub 버전을 받습니다. 설치할 때 Node.js/npm이 필요하며, Agensi에서 불러오는 버전과 다를 수 있습니다.

```bash
npx skills add dotoricode/korean-humanizer --skill korean-humanizer --agent codex claude-code --copy
```

Codex에서는 `$korean-humanizer`, Claude Code에서는 `/korean-humanizer`로 호출합니다. 스킬을 쓸 수 없는 환경에서는 [GitHub의 `PROMPT.short.md`](https://github.com/dotoricode/korean-humanizer/blob/main/PROMPT.short.md)를 모델의 지침이나 첫 메시지에 붙여 넣습니다.

## 포함 파일과 동작

실행 지침·표현 카탈로그·선택 설정 예시·MIT 라이선스를 포함합니다. 일반 LLM용 프롬프트·개발 설정·평가 도구는 GitHub에만 있습니다. 포함된 파일은 텍스트뿐이며 별도 의존성이나 API 키가 필요하지 않습니다. 평가 기록·연구·과거 자료 링크는 공개 GitHub 문서로 이어집니다. 선택한 모델과 서비스가 입력 텍스트를 처리합니다.

## 사용 범위와 한계

이메일·SNS·블로그·제품 소개·GitHub 답변 등 외부 한국어 글을 다듬습니다. 영어, 단순 오탈자 교정, 법률 문서와 내부 기술 문서에는 적용하지 않습니다. 편집 지침이므로 모든 실행에서 동일한 결과나 완전한 정보 보존을 보장하지 않습니다. 중요한 날짜·금액·조건은 결과에서 확인하세요.

## 소스와 라이선스

MIT 라이선스이며 `LICENSE`의 저작권 고지와 조건을 유지합니다. 무료 배포입니다. Agensi MCP 응답에는 Agensi의 이용 고지가 붙지만, 이 스킬의 원문은 GitHub에 공개되어 있습니다.

업데이트·전체 실행 기록·Issue·PR은 [GitHub 저장소](https://github.com/dotoricode/korean-humanizer)에서 확인할 수 있습니다. 도움이 됐다면 Star로 알려주세요. Star는 사용 조건이 아닙니다.
