#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
qBittorrent WebUI mobile UI injector.

Usage:

    python3 editui.py qbittorrent-next-ui

Directory layout:

    root/
    ├── private/
    │   └── index.html
    │
    ├── public/
    │   └── index.html
    │
    ├── webui/
    │   └── qbittorrent-next-ui/
    │       └── index.html
    │
    └── editui.py

After processing:

    root/
    ├── private/
    │   ├── index.html
    │   └── webui/
    │       └── qbittorrent-next-ui/
    │           └── index.html
    │
    ├── public/
    │   ├── index.html
    │   └── webui/
    │       └── qbittorrent-next-ui/
    │           └── index.html
    │
    ├── webui/
    │   └── qbittorrent-next-ui/
    │
    └── editui.py

Behavior:

    private/index.html
        mobile -> /webui/<ui>/index.html
        desktop -> normal private UI

    public/index.html
        mobile -> /webui/<ui>/index.html
        desktop -> normal public UI

    private/webui/<ui>/index.html
        mobile -> stay here
        desktop -> /

    public/webui/<ui>/index.html
        mobile -> stay here
        desktop -> /

The original webui/<ui>/ directory is never modified.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent

PRIVATE_DIR = ROOT_DIR / "private"
PUBLIC_DIR = ROOT_DIR / "public"
WEBUI_DIR = ROOT_DIR / "webui"

PRIVATE_INDEX = PRIVATE_DIR / "index.html"
PUBLIC_INDEX = PUBLIC_DIR / "index.html"

PRIVATE_WEBUI_DIR = PRIVATE_DIR / "webui"
PUBLIC_WEBUI_DIR = PUBLIC_DIR / "webui"


# ============================================================
# Mobile detection JavaScript
# ============================================================

