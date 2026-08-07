import os
import time
from bs4 import BeautifulSoup
from curl_cffi import requests

BASE_URL = "https://novelfull.com"
NOVEL_URL = f"{BASE_URL}/shadow-slave.html"
OUTPUT_DIR = "/home/darwin/Novis/shadow-slave/shadow-slave"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": BASE_URL,
}

def get_soup(session, url):
    response = session.get(url, headers=HEADERS, impersonate="chrome120", timeout=15)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def get_novel_id(soup):
    """Extracts novel ID needed for the AJAX chapter list."""
    novel_input = soup.find("input", {"id": "novel_id"})
    if novel_input and novel_input.get("value"):
        return novel_input["value"]
    
    # Fallback search inside scripts
    for script in soup.find_all("script"):
        if script.string and "novelId" in script.string:
            for line in script.string.split("\n"):
                if "novelId" in line:
                    return line.split("=")[-1].replace(";", "").strip().strip("'\"")
    return None

def get_all_chapter_links(session, novel_url):
    print("Fetching novel main page...")
    soup = get_soup(session, novel_url)
    
    novel_id = get_novel_id(soup)
    all_links = []

    if novel_id:
        print(f"Found Novel ID: {novel_id}. Fetching full chapter list via AJAX...")
        ajax_url = f"{BASE_URL}/ajax-chapter-option?novelId={novel_id}"
        ajax_soup = get_soup(session, ajax_url)
        
        for option in ajax_soup.find_all("option"):
            href = option.get("value")
            chap_title = option.text.strip()
            if href:
                chap_url = href if href.startswith("http") else BASE_URL + href
                all_links.append((chap_title, chap_url))
        return all_links

    # Fallback to pagination scraping if AJAX fails
    print("AJAX ID not found. Falling back to page parsing...")
    page_num = 1
    while True:
        page_url = f"{novel_url}?page={page_num}&per-page=50"
        soup = get_soup(session, page_url)
        container = soup.find("div", id="list-chapter")
        if not container:
            break

        anchors = container.find_all("a")
        if not anchors:
            break

        new_count = 0
        for a in anchors:
            chap_title = a.text.strip()
            href = a.get("href", "")
            chap_url = href if href.startswith("http") else BASE_URL + href
            if chap_url not in [l[1] for l in all_links]:
                all_links.append((chap_title, chap_url))
                new_count += 1

        if new_count == 0 or not soup.select_one("li.next a"):
            break
        page_num += 1

    return all_links

def scrape_chapter(session, url):
    soup = get_soup(session, url)
    content_div = soup.find("div", id="chapter-content")
    if not content_div:
        return ""

    for bad_tag in content_div.find_all(["script", "ins", "style", "div"]):
        bad_tag.decompose()

    paragraphs = content_div.find_all("p")
    if paragraphs:
        text_lines = [p.text.strip() for p in paragraphs if p.text.strip()]
        return "\n\n".join(text_lines)

    return content_div.text.strip()

def get_max_downloaded_index(output_dir):
    """Finds the highest numbered file prefix in the output directory."""
    if not os.path.exists(output_dir):
        return 0
    indices = []
    for filename in os.listdir(output_dir):
        if filename.endswith(".txt") and " - " in filename:
            prefix = filename.split(" - ", 1)[0]
            if prefix.isdigit():
                indices.append(int(prefix))
    return max(indices) if indices else 0

def save_chapter(output_dir, index, title, content):
    os.makedirs(output_dir, exist_ok=True)
    safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).strip()
    filename = f"{index:04d} - {safe_title}.txt"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"{title}\n\n{content}")
    print(f"  Saved: {filename}")

def main():
    session = requests.Session()
    
    print(f"Targeting: {NOVEL_URL}")
    print(f"Saving to: {OUTPUT_DIR}\n")

    chapters = get_all_chapter_links(session, NOVEL_URL)
    print(f"\nTotal Chapters Found: {len(chapters)}\n")

    if not chapters:
        print("No chapters found.")
        return

    # Determine last downloaded index
    max_index = get_max_downloaded_index(OUTPUT_DIR)
    print(f"Highest chapter index found on disk: {max_index}")

    if max_index >= len(chapters):
        print("All chapters are already downloaded!")
        return

    # Slice list to pick up right where it left off
    chapters_to_download = chapters[max_index:]
    print(f"Resuming download from chapter {max_index + 1} of {len(chapters)}...\n")

    failed = []

    for i, (chap_title, chap_url) in enumerate(chapters_to_download, start=max_index + 1):
        print(f"[{i}/{len(chapters)}] Downloading: {chap_title}")
        try:
            content = scrape_chapter(session, chap_url)
            if content:
                save_chapter(OUTPUT_DIR, i, chap_title, content)
            else:
                print("  Warning: Empty content.")
                failed.append((i, chap_title, chap_url))
        except Exception as e:
            print(f"  Error: {e}")
            failed.append((i, chap_title, chap_url))
            
        time.sleep(0.4)

    print(f"\nDone: {len(chapters_to_download) - len(failed)} downloaded | {max_index} skipped | {len(failed)} failed")

if __name__ == "__main__":
    main()