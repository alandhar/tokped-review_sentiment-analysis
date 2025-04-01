import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def scrape_reviews(max_review=12000):
    df_links = pd.read_csv("tokopedia_products.csv")
    product_links = df_links["product_link"].tolist()

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    all_reviews = []

    for idx, url in enumerate(product_links):
        if len(all_reviews) >= max_review:
            break

        print(f"\n[{idx+1}] Membuka: {url}")
        driver.get(url)
        time.sleep(3)

        found_review_feed = False
        for pos in range(0, 20000, 400):
            driver.execute_script(f"window.scrollTo(0, {pos});")
            time.sleep(1.5)
            try:
                driver.find_element(By.ID, "review-feed")
                found_review_feed = True
                break
            except:
                continue

        if not found_review_feed:
            continue

        while True:
            if len(all_reviews) >= max_review:
                break

            try:
                review_feed = driver.find_element(By.ID, "review-feed")
                last_height = driver.execute_script("return arguments[0].scrollHeight", review_feed)
                scroll_pos = 0
                while scroll_pos < last_height:
                    driver.execute_script("arguments[0].scrollTo(0, arguments[1]);", review_feed, scroll_pos)
                    time.sleep(1.2)
                    scroll_pos += 300
                    new_height = driver.execute_script("return arguments[0].scrollHeight", review_feed)
                    if new_height == last_height:
                        break
                    last_height = new_height
            except:
                pass

            try:
                buttons = driver.find_elements(By.XPATH, '//button[contains(text(),"Selengkapnya")]')
                for b in buttons:
                    driver.execute_script("arguments[0].click();", b)
                    time.sleep(0.3)
            except:
                pass

            reviews = driver.find_elements(By.CSS_SELECTOR, 'span[data-testid="lblItemUlasan"]')
            ratings = driver.find_elements(By.CSS_SELECTOR, 'div.rating')
            timestamps = driver.find_elements(By.CLASS_NAME, 'css-vqrjg4-unf-heading')

            for i in range(len(reviews)):
                if len(all_reviews) >= max_review:
                    break
                review = reviews[i].text.strip()
                rating = ratings[i].get_attribute("aria-label") if i < len(ratings) else ""
                rating_value = rating.split(" ")[1] if rating else ""
                timestamp = timestamps[i].text.strip() if i < len(timestamps) else ""
                if review:
                    all_reviews.append({
                        "id": idx + 1,
                        "review": review,
                        "rating": rating_value,
                        "timestamp": timestamp
                    })

            try:
                next_btn = driver.find_element(By.XPATH, '//button[@aria-label="Laman berikutnya"]')
                if not next_btn.is_enabled():
                    break
                else:
                    driver.execute_script("arguments[0].click();", next_btn)
                    time.sleep(3)
            except:
                break

    driver.quit()
    df_reviews = pd.DataFrame(all_reviews)
    df_reviews.to_csv("tokopedia_reviews.csv", index=False)
    print(f"\n✅ Total review disimpan: {len(df_reviews)}")