MOBILE_REDIRECT_TEMPLATE = r"""
<script>
(function () {
    "use strict";

    /*
     * ========================================================
     * qBittorrent Mobile UI Detector
     * ========================================================
     *
     * This detector is intentionally injected into:
     *
     *   private/index.html
     *   public/index.html
     *
     * and also:
     *
     *   private/webui/<ui>/index.html
     *   public/webui/<ui>/index.html
     *
     * The behavior depends on the current page:
     *
     *   Normal qBittorrent entry:
     *
     *       mobile  -> mobile UI
     *       desktop -> continue normally
     *
     *   Mobile UI:
     *
     *       mobile  -> stay here
     *       desktop -> return to /
     *
     * ========================================================
     */

    var ua =
        navigator.userAgent || "";

    var platform =
        navigator.platform || "";

    /*
     * --------------------------------------------------------
     * CSS logical viewport
     * --------------------------------------------------------
     */

    var viewportWidth =
        window.innerWidth || 0;

    var viewportHeight =
        window.innerHeight || 0;

    var clientWidth =
        document.documentElement &&
        document.documentElement.clientWidth
            ? document.documentElement.clientWidth
            : 0;

    var clientHeight =
        document.documentElement &&
        document.documentElement.clientHeight
            ? document.documentElement.clientHeight
            : 0;

    /*
     * --------------------------------------------------------
     * Screen information
     *
     * Used only as an additional signal for browser
     * device emulation.
     * --------------------------------------------------------
     */

    var screenWidth =
        screen.width || 0;

    var screenHeight =
        screen.height || 0;

    var dpr =
        window.devicePixelRatio || 1;

    var maxTouchPoints =
        navigator.maxTouchPoints || 0;

    /*
     * --------------------------------------------------------
     * UA detection
     * --------------------------------------------------------
     */

    var uaAndroid =
        /Android/i.test(ua);

    var uaIPhone =
        /iPhone/i.test(ua);

    var uaIPad =
        /iPad/i.test(ua);

    var uaIPod =
        /iPod/i.test(ua);

    var uaWindowsPhone =
        /Windows Phone/i.test(ua);

    var uaWebOS =
        /webOS/i.test(ua);

    var uaBlackBerry =
        /BlackBerry/i.test(ua);

    var uaIEMobile =
        /IEMobile/i.test(ua);

    var uaOperaMini =
        /Opera Mini/i.test(ua);

    var uaOperaMobi =
        /Opera Mobi/i.test(ua);

    var uaMobileKeyword =
        /Mobile/i.test(ua);

    var uaTabletKeyword =
        /Tablet/i.test(ua);

    var uaMobiKeyword =
        /Mobi/i.test(ua);

    var mobileUA =
        uaAndroid ||
        uaIPhone ||
        uaIPad ||
        uaIPod ||
        uaWindowsPhone ||
        uaWebOS ||
        uaBlackBerry ||
        uaIEMobile ||
        uaOperaMini ||
        uaOperaMobi;

    var mobileKeywordUA =
        uaMobileKeyword ||
        uaTabletKeyword ||
        uaMobiKeyword;

    /*
     * --------------------------------------------------------
     * Touch detection
     * --------------------------------------------------------
     */

    var hasOntouchstart =
        "ontouchstart" in window;

    var hasTouchPoints =
        maxTouchPoints > 0;

    var hasMSTouchPoints =
        (navigator.msMaxTouchPoints || 0) > 0;

    var touch =
        hasOntouchstart ||
        hasTouchPoints ||
        hasMSTouchPoints;

    /*
     * --------------------------------------------------------
     * CSS viewport classification
     * --------------------------------------------------------
     *
     * Uses CSS logical pixels.
     *
     * No fixed 524 × 829 style physical screen size
     * is used here.
     * --------------------------------------------------------
     */

    var viewportShortSide =
        Math.min(
            viewportWidth,
            viewportHeight
        );

    var viewportLongSide =
        Math.max(
            viewportWidth,
            viewportHeight
        );

    var portrait =
        viewportHeight >
        viewportWidth;

    var landscape =
        viewportWidth >
        viewportHeight;

    var veryNarrowViewport =
        viewportShortSide <= 480;

    var narrowViewport =
        viewportShortSide <= 600;

    var tabletViewport =
        viewportShortSide <= 768;

    /*
     * --------------------------------------------------------
     * Media queries
     * --------------------------------------------------------
     */

    var media600 = false;
    var media768 = false;
    var media1024 = false;

    if (window.matchMedia) {

        media600 =
            window.matchMedia(
                "(max-width: 600px)"
            ).matches;

        media768 =
            window.matchMedia(
                "(max-width: 768px)"
            ).matches;

        media1024 =
            window.matchMedia(
                "(max-width: 1024px)"
            ).matches;
    }

    /*
     * --------------------------------------------------------
     * Normal mobile CSS viewport
     * --------------------------------------------------------
     */

    var responsiveMobileViewport =
        narrowViewport &&
        portrait;

    /*
     * --------------------------------------------------------
     * Browser responsive/device emulation
     * --------------------------------------------------------
     *
     * Firefox responsive mode may produce:
     *
     *     viewport: 980 × 1642
     *     screen:    314 × 526
     *
     * Therefore detect an abnormal screen/viewport ratio.
     *
     * This is an additional signal only.
     * --------------------------------------------------------
     */

    var screenViewportWidthRatio = 0;
    var screenViewportHeightRatio = 0;

    if (
        viewportWidth > 0 &&
        viewportHeight > 0 &&
        screenWidth > 0 &&
        screenHeight > 0
    ) {

        screenViewportWidthRatio =
            screenWidth /
            viewportWidth;

        screenViewportHeightRatio =
            screenHeight /
            viewportHeight;
    }

    var emulatedMobileViewport =
        screenWidth > 0 &&
        screenHeight > 0 &&
        viewportWidth > 0 &&
        viewportHeight > 0 &&
        screenViewportWidthRatio < 0.6 &&
        screenViewportHeightRatio < 0.6;

    /*
     * --------------------------------------------------------
     * Final mobile decision
     * --------------------------------------------------------
     */

    var isMobile =
        mobileUA ||
        mobileKeywordUA ||
        responsiveMobileViewport ||
        emulatedMobileViewport;

    /*
     * --------------------------------------------------------
     * Detect whether we are already inside the mobile UI.
     * --------------------------------------------------------
     */

    var currentPath =
        window.location.pathname || "";

    var mobilePath =
        "/webui/__UI_NAME__/";

    var insideMobileUI =
        currentPath.indexOf(
            mobilePath
        ) !== -1;

    /*
     * --------------------------------------------------------
     * Decision reasons
     * --------------------------------------------------------
     */

    var reasons = [];

    if (mobileUA) {

        reasons.push(
            "mobile device UA"
        );
    }

    if (mobileKeywordUA) {

        reasons.push(
            "mobile UA keyword"
        );
    }

    if (responsiveMobileViewport) {

        reasons.push(
            "mobile-sized CSS viewport"
        );
    }

    if (emulatedMobileViewport) {

        reasons.push(
            "browser device emulation detected"
        );
    }

    /*
     * --------------------------------------------------------
     * Console diagnostics
     * --------------------------------------------------------
     */

    console.group(
        "%cqBittorrent Mobile UI Detector",
        "font-weight:bold;font-size:14px;"
    );

    console.log(
        "User Agent:",
        ua
    );

    console.log(
        "Platform:",
        platform
    );

    console.log(
        "Viewport (CSS px):",
        viewportWidth,
        "×",
        viewportHeight
    );

    console.log(
        "Document client (CSS px):",
        clientWidth,
        "×",
        clientHeight
    );

    console.log(
        "Screen (CSS px):",
        screenWidth,
        "×",
        screenHeight
    );

    console.log(
        "Device Pixel Ratio:",
        dpr
    );

    console.log(
        "maxTouchPoints:",
        maxTouchPoints
    );

    console.log(
        "--------------------------------"
    );

    console.log(
        "UA Android:",
        uaAndroid
    );

    console.log(
        "UA iPhone:",
        uaIPhone
    );

    console.log(
        "UA iPad:",
        uaIPad
    );

    console.log(
        "UA iPod:",
        uaIPod
    );

    console.log(
        "UA Windows Phone:",
        uaWindowsPhone
    );

    console.log(
        "UA Mobile keyword:",
        uaMobileKeyword
    );

    console.log(
        "UA Tablet keyword:",
        uaTabletKeyword
    );

    console.log(
        "UA Mobi keyword:",
        uaMobiKeyword
    );

    console.log(
        "mobileUA:",
        mobileUA
    );

    console.log(
        "mobileKeywordUA:",
        mobileKeywordUA
    );

    console.log(
        "--------------------------------"
    );

    console.log(
        "ontouchstart:",
        hasOntouchstart
    );

    console.log(
        "maxTouchPoints > 0:",
        hasTouchPoints
    );

    console.log(
        "msMaxTouchPoints > 0:",
        hasMSTouchPoints
    );

    console.log(
        "touch:",
        touch
    );

    console.log(
        "--------------------------------"
    );

    console.log(
        "CSS viewport short side:",
        viewportShortSide
    );

    console.log(
        "CSS viewport long side:",
        viewportLongSide
    );

    console.log(
        "portrait:",
        portrait
    );

    console.log(
        "landscape:",
        landscape
    );

    console.log(
        "max-width:600px:",
        media600
    );

    console.log(
        "max-width:768px:",
        media768
    );

    console.log(
        "max-width:1024px:",
        media1024
    );

    console.log(
        "short side <= 480:",
        veryNarrowViewport
    );

    console.log(
        "short side <= 600:",
        narrowViewport
    );

    console.log(
        "short side <= 768:",
        tabletViewport
    );

    console.log(
        "responsiveMobileViewport:",
        responsiveMobileViewport
    );

    console.log(
        "--------------------------------"
    );

    console.log(
        "screen/viewport width ratio:",
        screenViewportWidthRatio.toFixed(3)
    );

    console.log(
        "screen/viewport height ratio:",
        screenViewportHeightRatio.toFixed(3)
    );

    console.log(
        "emulatedMobileViewport:",
        emulatedMobileViewport
    );

    console.log(
        "--------------------------------"
    );

    console.log(
        "Current path:",
        currentPath
    );

    console.log(
        "Mobile UI path:",
        mobilePath
    );

    console.log(
        "Inside mobile UI:",
        insideMobileUI
    );

    console.log(
        "--------------------------------"
    );

    console.log(
        "RESULT:",
        isMobile
            ? "MOBILE"
            : "DESKTOP"
    );

    if (reasons.length > 0) {

        console.log(
            "DECISION REASONS:"
        );

        for (
            var i = 0;
            i < reasons.length;
            i++
        ) {

            console.log(
                "  •",
                reasons[i]
            );
        }

    }
    else {

        console.log(
            "DECISION REASONS: none"
        );
    }

    /*
     * --------------------------------------------------------
     * Redirect logic
     * --------------------------------------------------------
     */

    if (insideMobileUI) {

        /*
         * We are already inside the mobile UI.
         *
         * Mobile:
         *     stay here
         *
         * Desktop:
         *     return to normal qBittorrent entry point.
         */

        if (isMobile) {

            console.log(
                "Already inside mobile UI.",
                "Device is MOBILE, staying here."
            );

        }
        else {

            console.log(
                "%cDesktop detected inside mobile UI.",
                "font-weight:bold;"
            );

            console.log(
                "Returning to normal qBittorrent UI: /"
            );

            window.location.replace(
                "/"
            );
        }

    }
    else {

        /*
         * We are inside the normal private/public entry
         * page.
         *
         * Mobile:
         *     enter mobile UI
         *
         * Desktop:
         *     do nothing
         */

        if (isMobile) {

            var target =
                "./webui/__UI_NAME__/index.html";

            console.log(
                "REDIRECT TARGET:",
                target
            );

            console.log(
                "%cRedirecting to mobile UI...",
                "font-weight:bold;"
            );

            window.location.replace(
                target
            );

        }
        else {

            console.log(
                "Desktop detected.",
                "Continuing with normal qBittorrent UI."
            );
        }
    }

    console.groupEnd();

})();
</script>
"""


