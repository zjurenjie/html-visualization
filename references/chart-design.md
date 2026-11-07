# 图表设计参考：数据特征 → 图型判定 · 喜好维度 · 配色 · ECharts 配方

生成图表 HTML 前必读。工作流程见 SKILL.md，本文解决「画什么图、长什么样」。14 种图型 × 4 套主题的可视化预览见 `templates/gallery.html`。

## 1. 数据特征 → 图型判定表

先分析用户数据（字段、维度、指标个数、是否含时间/顺序），按顺序首次命中即选定：

| # | 数据特征 | 首选图型 | 备选 | 关键注意 |
|---|---------|---------|------|---------|
| 1 | 单指标随时间/顺序变化（≥4 个时间点） | 折线图（可加面积） | 阶梯图 | 点少(≤3)改柱状图 |
| 2 | 多指标随时间变化（2-4 条线） | 多系列折线 | 分组柱状 | 系列超 4 条拆图或取 Top |
| 3 | 多指标随时间变化，关注累计总量（2-5 个系列） | 堆叠折线图 | 堆叠面积图 | 所有系列 `stack` 值一致；累计后难读个体值 |
| 4 | 少量类别（≤8）比较单指标 | 柱状图 | 条形图 | 类别名长(>4字)用横向条形 |
| 5 | 类别较多（>8）比较单指标 | 横向条形图 | 排序柱状 | 必须按值排序 |
| 6 | 构成占比，部分→整体（≤6 项） | 环形图 | 堆叠条 | 占比差异小(<2%)慎用饼图 |
| 7 | 构成占比，项目多（>6 项） | 横向堆叠单条 | 矩形树图 | 小项合并「其他」 |
| 8 | 两个连续变量关系（点少，关注个体） | 散点图 | 气泡图（加第三维） | 点>500 改用分布散点或降透明度 |
| 9 | 大量样本、按类别看两个连续变量的分布（数百点） | 分布散点图 | 分组散点 / 密度图 | 类别用颜色编码；点数>5000 开 large/progressive |
| 10 | 单变量分布 | 直方图 | 箱线图 | 分箱 8-15 个 |
| 11 | 多维能力/指标对比（3-8 维，1-2 个对象） | 雷达图 | 分组柱状 | 维度>8 不用雷达 |
| 12 | 流程/漏斗各阶段转化 | 漏斗图 | 横向堆叠条 | 阶段按转化率降序 |
| 13 | 层级结构（树形） | 矩形树图 | 旭日图 | 两层以内用树图 |
| 14 | 排名变化（两时间点对比） | 斜率图 | 哑铃图 | 只适合两期 |
| 15 | 目标 vs 实际 | 子弹图 | 进度环 | 偏差用参考线标出 |
| 16 | 地理分布 | 地图 | 分省着色 | ECharts 需另配 GeoJSON，无地图数据时降级为条形图 |
| 17 | 表格类多维明细 | 热力图 | HTML 表格 | 单元格≤200 个 |
| 18 | 两连续变量相关性 + 需要拟合趋势线 | 线性回归图 | 散点 + 参考线 | 必须标注公式与 R² |
| 19 | 任务/事件的起止时间区间，按车道（人/组/机器/阶段）分行 | 甘特图 | 横向堆叠条 / 时间线 | custom series + 时间轴；交互版见 `templates/gantt-template.html` |

判定不清时（如既可折线又可柱状），按用户喜好决定；喜好未表达则选信息密度更高、更不易误读的一种，并在交付说明中注明理由。

## 2. 喜好维度（用户未表达项用默认值，交付时说明，不反复追问）

| 维度 | 取值 | 默认 |
|------|------|------|
| 主题 | `light` / `business` / `dark` / `warm` | `light` |
| 长宽比 | `16:9` `4:3` `1:1` `9:16` `3:4` `21:9` 或任意 `W:H` | `16:9` |
| 逻辑宽度 | 600-2400 px | `1200` |
| 输出倍率 | 1(屏幕) / 2(视网膜，默认) / 3(印刷) | `2` |
| 风格 | 简约(默认) / 商务 / 科技感 / 活泼 | 简约 |
| 主题（配色） | 见 §3 四套主题 | `light` |
| 数值标签 | 显示 / 不显示 | 关键点显示（折线）或全显示（柱状/条形） |
| 图表库 | ECharts(默认) / 纯 SVG+CSS 手写（无 JS 依赖需求时） | ECharts |

