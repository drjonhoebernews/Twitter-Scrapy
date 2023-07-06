from bs4 import BeautifulSoup
from selenium import webdriver
from elasticsearch import Elasticsearch
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Elasticsearch setup
# es = Elasticsearch()

# Selenium setup with Chrome profile
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # disables the message
chrome_options.add_argument("user-data-dir=C:\\Users\\dogan\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1")

webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

while True:  # start infinite loop
    # Visit the website
    driver.get('https://twitter.com/search?q=kemal%20kilicdaroglu&src=typeahead_click&f=live')
    time.sleep(3)  # wait for page to load
    # Parse the HTML content
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # ... Selenium ve BeautifulSoup setup

    # Find all outer <div> elements with the specified CSS classes
    outer_div_elements = soup.find_all('div', class_='css-1dbjc4n r-zl2h9q')

    # For each outer <div> element, find the inner <div> elements with the specified CSS classes
    for outer_div_element in outer_div_elements:
        inner_div_elements = outer_div_element.find_all('div', class_='css-1dbjc4n r-18u37iz r-1q142lx')

        # For each inner <div> element, find the <a> elements with the specified CSS classes and print their href attribute
        for inner_div_element in inner_div_elements:
            a_elements = inner_div_element.find_all('a', class_='css-4rbku5 css-18t94o4 css-901oao r-1bwzh9t r-1loqt21 r-xoduu5 r-1q142lx r-1w6e6rj r-37j5jr r-a023e6 r-16dba41 r-9aw3ui r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0')
            for a_element in a_elements:
                href = a_element.get('href')
                print(href)

    time.sleep(10)  # wait for 10 seconds before refreshing

# Close the Selenium driver
driver.close()
