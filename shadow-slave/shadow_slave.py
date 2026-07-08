import requests
from bs4 import BeautifulSoup
import time
import os

BASE_URL = "https://allnovel.org"
NOVEL_URL = f"{BASE_URL}/shadow-slave.html"
OUTPUT_DIR = "shadow-slave"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

def get_soup(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def get_novel_info(soup):
    title = soup.find("meta", {"name": "title"})["content"].strip()
    description = soup.find("meta", {"name": "description"})["content"].strip()
    return title, description

def get_all_chapter_links(novel_url):
    all_links = []
    page = 1

    base = novel_url.rstrip("/")

    while True:
        url = f"{base}?page={page}"
        print(f"  Fetching page {page}: {url}")
        soup = get_soup(url)

        chapter_list = soup.find("ul", class_="list-chapter")
        if not chapter_list:
            print("  No chapter list found, stopping.")
            break

        links = []
        for li in chapter_list.find_all("li"):
            a = li.find("a")
            if not a:
                continue
            chapter_title = a.find("span", class_="chapter-text")
            chapter_title = chapter_title.text.strip() if chapter_title else a.text.strip()
            chapter_url = BASE_URL + a["href"]
            links.append((chapter_title, chapter_url))

        if not links:
            print("  No links found, stopping.")
            break

        all_links.extend(links)
        print(f"  Got {len(links)} chapters (total so far: {len(all_links)})")

        pagination = soup.find("ul", class_="pagination")
        if not pagination:
            print("  No pagination found, stopping.")
            break

        next_page = pagination.find("a", string=">")
        if not next_page:
            print("  No next page button found, stopping.")
            break

        page += 1
        time.sleep(1)

    return all_links

def scrape_chapter(url):
    soup = get_soup(url)
    content_div = soup.find("div", class_="chapter-c")
    if not content_div:
        return ""
    paragraphs = content_div.find_all("p")
    return "\n\n".join(p.text.strip() for p in paragraphs)

def save_chapter(output_dir, index, title, content):
    os.makedirs(output_dir, exist_ok=True)
    safe_title = title.replace("/", "-").replace("\\", "-")
    filename = f"{index:04d} - {safe_title}.txt"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"{title}\n\n{content}")
    print(f"  Saved: {filename}")

def already_downloaded(output_dir, index, title):
    safe_title = title.replace("/", "-").replace("\\", "-")
    filename = f"{index:04d} - {safe_title}.txt"
    filepath = os.path.join(output_dir, filename)
    return os.path.exists(filepath)

def main():
    print("Fetching novel info...")
    soup = get_soup(NOVEL_URL)

    title, description = get_novel_info(soup)
    print(f"Novel : {title}")
    print(f"Info  : {description[:100]}...")

    print("\nFetching all chapter links...")
    chapters = get_all_chapter_links(NOVEL_URL)
    print(f"\nTotal chapters found: {len(chapters)}\n")

    print("\nStarting downloads...")
    failed = []
    skipped = 0

    for i, (chapter_title, chapter_url) in enumerate(chapters, 1):
        if already_downloaded(OUTPUT_DIR, i, chapter_title):
            print(f"  Skipping {i}/{len(chapters)}: {chapter_title} (already downloaded)")
            skipped += 1
            continue

        print(f"\nDownloading {i}/{len(chapters)}: {chapter_title}")
        try:
            content = scrape_chapter(chapter_url)
            if not content:
                print(f"  Warning: no content found for chapter {i}")
                failed.append((i, chapter_title, chapter_url))
                continue
            save_chapter(OUTPUT_DIR, i, chapter_title, content)
        except Exception as e:
            print(f"  Failed: {e}")
            failed.append((i, chapter_title, chapter_url))
        time.sleep(1.5)

    print(f"\nDone.")
    print(f"  Downloaded : {len(chapters) - skipped - len(failed)}")
    print(f"  Skipped    : {skipped}")
    print(f"  Failed     : {len(failed)}")
    print(f"  Saved to   : '{OUTPUT_DIR}/'")

    if failed:
        print(f"\nFailed chapters:")
        for i, chapter_title, chapter_url in failed:
            print(f"  {i:04d} - {chapter_title} -> {chapter_url}")

main()