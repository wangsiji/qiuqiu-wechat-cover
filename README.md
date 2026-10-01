<p align="center">
  <img src="examples/cover-japan-12days.png" alt="示例封面" width="820"/>
</p>
<h1 align="center">qiuqiu-wechat-cover</h1>

<p align="center">
  <b>把一篇公众号文章，变成一张统一 2.35:1 品牌封面</b> 的 Agent Skill<br/>
  读正文 → 提炼钩子 → 确认文案 → 内置 Lovart 后端出图
</p>

<p align="center">
  <a href="LICENSE"><img alt="MIT" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <a href=".github/workflows/validate.yml"><img alt="CI" src="https://img.shields.io/badge/CI-validate_skill-brightgreen"></a>
  <a href="https://github.com/wangsiji"><img alt="author" src="https://img.shields.io/badge/author-wangsiji-ff69b4"></a>
</p>

---

## 为什么会有它

做公众号的人都知道：封面是「点击率」的第一张入场券。但**统一**才是最难的事——手动做，风格一个月飘三次；让 AI 生图，又常常编造人物、品牌、旅行照，脸一次一个样。

这个 Skill 把一条「可复现的品牌封面流水线」压缩成一个文件夹：自带真人身份图 + 品牌风格图，从真实文章里提钩子，先确认文案再出图，出图再用内置 Lovart 后端免费跑通。**你只负责提供文章和素材，其余交给它。**

> 💡 这套「读正文 → 提钩子 → 确认 → 出图 → 验收」的流程，也是公众号封面统一性的方法论，可复制到任何单人 / 小团队账号。

## 案例墙

| 案例 | 说明 |
|---|---|
| ![案例1](examples/cover-case-01.jpg) | 「秋秋很开心」在产封面 |
| ![案例2](examples/cover-case-02.jpg) | 「秋秋很开心」在产封面 |
| ![日本12天](examples/cover-japan-12days.png) | 日本 12 天攻略 · 2.35:1 · 1888×800 |

### 近 3 个月在产文章（真实链接）

- 2026-09-22 [我的 100 件长期好物：头发护理神器来啦！](https://mp.weixin.qq.com/s/oQ3wi4pJ14ug6QoDsDDDEw)
- 2026-09-21 [我的 100 件长期好物：随身配饰来啦！](https://mp.weixin.qq.com/s/ncwJ6NXK-meRE3FOLlWqfg)
- 2026-09-11 [懒人要避开的思维方式！](https://mp.weixin.qq.com/s/RCbIz2iI9KNyF63zfRaiaw)
- 2026-09-09 [日常好用，分享 7 款超可爱的收纳小包！](https://mp.weixin.qq.com/s/7k8O-D1U2RUZLmlN4nw9Xg)
- 2026-09-06 [照片 Skill｜拯救旅行废片，试试这 6 种风格！！！](https://mp.weixin.qq.com/s/Elf3PrEmMURfTOr2zNohuA)
- 2026-09-04 [不到 50 块，就能打造高颜值书桌！](https://mp.weixin.qq.com/s/ul-JXY4gMjH15E1IrPqiig)
- 2026-09-01 [本子大集合](https://mp.weixin.qq.com/s/Rfnugp22ysYqD8c9PjkRZw)

## 它怎么工作

三个不可跳过的心流：

1. **读** — 从真实正文提炼主题、点击理由、一个核心数字 / 冲突、必须真实呈现的对象。
2. **确认** — 先给 3 个钩子 + 1 个构图建议，你确认文案后才出图。**文案未确认，绝不出图。**
3. **出图** — 内置身份图 + 风格图注入 Lovart 后端（纯 Python 标准库），产品 / 品牌 / 旅行照原样使用。

> 🛡️ **真实优先**：产品、Logo、旅行照一律原样用，绝不凭空编造。没有真人图就不虚构人物；没有 Logo 图就文字名牌。默认保留口罩，不换脸、不美颜、不像素化。

## 快速开始

```bash
# 1. 克隆
git clone https://github.com/wangsiji/qiuqiu-wechat-cover
cd qiuqiu-wechat-cover

# 2. 挂到 Agent Skill 目录（以 Hermes 为例）
cp -r . ~/.hermes/skills/qiuqiu-wechat-cover

# 3. 配置出图后端密钥（Lovart）
export LOVART_ACCESS_KEY="ak_..."   # 你的密钥，别提交
export LOVART_SECRET_KEY="sk_..."

# 4. 校验内置资产与结构
python3 tools/resolve_assets.py  # → ok:true + 两个 absolute_path
python3 tools/validate_skill.py .

# 5. 交给智能体
#    → 「对这篇公众号文章生成封面：/path/to/article.md」
```

出图默认走 Lovart **免费队列**（`set-mode --unlimited`，排队换额度），完整细节见 [references/lovart-channel.md](references/lovart-channel.md)。

## 完整案例

见 [examples/ai-agent-cover.md](examples/ai-agent-cover.md)：一篇《办公 AI 三国杀》从**读文章 → 提钩子 → 定文案 → 构图 → 出图**的完整流程（含可直接粘贴的提示词）。新手照着走即可复现「统一却不死板」的封面。

## Skill 结构

```
qiuqiu-wechat-cover/
├── SKILL.md              入口规则与硬约束（品牌、流程、验收）
├── agents/openai.yaml    UI 展示与默认提示
├── references/
│   ├── workflow.md       阶段协议与处理边界
│   ├── cover-brief.md    结构化 Brief（文章 → 提示词的中枢）⭐
│   ├── identity-contract.md  身份层不可变 + Asset Fidelity 分级
│   ├── copy-contract.md  Copy Lock：文案白名单（allowed_text）
│   ├── layout-system.md  构图编号模板 L01–L05（category → template）
│   ├── style-guide.md    2.35:1 视觉系统（暖木×复古像素×真实）
│   ├── prompt-template.md   Brief → 提示词的编译器骨架
│   ├── prompt-checklist.md 生成前后验收清单 + 失败分类 F01–F10
│   ├── lovart-channel.md 出图后端操作细节
│   └── assets/           内置 Image 1（身份）+ Image 2（风格）
├── tools/
│   ├── resolve_assets.py 校验 / 暴露内置资产
│   ├── validate_skill.py 本地 & CI 完整性校验
│   └── lovart-agent.py   Lovart 出图后端（纯标准库，MIT）
└── examples/            在产示例（封面图 + 完整案例）
```

## 约束（品牌基线）

- 画布严格 **2.35:1**（优先 1880×800）。
- 视觉 = 暖木 × 复古像素 × 温馨工作台 × 真实主体（明亮温暖，避免暗色科技风）。
- 文案至多 3 组、全页 20~35 汉字，**主标题是唯一视觉焦点**。
- 保留口罩；真实感 ~80% + 像素 20%；不换脸、不美颜、不彻底像素化、不戴卡通。
- 真人身份、风格**禁止外部检索**；缺真人照不虚构人物。身份图已被锁定为一种确认过的人物脸（保证跨文章统一）——通常不换。

## 校验 & CI

每次提交由 GitHub Actions 跑 `tools/validate_skill.py`，检查必需文件、相对链接、资产文件头、Lovart 后端存在且纯标准库：

```bash
python3 tools/validate_skill.py .
```

⚠️ 校验只检查**结构**，不替代出图后的视觉验收：中文逐字、人物轮廓、实际出图请人工核对。

## 许可

[MIT](LICENSE)。内置 `tools/lovart-agent.py` 取自 [lovartai/lovart-skill](https://github.com/lovartai/lovart-skill)（MIT），归属声明见 [NOTICE](NOTICE)。