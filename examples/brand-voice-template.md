---
name: my-brand
domain_default: blog
ending_default: ~다
emoji_policy: sparse
length_bias: concise
preserve:
  - "딥다이브"
  - "프로덕트 마켓 핏"
ban:
  - "활용"
  - "혁신적인"
prefer:
  - "사용 → 쓰기"
  - "유용하다 → 쓸만하다"
---

# Brand Voice 템플릿

> 자기 브랜드 / 개인 톤을 humanizer 의 **4 번째 mode** 로 등록하기 위한 템플릿. SKILL.md / PROMPT.md "방식 D" 의 입력값.
>
> **이 파일을 통째로 복사해 새 이름으로 저장한 뒤** frontmatter 와 본문 톤 가이드를 채운다. humanizer 는 frontmatter 와 본문을 모두 읽고 기본 카탈로그보다 *먼저* 적용한다.

---

## 적용 순서 (중요)

humanizer 는 다음 순서로 brand voice 를 우선 반영한다 — 같은 단어가 여러 룰에 걸리면 윗줄이 이긴다.

1. **Brand voice profile** (이 파일) — 개인 / 팀 / 회사 톤
2. **Personal list** (Mode A 인라인 / B 자연어 / C 파일) — 그때그때 즉석 입력
3. **12 카테고리 카탈로그** — `references/ko-ai-signals.md` 의 도메인-가중치 매트릭스

같은 brand voice 안에서는 `preserve` > `ban` > `prefer` 순. (보존이 가장 강한 신호. 금지가 그 다음. 매핑은 마지막.)

---

## frontmatter 필드

| 필드 | 필수 | 값 | 설명 |
|---|---|---|---|
| `name` | ✓ | string | brand voice 식별자. CLI / 로그용. |
| `domain_default` | ✓ | 12 도메인 코드 중 1 | raw 가 도메인 명시 안 했을 때 가정값. 예: `blog` / `email` / `marketing`. |
| `ending_default` | ✓ | `~합니다` / `~해요` / `~다` / `반말` / `auto` | 종결어미 디폴트. `auto` 는 도메인 디폴트 따름. |
| `emoji_policy` | 선택 | `none` / `sparse` / `liberal` | 이모지 허용량. `sparse` = 글당 0-1 개. |
| `length_bias` | 선택 | `concise` / `neutral` / `verbose` | 같은 의미 두 표현 중 어느 쪽을 선호? |
| `preserve` | 선택 | string list | **자동 치환에서 제외할 단어**. brand 핵심 단어 / 의도된 격식어. |
| `ban` | 선택 | string list | **반드시 빼는 단어**. brand 가 안 쓰는 표현. |
| `prefer` | 선택 | `"A → B"` 형식 list | A 가 보이면 B 로 매핑. 양방향 아님 (A → B 만). |

**최소 작동 조건**: `name` + `domain_default` + `ending_default` 만 있어도 동작. `preserve` / `ban` / `prefer` 는 비워도 됨.

---

## Tone guide (자유 기술)

frontmatter 로 못 잡는 톤 디테일은 본문에 자유 형식으로 적는다. humanizer 가 읽고 휴리스틱으로 반영.

작성 가이드:

- 한 줄 / 한 항목당 한 가지 룰만
- "이렇게 써라" 보다 **"이렇게는 쓰지 마라"** 가 더 잘 통함
- 예시 1-2 개 포함 권장 (긍정·부정 각각)

### 예시 항목

- 1 문장 8-15 자 권장. 길어지면 자르지 말고 끊어 쓴다.
- 강조는 단어가 아니라 문장 길이로. (× "정말 빠릅니다", ○ "빠릅니다.")
- 인사·마무리 말은 의도된 자리에만. 자동 부착 금지.
- 1 인칭은 "나" / "저" 중 도메인에 맞춰 1 개로 고정.
- 부정 표현은 직설로 — "어렵다" 를 "쉽지 않다" 로 빼지 않는다.
- 영어 차용어는 **있는 그대로** 보존 (한글 대체어 강제 금지).

---

## 사용법

### 환경별 등록

| 환경 | 방법 |
|---|---|
| Claude Code / OpenCode / Codex | `examples/brand-voice-<name>.md` 로 저장 후 humanizer 호출 시 "이 brand voice 로 다듬어줘: [path]" 명시 |
| Claude.ai (Cowork) | 대화 시작 시 이 파일 본문을 첨부 / 붙여넣기 |
| ChatGPT / Cursor / Gemini | `PROMPT.md` 시스템 프롬프트 뒤에 이 frontmatter + 본문을 그대로 이어붙이기 |

### 호환성

- **Personal list 와 공존**: brand voice 의 `preserve` / `ban` / `prefer` 가 personal list 와 충돌하면 brand voice 가 이긴다 (개인 > 즉석).
- **Personal list 가 brand voice 를 덮어쓰는 경우**: 같은 세션 메시지에 `금지=...` 인라인이 보이면 그 단어에 한해 personal list 가 우선 (즉석 의도 반영).
- **다중 brand voice**: 한 세션에 동시 활성화는 1 개만. 두 개 필요하면 별도 세션.

### 검증

- humanize 결과의 출력 마지막에 `brand: <name>` 한 줄이 보이면 정상 적용.
- `preserve` 단어가 humanized 에 사라지면 fail — humanizer 가 알림 후 보정.
- `ban` 단어가 humanized 에 남아있으면 fail — humanizer 가 알림 후 재시도.

---

## 전체 예시 (가상 SaaS 팀)

```markdown
---
name: acme-saas
domain_default: blog
ending_default: ~합니다
emoji_policy: none
length_bias: concise
preserve:
  - "온보딩"
  - "리텐션"
  - "멀티테넌트"
ban:
  - "활용"
  - "혁신적인"
  - "솔루션"
  - "극대화"
prefer:
  - "고객 → 사용자"
  - "이용 → 쓰기"
  - "구축 → 만들기"
---

## Tone guide

- 모든 글은 ~합니다체. 친근 표현은 단어 선택으로만.
- 1 문단 3-5 줄 권장.
- 한 글에 같은 명사 3 회 반복 금지 — 두 번째부터 대명사 / 생략.
- 이모지 / 이모티콘 어떤 자리든 금지.
- 마무리 인사 (`~ 바랍니다 / 감사합니다`) 자동 부착 금지.
- 비교 시 "~보다 더" 대신 "더" 단독 사용.
```

---

## 케이스 스터디

본 템플릿을 채워본 두 가상 케이스:

- [`brand-voice-toss-style.md`](brand-voice-toss-style.md) — 짧고 직설, 친근 격식 최소화 (가상 핀테크)
- [`brand-voice-essayist.md`](brand-voice-essayist.md) — 길고 사변, 1 인칭, 비유 (가상 에세이스트)

두 케이스의 brand voice frontmatter 가 어떻게 다른지 비교하면 자기 톤 정의가 빠르다.

---

## 관련 문서

- [SKILL.md "방식 D"](../SKILL.md) — Brand voice 적용 워크플로우
- [PROMPT.md "형식 D"](../PROMPT.md) — 시스템 프롬프트 등록 방법
- [`examples/personal-list.md`](personal-list.md) — Mode A/B/C 즉석 / 영구 입력
- [`references/ko-ai-signals.md` 부록 E·F](../references/ko-ai-signals.md) — 도메인 코드 표준
