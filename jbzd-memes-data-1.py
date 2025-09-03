import time
import csv
import requests
from bs4 import BeautifulSoup
import os

BASE_URL = "https://jbzd.com.pl/oczekujace/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

start_page = 1
end_page = 100
folder = r"C:\jbzd-memes-data-1"
csv_file = os.path.join(folder, f"memes_{start_page}_{end_page}.csv")

os.makedirs(folder, exist_ok=True)
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "Tytuł", "URL_obrazka"])

start_time = time.time()

for page in range(start_page, end_page + 1):
    page_start = time.time()
    try:
        r = requests.get(f"{BASE_URL}{page}", headers=HEADERS, timeout=15)
        if r.status_code != 200: continue
    except: continue

    soup = BeautifulSoup(r.text, "html.parser")
    articles = soup.find_all("div", class_="article-content")

    for article in articles:
        badge = article.find("content-badges-view")
        meme_id = badge.get(":id") if badge else ""
        title_tag = article.find("h3", class_="article-title")
        title = title_tag.a.get_text(strip=True) if title_tag and title_tag.a else ""
        img_tag = article.find("div", class_="article-image")
        img_url = img_tag.img.get("src") if img_tag and img_tag.img else ""

        with open(csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([meme_id, title, img_url])

end_time = time.time()
print(f"Zakres {start_page}-{end_page} pobrany w {end_time - start_time:.2f} s")