常用比例与场景速查：

| 比例 | 典型场景 | 建议逻辑宽 |
|------|---------|-----------|
| 16:9 | PPT、汇报、博客封面 | 1200 |
| 4:3 | 文档插图 | 1000 |
| 1:1 | 社交媒体方图 | 1080 |
| 3:4 | 小红书/竖版卡片 | 1080 |
| 9:16 | 手机竖屏、短视频贴片 | 1080 |
| 21:9 | 横幅 banner | 1600 |

## 3. 四套主题（CSS 变量 + series 调色盘）

每套主题包含背景、文字、网格、强调色和 6 色系列盘。模板通过 `body[data-theme]` 切换；`templates/gallery.html` 可实时预览。未表达偏好时用 `light`。

### 3.1 简约浅色 `light`（默认）

| 令牌 | 值 |
|------|----|
| `--bg` | `#ffffff` |
| `--fg` | `#1f2329` |
| `--muted` | `#86909c` |
| `--grid` | `#e5e6eb` |
| `--accent` | `#3b82f6` |
| series 盘 | `#3b82f6` `#10b981` `#f59e0b` `#8b5cf6` `#ef4444` `#14b8a6` |

适用：通用汇报、博客、知识卡片。

### 3.2 商务蓝金 `business`

| 令牌 | 值 |
|------|----|
| `--bg` | `#fffdf8` |
| `--fg` | `#1f2937` |
| `--muted` | `#6b7280` |
| `--grid` | `#e7e0d4` |
| `--accent` | `#1d4ed8` |
| series 盘 | `#1d4ed8` `#b8860b` `#64748b` `#0f766e` `#9333ea` `#78716c` |

适用：汇报、金融、正式商务场景。

### 3.3 科技深色 `dark`

| 令牌 | 值 |
|------|----|
| `--bg` | `#0f172a` |
| `--fg` | `#f1f5f9` |
| `--muted` | `#94a3b8` |
| `--grid` | `#1e293b` |
| `--accent` | `#38bdf8` |
| series 盘 | `#38bdf8` `#34d399` `#a78bfa` `#f472b6` `#fbbf24` `#22d3ee` |

适用：监控、技术分享、深色海报。想要更强的霓虹感时，可把 series 盘替换为 `#a78bfa` `#f472b6` `#38bdf8` `#4ade80` `#facc15` `#fb923c`。

### 3.4 暖色活力 `warm`

| 令牌 | 值 |
|------|----|
| `--bg` | `#fffaf5` |
| `--fg` | `#292524` |
| `--muted` | `#78716c` |
| `--grid` | `#f0e0d2` |
| `--accent` | `#f97316` |
| series 盘 | `#f97316` `#e11d48` `#f59e0b` `#be123c` `#ea580c` `#fbbf24` |

适用：营销、社交、活跃数据。

规则：单系列用第一色（`--accent`）；多系列按序取 `C.palette`；语义色（正/负、涨/跌）优先用绿 `#10b981` / 红 `#ef4444`（深色主题提亮为 `#34d399` / `#f87171`）；同图系列 ≤6，超出取 Top5 + 「其他」灰 `#9ca3af`；一张图只用一套主题，不混搭。

## 4. ECharts 配方速查

14 种图型的可运行效果见 `templates/gallery.html`（支持 `?theme=light|business|dark|warm`）。本节给出最小可复制配方：折线见模板，堆叠折线、柱状、横向条形、环形、散点、分布散点、线性回归、雷达、漏斗、饼图、堆叠柱状、仪表盘、甘特图见下。未列入的图型（直方图、矩形树图、地图、热力图等）按 §1 判定表选型，option 参考 ECharts 官方示例。

通用骨架（所有配方共用，`fs()` / `C` 已在模板中定义；`C.palette` 为主题 6 色盘）：

```js
const option = {
  animation: false,           // 静态截图必须关
  tooltip: { show: false },
  color: C.palette,           // 多系列按主题 6 色盘取色
  // grid: 按图型调整，
  // 坐标轴 / series 见下
};
```

**堆叠折线图**（多系列累计趋势；`stack` 取同一值时，线的高度是累计值）：

