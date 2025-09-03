import time
import csv
import requests
from bs4 import BeautifulSoup
import os

# ===================== KONFIGURACJA =====================
BASE_URL = "https://jbzd.com.pl/oczekujace/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

# Zakres stron (ustaw w repozytorium)
start_page = 1
end_page = 100  # np. testowo
folder = "memes-data"  # folder w repozytorium
csv_file = os.path.join(folder, f"memes_{start_page}_{end_page}.csv")

# ===================== TWORZENIE FOLDERU I CSV =====================
os.makedirs(folder, exist_ok=True)
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "Tytuł", "URL_obrazka"])

# ===================== POBIERANIE STRON =====================
start_time = time.time()

for page in range(start_page, end_page + 1):
    try:
        r = requests.get(f"{BASE_URL}{page}", headers=HEADERS, timeout=15)
        if r.status_code != 200:
            print(f"Strona {page} nie pobrana, status: {r.status_code}")
            continue
    except Exception as e:
        print(f"Błąd strony {page}: {e}")
        continue

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

    time.sleep(0.5)  # aby nie wyglądało jak bot

end_time = time.time()
print(f"Pobrano strony {start_page}-{end_page} w {end_time - start_time:.2f} s")
