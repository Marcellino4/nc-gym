import cloudscraper

# Inisialisasi scraper
scraper = cloudscraper.create_scraper()

# URL yang ingin diakses
url = "https://nc-gym.com"

# Melakukan request menggunakan cloudscraper
response = scraper.get(url)

# Tampilkan hasil status dan response dari API
print(f"Status Code: {response.status_code}")
print(f"Response API: {response.text}")