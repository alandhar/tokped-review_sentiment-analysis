from scraping_module.product_scraper import scrape_product_links
from scraping_module.review_scraper import scrape_reviews

# Daftar keyword produk (fokus netral/negatif)
keywords = [
    "casing hp", "lampu led", "power bank", "kaos kaki", "tripod hp",
    "mouse wireless", "screen protector", "botol minum", "baju wanita",
    "headset bluetooth", "tas laptop", "stand hp"
]

print("\n🚀 MULAI SCRAPING PRODUK...")
scrape_product_links(keywords, jumlah_halaman=2, limit_per_keyword=75)

print("\n📝 MULAI SCRAPING REVIEW...")
scrape_reviews(max_review=12000)
