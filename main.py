from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_binary
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import html2text

visited = set()

def sanitize_filename(filename):
    return re.sub(r'(?u)[^-\w.]', '', filename)

def scrape_page(driver, url):
    driver.get(url)
    time.sleep(2)
    page_source = driver.page_source
    page_source = page_source.replace('\n', ' ')
    filename = sanitize_filename(url.replace('/', '_') + '.md')  # Save as .md
    with open(filename, 'w', encoding='utf-8') as f:  # Specify UTF-8 encoding
        # Convert HTML to Markdown
        h = html2text.HTML2Text()
        markdown = h.handle(page_source)
        f.write(markdown)

def scrape_urls(base_url):
    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(base_url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href^='/api/resources']")))

    links = driver.find_elements(By.CSS_SELECTOR, "a[href^='/api']")

    for i in range(len(links)):
        links = driver.find_elements(By.CSS_SELECTOR, "a[href^='/api']")
        link = links[i]

        url = link.get_attribute("href")
        if not url.startswith('http'):
            url = base_url + url

        if url not in visited:
            print(f"Processing link: {url}")
            visited.add(url)
            scrape_page(driver, url)

    driver.quit()

def main():
    base_url = "https://docs.athenahealth.com/api"
    scrape_urls(base_url)


if __name__ == "__main__":
    main()