```js
legend: { top: 0, left: 'center', itemWidth: 10, itemHeight: 10,
  textStyle: { color: C.muted, fontSize: fs(11) } },
grid: { left: 8, right: 20, top: 50, bottom: 8, containLabel: true },
xAxis: { type: 'category', boundaryGap: false,
  data: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
  axisTick: { show: false }, axisLine: { lineStyle: { color: C.grid } },
  axisLabel: { color: C.muted, fontSize: fs(11) } },
yAxis: { type: 'value',
  splitLine: { lineStyle: { color: C.grid, type: 'dashed' } },
  axisLabel: { color: C.muted, fontSize: fs(11) } },
series: [
  { name: 'Email', type: 'line', stack: 'Total', symbolSize: 4,
    data: [120, 132, 101, 134, 90, 230, 210] },
  { name: 'Union Ads', type: 'line', stack: 'Total', symbolSize: 4,
    data: [220, 182, 191, 234, 290, 330, 310] },
  { name: 'Video Ads', type: 'line', stack: 'Total', symbolSize: 4,
    data: [150, 232, 201, 154, 190, 330, 410] },
  { name: 'Direct', type: 'line', stack: 'Total', symbolSize: 4,
    data: [320, 332, 301, 334, 390, 330, 320] },
  { name: 'Search Engine', type: 'line', stack: 'Total', symbolSize: 4,
    data: [820, 932, 901, 934, 1290, 1330, 1320] },
]
```

注意：所有系列的 `stack` 值必须完全一致；图例项多时用顶部居中 + 小字号，或换成底部两行。堆叠后读的是累计高度，关注个体值时改用普通多系列折线；系列超过 5 条或量级差异过大时，考虑堆叠面积或拆图。`boundaryGap: false` 让首尾点贴边，符合时间序列习惯。

**柱状图**（类别比较）：

```js
grid: { left: 50, right: 30, top: 30, bottom: 40 },
xAxis: { type: 'category', data: ['A','B','C'],
  axisTick: { show: false },
  axisLine: { lineStyle: { color: C.grid } },
  axisLabel: { color: C.muted, fontSize: fs(12) } },
yAxis: { type: 'value',
  splitLine: { lineStyle: { color: C.grid, type: 'dashed' } },
  axisLabel: { color: C.muted, fontSize: fs(12) } },
series: [{ type: 'bar', data: [120, 200, 150],
  barWidth: '55%', itemStyle: { color: C.accent, borderRadius: [4, 4, 0, 0] },
  label: { show: true, position: 'top', color: C.fg, fontSize: fs(11) } }]
```

**横向条形图**（类别多/名字长，数据先按值降序）：

```js
grid: { left: 100, right: 60, top: 20, bottom: 30 },   // 左侧留类别名
xAxis: { type: 'value', splitLine: { lineStyle: { color: C.grid, type: 'dashed' } },
  axisLabel: { color: C.muted, fontSize: fs(12) } },
yAxis: { type: 'category', data: [...],
  axisTick: { show: false }, axisLine: { show: false },
  axisLabel: { color: C.fg, fontSize: fs(12) } },
series: [{ type: 'bar', data: [...], barWidth: '60%',
  itemStyle: { color: C.accent, borderRadius: [0, 4, 4, 0] },
  label: { show: true, position: 'right', color: C.fg, fontSize: fs(11) } }]
```

**环形图**（构成占比）：

```js
series: [{ type: 'pie', radius: ['55%', '78%'], center: ['50%', '52%'],
  data: [{ value: 460, name: '移动端' }, { value: 320, name: '桌面端' }, ...],
  label: { color: C.fg, fontSize: fs(12),
    formatter: '{b}\n{d}%' },        // 名称 + 百分比
  labelLine: { lineStyle: { color: C.grid } },
  itemStyle: { borderColor: C.bg, borderWidth: 2 } }]
// 中心可加总计：graphic 或 title:{text:'总数', subtext:'780', left:'center', top:'45%'}
```

**散点图**（两变量关系）：

```js
xAxis: { type: 'value', scale: true, ... },   // 同柱状图轴样式
yAxis: { type: 'value', scale: true, ... },
series: [{ type: 'scatter', data: [[x1,y1],[x2,y2],...],
  symbolSize: fs(10), itemStyle: { color: C.accent, opacity: 0.75 } }]
```

