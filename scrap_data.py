# Libraries for request and prepare text to extract keywords;
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
#
from time import sleep
#


def set_headers():

    """ 
    This function is about setting headers for new requests. Is important step to scraping!
    """
    user_agent = UserAgent() # after set a random fake_useragent;

    HEADERS = {
        'User-Agent': user_agent.random,
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
        'DNT': '1'
    }

    return HEADERS


def extract_text(link):

    """ 
    This function extract text from link and return all text with h1, h2, h3 and p elements;
    """

    response = requests.get(link, headers=set_headers())
    sleep(1.5)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')

        # concatenate text here...
        concat_text = ''

        # try find h1;
        try:
            h1 = soup.find('h1').text

            if h1: 
                concat_text += h1 + '\n'

        except:
            h1 = ''       

        # try to find h2;
        try:
            h2 = soup.find_all('h2')

            # if h2 exist in the blog post;
            if h2:
                for elem_h2 in h2:
                    concat_text += elem_h2.text + '\n'

        except:
            h2 = ''


        # try to find h3;
        try:
            h3 = soup.find_all('h3')

            # if h3 exist in the blog post;
            if h3:               
                for elem_h3 in h3: 
                    concat_text += elem_h3.text + '\n'

        except:
            h3 = ''

        # try to find p;
        try:
            p_elements = soup.find_all('p')

            # Concatenate all elements;
            if p_elements:
                for p in p_elements:
                    concat_text += p.text + '\n'

        except:
            p_elements = ''


        return concat_text


    else: 
        return 'We have not acces to this site!!!'