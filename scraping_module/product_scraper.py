from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

def scrape_product_links(keywords, jumlah_halaman=10, limit_per_keyword=75):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    product_links = set()

    def slow_scroll():
        scroll_step = 500
        pause_time = 1.5
        last_height = driver.execute_script("return document.body.scrollHeight")
        current_position = 0
        while current_position < last_height:
            current_position += scroll_step
            driver.execute_script(f"window.scrollTo(0, {current_position});")
            time.sleep(pause_time)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height > last_height:
                last_height = new_height
            elif current_position >= new_height:
                break

    for keyword in keywords:
        print(f"\n🔍 Keyword: {keyword}")
        for page in range(1, jumlah_halaman + 1):
            if len(product_links) >= limit_per_keyword * len(keywords):
                break

            url = f"https://www.tokopedia.com/search?st=product&q={keyword}&page={page}"
            print(f"[INFO] {keyword} - Page {page}")
            driver.get(url)
            time.sleep(3)
            slow_scroll()

            containers = driver.find_elements(By.XPATH, '//a[contains(@class, "oQ94Awb6LlTiGByQZo8Lyw")]')
            for c in containers:
                link = c.get_attribute('href')
                if link:
                    product_links.add(link)
                    if len(product_links) >= limit_per_keyword * len(keywords):
                        break

    driver.quit()
    df = pd.DataFrame(list(product_links), columns=["product_link"])
    df.to_csv("tokopedia_products.csv", index=False)
    print(f"\n✅ Total produk terkumpul: {len(product_links)}")
