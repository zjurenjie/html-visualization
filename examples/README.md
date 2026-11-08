# examples

可直接渲染的成品示例，均基于 [`templates/`](../templates/) 中的模板，可先渲染对照学习，再改造为自己的图表。

| 文件 | 基于模板 | 主题 | 比例 | 说明 |
|------|----------|------|------|------|
| [line-trend.html](line-trend.html) | `echarts-template.html` | `light` | 16:9 | 月度活跃用户折线图（模板默认示例） |
| [vertical-dark.html](vertical-dark.html) | `echarts-template.html` | `dark` | 9:16 | 竖屏深色主题，演示字号随视口等比缩放 |
| [gantt-schedule.html](gantt-schedule.html) | `gantt-template.html` | `light` | 16:9 | 项目排期甘特图（车道泳道 + 状态着色 + 拖拽） |

## 渲染示例

在项目根目录执行：

```bash
python scripts/html2img.py examples/line-trend.html
python scripts/html2img.py examples/vertical-dark.html --ratio 9:16 --width 1080
python scripts/html2img.py examples/gantt-schedule.html
```

输出的 PNG 默认生成在 `examples/` 下（已被 `.gitignore` 忽略）。

> 提示：HTML 中 ECharts 的离线兜底路径为 `../assets/echarts.min.js`，图表文件需保持在 `assets/` 的下一级目录（`templates/` 或 `examples/`），移动位置时同步修正该相对路径。

## 一键重建 README 展示截图

[`build/build-examples.py`](../build/build-examples.py) 会渲染本目录的示例，并生成 [`docs/showcase/`](../docs/showcase/) 下的全部展示截图（含 4 套主题 2×2 拼接对比图与 14 种图型总览长图）：

```bash
pip install pillow
python build/build-examples.py
```

更多用法（`--list` / `--only` / `--browser`）见[项目 README](../README.md) 的「重建展示截图」。
