import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from collections import defaultdict

def scrape_reviews(
    max_per_rating={1: 800, 2: 800, 3: 800, 4: 800, 5: 1600},
    csv_path="tokopedia_products.csv",
    output_file="tokopedia_reviews.csv"
):
    df_links = pd.read_csv(csv_path)
    product_links = df_links["product_link"].tolist()

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    all_reviews = []
    rating_counts = defaultdict(int)

    try:
        for idx, url in enumerate(product_links):
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
                    if len(ratings) <= i:
                        continue

                    rating_text = ratings[i].get_attribute("aria-label")
                    if not rating_text or "bintang" not in rating_text:
                        continue

                    try:
                        rating_value = int(rating_text.split(" ")[1])
                    except:
                        continue

                    if rating_counts[rating_value] >= max_per_rating.get(rating_value, 0):
                        continue

                    review = reviews[i].text.strip()
                    timestamp = timestamps[i].text.strip() if i < len(timestamps) else ""

                    if review:
                        all_reviews.append({
                            "id": idx + 1,
                            "review": review,
                            "rating": rating_value,
                            "timestamp": timestamp
                        })
                        rating_counts[rating_value] += 1

                if all(rating_counts[r] >= max_per_rating.get(r, 0) for r in max_per_rating):
                    print("\nSemua batas rating tercapai.")
                    break

                try:
                    next_btn = driver.find_element(By.XPATH, '//button[@aria-label="Laman berikutnya"]')
                    if not next_btn.is_enabled():
                        break
                    else:
                        driver.execute_script("arguments[0].click();", next_btn)
                        time.sleep(3)
                except:
                    break

            print(f"Akumulasi sementara setelah produk ke-{idx+1}:")
            for r in sorted(max_per_rating):
                print(f"   Rating {r}: {rating_counts[r]} / {max_per_rating[r]}")

            if all(rating_counts[r] >= max_per_rating.get(r, 0) for r in max_per_rating):
                break

    except KeyboardInterrupt:
        print("\n(-) Scraping dihentikan manual oleh pengguna (Ctrl+C).")
    finally:
        print("\nMenyimpan data yang sudah berhasil dikumpulkan...")
        df_reviews = pd.DataFrame(all_reviews)
        df_reviews.to_csv(output_file, index=False)
        print(f"Total review disimpan: {len(df_reviews)}")
        print(f"Distribusi rating akhir:")
        for r in sorted(max_per_rating):
            print(f"   Rating {r}: {rating_counts[r]} / {max_per_rating[r]}")
        driver.quit()
