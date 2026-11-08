#!/usr/bin/env python3
"""一键重建 examples/ 示例对应的 docs/showcase/ 成品截图。

用法（在项目根目录执行）：

    python build/build-examples.py                 # 重建全部 5 张
    python build/build-examples.py --only a,b      # 只重建指定任务
    python build/build-examples.py --list          # 列出全部任务
    python build/build-examples.py --browser PATH  # 显式指定浏览器

产出（均写入 docs/showcase/，该目录是 .gitignore 中唯一放行 PNG 的位置）：

    line-trend.png        16:9 折线图示例（2400x1350，scale 2）
    vertical-dark.png     9:16 竖屏 + dark 主题示例（2160x3840，scale 2）
    gantt-schedule.png    16:9 甘特图示例（2400x1350，scale 2）
    gallery-overview.png  全部 14 种图型总览长图（1480x2620，scale 1）
    themes-comparison.png 4 套主题 2x2 拼接对比图（1600x900，需 Pillow）

依赖：scripts/html2img.py、本仓库 assets/echarts.min.js（离线兜底）；
themes-comparison 任务额外依赖 Pillow（pip install pillow）。
"""

from __future__ import annotations

import argparse
import pathlib
import shutil
import sys
import tempfile
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "scripts"))

from html2img import convert  # noqa: E402

SHOWCASE = ROOT / "docs" / "showcase"
THEMES = ["light", "business", "dark", "warm"]

# 简单任务：单个 HTML 渲染为单张 PNG
SIMPLE_JOBS: list[dict[str, Any]] = [
    {
        "name": "line-trend",
        "html": "examples/line-trend.html",
        "out": "line-trend.png",
        "width": 1200,
        "height": None,
        "ratio": "16:9",
        "scale": 2,
        "note": "16:9 折线图示例",
    },
    {
        "name": "vertical-dark",
        "html": "examples/vertical-dark.html",
        "out": "vertical-dark.png",
        "width": 1080,
        "height": None,
        "ratio": "9:16",
        "scale": 2,
        "note": "9:16 竖屏 + dark 主题示例",
    },
    {
        "name": "gantt-schedule",
        "html": "examples/gantt-schedule.html",
        "out": "gantt-schedule.png",
        "width": 1200,
        "height": None,
        "ratio": "16:9",
        "scale": 2,
        "note": "16:9 甘特图示例",
    },
    {
        "name": "gallery-overview",
        "html": "templates/gallery.html",
        "out": "gallery-overview.png",
        "width": 1480,
        "height": 2620,
        "ratio": "16:9",
        "scale": 1,
        "note": "14 种图型总览长图",
    },
]

SPECIAL_JOBS = ["themes-comparison"]
ALL_JOB_NAMES = [j["name"] for j in SIMPLE_JOBS] + SPECIAL_JOBS


def run_simple(job: dict[str, Any], browser: str | None) -> dict[str, Any]:
    result = convert(
        html_file=str(ROOT / job["html"]),
        out=str(SHOWCASE / job["out"]),
        width=job["width"],
        height=job["height"],
        ratio=job["ratio"],
        scale=job["scale"],
        browser=browser,
        verify_dom=True,
    )
    return result


