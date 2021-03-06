# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
# full_image_elem.click(). --> The button "More" is not clickable at moment


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)

df.to_html()

##browser.quit()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.container', wait_time=1)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
title_lst = []
url_lst = []
urlFull_img_lst = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# Parse the HTML
html = browser.html
html_soup = soup(html, 'html.parser')

# Define the sections for scrape
section = html_soup.find('div', class_= 'collapsible results')
items = section.find_all('div', class_='item')

# ForLoop in each items
for item in items:
    # Scrape the title
    title = item.find('h3').text
    title_lst.append(title)
    
    # Scrape the url for the detail page
    url = f'https://marshemispheres.com/{item.find("a")["href"]}'
    url_lst.append(url)
    
    # Go to the detail page - Use browser to visit the URL 
    browser.visit(url)
    
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.container', wait_time=1)
    
    # Parse the HTML detail page
    html = browser.html
    html_soup = soup(html, 'html.parser')
    
    # Scrape the full image url
    section = html_soup.find('div', class_='downloads')
    url_full_img = f'https://marshemispheres.com/{section.find("a")["href"]}'
    urlFull_img_lst.append(url_full_img)


for url,title in zip(urlFull_img_lst,title_lst):
    # Create the dictonary
    dic = {
        "img_url": url,
        "title": title
    }
    # Add the objet to the list
    hemisphere_image_urls.append(dic)

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# 5. Quit the browser
browser.quit()




