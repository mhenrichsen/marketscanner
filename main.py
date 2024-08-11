import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration

# Set up the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define the URL to scrape
url = 'https://www.marketscreener.com/quote/stock/DELL-TECHNOLOGIES-INC-50061235/'

# Define the headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://light.it-finance.com/',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://light.it-finance.com',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Priority': 'u=4'
}


driver.get(url)

# Wait for 10 seconds
time.sleep(5)

# Get the page source
html_content = driver.page_source

# Parse the content of the request with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the desired information using the CSS selector
pe_forward = soup.select_one('#efd > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(4) > th:nth-child(2) > div:nth-child(1)')
yield_forward = soup.select_one('#efd > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(5) > th:nth-child(2) > div:nth-child(1)')
trading_rating = soup.select_one('#ratings > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1)')
investor_rating = soup.select_one('#ratings > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > span:nth-child(1)')
mean_consensus = soup.select_one('html body div.pcontent.empwidget div.container.pt-m-15 div.grid.gcenter main.c-12.cl div.grid.my-15 div.c-12.cm-4 div#consensusDetail.card.mb-15.card--collapsible.pos-next div.card-content div.txt-s1 div.grid.py-5 div.c-auto.txt-align-right')
spread_avg_target = soup.select_one('div.txt-s1:nth-child(1) > div:nth-child(6) > div:nth-child(2) > span:nth-child(1)')
# Check if the element exists and get its text
if pe_forward:
    # split on newline
    text = pe_forward.get_text(strip=True).split('\n')[0]
    print(f"P/E Forward: {text}")
else:
    print('P/E Forward: Element not found')

if yield_forward:
    # split on newline
    text = yield_forward.get_text(strip=True).split('%')[0]
    print(f"Yield Forward: {text}%")

# get title of the trading rating
print(f"Trading Rating: {trading_rating.get('title').split('%')[0]}%")
print(f"Investor Rating: {investor_rating.get('title').split('%')[0]}%")
print(f"Mean Consensus: {mean_consensus.get_text(strip=True)}")
print(f"Spread Average Target: {spread_avg_target.get_text(strip=True)}")


# Open the webpage
url_qoute_page = "https://www.marketscreener.com/quote/stock/DELL-TECHNOLOGIES-INC-50061235/quotes/"
driver.get(url_qoute_page)

# Wait for 10 seconds
time.sleep(10)

# Get the page source
html_content = driver.page_source


# Parse the content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Locate the element using BeautifulSoup
quote_1_month = soup.select_one('#performances > div:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2) > span:nth-child(1)')
quote_3_month = soup.select_one('#performances > div:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(2) > span:nth-child(1)')
quote_6_month = soup.select_one('#performances > div:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(6) > td:nth-child(2) > span:nth-child(1)')

print(f"1 Month Quote: {quote_1_month.get_text(strip=True).split('%')[0]}%")
print(f"3 Month Quote: {quote_3_month.get_text(strip=True).split('%')[0]}%")
print(f"6 Month Quote: {quote_6_month.get_text(strip=True).split('%')[0]}%")


# Get ratings page
driver.get('https://www.marketscreener.com/quote/stock/DELL-TECHNOLOGIES-INC-50061235/ratings/')

# Wait for 10 seconds
time.sleep(5)

# Get the page source
html_content = driver.page_source

# Parse the content of the request with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
percent_70 = soup.select_one('#snw-synth > div:nth-child(3) > ul:nth-child(1) > li:nth-child(1)').get_text(strip=True)
if "70%" in percent_70:
    print("70% or more analysts positive: True")
    percent_70 = True
else:
    print("70% or more analysts positive: False")
    percent_70 = False

print(f"70% or more analysts positive: {percent_70}")


driver.get('https://www.marketscreener.com/quote/stock/DELL-TECHNOLOGIES-INC-50061235/calendar/')

# Wait for 10 seconds
time.sleep(5)

# Get the page source
html_content = driver.page_source

# Parse the content of the request with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Use CSS selector to find the specific <g> element with the desired class and attribute
spread_2020 = soup.select_one('#anualResultsTable > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(3) > b:nth-child(5) > span:nth-child(1)').get_text(strip=True)
spread_2021 = soup.select_one('#anualResultsTable > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(4) > b:nth-child(5) > span:nth-child(1)').get_text(strip=True)
spread_2022 = soup.select_one('#anualResultsTable > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(5) > b:nth-child(5) > span:nth-child(1)').get_text(strip=True)
spread_2023 = soup.select_one('#anualResultsTable > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(6) > b:nth-child(5) > span:nth-child(1)').get_text(strip=True)
spread_2024 = soup.select_one('#anualResultsTable > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(7) > b:nth-child(5) > span:nth-child(1)').get_text(strip=True)