def _load_font(size: int) -> Any:
    """加载标签字体：Windows 常见字体兜底，最终回退 PIL 默认。"""
    from PIL import ImageFont

    for path in (
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arial.ttf",
    ):
        if pathlib.Path(path).is_file():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def build_themes_comparison(browser: str | None) -> dict[str, Any]:
    """渲染 4 套主题的 echarts 模板并拼接为 2x2 对比图。

    临时 HTML 写入 examples/（必须与 assets/ 同级才能命中离线兜底），
    临时 PNG 写入系统临时目录，结束后统一清理。
    """
    try:
        from PIL import Image, ImageDraw
    except ImportError as exc:
        raise RuntimeError(
            "themes-comparison 需要 Pillow：pip install pillow"
        ) from exc

    src = (ROOT / "templates" / "echarts-template.html").read_text(
        encoding="utf-8"
    )
    anchor = '<body data-theme="light">'
    if anchor not in src:
        raise RuntimeError(
            'echarts-template.html 中未找到 <body data-theme="light">，'
            "无法生成主题对比图，请检查模板"
        )

    tmp_dir = pathlib.Path(tempfile.mkdtemp(prefix="htmlviz_themes_"))
    tmp_htmls: list[pathlib.Path] = []
    cell_w, cell_h = 800, 450
    try:
        quadrants: dict[str, pathlib.Path] = {}
        for theme in THEMES:
            html = src.replace(anchor, f'<body data-theme="{theme}">', 1)
            tmp_html = ROOT / "examples" / f".tmp-theme-{theme}.html"
            tmp_html.write_text(html, encoding="utf-8")
            tmp_htmls.append(tmp_html)
            tmp_png = tmp_dir / f"{theme}.png"
            convert(
                html_file=str(tmp_html),
                out=str(tmp_png),
                width=cell_w,
                height=cell_h,
                ratio="16:9",
                scale=1,
                browser=browser,
                verify_dom=True,
            )
            quadrants[theme] = tmp_png

        canvas = Image.new("RGB", (cell_w * 2, cell_h * 2), "#ffffff")
        draw = ImageDraw.Draw(canvas, "RGBA")
        font = _load_font(22)
        for idx, theme in enumerate(THEMES):
            img = Image.open(quadrants[theme]).convert("RGB")
            if img.size != (cell_w, cell_h):
                img = img.resize((cell_w, cell_h))
            x = (idx % 2) * cell_w
            y = (idx // 2) * cell_h
            canvas.paste(img, (x, y))
            # 左上角主题标签：半透明黑底白字 + 细白描边，明暗主题均清晰
            text = f" {theme} "
            bbox = draw.textbbox((0, 0), text, font=font)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            pad = 8
            chip = (x + 16, y + 16, x + 16 + tw + pad * 2, y + 16 + th + pad * 2)
            draw.rounded_rectangle(
                chip, radius=8, fill=(0, 0, 0, 165), outline=(255, 255, 255, 90), width=1
            )
            draw.text(
                (chip[0] + pad, chip[1] + pad), text, font=font, fill=(255, 255, 255, 255)
            )

        out_path = SHOWCASE / "themes-comparison.png"
        canvas.save(out_path)
        return {
            "output": str(out_path),
            "pixels": {"width": cell_w * 2, "height": cell_h * 2},
            "themes": THEMES,
        }
    finally:
        for tmp_html in tmp_htmls:
            try:
                tmp_html.unlink()
            except OSError:
                pass
        shutil.rmtree(tmp_dir, ignore_errors=True)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="一键重建 docs/showcase/ 示例成品截图"
    )
    parser.add_argument(
        "--only",
        default=None,
        help=f"逗号分隔的任务名，可选：{','.join(ALL_JOB_NAMES)}",
    )
    parser.add_argument("--list", action="store_true", help="列出全部任务后退出")
    parser.add_argument(
        "--browser", default=None, help="浏览器可执行文件路径，默认自动发现"
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.list:
        for job in SIMPLE_JOBS:
            print(f"{job['name']:<20} {job['note']}")
        print(f"{'themes-comparison':<20} 4 套主题 2x2 拼接对比图")
        return 0

    selected = ALL_JOB_NAMES
    if args.only:
        wanted = [s.strip() for s in args.only.split(",") if s.strip()]
        unknown = [s for s in wanted if s not in ALL_JOB_NAMES]
        if unknown:
            print(f"未知任务名：{','.join(unknown)}，可用：{','.join(ALL_JOB_NAMES)}")
            return 1
        selected = wanted

    SHOWCASE.mkdir(parents=True, exist_ok=True)
    total = len(selected)
    done = 0

    try:
        for job in SIMPLE_JOBS:
            if job["name"] not in selected:
                continue
            done += 1
            print(f"[{done}/{total}] {job['name']}: {job['note']} ...", flush=True)
            result = run_simple(job, args.browser)
            px = result["pixels"]
            print(
                f"      -> {pathlib.Path(result['output']).relative_to(ROOT)}"
                f" ({px['width']}x{px['height']})"
            )

        if "themes-comparison" in selected:
            done += 1
            print(f"[{done}/{total}] themes-comparison: 4 套主题拼接 ...", flush=True)
            result = build_themes_comparison(args.browser)
            px = result["pixels"]
            print(
                f"      -> {pathlib.Path(result['output']).relative_to(ROOT)}"
                f" ({px['width']}x{px['height']})"
            )
    except (RuntimeError, ValueError) as exc:
        print(f"\n[FAILED] {exc}", file=sys.stderr)
        return 1

    print(f"\n完成：{done}/{total} 张截图已写入 {SHOWCASE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
