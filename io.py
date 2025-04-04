from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from serpapi import GoogleSearch
import time

import openai

SERPAPI_KEY = "56ada434555f5c4f84211880493227f59e42409c19eca048840dc56cd526e313"

def get_top_links(query, num_results=5):
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": num_results
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    links = []
    for result in results.get("organic_results", [])[:num_results]:
        link = result.get("link")
        if link:
            links.append(link)
    return links

def extract_text_from_url(driver, url):
    try:
        driver.get(url)
        time.sleep(3)
        title = driver.title
        body = driver.find_element(By.TAG_NAME, "body")
        return title, body.text[:5000]  # Limit to first 5k characters
    except Exception as e:
        return "Error loading page", f"Error: {e}"

def main():
    query = input("Enter your query: ")
    top_links = get_top_links(query)

    if not top_links:
        print("No links found.")
        return

    print(f"\n🔍 Top {len(top_links)} results for: '{query}'\n")

    # Set up Selenium WebDriver
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        for idx, link in enumerate(top_links, 1):
            print(f"\n{'='*80}\nResult {idx}: {link}")
            title, content = extract_text_from_url(driver, link)
            print(f"\n📰 Title: {title}\n\n📝 Extracted Text:\n{content[:1000]}...")  # Limit output per result
    finally:
        # Leave browser open for inspection or debugging
        pass
        # driver.quit()

if __name__ == "__main__":
    main()