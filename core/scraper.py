import cloudscraper
from bs4 import BeautifulSoup

def fetch_test_cases(url):
    """
    Scrapes a Codeforces problem URL and returns a list of dictionaries
    containing the sample inputs and expected outputs.
    """
    print(f"[*] Fetching problem from: {url}")
    
    # Create a cloudscraper instance to bypass Cloudflare
    scraper = cloudscraper.create_scraper(browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    })
    response = scraper.get(url)

    if response.status_code != 200:
        print(f"[!] Failed to fetch the page. Status code: {response.status_code}")
        return []

    # Parse the raw HTML into a BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')

    inputs = []
    outputs = []

    # 1. Extract all sample inputs
    for input_div in soup.find_all('div', class_='input'):
        pre_tag = input_div.find('pre')
        if pre_tag:
            inputs.append(pre_tag.get_text(separator='\n').strip())

    # 2. Extract all sample outputs
    for output_div in soup.find_all('div', class_='output'):
        pre_tag = output_div.find('pre')
        if pre_tag:
            outputs.append(pre_tag.get_text(separator='\n').strip())

    # 3. Pair the inputs and outputs together
    test_cases = []
    for i in range(len(inputs)):
        test_cases.append({
            'input': inputs[i],
            'output': outputs[i]
        })

    print(f"[*] Successfully scraped {len(test_cases)} test cases!\n")
    return test_cases

# --- Quick Test Block ---
if __name__ == "__main__":
    test_url = "https://codeforces.com/problemset/problem/4/A"
    cases = fetch_test_cases(test_url)

    for i, case in enumerate(cases, 1):
        print(f"--- Test Case {i} ---")
        print("Input:")
        print(case['input'])
        print("Expected Output:")
        print(case['output'])
        print()