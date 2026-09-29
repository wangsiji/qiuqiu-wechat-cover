# qiuqiu-wechat-cover

> 把一篇真实公众号文章，变成一张**统一 2.35:1 横版品牌封面**的 Agent Skill。读正文 → 提炼钩子 → 确认文案 → 内置 Lovart 后端出图，真人形象与视觉风格随包分发，无需任何外部素材。

[![MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![CI](https://img.shields.io/badge/CI-validate_skill-brightgreen)](.github/workflows/validate.yml)

规范名：`$qiuqiu-wechat-cover`

---

## 成品就是最好的说明

| 案例封面 | 说明 |
|---|---|
| ![案例 1](examples/cover-case-01.jpg) | 「秋秋很开心」在产封面 |
| ![案例 2](examples/cover-case-02.jpg) | 「秋秋很开心」在产封面 |
| ![日本 12 天攻略](examples/cover-japan-12days.png) | 日本 12 天攻略（2.35:1 · 1888×800） |

在产文章（真实微信链接，摘自 [qiuqiu-content-engine](https://github.com/wangsiji/qiuqiu-content-engine) 的 `articles_data.json`）：

| 日期 | 文章 |
|---|---|
| 2026-09-22 | [我的 100 件长期好物：头发护理神器来啦！](https://mp.weixin.qq.com/s/oQ3wi4pJ14ug6QoDsDDDEw) |
| 2026-09-21 | [我的 100 件长期好物：随身配饰来啦！](https://mp.weixin.qq.com/s/ncwJ6NXK-9eRE3FOLlWqfg) |
| 2026-09-11 | [懒人要避开的思维方式！](https://mp.weixin.qq.com/s/RCbIz2iI9KNyF63zfRaiaw) |
| 2026-09-09 | [日常好用，分享 7 款超可爱的收纳小包！](https://mp.weixin.qq.com/s/7k8O-D1U2RUZLmlN4nw9Xg) |
| 2026-09-06 | [照片 Skill｜拯救旅行废片，试试这 6 种风格！！！](https://mp.weixin.qq.com/s/Elf3PrEmMURTfOr2zNohuA) |
| 2026-09-04 | [不到 50 块，就能打造高颜值书桌！](https://mp.weixin.qq.com/s/ul-JXY4gMjH15E1IrPqiig) |
| 2026-09-01 | [会无限回购，提高效率的好用本子来啦！](https://mp.weixin.qq.com/s/Rfnugp22ysYqD8c9PjkRZw) |

## 它解决什么

公众号封面难在「统一」：手动做，风格飘、费时间；AI 生图，又常常**编造人物、品牌、旅行照**。这个 Skill 把一条可复现的封面流水线压缩成一个文件夹：

1. **读** 真实文章正文，产出主题判断 + 3 个钩子 + 推荐构图；
2. **确认** 文案，未确认绝不出图（只有标题会自动标记「待确」）；
3. **生成** 由内置 Lovart 后端出图（纯 Python 标准库），身份图 + 风格图随包自带。

真实优先：产品、Logo、旅行照**原样使用**，绝不凭空编造事实。

## 快速开始

```bash
# 1. 克隆
git clone https://github.com/wangsiji/qiuqiu-wechat-cover
cd qiuqiu-wechat-cover

# 2. 挂到智能体 Skill 目录（以 Hermes 为例）
cp -r . ~/.hermes/skills/qiuqiu-wechat-cover

# 3. 配置出图后端密钥
export LOVART_ACCESS_KEY="ak_..."
export LOVART_SECRET_KEY="sk_..."

# 4. 校验结构与内置资产
python3 tools/resolve_assets.py     # → ok:true + 两个 absolute_path
python3 tools/validate_skill.py .

# 5. 交给智能体
#    → 「对这篇公众号文章生成封面：/path/to/article.md」
```

> 只需完整正文 / Markdown / 可读路径。默认 图 1=读者身份、图 2=封面风格；按文章需要补产品 / Logo / 截图 / 旅行照（从 图 3 起编号）。出图默认走 Lovart 免费队列，详见 [references/lovart-channel.md](references/lovart-channel.md)。

## 特性

- **品牌内置**：真人身份图 + 暖木复古像素风格图随包分发，不用搜图、传图、连素材库。
- **流程闭环**：收集 → 分析 → 提案 3 钩子 → 生成 / 编辑 → 验收。
- **真实优先**：真实产品 / Logo / 旅行照原样使用，绝不编造。
- **可迁移**：纯标准库后端 `tools/lovart-agent.py` 与辅助脚本全部随包分发，零第三方依赖。

## 目录

```
SKILL.md                   入口规则与硬约束
agents/openai.yaml         UI 展示与默认提示
references/
  workflow.md              输入角色、阶段协议、处理边界
  style-guide.md           2.35:1 视觉系统
  prompt-template.md       可复制的提示词结构
  prompt-checklist.md      生成前后验收清单
  lovart-channel.md        出图后端操作细节（含免费跑通法）
  assets/                  内置 Image 1（身份）与 Image 2（风格）
tools/
  resolve_assets.py        查找、校验、暴露内置资产
  validate_skill.py        本地 & CI 完整性校验
  lovart-agent.py          Lovart 出图后端（纯标准库）
examples/                  在产示例
```

## 约束

- 画布严格 **2.35:1**（优先 1880×800）。
- 视觉 = 暖木 × 复古像素 × 温馨工作台 × 真实主体。
- 文案至多 3 组、全页 20~35 汉字，主标题唯一焦点。
- 保留口罩，真实感 ~80% + 像素 20%；不做全像素 / 卡通 / 换脸。
- 身份与风格禁止外部检索；缺真人交互时不虚构人物。

## 校验与 CI

`tools/validate_skill.py` 检查必需文件、相对链接、资产文件头、Lovart 后端存在且纯标准库。每次提交由 GitHub Actions 运行：

```bash
python3 tools/validate_skill.py .
```

该校验检查**结构**，不替代出图后的视觉验收（中文逐字、人物轮廓需人工核对）。

## 许可

[MIT](LICENSE)。内置 `tools/lovart-agent.py` 取自 [lovartai/lovart-skill](https://github.com/lovartai/lovart-skill)（MIT），归属声明见 [NOTICE](NOTICE)。