**分布散点图**（大量样本；类别颜色 + 亮度编码，底部不再重复放图例）：

```js
// 确定性伪随机：重复截图时分布不漂移；真实数据直接替换 data
function hash01(index, seed) {
  const v = Math.sin(index * 12.9898 + seed * 78.233) * 43758.5453;
  return v - Math.floor(v);
}
const groups = [
  { name: '谷物', cx: 12, cy: 45, sx: 6, sy: 20 },
  { name: '蔬果', cx: 4.5, cy: 65, sx: 2.5, sy: 30 },
  { name: '肉蛋', cx: 22, cy: 25, sx: 6, sy: 12 },
  { name: '乳品', cx: 7, cy: 170, sx: 3.5, sy: 65 },
];
const data = [];
groups.forEach((g, gi) => {
  for (let i = 0; i < 150; i++) {
    const rr = Math.sqrt(hash01(i + 1, gi * 10 + 1));   // 半径开方，椭圆内均匀
    const theta = hash01(i + 1, gi * 10 + 2) * Math.PI * 2;
    data.push([
      Number((g.cx + Math.cos(theta) * rr * g.sx).toFixed(1)),
      Number((g.cy + Math.sin(theta) * rr * g.sy).toFixed(1)),
      g.name,                                            // 类别名，供 visualMap 取色
      Math.round(hash01(i + 1, gi * 10 + 3) * 100),     // 第三维，供亮度映射
    ]);
  }
});
visualMap: [
  { show: true, type: 'piecewise', categories: groups.map((g) => g.name),
    dimension: 2, inRange: { color: C.palette.slice(0, groups.length) },
    orient: 'horizontal', left: 'center', top: 0, itemWidth: 9,
    itemHeight: 9, itemGap: 10, textStyle: { color: C.muted, fontSize: fs(10) },
    realtime: false },
  { show: false, dimension: 3, max: 100,
    inRange: { colorLightness: [0.35, 0.7] }, realtime: false },
],
grid: { left: 8, right: 16, top: 42, bottom: 42, containLabel: true },
xAxis: { type: 'value', name: '蛋白质 (g)', scale: true, splitLine: { show: false } },
yAxis: { type: 'value', name: '钙 (mg)', scale: true, splitLine: { show: false } },
series: [{ type: 'scatter', data, symbolSize: fs(5),
  itemStyle: { opacity: 0.78 }, progressiveThreshold: 5000 }]
```

注意：`visualMap` 的第一项既是类别图例也是筛选器；不想交互时把 `show` 设为 `false`，但需另加图例说明颜色。`piecewise` 的 `categories` 按**值相等**匹配 `dimension` 指定的那一维——该维必须放类别名本身（如 `g.name`），放数字索引会全部落入 outOfRange，点变灰、浅底上近似不可见。第二项隐藏的 `visualMap` 用 `colorLightness` 编码第三维，制造深浅层次；静态截图保留 `animation: false`，不要加 `motionBlur` 尾迹。点数 >5000 时改用 `large: true` 与 `largeThreshold`，避免渲染卡顿。

**线性回归图**（散点 + 最小二乘拟合线 + 公式标注；内联实现，离线无需 echarts-stat）：

```js
// 样本：[[x, y], ...]，必须是用户提供的真实数据
const data = [[0.067732, 3.176513], [0.42781, 3.816464], ...];
// 最小二乘：斜率 / 截距 / R²（与 ecStat 的 linear 方法等价）
const n = data.length;
let sx = 0, sy = 0, sxx = 0, sxy = 0;
data.forEach(([x, y]) => { sx += x; sy += y; sxx += x * x; sxy += x * y; });
const slope = (n * sxy - sx * sy) / (n * sxx - sx * sx);
const intercept = (sy - slope * sx) / n;
const meanY = sy / n;
let ssRes = 0, ssTot = 0;
data.forEach(([x, y]) => {
  ssRes += (y - (slope * x + intercept)) ** 2;
  ssTot += (y - meanY) ** 2;
});
const r2 = 1 - ssRes / ssTot;
// 拟合线只画 [xMin, xMax] 两点，不外插到轴边界
const xMin = Math.min(...data.map((d) => d[0]));
const xMax = Math.max(...data.map((d) => d[0]));
const line = [
  [xMin, slope * xMin + intercept],
  [xMax, slope * xMax + intercept],
];
grid: { left: 8, right: 130, top: 32, bottom: 42, containLabel: true },
xAxis: { type: 'value', scale: true, splitLine: { show: false },
  axisLine: { show: true, lineStyle: { color: C.grid } } },
yAxis: { type: 'value', scale: true, splitLine: { show: false },
  axisLine: { show: true, lineStyle: { color: C.grid } } },
series: [
  { name: '样本', type: 'scatter', data, symbolSize: fs(6),
    itemStyle: { color: C.palette[0], opacity: 0.55 } },
  { name: '回归线', type: 'line', data: line, symbol: 'none',
    lineStyle: { width: 2.5, color: C.palette[1] },
    endLabel: { show: true, distance: fs(8), color: C.fg, fontSize: fs(11),
      formatter: 'y = ' + slope.toFixed(2) + 'x + ' + intercept.toFixed(2)
        + '  R² = ' + r2.toFixed(2) } },
]
```

