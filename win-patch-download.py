from playwright.sync_api import sync_playwright, Playwright, TimeoutError
import argparse
import os
import requests
from datetime import datetime
import re
import logging

WAIT_TIMEOUT = 3000  # Adjust the timeout value (in milliseconds) to a shorter duration if needed


def configure_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
    logger = logging.getLogger()
    logger.handlers[0].setFormatter(logging.Formatter("%(asctime)s - %(message)s"))


def handle_no_search_results(page, context, browser, search_keyword):
    logging.info(f"No search results found: {search_keyword}")
    context.close()
    browser.close()


def handle_download_button_not_found(page, context, browser, search_keyword):
    logging.info(f"Failed to find the Download button: {search_keyword}")
    context.close()
    browser.close()


def download_msu_file(page, popup, download_path, month):
    msu_link = popup.wait_for_selector("#downloadFiles > div:nth-child(3) > a", timeout=WAIT_TIMEOUT)
    if msu_link:
        msu_url = msu_link.get_attribute("href")
        logging.info(f"Downloading MSU/CAB file: {msu_url}")

        # Extract the filename from the URL
        file_name = os.path.basename(msu_url)
        month_suffix = datetime.strptime(month, "%Y-%m").strftime("%Y%m")

        # Use regular expressions to match the original filename pattern
        pattern = r"windows\d+\.\d+-kb\d+-x64_\w+\.(msu|cab)"
        match = re.search(pattern, file_name)

        if match:
            original_name = match.group(0)
            new_file_name = re.sub(r"-x64_\w+", "-{}".format(month_suffix), original_name)
            file_path = os.path.join(download_path, new_file_name)

            # Download the file using requests library
            response = requests.get(msu_url)
            if response.status_code == 200:
                with open(file_path, "wb") as file:
                    file.write(response.content)
                logging.info(f"Download completed. File saved at: {file_path}")
            else:
                logging.info("Failed to download the file.")
        else:
            logging.info("Failed to match the filename pattern.")
    else:
        logging.info("Failed to find the MSU/CAB download link.")


def run(playwright: Playwright, search_keyword: str, month: str, download_path: str, headless: bool) -> None:
    browser = playwright.chromium.launch(headless=headless)  # Run in headless mode
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.catalog.update.microsoft.com/")
    page.goto("https://www.catalog.update.microsoft.com/Home.aspx")
    page.get_by_role("row", name="Search Search", exact=True).get_by_role("cell", name="Search Search").click()

    new_search_keyword = f"{month} {search_keyword}"
    page.get_by_role("textbox", name="Search Search").fill(new_search_keyword)
    page.get_by_role("button", name="Search").click()

    # Check if search results are empty or error
    try:
        page.wait_for_selector("span#ctl00_catalogBody_noResultText", state="visible", timeout=WAIT_TIMEOUT)
        handle_no_search_results(page, context, browser, new_search_keyword)
        return
    except TimeoutError:
        pass

    # Click the "Download" button of the first row
    try:
        first_row_download_button = page.wait_for_selector(
            "tr:nth-child(1) input[type='button'][value='Download']", state="visible", timeout=WAIT_TIMEOUT
        )
    except TimeoutError:
        handle_download_button_not_found(page, context, browser, new_search_keyword)
        return

    if first_row_download_button:
        first_row_download_button.click()

        with page.expect_popup() as popup_info:
            pass

        popup = popup_info.value
        download_msu_file(page, popup, download_path, month)

    context.close()
    browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Windows OS Patch Download and Install",
        epilog="Examples:\n"
        "1. win-patch-download.py\n"
        "2. win-patch-download.py -month '2023-06'\n"
        "3. win-patch-download.py -month '2023-06' -headless False\n"
        "4. win-patch-download.py -search 'Cumulative Update for Windows Server 2016 for x64-based Systems' -month '2023-06' -downloadpath 'C:\\cdrive'\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-search",
        help="Search keyword",
        default="Cumulative Update for Windows Server 2016 for x64-based Systems",
    )
    parser.add_argument("-month", help="Month in format YYYY-MM", default=datetime.now().strftime("%Y-%m"))
    parser.add_argument("-downloadpath", help="Download path", default="c:\\cdrive")
    parser.add_argument(
        "-headless",
        help="Run in headless mode (default: True)",
        default="True",
        choices=["True", "False"],
    )
    args = parser.parse_args()

    configure_logging()

    try:
        with sync_playwright() as playwright:
            run(playwright, args.search, args.month, args.downloadpath, args.headless == "True")
    except Exception as e:
        logging.exception("An error occurred during script execution.")
