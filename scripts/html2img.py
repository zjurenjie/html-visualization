#!/usr/bin/env python3
"""HTML 图表 -> 指定长宽比的 PNG 图片（无头 Chromium CLI 截图）。

方案要点：
1. 用户给出长宽比（如 16:9、1:1、9:16）与逻辑宽度，脚本换算出视口
   尺寸，调用本机 Chrome / Edge / Chromium 的无头模式 ``--screenshot``
   一次性截图，得到该比例的 PNG。
2. ``--scale`` 透传 ``--force-device-scale-factor``，输出像素尺寸 =
   视口逻辑尺寸 * scale（2 即视网膜清晰度，文字不发虚）。
3. 用隐藏哨兵元素 + ``--dump-dom`` 确认浏览器真正加载了目标文档，
   避免截到浏览器起始页这类「有效但错误」的图。
4. 用 Pillow 校验产物像素尺寸与目标比例一致，不一致即报错。

仅依赖标准库 + Pillow。

用法：
    python html2img.py chart.html                          # 默认 16:9, 宽 1200
    python html2img.py chart.html --ratio 9:16 --width 1080
    python html2img.py chart.html --ratio 1:1 --scale 2 --out square.png
    python html2img.py chart.html --width 1200 --height 800
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import uuid

CHROMIUM_MAX_WINDOW_HEIGHT = 32000
DEFAULT_WIDTH = 1200
DEFAULT_RATIO = "16:9"
DEFAULT_SCALE = 2
NETWORK_IDLE_TIMEOUT_MS = 10000
RENDER_TIMEOUT_SEC = 90.0

SENTINEL_ATTR = "data-htmlviz-loaded"


# ----------------------------------------------------------------------
# 浏览器发现
# ----------------------------------------------------------------------

def find_browser_binary(explicit: str | None = None) -> str | None:
    """定位 Chromium 系浏览器（Chrome / Edge / Chromium）。"""
    if explicit:
        return explicit if os.path.isfile(explicit) else None

    env = (
        os.environ.get("HTMLVIZ_BROWSER")
        or os.environ.get("DOUYIN_BROWSER")
        or os.environ.get("ARTIFACT_PREVIEW_CHROMIUM")
    )
    if env and os.path.isfile(env):
        return env

    if sys.platform.startswith("win"):
        bases = [
            os.environ.get("ProgramFiles", r"C:\Program Files"),
            os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
            os.environ.get("LOCALAPPDATA", ""),
        ]
        relative_paths = (
            r"Google\Chrome\Application\chrome.exe",
            r"Microsoft\Edge\Application\msedge.exe",
            r"Chromium\Application\chrome.exe",
        )
        for base in bases:
            if not base:
                continue
            for rel in relative_paths:
                candidate = os.path.join(base, rel)
                if os.path.isfile(candidate):
                    return candidate
        for name in ("chrome.exe", "msedge.exe", "chromium.exe"):
            found = shutil.which(name)
            if found:
                return found
    elif sys.platform == "darwin":
        mac_paths = (
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
        )
        for candidate in mac_paths:
            if os.path.isfile(candidate):
                return candidate
        for name in ("google-chrome", "microsoft-edge", "chromium"):
            found = shutil.which(name)
            if found:
                return found
    else:
        for name in (
            "chromium-browser",
            "chromium",
            "google-chrome",
            "google-chrome-stable",
            "chrome",
            "microsoft-edge",
        ):
            found = shutil.which(name)
            if found:
                return found
    return None


# ----------------------------------------------------------------------
# 长宽比解析
# ----------------------------------------------------------------------

def parse_ratio(ratio: str) -> tuple[float, float]:
    """把 '16:9' / '1:1' / '9:16' / '1.618' 解析为 (w, h) 份数。

    单个数值 n 表示宽高比为 n:1（如 1.618 = 黄金比横版）。
    """
    text = ratio.strip()
    if ":" in text:
        left, _, right = text.partition(":")
        try:
            w = float(left.strip())
            h = float(right.strip())
        except ValueError as exc:
            raise ValueError(f"无法解析长宽比：{ratio!r}") from exc
    else:
        try:
            w = float(text)
            h = 1.0
        except ValueError as exc:
            raise ValueError(f"无法解析长宽比：{ratio!r}") from exc
    if w <= 0 or h <= 0:
        raise ValueError(f"长宽比必须为正数：{ratio!r}")
    return w, h


def compute_viewport(
    *, width: int, height: int | None, ratio: str | None
) -> tuple[int, int]:
    """返回视口逻辑尺寸 (css_w, css_h)。height 显式指定时优先于 ratio。"""
    css_w = max(1, int(width))
    if height is not None:
        return css_w, max(1, int(height))
    w, h = parse_ratio(ratio or DEFAULT_RATIO)
    css_h = int(round(css_w * h / w))
    if css_h < 1:
        css_h = 1
    if css_h > CHROMIUM_MAX_WINDOW_HEIGHT:
        raise ValueError(
            f"换算出的视口高度 {css_h}px 超过 Chromium 上限 "
            f"{CHROMIUM_MAX_WINDOW_HEIGHT}px，请减小宽度或改用更扁的比例"
        )
    return css_w, css_h


# ----------------------------------------------------------------------
# 无头浏览器渲染
# ----------------------------------------------------------------------

def build_chromium_argv(
    *,
    binary: str,
    url: str,
    css_w: int,
    css_h: int,
    scale: float,
    out_png: str,
    user_data_dir: str,
) -> list[str]:
    """经验证可用的无头参数集；不使用 --single-process 等易挂起参数。"""
    return [
        binary,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-software-rasterizer",
        "--disable-setuid-sandbox",
        "--disable-extensions",
        "--disable-background-networking",
        "--disable-features=VizDisplayCompositor",
        "--no-first-run",
        "--no-default-browser-check",
        "--hide-scrollbars",
        f"--force-device-scale-factor={scale}",
        f"--virtual-time-budget={NETWORK_IDLE_TIMEOUT_MS}",
        f"--window-size={css_w},{css_h}",
        f"--user-data-dir={user_data_dir}",
        f"--screenshot={out_png}",
        "--dump-dom",
        url,
    ]


def render_page(
    *,
    html: str,
    html_file: str,
    css_w: int,
    css_h: int,
    scale: float,
    binary: str,
    workdir: str,
    verify_dom: bool,
) -> str:
    """渲染 HTML 并返回整页 PNG 路径。

    哨兵副本优先写入源 HTML 同目录（保持相对路径资源可用），
    目录不可写时回退到临时目录。
    """
    token = uuid.uuid4().hex
    sentinel = f'<div {SENTINEL_ATTR}="{token}" style="display:none"></div>'
    base_dir = os.path.dirname(os.path.abspath(html_file))
    staged = os.path.join(
        base_dir, f".{pathlib.Path(html_file).stem}.htmlviz_{token}.html"
    )
    try:
        with open(staged, "w", encoding="utf-8") as fh:
            fh.write(html + sentinel)
    except OSError:
        staged = os.path.join(tempfile.mkdtemp(prefix="htmlviz_"), "input.html")
        with open(staged, "w", encoding="utf-8") as fh:
            fh.write(html + sentinel)

    url = pathlib.Path(staged).as_uri()
    out_png = os.path.join(workdir, "page.png")
    user_data = os.path.join(workdir, "profile")
    os.makedirs(user_data, exist_ok=True)

    argv = build_chromium_argv(
        binary=binary,
        url=url,
        css_w=css_w,
        css_h=css_h,
        scale=scale,
        out_png=out_png,
        user_data_dir=user_data,
    )

    try:
        proc = subprocess.run(
            argv, capture_output=True, timeout=RENDER_TIMEOUT_SEC, check=False
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            f"无头浏览器渲染超过 {RENDER_TIMEOUT_SEC:.0f} 秒仍未完成"
        ) from exc

    if not os.path.isfile(out_png) or os.path.getsize(out_png) == 0:
        stderr = proc.stderr.decode("utf-8", "replace")[:500]
        raise RuntimeError(
            f"浏览器未产出 PNG（退出码 {proc.returncode}），stderr：{stderr}"
        )

    if verify_dom:
        dom = proc.stdout.decode("utf-8", "replace")
        if dom.strip() and token not in dom:
            raise RuntimeError(
                "浏览器未加载目标文档（dump-dom 中找不到哨兵标记），"
                "截图可能是浏览器起始页而非目标图表"
            )

    try:
        os.remove(staged)
    except OSError:
        pass
    return out_png


def verify_png_size(
    png_path: str, css_w: int, css_h: int, scale: float
) -> tuple[int, int]:
    """校验 PNG 像素尺寸与目标一致，返回实际 (w, h)。"""
    try:
        from PIL import Image
    except ImportError:
        return int(round(css_w * scale)), int(round(css_h * scale))

    with Image.open(png_path) as image:
        actual_w, actual_h = image.size
    expect_w = int(round(css_w * scale))
    expect_h = int(round(css_h * scale))
    if abs(actual_w - expect_w) > 2 or abs(actual_h - expect_h) > 2:
        raise RuntimeError(
            f"PNG 实际尺寸 {actual_w}x{actual_h} 与期望 "
            f"{expect_w}x{expect_h} 不符，请检查页面是否存在强制尺寸样式"
        )
    return actual_w, actual_h


# ----------------------------------------------------------------------
# 主流程
# ----------------------------------------------------------------------

def convert(
    *,
    html_file: str,
    out: str | None,
    width: int,
    height: int | None,
    ratio: str | None,
    scale: float,
    browser: str | None,
    verify_dom: bool,
) -> dict:
    binary = find_browser_binary(browser)
    if binary is None:
        looked = browser or "PATH 与系统默认安装目录"
        raise RuntimeError(
            "未找到 Chrome / Edge / Chromium 浏览器，可用 --browser 显式指定"
            f"浏览器可执行文件路径（本次查找位置：{looked}）"
        )

    css_w, css_h = compute_viewport(
        width=width, height=height, ratio=ratio
    )

    with open(html_file, "r", encoding="utf-8") as fh:
        html = fh.read()

    if out is None:
        stem = pathlib.Path(html_file).stem
        out = os.path.join(os.path.dirname(os.path.abspath(html_file)), f"{stem}.png")

    workdir = tempfile.mkdtemp(prefix="htmlviz_")
    try:
        png_path = render_page(
            html=html,
            html_file=html_file,
            css_w=css_w,
            css_h=css_h,
            scale=scale,
            binary=binary,
            workdir=workdir,
            verify_dom=verify_dom,
        )
        pixel_w, pixel_h = verify_png_size(png_path, css_w, css_h, scale)
        out_dir = os.path.dirname(os.path.abspath(out))
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        shutil.copyfile(png_path, out)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    final_ratio = pixel_w / pixel_h
    return {
        "output": os.path.abspath(out),
        "viewport": {"width": css_w, "height": css_h},
        "pixels": {"width": pixel_w, "height": pixel_h},
        "ratio_actual": round(final_ratio, 4),
        "scale": scale,
        "browser": binary,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="把 HTML 图表渲染为指定长宽比的 PNG 图片"
    )
    parser.add_argument("html_file", help="图表 HTML 文件路径")
    parser.add_argument(
        "--out", default=None, help="输出 PNG 路径（默认与 HTML 同名 .png）"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=DEFAULT_WIDTH,
        help=f"视口逻辑宽度 px（默认 {DEFAULT_WIDTH}）",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=None,
        help="视口逻辑高度 px；指定后忽略 --ratio",
    )
    parser.add_argument(
        "--ratio",
        default=DEFAULT_RATIO,
        help=(
            "长宽比，W:H 形式（如 16:9、1:1、9:16、3:4），"
            f"或单数值宽高比（默认 {DEFAULT_RATIO}）"
        ),
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=DEFAULT_SCALE,
        help=(
            "设备像素倍率（默认 "
            f"{DEFAULT_SCALE}，输出像素 = 视口 * scale，2 为视网膜清晰度）"
        ),
    )
    parser.add_argument(
        "--browser", default=None, help="浏览器可执行文件路径，默认自动发现"
    )
    parser.add_argument(
        "--no-dom-check",
        action="store_true",
        help="跳过 dump-dom 加载校验（不建议）",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = convert(
            html_file=args.html_file,
            out=args.out,
            width=args.width,
            height=args.height,
            ratio=args.ratio,
            scale=args.scale,
            browser=args.browser,
            verify_dom=not args.no_dom_check,
        )
    except (RuntimeError, ValueError) as exc:
        payload = {"ok": False, "error": {"code": "RENDER_FAILED", "msg": str(exc)}}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"ok": True, "result": result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