# ============================================================
# Helper functions
# ============================================================

def print_error(message: str) -> None:
    print(
        f"[ERROR] {message}",
        file=sys.stderr
    )


def print_info(message: str) -> None:
    print(
        f"[INFO]  {message}"
    )


def print_ok(message: str) -> None:
    print(
        f"[ OK ]  {message}"
    )


def backup_file(path: Path) -> Path:
    """
    Create a timestamped backup.
    """

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_path = path.with_name(
        f"{path.stem}.bak_{timestamp}{path.suffix}"
    )

    shutil.copy2(
        path,
        backup_path
    )

    return backup_path


def validate_ui_name(ui_name: str) -> None:
    """
    Prevent path traversal.

    Only a single directory name is allowed.
    """

    path = Path(ui_name)

    if (
        not ui_name
        or ui_name in {".", ".."}
        or path.is_absolute()
        or len(path.parts) != 1
        or path.name != ui_name
    ):
        raise ValueError(
            "UI 名称必须是 webui 目录下的单级文件夹名称，"
            "不能包含路径，例如：qbittorrent-next-ui"
        )


def get_ui_source(
    ui_name: str
) -> Path:

    return WEBUI_DIR / ui_name


def get_private_ui_target(
    ui_name: str
) -> Path:

    return PRIVATE_WEBUI_DIR / ui_name


