# playwright-snapper

## Usage

1. Preferably set up a virtualenv, as you do for a Python project.
2. Install `playwright`:
   1. `pip install playwright`
   2. `playwright install`
3. Run the script:
   1. `python playwright-snapper.py -d snapshots https://akx.github.io`
   2. `snapshots/` will now contain PNG and PDF files.
   3. The script will not overwrite pre-existing files.

### Shell protip!

To run the script against multiple URLs in a text file, use `xargs`:

`cat urls.txt | xargs python playwright-snapper.py -d snapshots`

### TODO

Pull requests welcome. :-)

* This script could be made more efficient by not using `playwright screenshot` etc.,
  but the Playwright Python API instead, so the same session is used for both the screenshot
  and the PDF.
* The script could be made multi-threaded, so each URL is processed in parallel.
