import cloudscraper

# URL API dan data payload
api_url = "https://www.nc-gym.com/api/gate-log"
payload = {'id': '786195', 'status': 'keluar'}

# Headers yang dibutuhkan
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0'
}

# Inisialisasi cloudscraper untuk melewati Cloudflare
scraper = cloudscraper.create_scraper()

# Kirim permintaan POST ke API
try:
    response = scraper.post(api_url, json=payload, headers=headers)
    response.raise_for_status()  # Periksa apakah ada error HTTP
    print(f"Status Code: {response.status_code}")
    print(f"Response API: {response.text}")
except Exception as e:
    print(f"Error occurred: {e}")