def get_public_ui_target(
    ui_name: str
) -> Path:

    return PUBLIC_WEBUI_DIR / ui_name


# ============================================================
# Validate source UI
# ============================================================

def validate_source_ui(
    ui_name: str
) -> Path:

    source_dir = get_ui_source(
        ui_name
    )

    if not source_dir.exists():

        raise FileNotFoundError(
            f"找不到 UI 目录：{source_dir}"
        )

    if not source_dir.is_dir():

        raise NotADirectoryError(
            f"UI 路径不是目录：{source_dir}"
        )

    source_index = (
        source_dir /
        "index.html"
    )

    if not source_index.exists():

        raise FileNotFoundError(
            f"指定 UI 中不存在 index.html："
            f"{source_index}"
        )

    if not source_index.is_file():

        raise FileNotFoundError(
            f"指定 UI 的 index.html 不是普通文件："
            f"{source_index}"
        )

    return source_dir


# ============================================================
# Copy UI
# ============================================================

def copy_ui_to_target(
    source_dir: Path,
    target_dir: Path
) -> None:

    target_dir.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if target_dir.exists():

        print_info(
            f"删除旧 UI：{target_dir}"
        )

        if target_dir.is_dir():

            shutil.rmtree(
                target_dir
            )

        else:

            target_dir.unlink()

    print_info(
        f"复制 UI：{source_dir}"
    )

    shutil.copytree(
        source_dir,
        target_dir
    )

    print_ok(
        f"UI 已复制到：{target_dir}"
    )


