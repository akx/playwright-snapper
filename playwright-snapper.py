import argparse
import os
import re
import shutil
import subprocess
from urllib.parse import urlparse

PLAYWRIGHT_BINARY = shutil.which("playwright")


def get_filename_from_url(url: str) -> str:
    parsed_url = urlparse(url)
    dirty_filename = parsed_url.netloc
    if parsed_url.path.strip("/"):
        dirty_filename += "__" + parsed_url.path.strip("/")
    filename_base = re.sub(r"\W+", "_", dirty_filename)
    return filename_base


def process_url(dest_dir: str, url: str, *, timeout: int) -> None:
    filename_base = get_filename_from_url(url)
    pdf_filename = os.path.join(dest_dir, f"{filename_base}.pdf")
    png_filename = os.path.join(dest_dir, f"{filename_base}.png")
    if not os.path.isfile(png_filename):
        print(f"Generating {png_filename}")
        subprocess.check_call(
            [
                PLAYWRIGHT_BINARY,
                "screenshot",
                "--full-page",
                "--wait-for-timeout",
                str(timeout),
                url,
                png_filename,
            ]
        )
    if not os.path.isfile(pdf_filename):
        print(f"Generating {pdf_filename}")
        subprocess.check_call(
            [
                PLAYWRIGHT_BINARY,
                "pdf",
                "--wait-for-timeout",
                str(timeout),
                url,
                pdf_filename,
            ]
        )


def main() -> None:
    assert PLAYWRIGHT_BINARY, "playwright not found"
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="+")
    ap.add_argument("-d", "--dest-dir", required=True)
    ap.add_argument(
        "-t", "--timeout", type=int, default=5000, help="wait this many milliseconds"
    )
    args = ap.parse_args()
    dest_dir = args.dest_dir
    os.makedirs(dest_dir, exist_ok=True)
    for url in args.urls:
        process_url(dest_dir, url, timeout=args.timeout)


if __name__ == "__main__":
    main()
