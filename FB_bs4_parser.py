import datetime
import re
import time
import json
import pandas as pd
import urllib.request
from unidecode import unidecode
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as bs
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from numpy import full
from pickle import TRUE
from os import remove
import numbers
from multiprocessing.dummy import current_process
from inspect import FullArgSpec
from asyncio.subprocess import DEVNULL

company = [

    # By Market Cap
    "jnj",
    "roche",
    "Pfizer",
    "AbbVieGlobal",
    "novonordisk",
    "novartis",
    "elilillyandco",
    "BristolMyersSquibb",
    "CVSHealth",
    "GSK",
    "amgenbiotech",
    "Regeneron",
    "modernatx",
    "Bayer",
    "LonzaGroupAG",
    "Biogen",
    "SunPharmaLive",
    "HorizonTherapeutics",
    "PPDCRO",
    "Servier",
    "boehringeringelheim",
    "Abbott",
    "Incyte",
    "Dr.ReddysLaboratoriesLtd"
]

##Functions##


def remove_reaction_strings(list, new_list, num):
    for i in list:

        i = i.replace('K', '000')

        for j in i:
            if j not in num:

                i = i.replace(j, '')

        new_list.append(i)


## DATA EXTRACTION ##

# Final csv files

FinalMeta = []
FinalComment = []

for i in company:
    with open(f'C:/web_scrap{i}.html', "r", encoding="utf-8") as file:
        f = file.read()

    page = bs(f, 'lxml')

    shares = page.find_all('span', {
        'class': 'd2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em iv3no6db jq4qci2q a3bd9o3v b1v8xokw m9osqain'})

    # Removing user names
    user_mention = page.find_all('span', {"class": "nc684nl6"})
    for match in user_mention:
        match.decompose()

    reviews = page.find_all('div', {
        'class': 'du4w35lb k4urcfbm l9j0dhe7 sjgh65i0'
    })

    #### Posts ####
    ref_titles = []
    ref_posts = []
    id = []
    titles = []
    descriptions = []
    dates = []
    Shares = []
    Shares_new = []
    Like = []
    Love = []
    Haha = []
    Angry = []
    Wow = []
    Like_new = []
    Love_new = []
    Haha_new = []
    Angry_new = []
    Wow_new = []
    num_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    shares = page.find_all('span', {
        'class': 'd2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em iv3no6db jq4qci2q a3bd9o3v b1v8xokw m9osqain'})
    # removing comment spans and text from shares
    for share in shares:
        if share is None:
            Shares.append('0')
        else:
            Shares.append(share.get_text().strip())

    for share in Shares:
        if "Share" in share:
            for string in share:
                if string not in num_list:
                    share = share.replace(string, '')
            Shares_new.append(share)

    for idx, r in enumerate(reviews):

        # Set reference of company
        ref_titles.append(company.index(i))

        # Set reference for post
        ref_posts.append(str(idx))

        # Titles

        title = r.find(
            'div', {'class': 'kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q'})
        if title is not None:
            title_txt = ' '.join([i.strip() for i in title.get_text().split()])
            fxd_title_txt = unidecode(title_txt)
            titles.append(fxd_title_txt)
        else:
            title = r.find(
                'div', {'class': 'kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql'})
            if title is not None:
                title_txt = title.get_text().strip()
                fxd_title_txt = unidecode(title_txt)
                titles.append(fxd_title_txt)
            else:
                titles.append('no title')

        # Dates

        date = r.find(
            'a', {'class': 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw'}).get('aria-label')
        if date == None:
            dates.append('the Dawn of TiMe')
        elif (' ' not in date) and ('h' in date):
            dates.append('February 19, 2022')  # REMEMBER TO CHANGE
        elif (' ' not in date) and ('d' in date):
            date0 = datetime.datetime.strptime('10/01/21', "%m/%d/%y")
            date1 = date0 - datetime.timedelta(days=int(date[0]))
            dates.append(date1)
        elif ('2021' in date) or ('2020' in date) or ('2019' in date) or ('2018' in date):
            dates.append(date)
        else:
            dates.append(' '.join(date.split()[:2])+', 2022')

    #### And their Reactions ####

    reaction_types_str = [
        'Like',
        'Love',
        'Haha',
        'Angry',
        'Wow'
    ]

    reaction_types = [
        Like,
        Love,
        Haha,
        Angry,
        Wow
    ]

    reaction_types_new = [
        Like_new,
        Love_new,
        Haha_new,
        Angry_new,
        Wow_new
    ]

    reaction_lists = {
        'Like': Like,
        'Love': Love,
        'Haha': Haha,
        'Angry': Angry,
        'Wow': Wow
    }

    for types in reaction_types_str:
        for r in reviews:
            presence = r.find('div', {"class": "oajrlxb2 gs1a9yip g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 mg4g778l pfnyh3mw p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb n00je7tq arfg74bv qs9ysxi8 k77z8yql pq6dq46d btwxx1t3 abiwlrkh p8dawk7l lzcic4wl", "aria-label": re.compile(r".*({}).*".format(types))})
            if presence is None:
                reaction_lists[types].append('0')
            else:

                reaction_lists[types].append(presence['aria-label'])

    for types, types_new in zip(reaction_types, reaction_types_new):
        remove_reaction_strings(types, types_new, num_list)

    master = {
        'coref': ref_titles,
        'postref': ref_posts,
        'Titles': titles,
        'Dates': dates,
        'Shares': Shares_new,
        'Like': Like_new,
        'Love': Love_new,
        'Haha': Haha_new,
        'Angry': Angry_new,
        'Wow': Wow_new
    }

    master = pd.DataFrame.from_dict(master, orient='index')
    master = master.transpose()
    master.to_csv(r'C:/Users/theog/Desktop/diss/Meta_Data/' +
                  f'Meta_{i}.csv', index=False)

    #### Comments ####
    ref_comments = []
    ref_individual = []
    ids = []
    texts = []

    for idx, r in enumerate(reviews):
        comments = r.find_all('span', {
            "class": "d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em iv3no6db jq4qci2q a3bd9o3v b1v8xokw oo9gr5id"})

        for comment in comments:
            ids.append(str(idx))
            ref_individual.append(comments.index(comment))
            ref_comments.append(company.index(i))
            if comment is None:
                texts.append('no text')
            else:
                fixed_comment_text = unidecode(comment.get_text().strip())
                texts.append(fixed_comment_text)

    replies = {
        'Company ID': ref_comments,
        'Post ID': ids,
        'Comment ID': ref_individual,
        'Text': texts
    }
    reply_master = pd.DataFrame.from_dict(replies, orient='index')
    reply_master = reply_master.transpose()
    reply_master.to_csv(
        r'C:/path'+f'Comments_{i}.csv', index=False)


meta_frames = []
comment_frames = []
for i in company:
    meta_frames.append(pd.read_csv(
        r'C:/path/Meta_Data/'+f'Meta_{i}.csv'))
    comment_frames.append(pd.read_csv(
        r'C:/path/Comment_Data/'+f'Comments_{i}.csv'))

# combining meta
combined_meta = pd.concat(meta_frames, ignore_index=True)
combined_meta.to_csv('Full_Meta.csv', index=False)

# combining comments
combined_meta = pd.concat(comment_frames, ignore_index=True)
combined_meta.to_csv('Full_Comments.csv', index=False)
