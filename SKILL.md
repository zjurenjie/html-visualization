---
name: html-visualization
description: 把用户提供的数据渲染成 HTML 图表，并按用户设定的长宽比（16:9、1:1、9:16 等）导出为 PNG 图片。当用户提供数据要求画图、做图表、数据可视化、生成数据看板图、把数据转成图片、做甘特图/排期图/进度图、或要求按特定比例输出图表图片时触发。内置折线、堆叠折线、散点、分布散点、线性回归、柱状、饼图、甘特图等 14 种常用图型与 light/business/dark/warm 4 套主题。
---

# HTML 数据可视化技能（数据 → HTML 图表 → 指定比例 PNG）

## 概述

根据用户输入数据的**特征**（时间性、类别数、维度、构成关系等）与用户的**喜好**（主题、配色、风格、长宽比），生成单页 HTML 图表，再用无头浏览器把 HTML 截图为用户设定长宽比的 PNG。产物：可复用的 `.html` + 精确比例的 `.png`。

## 工作流（按序执行）

**第 1 步：解析数据特征。** 从用户输入提取：字段与类型、维度/指标个数、是否含时间或顺序、数据量级。数据不完整或语义不明时先向用户确认，不猜数据。

**第 2 步：确认喜好与输出参数。** 采纳用户已表达的全部偏好；未表达项用默认值（`light` 简约浅色、16:9、逻辑宽 1200、倍率 2、ECharts），在交付说明中列出所用默认值，**不反复追问**。4 套主题：

| 主题 | `data-theme` | 适用 |
|------|--------------|------|
| 简约浅色（默认） | `light` | 通用、博客、知识卡片 |
| 商务蓝金 | `business` | 汇报、金融、正式商务 |
| 科技深色 | `dark` | 监控、技术分享、深色海报 |
| 暖色活力 | `warm` | 营销、社交、活跃数据 |

默认值与可选项见 `references/chart-design.md` §2，完整令牌见 §3。

**第 3 步：选定图型与主题。** 按 `references/chart-design.md` §1 判定表首次命中选定图型；从 §3 的 4 套主题中按用户喜好选一套（未表达用 `light`）；多系列用 `C.palette`，单系列用 `C.accent`。不确定效果时先看 `templates/gallery.html` 的 14 种图型实时预览。

**第 4 步：生成 HTML。** 复制 `templates/echarts-template.html` 为工作文件，设置 `body[data-theme]` 为选定主题，替换标题、副标题、脚注与 ECharts option（配方见 `references/chart-design.md` §4，效果见 `templates/gallery.html`）。**甘特图（任务/事件起止区间）除外**：复制 `templates/gantt-template.html`，它基于 ECharts 官方「机场航班甘特图」示例改写，内置车道泳道、状态着色、进度分层、dataZoom 缩放与工期条拖拽，替换 `LANES`/`TASKS` 数据即可。硬性要求：

- `animation: false`，`tooltip: { show: false }`（静态截图）；
- 容器铺满视口：`html, body { width/height: 100%; overflow: hidden }`，图表区 `flex: 1`；
- 字号使用模板的 `fs()` 自适应函数，不写死大字号；
- 保留 CDN + 本地 `assets/echarts.min.js` 双通道；移动 HTML 后同步修正兜底相对路径；
- 数据必须是用户提供的真实数据，缺失用 `null` 并加脚注，不虚构。

**第 5 步：渲染为指定比例的 PNG。**

```
python scripts/html2img.py <工作文件>.html --ratio <比例> --width <逻辑宽> --scale <倍率> --out <输出.png>
```

例：`python scripts/html2img.py chart.html --ratio 9:16 --width 1080 --scale 2 --out chart.png`

输出 JSON 中 `ok: true` 且 `pixels` 与目标一致才算成功。

**第 6 步：视觉自检后交付。** 用 `Read` 打开 PNG 检查：图表空白（ECharts 未加载）、中文方块字、文字溢出/裁切、元素重叠、比例与预期不符。发现问题改 HTML 后重新渲染。最后向用户交付 `.html` 与 `.png`，并说明：图型选择依据、所用喜好参数（含默认项）、输出像素尺寸。

## 命令速查

| 需求 | 命令 |
|------|------|
| 横版汇报图 | `python scripts/html2img.py chart.html --ratio 16:9` |
| 方形社交图 | `python scripts/html2img.py chart.html --ratio 1:1 --width 1080` |
| 竖屏手机图 | `python scripts/html2img.py chart.html --ratio 9:16 --width 1080` |
| 指定浏览器 | `--browser "C:\Program Files\Google\Chrome\Application\chrome.exe"` |
| 预览图型/主题 | 浏览器打开 `templates/gallery.html`，右上角切换；也可用 `?theme=dark` 指定初始主题 |

脚本仅依赖标准库 + Pillow，浏览器自动发现 Chrome / Edge / Chromium（可用 `HTMLVIZ_BROWSER` 环境变量指定）。

## 常见错误速查

详细排查表见 `references/chart-design.md` §6。高频项：本地兜底路径错误导致图表空白；`overflow` 未隐藏导致截图比例漂移；CDN 不可用时未修正 `../assets/echarts.min.js` 相对路径。

## 文件清单

- `templates/echarts-template.html` — 单图模板（4 套主题，自带可渲染示例，占位项 ①-⑦ 有注释标记）
- `templates/gantt-template.html` — 甘特图模板（custom series + 时间轴 + dataZoom + 拖拽调整，参考官方机场甘特图示例；4 套主题，替换 LANES/TASKS 数据即可）
- `templates/gallery.html` — 14 种图型 × 4 套主题的可交互预览页（仅用于选型/选主题，不参与最终截图；支持 `?theme=light|business|dark|warm`）
- `scripts/html2img.py` — HTML → 指定比例 PNG 渲染脚本
- `assets/echarts.min.js` — 本地 ECharts（离线兜底）
- `references/chart-design.md` — 图型判定表、4 套主题令牌、13 种 ECharts 配方、设计规范
