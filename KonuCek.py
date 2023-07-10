from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests  # import the requests library

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # disables the message
chrome_options.add_argument("user-data-dir=C:\\Users\\dogan\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 2")

webdriver_service = Service(ChromeDriverManager().install())
# Fetch the URLs
url_response = requests.get('http://172.29.153.240/api/twitter/twitter-aigiris')
urls = [item['url'] for item in url_response.json() if not item['geton']]

for url in urls:
    # Start the webdriver
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    outer_div = soup.find('div', class_='css-1dbjc4n r-16y2uox r-1wbh5a2 r-1ny4l3l')

    # Check if the div was found
    if outer_div is None:
        print(f'Could not find div for URL: {url}')

        # Update the 'geton' field for the URL
        url_update_data = {
            "url": url,
            "geton": True,
        }
        update_response = requests.post('http://172.29.153.240/api/twitter/twitter-update', json=url_update_data)
        if update_response.status_code == 200:
            print('Successfully updated the URL status.')
        else:
            print(f'Failed to update the URL status. Status code: {update_response.status_code}.')

        continue  # Skip the rest of the loop for this URL

    spans = outer_div.find_all('span', class_='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0')

    interactions_count = 0
    views = 0
    content = []

    for i, span in enumerate(spans):
        if span.text == "Görüntülenme":
            interactions_count = spans[i - 1].text
            if i + 1 < len(spans):  # make sure we do not go beyond the list boundary
                views = spans[i + 1].text
        else:
            content.append(span.text)

    # Assuming that the first span is fullname, the second is username, and the rest is content.
    fullname = spans[0].text
    username = spans[1].text
    content = ' '.join(span.text for span in spans[2:])  # Join all the parts of the content

    # Remove HTML special characters
    import html

    content = html.unescape(content)

    # If there are more than two spaces in the content, remove the extra spaces
    content = ' '.join(content.split())


    # Prepare the data to be sent
    data = {
        "username": username,
        "fullname": fullname,
        "gender": "unknown",  # we do not have this information
        "lokasyon": "unknown",  # we do not have this information
        "followers_count": 0,  # we do not have this information
        "following_count": 0,  # we do not have this information
        "tweet": {
            "content": content[:450],
            "likes_count": 0,  # we do not have this information
            "interactions_count": 0,  # we do not have this information
            "retweet_count": 0,  # we do not have this information
            "comments_count": 0,  # we do not have this information
            "category": "unknown",  # we do not have this information
            "pgsstatus": "unknown"  # we do not have this information
        },
        "created_at": "2023-06-27T00:00:00Z",
        "updated_at": "2023-06-27T00:00:00Z"
    }

    # Send a POST request
    print(data)
    response = requests.post('http://172.29.153.240/api/twitter/tweetgiris', json=data)
    # Check the response
    if response.status_code == 201:
        print('Successfully posted data to the API.')

        # If successful, update the 'geton' field for the URL
        url_update_data = {
            "url": url,
            "geton": True,
        }
        update_response = requests.post('http://172.29.153.240/api/twitter/twitter-update', json=url_update_data)

        if update_response.status_code == 200:
            print('Successfully updated the URL status.')
        else:
            print(f'Failed to update the URL status. Status code: {update_response.status_code}.')

    else:
        print(f'Failed to post data. Status code: {response.status_code}.')

    # Close the Selenium driver
    driver.quit()

    time.sleep(10)  # wait for 10 seconds before moving on to the next URL