注意：公式与 R² 必须标注在图上（`endLabel`），`grid.right` 预留 ≥130px 防止公式被裁切；R² < 0.3 说明线性解释力弱，改画纯散点并用文字描述走势，不画误导性趋势线；样本 <10 个时拟合不稳定，同样退回散点图。需要指数 / 对数 / 多项式拟合时引入 [echarts-stat](https://github.com/ecomfe/echarts-stat)：`echarts.registerTransform(ecStat.transform.regression)` 后用 dataset transform `{ type: 'ecStat:regression', config: { method: 'exponential' } }`（linear/logarithmic/polynomial 同理），公式标签 `formulaOn: 'end'`；该库需另行 CDN + 本地兜底，仅线性回归时不引入。

**雷达图**（多维对比）：

```js
radar: { indicator: [{ name: '维度A', max: 100 }, ...],
  radius: '65%', axisName: { color: C.fg, fontSize: fs(12) },
  splitLine: { lineStyle: { color: C.grid } },
  splitArea: { show: false }, axisLine: { lineStyle: { color: C.grid } } },
series: [{ type: 'radar', data: [
  { value: [...], name: '对象1', areaStyle: { opacity: 0.2 },
    lineStyle: { color: C.accent, width: 2 }, itemStyle: { color: C.accent } } ] }]
```

**漏斗图**（阶段转化）：

```js
series: [{ type: 'funnel', left: '10%', width: '80%', top: 20, bottom: 20,
  sort: 'descending', gap: 4,
  data: [{ value: 100, name: '曝光' }, { value: 60, name: '点击' }, ...],
  label: { show: true, position: 'inside', color: '#ffffff', fontSize: fs(12),
    formatter: '{b}  {c}%' },
  itemStyle: { borderColor: 'transparent' } }]
```

**饼图**（少量类别看占比；中心不需要放指标时用饼图，需要放总计用环形图）：

```js
series: [{
  type: 'pie',
  radius: '62%',
  center: ['50%', '50%'],
  minAngle: 3,                       // 防止极小扇区不可见
  data: [{ value: 460, name: '移动端' }, { value: 320, name: '桌面端' },
         { value: 140, name: '平板' }, { value: 80, name: '其他' }],
  itemStyle: { borderColor: C.bg, borderWidth: 2, borderRadius: 4 },
  label: { color: C.fg, fontSize: fs(12), lineHeight: fs(16),
    formatter: '{b}\n{d}%' },
  labelLine: { length: fs(8), length2: fs(6), lineStyle: { color: C.grid } },
}]
```

注意：类别 >6 或占比差异 <2% 时改横向堆叠条/条形；标签重叠时缩小 `radius`，或把 `label.position` 设为 `'inside'`。

**堆叠柱状图**（构成随时间变化，2-4 个系列）：

```js
legend: { top: 0, right: 0, itemWidth: 10, itemHeight: 10,
  textStyle: { color: C.muted, fontSize: fs(11) } },
grid: { left: 50, right: 30, top: 50, bottom: 40 },
xAxis: { type: 'category', data: ['1月','2月','3月','4月','5月','6月'] },
yAxis: { type: 'value' },
series: [
  { name: '线上', type: 'bar', stack: 'total', data: [120,135,128,150,162,175],
    barWidth: '52%', itemStyle: { color: C.palette[0] } },
  { name: '门店', type: 'bar', stack: 'total', data: [90,92,105,98,110,118],
    itemStyle: { color: C.palette[1] } },
  { name: '渠道', type: 'bar', stack: 'total', data: [60,72,68,80,86,95],
    itemStyle: { color: C.palette[2], borderRadius: [4, 4, 0, 0] } },
]
```

注意：圆角只加在最上层系列，系列顺序变化时同步调整；不要用堆叠柱表达占比差异很小的数据。

**仪表盘**（单个 KPI 完成率/健康度）：

```js
series: [{
  type: 'gauge',
  startAngle: 210, endAngle: -30, min: 0, max: 100,
  radius: '76%', center: ['50%', '55%'],
  progress: { show: true, width: 12, itemStyle: { color: C.accent } },
  axisLine: { lineStyle: { width: 12, color: [[1, C.grid]] } },
  axisTick: { show: false },
  splitLine: { length: 7, lineStyle: { color: C.muted } },
  axisLabel: { color: C.muted, fontSize: fs(10), distance: 12 },
  splitNumber: 4,
  pointer: { show: false }, anchor: { show: false },
  title: { offsetCenter: [0, '38%'], color: C.muted, fontSize: fs(12) },
  detail: { valueAnimation: false, offsetCenter: [0, '4%'], color: C.fg,
    fontSize: fs(28), fontWeight: 'bold', formatter: '{value}%' },
  data: [{ value: 72, name: '目标完成率' }],
}]
```

注意：仪表盘只承载一个数；多指标用进度条或分组柱状。`valueAnimation: false` 保证截图稳定；刻度拥挤时把 `axisLabel.show` 与 `splitLine.show` 设为 `false`，只留进度弧和数值。

**甘特图**（任务/事件起止区间，按车道分行；核心是 custom series + 时间轴，参考 ECharts 官方「机场航班甘特图」示例。交互完整版——dataZoom 缩放、状态/进度分层、工期条拖拽、车道多时纵向滚动——直接用 `templates/gantt-template.html`）：

```js
const HEIGHT_RATIO = 0.6;                    // 条形高度 / 车道高度
// 车道与任务：[车道索引, 开始, 结束, 任务名]，时间用 'YYYY-MM-DD' 或 'YYYY-MM-DD HH:mm'
const lanes = ['设计组', '前端组', '后端组', '测试组'];
const tasks = [
  [0, '2026-11-02', '2026-11-06', '需求评审'],
  [1, '2026-11-09', '2026-11-17', '管理后台'],
  // ...
];
const toTs = (s) => typeof s === 'number' ? s : +new Date(s.replace(/-/g, '/'));
grid: { left: 90, right: 20, top: 40, bottom: 20 },   // 左侧留车道名
xAxis: {
  type: 'time', position: 'top',
  splitLine: { lineStyle: { color: C.grid } },
  axisLine: { show: false }, axisTick: { show: false },
  axisLabel: { color: C.muted, fontSize: fs(11), hideOverlap: true, formatter: '{M}/{d}' },
},
yAxis: {
  min: 0, max: lanes.length, inverse: true,   // inverse 让第 0 车道在最上方
  axisTick: { show: false }, splitLine: { show: false },
  axisLine: { show: false }, axisLabel: { show: false },   // 车道名由标签系列绘制
},
series: [
  { name: '任务', type: 'custom', renderItem: renderGanttBar,
    encode: { x: [1, 2], y: 0 },              // x 用 [开始, 结束] 两维占一段区间
    data: tasks.map((t) => [t[0], toTs(t[1]), toTs(t[2]), t[3]]) },
  { name: '车道标签', type: 'custom', renderItem: renderLaneLabel,
    encode: { x: -1, y: 0 }, data: lanes.map((n, i) => [i, n]) },
]

function renderGanttBar(params, api) {
  const lane = api.value(0);
  const start = api.coord([api.value(1), lane]);
  const end = api.coord([api.value(2), lane]);
  const barLength = end[0] - start[0];
  const barHeight = api.size([0, 1])[1] * HEIGHT_RATIO;
  // 裁剪到网格内，dataZoom 聚焦窗口时条形不溢出；完全在窗外返回 undefined
  const bar = echarts.graphic.clipRectByRect(
    { x: start[0], y: start[1], width: barLength, height: barHeight },
    { x: params.coordSys.x, y: params.coordSys.y,
      width: params.coordSys.width, height: params.coordSys.height });
  if (!bar) return;
  const name = api.value(3) + '';
  const text = barLength > echarts.format.getTextRect(name, fs(11) + 'px sans-serif').width + 24
    ? name : '';                               // 条内任务名，放不下自动省略
  return { type: 'group', children: [
    { type: 'rect', shape: bar, style: { fill: C.accent } },
    { type: 'rect', shape: bar,
      style: { fill: 'transparent', text, textFill: '#fff', fontSize: fs(11) } },
  ]};
}
function renderLaneLabel(params, api) {
  const y = api.coord([0, api.value(0)])[1];
  const cy = y + api.size([0, 1])[1] * HEIGHT_RATIO / 2;   // 与条形垂直居中
  return { type: 'group', position: [0, cy], children: [
    { type: 'text', style: { x: 8, y: 0, text: api.value(1) + '',
      textAlign: 'left', textVerticalAlign: 'middle', textFill: C.fg, fontSize: fs(12) } },
  ]};
}
```

注意：`inverse: true` 时条形自车道线**向下**绘制（`y = start[1]`，占车道上侧 60%）；去掉 inverse 则改为 `y = start[1] - barHeight` 向上画，方向必须与轴向同步翻转，否则条形串道。`encode.x: [开始, 结束]` 让一个数据项占一段区间，这是 custom series 画甘特的关键。状态着色、进度分层（浅色 = 剩余工期）、`dataZoom`（`filterMode: 'weakFilter'` 保住跨窗口边缘的条形）、工期条拖拽（mousedown/mouseup + 落点阴影 + 同车道冲突检测 + 拖到边缘外自动平移）都已内置在 `templates/gantt-template.html`，需要时复制该模板而不是从零拼。同车道任务时间重叠会互相遮挡，输入数据先做冲突检查；车道 >15 条或时间跨度很大时启用对应的 yAxis/xAxis dataZoom。

## 5. 设计规范

- **层级**：标题 1.75rem 粗体 → 副标题 1rem 灰（范围+单位）→ 图 → 脚注 0.8rem 灰。一张图只讲一件事。
- **留白**：`.stage` 内边距 2.5rem/3rem；grid 四边 ≥30；不要让轴标签贴边。
- **网格线**：弱化为虚线 `type:'dashed'`，颜色用 `--grid`；能少则少。
- **数值标签**：柱/条形默认全显；折线显峰值、末值或全显（点 ≤12）；字号 11-12。
- **单位**：大数缩写（1.2万、3.4亿）进副标题或轴名，避免长数字挤轴。
- **空值**：数据缺失用 `null` 让折线断开并加脚注说明，不填 0 造假点。

## 6. 常见错误

| 症状 | 原因 | 修复 |
|------|------|------|
| 图表区域空白 | CDN 失败且本地兜底路径错 | 检查 `assets/echarts.min.js` 相对路径；模板在 `templates/` 下时为 `../assets/` |
| 截图是浏览器起始页 | 哨兵校验被跳过（`--no-dom-check`） | 去掉该参数重跑 |
| 图片比例不对 | `--ratio` 与页面内容溢出视口 | 保持 `overflow:hidden`；核对 JSON 输出里的 `pixels` |
| 中文显示为方块 | 系统无中文字体 | 在 HTML 里改用系统可用字体，或引入 Web 字体后重渲染 |
| 文字太小/发虚 | 倍率不够 | `--scale 2` 或 `3`；字号用模板的 `fs()` 自适应 |
| 内容被裁切 | 内容实际高度 > 视口 | 加大 `--width`、换更扁比例，或精简数据 |
| 甘特图条形消失或溢出网格 | `inverse` 与条形绘制方向不匹配；未用 `clipRectByRect` 裁剪 | inverse 轴条形自车道线向下画（非 inverse 向上）；渲染时统一走 `echarts.graphic.clipRectByRect` |
| 甘特图任务名不显示 | 条形宽度 < 文字宽度 + 边距 | 属于预期的自动省略；缩短任务名、收窄时间窗口或放大 `--width` |
| 切换主题后配色没变 | `body[data-theme]` 值拼错，或主题缺少 `--s1`…`--s6` | 对照 §3 检查属性值与令牌 |
