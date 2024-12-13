import cloudscraper

scraper = cloudscraper.create_scraper()

# Headers yang disalin dari browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://nc-gym.com/",
}

url = "https://nc-gym.com"
response = scraper.get(url, headers=headers)

print(f"Status Code: {response.status_code}")
print(f"Response API: {response.text}")