def copy_ui_to_private_and_public(
    ui_name: str
) -> tuple[Path, Path, Path]:

    source_dir = validate_source_ui(
        ui_name
    )

    private_target = get_private_ui_target(
        ui_name
    )

    public_target = get_public_ui_target(
        ui_name
    )

    print_info(
        "========================================"
    )

    print_info(
        "复制到 private/"
    )

    copy_ui_to_target(
        source_dir,
        private_target
    )

    print_info(
        "复制到 public/"
    )

    copy_ui_to_target(
        source_dir,
        public_target
    )

    return (
        source_dir,
        private_target,
        public_target
    )


# ============================================================
# HTML helpers
# ============================================================

def find_html_head(
    html: str
) -> tuple[int, int]:

    lower = html.lower()

    start = lower.find(
        "<head"
    )

    if start == -1:

        raise ValueError(
            "index.html 中找不到 <head> 标签"
        )

    end = lower.find(
        ">",
        start
    )

    if end == -1:

        raise ValueError(
            "index.html 中的 <head> 标签不完整"
        )

    return (
        start,
        end + 1
    )


def remove_previous_redirect(
    html: str
) -> str:

    marker_start = (
        "<!-- "
        "QBITTORRENT MOBILE UI REDIRECT START"
        " -->"
    )

    marker_end = (
        "<!-- "
        "QBITTORRENT MOBILE UI REDIRECT END"
        " -->"
    )

    while (
        marker_start in html
        and
        marker_end in html
    ):

        start = html.find(
            marker_start
        )

        end = html.find(
            marker_end,
            start
        )

        if end == -1:

            break

        end += len(
            marker_end
        )

        html = (
            html[:start]
            +
            html[end:]
        )

    return html


def build_redirect_script(
    ui_name: str
) -> str:

    return MOBILE_REDIRECT_TEMPLATE.replace(
        "__UI_NAME__",
        ui_name
    )


# ============================================================
# Inject detector
# ============================================================

def inject_detector(
    html: str,
    ui_name: str
) -> str:

    html = remove_previous_redirect(
        html
    )

    _, head_end = find_html_head(
        html
    )

    script = build_redirect_script(
        ui_name
    )

    block = (
        "\n"
        "<!-- "
        "QBITTORRENT MOBILE UI REDIRECT START"
        " -->\n"
        f"{script}\n"
        "<!-- "
        "QBITTORRENT MOBILE UI REDIRECT END"
        " -->\n"
    )

    return (
        html[:head_end]
        +
        block
        +
        html[head_end:]
    )


# ============================================================
# Process a single HTML file
# ============================================================

def process_html(
    path: Path,
    ui_name: str
) -> None:

    if not path.exists():

        raise FileNotFoundError(
            f"找不到文件：{path}"
        )

    if not path.is_file():

        raise FileNotFoundError(
            f"不是普通文件：{path}"
        )

    print_info(
        f"读取：{path}"
    )

    try:

        html = path.read_text(
            encoding="utf-8"
        )

    except UnicodeDecodeError as exc:

        raise UnicodeDecodeError(
            exc.encoding,
            exc.object,
            exc.start,
            exc.end,
            f"{path} 不是有效的 UTF-8 文件"
        ) from exc

    original_html = html

    html = inject_detector(
        html,
        ui_name
    )

    if html == original_html:

        raise RuntimeError(
            f"注入失败：{path} 没有发生变化"
        )

    backup_path = backup_file(
        path
    )

    print_ok(
        f"原文件已备份：{backup_path.name}"
    )

    path.write_text(
        html,
        encoding="utf-8"
    )

    print_ok(
        f"检测器已注入：{path}"
    )


