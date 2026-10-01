# korean-humanizer

> 面向 Codex 和 Claude Code 的韩语 AI 文本 humanizer。
>
> 它会去掉韩语 AI 生成文本中的“AI 味”，但不改变事实、数字、专有名词、链接或原意。

[English](README.md) · [한국어](README.ko.md)

[![Next release](https://img.shields.io/badge/next-2.0_unreleased-orange.svg)](docs/MIGRATION-1.x-to-2.x.md)

最后发布的版本是 **v1.0.1**。本文说明**尚未发布的 2.0 准备变更**，请参阅 [1.x 兼容承诺](docs/STABILITY-PROMISE.md)和[迁移草案](docs/MIGRATION-1.x-to-2.x.md)。

![korean-humanizer preview](assets/translation-humanizer-card.svg)

## 30 秒试用

把 [`PROMPT.short.md`](PROMPT.short.md) 复制到你的 LLM 或 agent instructions 中，然后输入：

```text
Humanize this Korean text:

🚀 혁신적인 솔루션을 활용하여 다양한 비즈니스 가치를 극대화하고,
이러한 접근을 통해 사용자 경험을 한층 더 고도화할 수 있습니다. ✨
```

手工编辑示例（不是模型运行记录）：

```text
🚀 새로운 솔루션을 사용하여 다양한 비즈니스 가치를 극대화하고,
이러한 접근을 통해 사용자 경험을 한층 더 고도화할 수 있습니다. ✨
```

## 为什么需要韩语专用 humanizer

英语 AI 文本的特征不能直接套用到韩语。韩语有自己的 AI 写作痕迹：

- 翻译腔：`~에 있어서`, `~을 통해`, `~에 의해`
- 过度正式：`~인 것이다`, `~라고 할 수 있습니다`
- 指示词过多：`이러한`, `해당`
- 需要结合语境判断的词语：`활용`, `극대화`, `시사한다`, `도모`, `모색`
- 敬语和句尾语气不一致
- 口语脚本被改成书面 `~다` 风格

`korean-humanizer` 不是英文规则的翻译版，而是围绕韩语本身的写作信号设计的。

## 主要用途

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

上述命令安装默认分支；候选变更见 [PR #5](https://github.com/dotoricode/korean-humanizer/pull/5)。在克隆目录运行 `git checkout v1.0.1` 可固定已发布版本。本次验证了 Codex 安装及少量运行案例，未验证 Claude Code 全新安装到首次使用的完整流程。

然后直接请求：

```text
이거 AI 티 빼줘:
[韩语文本]
```

## 包含内容

- [`SKILL.md`](SKILL.md): skill 入口
- [`PROMPT.md`](PROMPT.md): 完整 system prompt
- [`PROMPT.short.md`](PROMPT.short.md): 快速试用版 prompt
- [`CHEATSHEET.md`](CHEATSHEET.md): 30 个常见韩语 AI 写作痕迹
- [`references/ko-ai-signals.md`](references/ko-ai-signals.md): 12 类 / 100+ 韩语模式目录
- [`eval/scorecard.md`](eval/scorecard.md): 固定输入与输出的回归检查结果，不是模型质量成功率

## 核心规则

- 保留事实、数字、专有名词、引用、链接。
- 保留核心信息、条件和确定程度；可删去重复和装饰表达，不设固定长度比例。
- 必要时可重新组织句子，保持信息和逻辑关系。
- 不重写全文，只修改高置信度 AI 痕迹。
- 不限制修改句数或比例，改善全文中生硬的表达。
- 保留韩语语气和敬语等级。
- YouTube / 播客 / 讲稿等口语文本不能改成书面 `~다` 体。

默认使用与 main 相同的 `Humanized` 和 `주요 변경 (최대 5개)` 两部分，并在首次回复附上修改提示。仅需正文时请明确说明。用 `personal=文件路径` 指定个人配置；示例列表不会自动生效。已自然的表达保持不变。

[文档索引](docs/README.md) · [手工示例](examples/before-after.md) · [评估方法与局限](eval/README.md)

## Services using korean-humanizer

由 Socialistic/Tinkerland 运营的第三方 community demo。这不是本仓库的官方服务。
由于这个 demo 在本仓库之外运行，用户输入的内容会由 Socialistic/Tinkerland 处理。

[![Try writing-dotoricode-korean-humanizer-5d759b on Socialistic][socialistic-demo-badge]][socialistic-demo-link]

## 许可证

MIT。

[socialistic-demo-badge]: https://socialistic.ai/api/embed/writing-dotoricode-korean-humanizer-5d759b
[socialistic-demo-link]: https://socialistic.ai/zh/skill/writing-dotoricode-korean-humanizer-5d759b?utm_source=github&utm_medium=readme&utm_campaign=20260520-writing-koc-creators&utm_content=badge
