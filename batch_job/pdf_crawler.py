import os
import re
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from urllib.robotparser import RobotFileParser
import zipfile

ua = UserAgent()
HEADERS = {"User-Agent": ua.random}

UNIVERSITY_URLS = [
    "https://catalog.ucdavis.edu",
    "https://catalog.calpoly.edu",
    "https://www.cs.cmu.edu",
    "https://www.eecs.mit.edu",
    "https://catalog.utah.edu",
    "https://www.cs.princeton.edu",
    "https://www.cs.stanford.edu"
]

PDF_DIR = "cs_pdfs"
ZIP_NAME = "cs_course_catalogs.zip"
os.makedirs(PDF_DIR, exist_ok=True)

PDF_KEYWORDS = re.compile(r"(computer[-_\s]?science|cs|syllabus|catalog).*\.pdf", re.IGNORECASE)

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def is_allowed_by_robots(url):
    parsed_url = urlparse(url)
    robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
    rp = RobotFileParser()
    try:
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(HEADERS["User-Agent"], url)
    except:
        print(f"⚠️ Could not read robots.txt for {parsed_url.netloc}. Skipping for safety.")
        return False

def crawl_and_download_pdfs(base_url):
    if not is_allowed_by_robots(base_url):
        print(f"🚫 Skipping {base_url} - Disallowed by robots.txt")
        return

    try:
        print(f"🔍 Scanning: {base_url}")
        response = requests.get(base_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.find_all("a", href=True)

        for link in links:
            href = link["href"]
            if ".pdf" in href.lower():
                full_url = urljoin(base_url, href)
                if PDF_KEYWORDS.search(href):
                    domain = urlparse(base_url).netloc.replace("www.", "").split(".")[0]
                    pdf_name = sanitize_filename(f"{domain}_{os.path.basename(href)}")
                    pdf_path = os.path.join(PDF_DIR, pdf_name)

                    if not os.path.exists(pdf_path):
                        print(f"⬇️ Downloading: {pdf_name}")
                        pdf_data = requests.get(full_url, headers=HEADERS, timeout=10)
                        with open(pdf_path, "wb") as f:
                            f.write(pdf_data.content)
    except Exception as e:
        print(f"⚠️ Error with {base_url}: {str(e)}")

def zip_pdfs():
    zip_path = os.path.join(os.getcwd(), ZIP_NAME)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(PDF_DIR):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=file)
    print(f"\n🗜️ PDFs zipped as: {zip_path}")

def main():
    for url in UNIVERSITY_URLS:
        crawl_and_download_pdfs(url)

    zip_pdfs()
    print(f"\n✅ Done. PDFs saved in: {os.path.abspath(PDF_DIR)}")

if __name__ == "__main__":
    main()
