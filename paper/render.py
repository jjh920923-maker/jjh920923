"""src/*.html 을 300dpi PNG로 렌더링해 png/ 에 저장합니다.

사용법:  python3 paper/render.py
필요:    pip install playwright && playwright install chromium
"""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent
SRC, OUT = ROOT / "src", ROOT / "png"
SCALE = 300 / 96  # 96dpi 기준 px → 300dpi

PAGES = {
    "outside": (944, 661),   # 청첩장 바깥면 250×175mm
    "inside": (944, 661),    # 청첩장 안쪽면 250×175mm
    "ticket": (340, 189),    # 식권 90×50mm
}


def main():
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as p:
        launch = {}
        chrome = pathlib.Path("/usr/bin/google-chrome")
        if chrome.exists():
            launch["executable_path"] = str(chrome)
        browser = p.chromium.launch(**launch)
        for name, (w, h) in PAGES.items():
            page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=SCALE)
            page.goto((SRC / f"{name}.html").as_uri(), wait_until="load", timeout=15000)
            page.evaluate("document.fonts.ready")
            page.screenshot(path=str(OUT / f"{name}.png"), clip={"x": 0, "y": 0, "width": w, "height": h})
            print("saved", OUT / f"{name}.png")
        browser.close()


if __name__ == "__main__":
    main()