print(f"Sales Spread 2020-2024: {spread_2020}, {spread_2021}, {spread_2022}, {spread_2023}, {spread_2024}")

eps_spread_2020 = soup.select_one('#anualResultsTable > tbody:nth-child(2) > tr:nth-child(6) > td:nth-child(3) > b:nth-child(5) > span:nth-child(1)').get_text(strip=True)
eps_spread_2021 = soup.select_one('#anualResultsTable > tbody:nth-child(2) > tr:nth-child(6) > td:nth-child(4) > b:nth-child(5) > span:nth-child(1)').get_text(strip=True)
eps_spread_2022 = soup.select_one('#anualResultsTable > tbody:nth-child(2) > tr:nth-child(6) > td:nth-child(5) > b:nth-child(5) > span:nth-child(1)').get_text(strip=True)
eps_spread_2023 = soup.select_one('#anualResultsTable > tbody:nth-child(2) > tr:nth-child(6) > td:nth-child(6) > b:nth-child(5) > span:nth-child(1)').get_text(strip=True)
eps_spread_2024 = soup.select_one('#anualResultsTable > tbody:nth-child(2) > tr:nth-child(6) > td:nth-child(7) > b:nth-child(5) > span:nth-child(1)').get_text(strip=True)

print(f"EPS Spread 2020-2024: {eps_spread_2020}, {eps_spread_2021}, {eps_spread_2022}, {eps_spread_2023}, {eps_spread_2024}")

# Get the page source
driver.get('https://www.marketscreener.com/quote/stock/DELL-TECHNOLOGIES-INC-50061235/company/')

## Wait for 10 seconds
time.sleep(5)

# Get the page source
html_content = driver.page_source

# Parse the content of the request with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

table = soup.select_one('#salesReg > div:nth-child(3) > table:nth-child(1)')

rows = table.find_all('tr')[1:]  # Skip the header row
data = []
for row in rows:
    columns = row.find_all('td')
    region = columns[0].find('span').text.strip()
    weight_2023 = float(columns[2].text.strip().replace('%', ''))
    weight_2024 = float(columns[4].text.strip().replace('%', ''))
    delta = float(columns[5].text.strip().replace('%', '').replace('(', '-').replace(')', ''))
    data.append({
        'Region': region,
        'Weight_2023': weight_2023,
        'Weight_2024': weight_2024,
        'Delta': delta
    })

# Calculate the weighted delta and sum the values
total_weighted_delta = 0
for entry in data:
    weighted_delta = entry['Delta'] * entry['Weight_2024'] / 100
    total_weighted_delta += weighted_delta

print(f"Total Weighted Delta: {total_weighted_delta}")

# Find all rows in the table body
competitors_table = soup.select_one('#competitors-list > div:nth-child(3) > table:nth-child(1)')

rows = competitors_table.find('tbody').find_all('tr')

# Extract the "1st Jan change" values
jan_changes = []
for row in rows:
    change_cell = row.find('td', class_='table-child--w80 table-child--right')
    if change_cell:
        change_text = change_cell.find('span', class_='variation').text.strip()
        # Remove the '%' sign and convert to float
        change_value = float(re.sub(r'[^-\d.]+', '', change_text))
        jan_changes.append(change_value)

print(f"Competitors' 1st Jan Changes: {jan_changes}")

market_table = soup.select_one('#competitors-list > div:nth-child(3) > table:nth-child(1)')

def parse_market_cap(cap_string):
    return float(cap_string.strip().rstrip('B'))

# Extract market caps
market_caps = []
rows = market_table.find_all('tr')[1:]  # Skip header row

# Get the market cap of the first row (target company)
target_cap = parse_market_cap(rows[0].find_all('td')[-1].text.strip())

# Get market caps for all rows including the first one
for row in rows:
    cap = parse_market_cap(row.find_all('td')[-1].text.strip())
    market_caps.append(cap)

# Sort market caps in descending order
sorted_caps = sorted(market_caps, reverse=True)

