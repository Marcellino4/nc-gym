from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Konfigurasi untuk headless browser
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Inisialisasi WebDriver dengan Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Akses API atau halaman yang dilindungi Cloudflare
api_url = "https://www.nc-gym.com"
driver.get(api_url)

# Dapatkan konten halaman setelah verifikasi Cloudflare
page_content = driver.page_source

# Cetak atau simpan respons API
print(page_content)

# Tutup browser setelah selesai
driver.quit()