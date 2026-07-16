# Beta 사용 가이드

> **체크인된 안내 템플릿**: 이 문서는 베타 사용자를 위한 설치·사용·피드백 안내 초안입니다. 배포, 베타 참여, Google Form 운영, v1.0 출시를 증명하지 않습니다.

---

## 한 줄 요약

평소 쓰시던 환경 (Claude Code / Claude.ai / ChatGPT / Cursor / Gemini) 에 humanizer 깔고, 한국어 글 다듬을 때 호출하고, 끝나고 30 초 폼 1 회.

---

## 1. 설치 (3 분)

평소 쓰시는 환경 1 개만 선택해 깔면 됩니다.

### Claude Code 사용자 (가장 빠름)

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/dotoricode/korean-humanizer.git ~/.claude/skills/korean-humanizer
```

### Claude.ai (Cowork) 사용자

1. [SKILL.md](https://github.com/dotoricode/korean-humanizer/blob/main/SKILL.md) + [references/ko-ai-signals.md](https://github.com/dotoricode/korean-humanizer/blob/main/references/ko-ai-signals.md) 다운로드
2. Cowork 프로젝트 또는 대화에 업로드

### ChatGPT / Cursor / Gemini 사용자

1. [PROMPT.md](https://github.com/dotoricode/korean-humanizer/blob/main/PROMPT.md) 전체 복사
2. 시스템 프롬프트 (또는 Cursor Rule) 에 붙여넣기

상세 가이드: [README — Installation](https://github.com/dotoricode/korean-humanizer#installation).

---

## 2. 사용 흐름 (매번 30 초)

### 기본 호출

**Claude Code / OpenCode / Codex**:

```
/korean-humanizer

[다듬을 한국어 텍스트]
```

또는 자연어:

```
이거 AI 티 빼줘:
[텍스트]
```

**ChatGPT / Cursor / Gemini**: 시스템 프롬프트 깔린 대화에서 그냥 한국어 텍스트만 입력.

### 받는 결과

```
## Humanized

[다듬어진 텍스트]

## 주요 변경 (최대 5개)
- "X" → "Y" (이유: ...)
- ...
```

5 개 초과면 마지막 줄에 `+N개 더` 안내. "전체 diff 로 보여줘" 하면 모두 표시.

### 만족 / 불만족 응답

만족 → 그대로 사용. 불만족 → "이 변경은 되돌려줘" / "이 부분만 다시 다듬어줘" 같이 자연어로 말하면 됩니다.

---

## 3. 권장 사용 패턴

### 자기 톤 캘리브레이션 (선택)

Humanizer 디폴트는 일반 한국어 LLM 톤 기준. 자기 스타일과 어긋나면 **Personal list** 또는 **Brand voice** 로 우선 룰을 깔아두세요.

#### 가벼운 캘리브레이션 — Personal list 인라인 (Mode A)

```
/korean-humanizer 금지=활용,매우,다양한; 선호=유용하다→쓸만하다; 유지=결과적으로

[텍스트]
```

#### 강한 캘리브레이션 — Brand voice (Mode D)

자기 톤이 일반보다 뚜렷하면 brand voice 프로필 만들기:

```bash
cp examples/brand-voice-template.md ~/.claude/skills/korean-humanizer/examples/brand-voice-mine.md
```

frontmatter 채운 뒤 호출:

```
/korean-humanizer brand=examples/brand-voice-mine.md