# Find the position of the target company
position = sorted_caps.index(target_cap) + 1  # Adding 1 because index is 0-based

print(f"Position of the target company based on market cap: {position}")

# Get the page source
driver.get('https://www.marketscreener.com/quote/stock/DELL-TECHNOLOGIES-INC-50061235/finances/')

# Wait for 10 seconds
time.sleep(5)

# Get the page source
html_content = driver.page_source

# Parse the content of the request with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

print("*** Extracting stock data ***")
stocks_row = soup.find('td', string=lambda text: 'Nbr of stocks' in text if text else False).parent

# Extract stock numbers from this row
stocks = []
for td in stocks_row.find_all('td', class_='table-child--w90'):
    content = td.text.strip()
    if content != '-':
        stocks.append(int(content.replace(',', '')))

# Calculate percentage changes
changes = []
for i in range(1, len(stocks)):
    change = (stocks[i] - stocks[i-1]) / stocks[i-1] * 100
    changes.append(change)

# Determine if values are increasing
increasing = all(change >= 0 for change in changes)

print(f"Number of stocks: {stocks}")
print(f"Percentage changes: {[f'{change:.2f}%' for change in changes]}")
print(f"Are values consistently increasing? {'Yes' if increasing else 'No'}")


print("\n*** Extracting net sales estimates ***")
if stocks:
    print(f"Total percentage change: {((stocks[-1] - stocks[0]) / stocks[0] * 100):.2f}%")
else:
    print("No stock data available to calculate total percentage change.")

# Use the provided CSS selector to find the 'Net sales' row
sales_row = soup.select_one('#iseTableA > tbody:nth-child(2) > tr:nth-child(1)')

if not sales_row:
    print("'Net sales' row not found. Please check the HTML structure and CSS selector.")
else:
    # Extract net sales estimates
    sales_estimates = []
    for td in sales_row.select('td.table-child--bg-estimates'):
        content = td.text.strip()
        sales_estimates.append(int(content.replace(',', '')))

    print(f"Extracted net sales estimates: {sales_estimates}")

    if sales_estimates:
        # Calculate percentage changes
        changes = []
        for i in range(1, len(sales_estimates)):
            change = (sales_estimates[i] - sales_estimates[i-1]) / sales_estimates[i-1] * 100
            changes.append(change)

        # Determine if values are increasing
        increasing = all(change >= 0 for change in changes)

        print(f"Net sales estimates: {sales_estimates}")
        print(f"Percentage changes: {[f'{change:.2f}%' for change in changes]}")
        print(f"Are estimates consistently increasing? {'Yes' if increasing else 'No'}")
        print(f"Total percentage change: {((sales_estimates[-1] - sales_estimates[0]) / sales_estimates[0] * 100):.2f}%")

        # Additional analysis: Average estimate and number of analysts
        avg_estimate = sum(sales_estimates) / len(sales_estimates)
        num_analysts = [td.get('title', '').split(':')[-1].strip() for td in sales_row.select('td.table-child--bg-estimates')]

        print(f"\nAverage sales estimate: {avg_estimate:.2f} million USD")
        print(f"Number of analysts per estimate: {', '.join(num_analysts)}")
    else:
        print("No sales estimate data found in the selected row.")


print("\n*** Extracting EPS estimates ***")
eps_row = soup.select_one('#iseTableA > tbody:nth-child(2) > tr:nth-child(8)')

if not eps_row:
    print("'EPS' row not found. Please check the HTML structure and CSS selector.")
else:
    # Extract EPS estimates
    eps_estimates = []
    for td in eps_row.select('td.table-child--bg-estimates'):
        content = td.text.strip()
        eps_estimates.append(float(content))

    print(f"Extracted EPS estimates: {eps_estimates}")

    if eps_estimates:
        # Calculate percentage changes
        changes = []
        for i in range(1, len(eps_estimates)):
            change = (eps_estimates[i] - eps_estimates[i-1]) / eps_estimates[i-1] * 100
            changes.append(change)

        # Determine if values are increasing
        increasing = all(change >= 0 for change in changes)

        print(f"EPS estimates: {[f'{eps:.4f}' for eps in eps_estimates]}")
        print(f"Percentage changes: {[f'{change:.2f}%' for change in changes]}")
        print(f"Are estimates consistently increasing? {'Yes' if increasing else 'No'}")
        print(f"Total percentage change: {((eps_estimates[-1] - eps_estimates[0]) / eps_estimates[0] * 100):.2f}%")

        # Additional analysis: Average estimate and number of analysts
        avg_estimate = sum(eps_estimates) / len(eps_estimates)
        num_analysts = [td.get('title', '').split(':')[-1].strip() for td in eps_row.select('td.table-child--bg-estimates')]

        print(f"\nAverage EPS estimate: {avg_estimate:.4f} USD")
        print(f"Number of analysts per estimate: {', '.join(num_analysts)}")
    else:
        print("No EPS estimate data found in the selected row.")