# ============================================================
# Process normal entry pages
# ============================================================

def process_entry_pages(
    ui_name: str
) -> None:

    print()
    print(
        "========================================"
    )
    print(
        "处理 private/public 入口页面"
    )
    print(
        "========================================"
    )

    process_html(
        PRIVATE_INDEX,
        ui_name
    )

    process_html(
        PUBLIC_INDEX,
        ui_name
    )


# ============================================================
# Process copied mobile UI pages
# ============================================================

def process_mobile_ui_pages(
    ui_name: str,
    private_ui_dir: Path,
    public_ui_dir: Path
) -> None:

    print()
    print(
        "========================================"
    )
    print(
        "处理 private/public 手机 UI"
    )
    print(
        "========================================"
    )

    private_mobile_index = (
        private_ui_dir /
        "index.html"
    )

    public_mobile_index = (
        public_ui_dir /
        "index.html"
    )

    process_html(
        private_mobile_index,
        ui_name
    )

    process_html(
        public_mobile_index,
        ui_name
    )


# ============================================================
# Main
# ============================================================

def main() -> int:

    parser = argparse.ArgumentParser(
        description=(
            "复制指定 qBittorrent WebUI 到 "
            "private/webui 和 public/webui，"
            "并给 private/public 的入口页面以及"
            "两个手机 UI 页面注入移动设备检测器。"
        )
    )

    parser.add_argument(
        "ui_name",
        help=(
            "webui 目录下的 UI 文件夹名称，例如："
            "qbittorrent-next-ui"
        )
    )

    args = parser.parse_args()

    ui_name = args.ui_name.strip()

    try:

        # ----------------------------------------------------
        # Validate
        # ----------------------------------------------------

        validate_ui_name(
            ui_name
        )

        # ----------------------------------------------------
        # Make sure private/public directories exist
        # ----------------------------------------------------

        if not PRIVATE_DIR.exists():

            raise FileNotFoundError(
                f"找不到 private 目录："
                f"{PRIVATE_DIR}"
            )

        if not PUBLIC_DIR.exists():

            raise FileNotFoundError(
                f"找不到 public 目录："
                f"{PUBLIC_DIR}"
            )

        # ----------------------------------------------------
        # Copy UI to both locations
        # ----------------------------------------------------

        (
            source_dir,
            private_ui_dir,
            public_ui_dir
        ) = copy_ui_to_private_and_public(
            ui_name
        )

        # ----------------------------------------------------
        # Inject detectors into:
        #
        #   private/index.html
        #   public/index.html
        # ----------------------------------------------------

        process_entry_pages(
            ui_name
        )

        # ----------------------------------------------------
        # Inject detectors into:
        #
        #   private/webui/<ui>/index.html
        #   public/webui/<ui>/index.html
        # ----------------------------------------------------

        process_mobile_ui_pages(
            ui_name,
            private_ui_dir,
            public_ui_dir
        )

    except KeyboardInterrupt:

        print_error(
            "操作已取消"
        )

        return 130

    except Exception as exc:

        print_error(
            str(exc)
        )

        return 1

    print()
    print(
        "========================================"
    )
    print(
        "处理完成"
    )
    print(
        "========================================"
    )

    print(
        f"源 UI："
        f"       {source_dir}"
    )

    print(
        f"Private UI："
        f"  {private_ui_dir}"
    )

    print(
        f"Public UI："
        f"   {public_ui_dir}"
    )

    print()
    print(
        "已注入检测器："
    )

    print(
        f"  {PRIVATE_INDEX}"
    )

    print(
        f"  {PUBLIC_INDEX}"
    )

    print(
        f"  {private_ui_dir / 'index.html'}"
    )

    print(
        f"  {public_ui_dir / 'index.html'}"
    )

    print()
    print(
        "手机："
    )

    print(
        f"  / -> /webui/{ui_name}/index.html"
    )

    print()
    print(
        "电脑："
    )

    print(
        "  手机 UI -> /"
    )

    print(
        "  普通 UI -> 保持原页面"
    )

    print(
        "========================================"
    )

    return 0


if __name__ == "__main__":
    sys.exit(
        main()
    )