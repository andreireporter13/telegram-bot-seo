# My telegram, like my web app made in Flask: seo_keyword_extractor;
#
# Telegram bot for SEO - SEO keyword extract v.1;
#
#
# New scraper (Flask) idea - scrape keywords from blogs - https://keywords-extract-seo.herokuapp.com/;
#
# Author: Andrei C. Cojocaru
# Github: https://github.com/andreireporter13
# LinkedIn: https://www.linkedin.com/in/andrei-cojocaru-985932204/
# Twitter: https://twitter.com/andrei_reporter
# Website: https://ideisioferte.ro && https://webautomation.ro
# Telegram bot - t.me/seokeywordsextractbot 
#
#
import telebot
from config import data_config
#
from rake_nltk import Rake
from scrap_data import extract_text
#
import io
#
import csv
import pandas as pd
import re
#


# define bot;
bot = telebot.TeleBot(data_config['TOKEN'])


# create a first start comand;
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, """

    Deci, poti afla mai multe despre SEO:
    1. /keywords - Download keywords from a blog article or a news story;
    2. /SEO - What does SEO mean!
    3. /video - How Video Content helps you with SEO;
    4. /writing - How Content Writing helps you;
    5. /index - how do you find out how well the site is indexed?
    6. /programming - Programming in the SEO process;
    """)

# this section is for keywords command - and return csv with keywords;
@bot.message_handler(commands=['KEYWORDS', 'Keywords', 'keywords'])
def get_seo_info(message):
    
    link = bot.send_message(message.chat.id, 'Please, insert your blog post link with "https://" in the front: ')
    # get only one command;

# this is about SEO commands;
@bot.message_handler(commands=['SEO', 'Seo', 'seo'])
def get_seo_info(message):
    bot.reply_to(message, 'This is the world where the SEO journey begins: https://www.semrush.com/blog/12-free-keyword-research-tools/?kw=&cmp=EE_SRCH_DSA_Blog_Core_BU_EN&label=dsa_pagefeed&Network=g&Device=c&utm_content=515816319497&kwid=dsa-1057183196875&cmpid=11776420745&agpid=113999303026&BU=Core&extid=23623718551&adpos=&gclid=CjwKCAjwrZOXBhACEiwA0EoRD6IY9aId9OiitUvNWanA8NI6aoVWdNrzHuu83W6vL1G9zWCxZ-yK5xoCrP4QAvD_BwE')


# this is about video SEO; 
@bot.message_handler(commands=['VIDEO', 'Video', 'video'])
def get_seo_video_info(message):
    bot.reply_to(message, 'This is the world where the SEO journey begins: https://www.semrush.com/blog/youtube-keyword-tools/?kw=&cmp=EE_SRCH_DSA_Blog_Core_BU_EN&label=dsa_pagefeed&Network=g&Device=c&utm_content=515715515937&kwid=dsa-1202477529003&cmpid=11776420745&agpid=119698375099&BU=Core&extid=23623719091&adpos=&gclid=CjwKCAjwrZOXBhACEiwA0EoRD35fEpLR4PJ1qhRbNg3l-6ZJ0dnvXvzQV10qRzGM7km_olTxBBt_QhoCBH4QAvD_BwE')


# this is about writing in SEO;
@bot.message_handler(commands=['WRITING', 'Writing', 'writing'])
def get_seo_writing_info(message):
    bot.reply_to(message, 'This is the world where the SEO journey begins: https://www.wiley.com/network/researchers/preparing-your-article/how-to-choose-effective-keywords-for-your-article')


# about domain authority checker;
@bot.message_handler(commands=['INDEX', 'Index', 'index'])
def get_seo_domain_info(message):
    bot.reply_to(message, 'This is the world where the SEO journey begins: https://websiteseochecker.com/domain-authority-checker/')


# for programming in SEO;
@bot.message_handler(commands=['PROGRAMMING', 'Programming', 'programming'])
def get_seo_domain_info(message):
    bot.reply_to(message, 'This is the world where the SEO journey begins: https://www.jcchouinard.com/python-for-seo/')


@bot.message_handler(content_types=['text'])
def echo_all(message):

    # catch a link -------------------------LINK CATCH ------------------------------>
    if message.text.startswith('https://') or message.text.startswith('http://'):
        link_for_extract = extract_text(message.text)
        # try to make it;
        r = Rake()
        r.extract_keywords_from_text(link_for_extract)

        # write data in list;
        list_with_keywords = []

        # run within for loop;
        for rating, keywords in r.get_ranked_phrases_with_scores():
            list_with_keywords.append([rating, keywords])

        # -----------------------
        re_expression = '[^https://]\w*[.]'
        #------------------------

        move_io = io.StringIO()
        csv.writer(move_io).writerows(list_with_keywords)
        move_io.seek(0)

        buff = io.BytesIO()
        buff.write(move_io.getvalue().encode())
        buff.seek(0)

        # buff_name = f'keywords-{re.findall(re_expression, message.text)[0][:-1]}.csv'
        bot.send_document(chat_id=message.chat.id, document=buff)

        # write data to csv;
        # headers = ['rating', 'keywords']
        # df = pd.DataFrame(list_with_keywords, columns = headers)
        # df.to_csv(f"keywords-{re.findall(re_expression, message.text)[0][:-1]}.csv", encoding="utf8")

    # ----------------------------------------------------------LINK END ------------------------>

    # catch a message;
    elif message.text.lower() == 'hello':
	    bot.reply_to(message, 'Hello, can we help you?')
    elif message.text.lower() == 'hi':
	    bot.reply_to(message, 'Hi, can we help you?')
    elif message.text.lower() in ['seo', 'keywords', 'video', 'writing', 'index', 'programming', 'start', 'help']:
        bot.send_message(message.chat.id, 'To be able to take advantage of the command, put a: / in front of the word.')
    else:
        bot.reply_to(message, 'Try the /start or /help commands for more details.')


if __name__ == "__main__":
    bot.polling(non_stop=True, interval=0)