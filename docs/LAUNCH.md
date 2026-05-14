# Launch Notes

> v1.0 공개 / 커뮤니티 공유 때 바로 쓸 수 있는 짧은 설명문.

## One-liner

한국어 AI 생성 텍스트에서 번역체, 과한 격식, "활용/극대화/이러한" 같은 AI 티를 걷어내는 한국어 전용 humanizer skill / prompt.

## Short Post — Korean

한국어 AI 글은 영어권 AI 글과 다른 티가 납니다.

`~에 있어서`, `이러한`, `해당`, `활용`, `극대화`, `~라고 할 수 있습니다` 같은 표현이 반복되고, 종결어미나 높임법도 장르와 어긋날 때가 많습니다.

그래서 한국어 전용 humanizer를 만들었습니다.

- 12 카테고리 / 100+ 한국어 AI 티 패턴
- 블로그, 이메일, LinkedIn, YouTube, 뉴스레터, 학술, 뉴스, 채팅, 리뷰, B2B 메시지 등 12 도메인
- Claude Code / OpenCode / Codex skill
- ChatGPT / Cursor / Gemini 에 붙여 넣는 system prompt
- 의미 보존, 20% cap, 문단 3곳 룰, 발화체 ~다체 금지

Repo: https://github.com/dotoricode/korean-humanizer

## Short Post — English

I built `korean-humanizer`, a Korean-specific AI writing humanizer.

English AI-writing tells do not map cleanly to Korean. Korean LLM text has its own patterns: translation-ese, stiff honorifics, overused words like `활용` / `극대화`, excessive `이러한` / `해당`, and register mismatches around sentence endings.

This repo packages:

- 12 categories of Korean AI-writing tells
- 100+ Korean-specific patterns
- 12 writing domains
- a Claude Code / OpenCode / Codex skill
- a portable system prompt for ChatGPT / Cursor / Gemini
- eval fixtures for meaning-preserving, low-touch edits

Repo: https://github.com/dotoricode/korean-humanizer

## README Pitch

If you write Korean with LLMs, this is a practical last-pass editor: paste the generated Korean, keep the meaning, remove the tells.

## Places To Share

- GitHub release
- X / Threads
- LinkedIn
- Korean writing / creator communities
- Cursor / Claude Code / OpenCode communities
- Korean NLP / LLM communities

## Suggested Topics

`ai-detection`, `ai-writing`, `chatgpt`, `claude`, `claude-code`, `claude-skill`, `cursor`, `cursor-rules`, `humanizer`, `korean`, `korean-language`, `korean-nlp`, `korean-writing`, `llm`, `opencode`, `prompt`, `prompt-engineering`, `style-transfer`, `writing-tools`
