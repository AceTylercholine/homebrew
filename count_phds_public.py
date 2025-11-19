import time
import requests
import urllib3
from bs4 import BeautifulSoup

# CONFIGURATION
START_URL = "https://www.dpz.eu/en/contact/employees"
BASE_URL = "https://www.dpz.eu"

# SEARCH TERMS (Case insensitive)
TARGET_TITLES = [
    "phd student",
    "ph.d. student",
    "doctoral candidate",
    "doctoral researcher",
    "doktorand",
    "doktorandin",
    "promovierend",
    "promovierende"
]

# --- THE FIX ---
# 1. Disable warnings about insecure requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_soup(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        # 2. verify=False tells Python to ignore the SSL certificate error
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def main():
    print(f"Fetching staff list from: {START_URL}")
    soup = get_soup(START_URL)
    
    if not soup:
        return

    # Find profile links
    profile_links = soup.select('a[href*="/profile/"]')

    unique_urls = set()
    for link in profile_links:
        href = link.get('href')
        if href:
            if href.startswith('/'):
                full_url = BASE_URL + href
            else:
                full_url = href
            unique_urls.add(full_url)

    print(f"Found {len(unique_urls)} unique profiles. Starting scan...")
    print("Press Ctrl+C to stop early.\n")
    
    count = 0
    phd_count = 0

    try:
        for profile_url in unique_urls:
            p_soup = get_soup(profile_url)
            
            if p_soup:
                # Check 'span.position' (standard) or 'div.job-title'
                title_element = p_soup.select_one('span.position')
                
                if title_element:
                    title_text = title_element.get_text(strip=True).lower()
                    
                    if any(t in title_text for t in TARGET_TITLES):
                        phd_count += 1
                        # print(f"  -> Found PhD: {title_text}")

            count += 1
            if count % 20 == 0:
                print(f"Checked {count}/{len(unique_urls)} profiles... (Found {phd_count} PhDs so far)")
            
            # Small delay
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nStopped by user.")

    print("-" * 30)
    print(f"Scan Complete.")
    print(f"Total Profiles Checked: {count}")
    print(f"Total PhD Students Found: {phd_count}")

if __name__ == "__main__":
    main()