import requests
from bs4 import BeautifulSoup

# URL of the Wikipedia page to scrape
url = "https://en.wikipedia.org/wiki/Web_scraping"

# Send a GET request to the webpage
response = requests.get(url)

# Create a BeautifulSoup object with the webpage content
soup = BeautifulSoup(response.content, "html.parser")

# Find the main content element on the page
content = soup.find(id="mw-content-text")

# Extract and print the text content
print(content.get_text())