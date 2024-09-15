import requests
import time

url = "https://nc-gym.com"
response = requests.get(url)

if "Please wait while your request is being verified" in response.text:
    print("Waiting for Cloudflare verification...")
    time.sleep(10)  # Tunggu 10 detik lalu coba lagi
    response = requests.get(url)

print(f"Status Code: {response.status_code}")
print(f"Response API: {response.text}")