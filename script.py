import requests
from bs4 import BeautifulSoup  

# Specify the URL
url = "https://www.accuweather.com/en/us/cambridge/02143/weather-forecast/329319?city=cambridge"

# Adding headers to simulate a web browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Send a GET request to the URL
response = requests.get(url, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the div with class "temp"
    temp_div = soup.find('div', class_='temp')

    # Check if the div was found
    if temp_div:
        # Extract and print the contents of the div
        temperature = temp_div.get_text(strip=True)
        print(f"Temperature in Cambridge: {temperature}")
    else:
        print("Div with class 'temp' not found on the page.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")