print("\n*** Extracting net margin estimates ***")
margin_row = soup.select_one('#iseTableA > tbody:nth-child(2) > tr:nth-child(7)')

if not margin_row:
    print("'Net margin' row not found. Please check the HTML structure and CSS selector.")
else:
    # Extract net margin estimates
    margin_estimates = []
    for td in margin_row.select('td.table-child--bg-estimates'):
        content = td.text.strip().rstrip('%')
        margin_estimates.append(float(content))

    print(f"Extracted net margin estimates: {margin_estimates}")

    if margin_estimates:
        # Calculate percentage point changes
        changes = []
        for i in range(1, len(margin_estimates)):
            change = margin_estimates[i] - margin_estimates[i-1]
            changes.append(change)

        # Determine if values are increasing
        increasing = all(change >= 0 for change in changes)

        print(f"Net margin estimates: {[f'{margin:.2f}%' for margin in margin_estimates]}")
        print(f"Percentage point changes: {[f'{change:+.2f}' for change in changes]}")
        print(f"Are estimates consistently increasing? {'Yes' if increasing else 'No'}")
        print(f"Total percentage point change: {margin_estimates[-1] - margin_estimates[0]:.2f}")

        # Additional analysis: Average estimate and number of analysts
        avg_estimate = sum(margin_estimates) / len(margin_estimates)
        num_analysts = [td.get('title', '').split(':')[-1].strip() for td in margin_row.select('td.table-child--bg-estimates')]

        print(f"\nAverage net margin estimate: {avg_estimate:.2f}%")
        print(f"Number of analysts per estimate: {', '.join(num_analysts)}")
    else:
        print("No net margin estimate data found in the selected row.")


print("\n*** Extracting ROE estimates ***")
roe_row = soup.select_one('#bsTable > tbody:nth-child(2) > tr:nth-child(5)')

if not roe_row:
    print("'ROE' row not found. Please check the HTML structure and CSS selector.")
else:
    # Extract ROE estimates
    roe_estimates = []
    for td in roe_row.select('td.table-child--bg-estimates'):
        content = td.text.strip().rstrip('%')
        roe_estimates.append(float(content))

    print(f"Extracted ROE estimates: {roe_estimates}")

    if roe_estimates:
        # Calculate percentage point changes
        changes = []
        for i in range(1, len(roe_estimates)):
            change = roe_estimates[i] - roe_estimates[i-1]
            changes.append(change)

        # Determine if values are increasing
        increasing = all(change >= 0 for change in changes)

        print(f"ROE estimates: {[f'{roe:.1f}%' for roe in roe_estimates]}")
        print(f"Percentage point changes: {[f'{change:+.1f}' for change in changes]}")
        print(f"Are estimates consistently increasing? {'Yes' if increasing else 'No'}")
        print(f"Total percentage point change: {roe_estimates[-1] - roe_estimates[0]:.1f}")

        # Additional analysis: Average estimate and number of analysts
        avg_estimate = sum(roe_estimates) / len(roe_estimates)
        num_analysts = [td.get('title', '').split(':')[-1].strip() for td in roe_row.select('td.table-child--bg-estimates')]

        print(f"\nAverage ROE estimate: {avg_estimate:.1f}%")
        print(f"Number of analysts per estimate: {', '.join(num_analysts)}")
    else:
        print("No ROE estimate data found in the selected row.")


print("\n*** Extracting Cash Flow per Share estimates ***")
cash_flow_row = soup.select_one('#bsTable > tbody:nth-child(2) > tr:nth-child(9)')
if not cash_flow_row:
    print("'Cash Flow per Share' row not found. Please check the HTML structure and CSS selector.")
