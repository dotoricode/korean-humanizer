# korean-humanizer

> A skill and prompt for editing awkward Korean AI prose while preserving meaning.

[한국어](README.ko.md) · [中文](README.zh-CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Next release](https://img.shields.io/badge/next-2.0_unreleased-orange.svg)](docs/MIGRATION-1.x-to-2.x.md)
[![Patterns](https://img.shields.io/badge/patterns-137%2B-brightgreen.svg)](references/ko-ai-signals.md)
[![Domains](https://img.shields.io/badge/domains-12-brightgreen.svg)](references/ko-ai-signals.md#부록-e-도메인별-카테고리-우선-적용)

The last released version is **v1.0.1**. This document describes **unreleased 2.0 preparation**. See the [1.x compatibility promise](docs/STABILITY-PROMISE.md) and [migration draft](docs/MIGRATION-1.x-to-2.x.md).

The catalog provides context-dependent editing candidates, not words to replace in every sentence. Preserve facts, tone, uncertainty and conditions; leave already natural text unchanged.

---

Conservative, manually edited examples; these are not recorded model runs.

```diff
# LinkedIn
- 이번 프로젝트를 통해 다양한 기술적 도전을 경험하고 성장할 수 있었습니다. 이러한 경험은 앞으로의 커리어에 있어서 매우 소중한 자산이 될 것이라 확신합니다. 🚀
+ 이번 프로젝트에서 여러 기술적 도전을 경험하고 성장할 수 있었습니다. 이러한 경험은 앞으로의 커리어에 있어서 매우 소중한 자산이 될 것이라 확신합니다. 🚀

# Email
- 안녕하세요. 다름이 아니오라 미팅 일정과 관련하여 말씀드리고자 연락드립니다. 부득이한 사정으로 인해 일정 변경이 불가피한 상황이 발생하여 양해를 구하고자 합니다.
+ 안녕하세요. 미팅 일정과 관련하여 말씀드리고자 연락드립니다. 부득이한 사정으로 인해 일정 변경이 불가피한 상황이 발생하여 양해를 구하고자 합니다.

# Marketing
- 🚀 혁신적인 솔루션을 활용하여 다양한 비즈니스 가치를 극대화하고, 이러한 접근을 통해 사용자 경험을 한층 더 고도화할 수 있습니다. ✨
+ 🚀 새로운 솔루션을 사용하여 다양한 비즈니스 가치를 극대화하고, 이러한 접근을 통해 사용자 경험을 한층 더 고도화할 수 있습니다. ✨
```

[More manual examples](examples/before-after.md) · [Small recorded execution checks](docs/reviews/2026-10-01-qa.md#새-문맥-실행-검사)

---

## Install

### Codex

```bash
git clone https://github.com/dotoricode/korean-humanizer.git
cd korean-humanizer
bash scripts/install-codex-skill.sh
bash scripts/check-codex-skill.sh
```

### Claude Code

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/dotoricode/korean-humanizer.git ~/.claude/skills/korean-humanizer
```

These commands install the default branch. Candidate changes are in [PR #5](https://github.com/dotoricode/korean-humanizer/pull/5); use `git checkout v1.0.1` in the clone to pin the released version. Codex installation and small execution checks were verified; a fresh Claude Code installation through first use was not.

Then ask naturally — `이거 AI 티 빼줘:` followed by your Korean text.

**Other LLMs:** paste [`PROMPT.short.md`](PROMPT.short.md) as a system prompt, or use the full [`PROMPT.md`](PROMPT.md).

---

## Editing rules

- Preserve facts, numbers, names, links, quotations, conditions and sentence endings.
- Edit at most `max(1, floor(sentence count × 0.20))` sentences and 3 places per paragraph.
- Keep at least 90% of the original length unless shortening is requested.
- Return the edited body by default; explain changes when asked.

These are instructions, not a guarantee of model compliance. Fixed-fixture checks are regression checks, not a model quality success rate. See the [evaluation guide](eval/README.md).

[Pattern catalog](references/ko-ai-signals.md) · [Quick reference](CHEATSHEET.md) · [Documentation index](docs/README.md)

---

## Customization

Ban words, set preferences, or define a brand voice — subject to meaning and tone preservation:

```text
이거 AI 티 빼줘. 금지=활용,매우; 선호=유용하다→쓸만하다:
[Korean text]
```

Load your personal file with `personal=path`; the supplied example list is not loaded automatically. For a persistent tone profile, see [`examples/brand-voice-template.md`](examples/brand-voice-template.md).

---

## Contributing · License · Services

Contributions welcome — [`CONTRIBUTING.md`](CONTRIBUTING.md) · [Pattern addition](.github/ISSUE_TEMPLATE/pattern_addition.md) · [Bug report](.github/ISSUE_TEMPLATE/bug_report.md)

MIT. Use it, fork it, adapt it. If it helps, a GitHub Star is welcome.

Third-party community demo by Socialistic/Tinkerland (not an official service — user input is processed by the external operator):

[![Try writing-dotoricode-korean-humanizer-5d759b on Socialistic][socialistic-demo-badge]][socialistic-demo-link]

[socialistic-demo-badge]: https://socialistic.ai/api/embed/writing-dotoricode-korean-humanizer-5d759b
[socialistic-demo-link]: https://socialistic.ai/en/skill/writing-dotoricode-korean-humanizer-5d759b?utm_source=github&utm_medium=readme&utm_campaign=20260520-writing-koc-creators&utm_content=badge
