import pandas as pd
import datetime as dt

from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
## new deploy####

options = Options()

options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')

options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
browser = webdriver.Chrome(executable_path=str(os.environ.get('CHROMEDRIVER_PATH')), chrome_options=options)
executable_path = {'executable_path':'GOOGLE_CHROME_BIN '}

def scrape_mars():
    url = 'https://mars.nasa.gov/news/'

    ########
    '''for splinter traversal'''
    ########
    # # browser = Browser('chrome',**executable_path, headless=True) # <<<<<<----- Set headless=False to have browser pop-up
    # browser.visit(url)
    # html = browser.html

    ##################
    '''selenium traversal'''
    ##################
    browser.get(url)
    html = browser.find_element_by_tag_name("body").get_attribute('innerHTML')

    # Create BeautifulSoup object; parse with 'lxml'
    nasa_gov = bs(html, 'lxml')
    # Returns a list of all the content title, only saving the first found (index [0]) as it is most recent.
    news_title = nasa_gov.find_all('div', class_="content_title")[0].get_text()
    # Returns a list of all the title body  contents/paragraphs, only saving the first found (index [0]) as it is most recent.
    news_content = nasa_gov.find_all('div', class_="article_teaser_body")[0].get_text()



    # Set initial url to JPL mars topic content.
    url2 ="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    #############
    '''Splinter traversal'''
    #############
    # browser = Browser('chrome',**executable_path, headless=True) # <<<<<<----- Set headless=False to have browser pop-up
    # # Visit landing page
    # browser.visit(url2)
    # # Save HTML to variable
    # jpl_html = browser.html

    ###################
    '''Selenium  traversal'''
    ###################
    browser.get(url2)
    jpl_html = browser.find_element_by_tag_name('body').get_attribute('innerHTML')



    # Create BSoup object. Parse HTML
    jpl = bs(jpl_html, 'html.parser')
    # Featured image on landing page is not the full size image.
    # Path to the full size image is contained within an <a> tag's href in the footer element.
    # This is the concise refactored code
    jpl_base = 'https://www.jpl.nasa.gov'
    jpl_link_format = str( jpl_base + (jpl.find_all('footer')[0].a.get('data-link')))

    # #Visit the next page i.e the page where we find the full size image.
    ######################## Splinter traversal
    # browser = Browser('chrome',**executable_path, headless=True) # <<<<<<----- Set headless=False to have browser pop-up
    # browser.visit(jpl_link_format)
    # # Save the html to var
    # jpl_target = browser.html

    ###########################
    '''Selenium traversal'''
    ###########################
    browser.get(jpl_link_format)
    jpl_target = browser.find_element_by_tag_name('body').get_attribute('innerHTML')

    # Create new Soup object
    jpl_target_html = bs(jpl_target, 'html.parser')
    # Refactored: Find the featued image url. Concise method
    featured_img_url = str( jpl_base+ ( jpl_target_html.find_all('figure', class_='lede')[0].a.get('href') )  )




    mars_twit="https://twitter.com/marswxreport?lang=en"
    ####################
    '''Splinter traversal'''
    ######################
    # browser = Browser('chrome',**executable_path, headless=True) # <<<<<<----- Set headless=False to have browser pop-up
    # #Visit the page
    # browser.visit(mars_twit)
    # # Save browsed page to var
    # mars_browse = browser.html

    ###################
    '''Selenium traversal'''
    ##################
    browser.get(mars_twit)
    mars_browse = browser.find_element_by_tag_name('body').get_attribute('innerHTML')

    # Parse HTML
    mars_twit_html = bs(mars_browse,'html.parser')
    # Returns a list of all <P> tags wityh class 'tweet-text'. This is where the tweets written content is contained.
    mars_tweet = mars_twit_html.find_all('p', class_='tweet-text')[0].text
    # Tweet <p> text is returned with '\n' newline special chatacter. .r/l/strip() neither worked. Must use replace.
    mars_tweet = mars_tweet.replace('\n',',')




    # Use pandas to read in the tabular data of facts
    facts_url = 'http://space-facts.com/mars/'
    mars_facts = pd.read_html(facts_url)
    # Reconstruct mars_facts DF(result of the scrape), to a dataframe that doesn't require list indexing.
    mars_facts_pd = pd.DataFrame(mars_facts[0])
    # Rename columns
    mars_facts_pd = mars_facts_pd.rename(columns = {0:'Descriptor',1:'Data'})
    mars_facts_pd = mars_facts_pd.set_index('Descriptor')
    mars_facts_html = mars_facts_pd.to_html()




    image_site_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    image_site_base = 'https://astrogeology.usgs.gov'

    ####################
    '''Splinter traversal'''
    ######################
    # browser = Browser('chrome',**executable_path, headless=True) # <<<<<<----- Set headless=False to have browser pop-up
    # #Visit the page
    # browser.visit(image_site_url)
    # # Save browsed page to var
    # mars_img_browse = browser.html

    ###################
    '''Selenium traversal'''
    ##################
    browser.get(image_site_url)
    mars_img_browse = browser.find_element_by_tag_name('body').get_attribute('innerHTML')

    # Parse HTML
    mars_img_html = bs(mars_img_browse,'html.parser')
    # Initialize list to store the link to the webpage for an individual hemisphere
    mars_hemi_targets = []
    # Link contained in a <div> , that has a nested <a>. Use .get() to access the a href.
    # Concat the website base url to the href before appending to list of links used in next traversal.
    [mars_hemi_targets.append(image_site_base + div.a.get('href')) for div in mars_img_html.find_all('div', class_='description')]

    # Create empty list for storing the image title and URL dictionary
    #Ex:  {"title": "Valles Marineris Hemisphere", "img_url": "..."},
    hemi_title_url = []

    #Loop through the 4 targets which correspond to individal pages for each hemisphere.
    # headless=True to execute without browser pop-up
    for target in mars_hemi_targets:

        ####################
        '''Splinter traversal'''
        ######################
        # browser = Browser('chrome', headless=True)
        # #Visit the page
        # browser.visit(target)
        # # Save browsed page to var
        # target_obj = browser.html

        ###################
        '''Selenium traversal'''
        ##################
        browser.get(target)
        target_obj = browser.find_element_by_tag_name('body').get_attribute('innerHTML')

        # Parse HTML
        target_html= bs(target_obj,'html.parser')
        # Even though the is only one h2 with class='title', find_all() returns the results as a list. Must use index [0].
        title = target_html.find_all('h2', class_='title')[0].text
        # Same logic as above
        hemi_url = target_html.find_all('a', text='Sample')[0].get('href')
        # Append the result in dict format to the empty list created prior
        hemi_title_url.append({'title':title,'img_url':hemi_url})



    content_data = {'news_title':news_title, 'news_content':news_content,
                   'featured_img_url':featured_img_url,'mars_tweet':mars_tweet,
                   'hemisphere_data':hemi_title_url, 'facts_tab_html': mars_facts_html}

    browser.quit()

    return content_data