else:
    # Extract Cash Flow per Share values
    cash_flow_values = []
    for td in cash_flow_row.select('td.table-child--w90'):
        content = td.text.strip()
        if content != '-':
            try:
                cash_flow_values.append(float(content))
            except ValueError:
                print(f"Warning: Could not convert '{content}' to float. Skipping this value.")
        else:
            cash_flow_values.append(None)

    # Separate historical data and estimates
    historical_data = cash_flow_values[:-3]  # All except the last 3 values
    estimates = cash_flow_values[-3:]  # Last 3 values are estimates

    print("Historical Cash Flow per Share:")
    for i, value in enumerate(historical_data):
        if value is not None:
            print(f"Year {i+1}: {value:.4f}")
        else:
            print(f"Year {i+1}: No data")

    print("\nEstimated Cash Flow per Share:")
    for i, value in enumerate(estimates):
        if value is not None:
            print(f"Estimate {i+1}: {value:.4f}")
        else:
            print(f"Estimate {i+1}: No data")

    # Calculate percentage changes for estimates
    changes = []
    for i in range(1, len(estimates)):
        if estimates[i] is not None and estimates[i-1] is not None:
            change = (estimates[i] - estimates[i-1]) / estimates[i-1] * 100
            changes.append(change)

    if changes:
        print("\nPercentage changes in estimates:")
        for i, change in enumerate(changes):
            print(f"Change {i+1} to {i+2}: {change:+.2f}%")

        increasing = all(change > 0 for change in changes)
        print(f"\nAre estimates consistently increasing? {'Yes' if increasing else 'No'}")

        if estimates[0] is not None and estimates[-1] is not None:
            total_change = (estimates[-1] - estimates[0]) / estimates[0] * 100
            print(f"Total change in estimates: {total_change:+.2f}%")
    else:
        print("\nNot enough data to calculate changes in estimates.")

    # Additional analysis
    valid_estimates = [e for e in estimates if e is not None]
    if valid_estimates:
        avg_estimate = sum(valid_estimates) / len(valid_estimates)
        print(f"\nAverage estimated Cash Flow per Share: {avg_estimate:.4f} USD")
        print(f"Lowest estimate: {min(valid_estimates):.4f} USD")
        print(f"Highest estimate: {max(valid_estimates):.4f} USD")
    else:
        print("\nNo valid estimates available for analysis.")

    # Number of analysts for estimates
    num_analysts = [td.get('title', '').split(':')[-1].strip() for td in cash_flow_row.select('td.table-child--bg-estimates')]
    print(f"\nNumber of analysts per estimate: {', '.join(num_analysts)}")


print("\n*** Extracting Leverage (Debt/EBITDA) estimates ***")
leverage_row = soup.select_one('#bsTable > tbody:nth-child(2) > tr:nth-child(3)')

if not leverage_row:
    print("'Leverage (Debt/EBITDA)' row not found. Please check the HTML structure and CSS selector.")
else:
    # Extract leverage estimates
    leverage_estimates = []
    num_analysts = []
    for td in leverage_row.select('td.table-child--bg-estimates'):
        content = td.text.strip()
        leverage_estimates.append(float(content.rstrip('x')))
        num_analysts.append(td.get('title', '').split(':')[-1].strip())

    print("Leverage (Debt/EBITDA) estimates:")
    for i, value in enumerate(leverage_estimates):
        print(f"Estimate {i+1}: {value:.3f}x (Analysts: {num_analysts[i]})")

    # Calculate changes
    changes = []
    for i in range(1, len(leverage_estimates)):
        change = (leverage_estimates[i] - leverage_estimates[i-1]) / leverage_estimates[i-1] * 100
        changes.append(change)

    print("\nPercentage changes:")
    for i, change in enumerate(changes):
        print(f"Change {i+1} to {i+2}: {change:.2f}%")

    # Determine if values are decreasing (improvement in leverage)
    decreasing = all(change < 0 for change in changes)

    print(f"\nAre estimates consistently decreasing? {'Yes' if decreasing else 'No'}")
    print(f"Total change: {(leverage_estimates[-1] - leverage_estimates[0]) / leverage_estimates[0] * 100:.2f}%")

    # Additional analysis
    avg_estimate = sum(leverage_estimates) / len(leverage_estimates)
    print(f"\nAverage leverage estimate: {avg_estimate:.3f}x")
    print(f"Lowest estimate: {min(leverage_estimates):.3f}x")
    print(f"Highest estimate: {max(leverage_estimates):.3f}x")

driver.quit()
