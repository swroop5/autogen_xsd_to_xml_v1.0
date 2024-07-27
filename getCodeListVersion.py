
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def download_webpage(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the content of the webpage
            return response.text
        else:
            print(f"Failed to download webpage. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def scrape_webpage(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Now you can use BeautifulSoup to extract specific elements or data from the page
            # For example, to get all the text within <p> tags:
            paragraphs = soup.find_all('p')
            for paragraph in paragraphs:
                print(paragraph.get_text())
        else:
            print(f"Failed to download webpage. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def scrape_webpage_with_edge(url):
    try:
        # Create a Selenium WebDriver instance for Microsoft Edge
        edge_options = webdriver.EdgeOptions()
        # Set the path to the Microsoft Edge WebDriver executable
        edge_driver_path = 'C:\\Weehron\\Project\\XML\\python14\\edgedriver_win64\\msedgedriver.exe'
        driver = webdriver.Edge(edge_driver_path)

        # Load the webpage
        driver.get(url)

        # Wait for a few seconds to allow JavaScript to execute (you can adjust the wait time)
        driver.implicitly_wait(5)

        # Get the fully rendered page content
        page_content = driver.page_source

        # You can now process the page content as needed
        print(page_content)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the WebDriver when done
        driver.quit()
        
def scrape_webpage_with_selenium(url, code_list_name):
    try:
        
        # Create a Selenium WebDriver instance (you'll need to specify the path to your web driver)
        driver = webdriver.Chrome()

        # Load the webpage
        driver.get(url + code_list_name)

        #wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
        #element = wait.until(EC.presence_of_element_located((By.ID, "root")))

        # Wait for a few seconds to allow JavaScript to execute (you can adjust the wait time)
        driver.implicitly_wait(5)
        time.sleep(5)
        
        # Get the fully rendered page content
        element = driver.find_element(By.ID, "root")
        # Get the inner HTML of the element (including its children)
        inner_html = element.get_attribute("innerHTML")
        soup = BeautifulSoup(inner_html, 'html.parser')

        target_role = 'menuitem'
        target_class = 'details-version-list__item details-version-list__item--selected'
        # Find the <a> tag within the parsed HTML
        matching_a_tags = soup.find_all('a', role=target_role, class_=target_class)

        # Extract information from the matching <a> tags
        if len(matching_a_tags) == 1:
            for a_tag in matching_a_tags:
                if code_list_name in a_tag['href']:
                    link_text = a_tag.text
                    href = a_tag['href']
                    print("Text:", link_text)
                    print("Href:", href)
                    #return {'Href': href, 'Text': link_text}
                    return {code_list_name: link_text}
        return ''

        #link_element = driver.find_element_by_css_selector('a.details-version-list__item.details-version-list__item--selected[role="menuitem"]')

        # Get the outer HTML of the element (including the element itself and its children)
        #outer_html = element.get_attribute("outerHTML")

        #print("Inner HTML:")
        #print(inner_html)

        #print("Outer HTML:")
        #print(outer_html)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the WebDriver when done
        driver.quit()

with open('all_codelisten_typ3.txt', 'r+') as f:
    lines = f.readlines()
    for line in lines:
        code_list_name = line.strip('\n')
        url = 'https://www.xrepository.de/details/urn:xoev-de:xjustiz:codeliste:'
            
        content = scrape_webpage_with_selenium(url, code_list_name.lower())

        with open('codelist_vers_from_webp_upd.txt', 'a+') as f:
            f.write(str(content) + '\n')