[텍스트]
```

자세한 예시: [`examples/brand-voice-toss-style.md`](https://github.com/dotoricode/korean-humanizer/blob/main/examples/brand-voice-toss-style.md), [`examples/brand-voice-essayist.md`](https://github.com/dotoricode/korean-humanizer/blob/main/examples/brand-voice-essayist.md).

---

## 4. 일정

| Week | 활동 |
|---|---|
| **1** | 설치 + 첫 humanize 1-2 회. 어색한 부분 발견하면 폼에 짧게. |
| **2** | 평소 글쓰기 흐름에 **자연스럽게 끼워넣기**. 일부러 humanize 만 하려고 글을 쓰지 마세요. |
| **3** (있을 시) | 마지막 1 주 — 비교적 길게 쓰는 글 (블로그 / 뉴스레터 / 학술) 1-2 개에 적용. wrap-up 폼. |

---

## 5. 피드백 폼

매 humanize 후 30 초:

🔗 **[피드백 폼 링크]** — 외부/수동 작업. 베타 운영이 시작되고 Google Form이 생성된 뒤에만 메인테이너가 안내.

질문 (5-7 개):

1. 도메인 (블로그 / 마케팅 / 이메일 / LinkedIn / 뉴스레터 / 학술 / 뉴스 / 채팅 / 리뷰 / B2B 메시지 / 기타)
2. 사용한 mode (None / Personal list A / B / C / Brand voice D)
3. humanize 결과 만족도 (1-5)
4. 의미 보존 정도 (1-5)
5. 톤 일치 정도 (1-5)
6. 부족한 부분 (자유 응답, 선택)
7. 좋았던 부분 (자유 응답, 선택)

**시간 측정**: 첫 1 회만 폼 작성 시간 4-5 분, 두 번째부터 30 초. 짧게 부탁드려요.

---

## 6. FAQ

### Q. 평소 쓰던 도메인이 12 도메인 안에 없어요. 사용해도 되나요?

A. 네! 12 도메인은 examples 가 있는 영역이고, humanizer 자체는 한국어 일반에 적용. 폼 응답 시 "기타" + 도메인 한 단어 (게임 / 부동산 / 정부 등) 적어주시면 도움 큽니다.

### Q. 결과가 너무 가벼워요 / 너무 강해요.

A. 두 케이스:
- **너무 가벼움**: "좀 더 강하게 다듬어줘" 또는 "단락 단위로 다시 봐줘" — 단락당 3 곳 룰을 좀 더 헐겁게.
- **너무 강함**: "보수적으로 다듬어줘" / "꼭 필요한 곳만" — 단락당 1-2 곳, 전체 10 % 수준.

### Q. 의미가 바뀐 것 같은데 어떻게 해요?

A. **그 문장을 폼에 적어주세요.** 의미 불변은 humanizer 의 핵심 약속. 패턴이 의미를 바꾸도록 동작했다면 hot-fix 대상입니다.

### Q. YouTube 인트로인데 ~다체로 바뀌어요.

A. 입력 앞에 **"이거 유튜브 인트로 스크립트야"** 한 줄 명시하면 ~합니다체 / ~해요체 strict 보존. 카탈로그 #9-A 룰. 명시 없으면 humanizer 가 도메인 추정 — 추정 실패 케이스도 폼에 적어주시면 가이드 보강에 도움 큽니다.

### Q. brand voice 만들기가 부담스러워요.

A. **Personal list (Mode A) 인라인 한 줄로 충분**합니다. Brand voice 는 매번 같은 톤으로 다듬는 사람용. 처음엔 Mode A 부터 쓰시고, "매번 같은 단어 빼고 같은 매핑" 패턴 보이면 그때 brand voice 만드세요.

### Q. 베타 기간이 끝나면 어떻게 되나요?

A. 그대로 계속 사용. v1.0 release 후에도 minor / patch 자동 적용 (`git pull` / 새 PROMPT.md 갱신). v1.0 부터 freeze 영역 ([`docs/STABILITY-PROMISE.md`](STABILITY-PROMISE.md)) 약속됩니다.

### Q. 폼 응답이 너무 부담돼요.

A. **첫 응답만 5 분, 두 번째부터 30 초** 정도. 1-2 주 동안 5-10 회 응답이면 충분합니다. 폼 디자인이 길다고 느끼시면 폼 자체를 짧게 갱신할게요 — 메인테이너에게 알려주세요.

---

## 7. 도움이 필요하면

- 설치 막힘 / 호출 안 됨 → X DM (`@dotoricode`) 또는 GitHub Issue `[beta]` prefix
- 결과 이상함 → 폼에 "부족한 부분" 자유 응답 + 가능하면 raw / humanized 텍스트 일부 (PII 마스킹 후)
- 그 외 → GitHub Issue 자유 형식

---

## 8. 감사

베타 참여해주셔서 감사합니다. 1-2 주 동안의 사용량은 v1.0 안정화 약속의 데이터 베이스가 됩니다. 동의해주시면 release notes 또는 README contributor 섹션에 이름 (또는 GitHub username / 닉네임) 표기 — 폼에 동의 옵션이 있어요.

— `@dotoricode`
