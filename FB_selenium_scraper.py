# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from unidecode import unidecode
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# other necessary ones
import pandas as pd
import time


option = Options()
option.add_argument('--headless')
option.set_preference("browser.cache.disk.enable", False)
option.set_preference("browser.cache.memory.enable", False)
option.set_preference("browser.cache.offline.enable", False)
option.set_preference("network.http.use-cache", False)
option.add_argument("--disable-notifications")
option.binary_location = r"C:/Program Files/Mozilla Firefox/firefox.exe"

# once logged in, free to open up any target page

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


for i in company:
    browser = webdriver.Firefox(options=option)
    # Log into FB and go to relvant company page

    browser.get("https://www.facebook.com")
    wait = WebDriverWait(browser, 30)
    email_field = wait.until(
        EC.visibility_of_element_located((By.NAME, 'email')))
    email_field.send_keys('USERNAME')
    pass_field = wait.until(
        EC.visibility_of_element_located((By.NAME, 'pass')))
    pass_field.send_keys('PASSWORD')
    pass_field.send_keys(Keys.RETURN)
    time.sleep(5)
    browser.get(
        f'https://www.facebook.com/{i}')

    # Print current company name
    print(i)

    time.sleep(5)

    ## FUNCTIONS ##

    def filter_comments(browser, filter):

        action = ActionChains(browser)

        if len(filter) > 0:
            for j in filter:
                try:
                    browser.execute_script(
                        "arguments[0].scrollIntoView(true)", j)
                    browser.execute_script("arguments[0].click();", j)

                except NoSuchElementException:
                    try:
                        action.move_to_element(j).click().perform()

                    except:
                        continue

    def error_loop(find):
        n = 0
        try:
            treasure = find.find_element(By.XPATH,
                                         ".//span[contains(@class,'d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em iv3no6db jq4qci2q a3bd9o3v ekzkrbhg oo9gr5id hzawbc8m') and contains(text(), 'All comments')]")
        except NoSuchElementException:
            try:
                n += 1
                error_loop(find)
                print(n, 'times')
            except:
                pass
        return treasure

    def filter_all_comments(browser, filter):
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        filter_box = browser.find_elements(By.XPATH,
                                           "//div[contains(@class, 'j34wkznp qp9yad78 pmk7jnqg kr520xx4')]")
        print(len(filter_box), 'box list length')
        filter_all = []
        check = True
        last_height = browser.execute_script(
            "return document.body.scrollHeight")
        count = 0
        while check is True:
            if len(filter_box) >= len(filter):
                check = False
            else:
                browser.execute_script(
                    "window.scrollBy(0, -2000);")
                filter_box = browser.find_elements(By.XPATH,
                                                   "//div[contains(@class, 'j34wkznp qp9yad78 pmk7jnqg kr520xx4')]")
                print(len(filter_box), ' box list length in progress')
                new_height = browser.execute_script(
                    "return document.body.scrollHeight")
                if new_height == last_height:
                    count += 1
                if count > 100:
                    count = 0
                    browser.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);")
                new_height = last_height

        for j in filter_box:
            try:
                element = j.find_element(By.XPATH,
                                         ".//span[contains(@class,'d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em iv3no6db jq4qci2q a3bd9o3v ekzkrbhg oo9gr5id hzawbc8m') and contains(text(), 'All comments')]")
                filter_all.append(element)
            except NoSuchElementException:
                try:
                    element = j.find_element(By.XPATH,
                                             ".//span[contains(@class,'d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d9wwppkn mdeji52x sq6gx45u a3bd9o3v b1v8xokw m9osqain hzawbc8m') and contains(text(), 'Show all comments, including potential spam. The most relevant comments will appear first.')]")
                    filter_all.append(element)
                except:
                    continue

        print(len(filter_box), 'filter all buttons')

        print(len(filter_all), 'filter_all buttons identified')

        action = ActionChains(browser)
        count = 0

        for i in filter_all:
            try:
                browser.execute_script(
                    "arguments[0].scrollIntoView(true);", i)
                browser.execute_script(
                    "arguments[0].click();", i)
                count += 1
                print('try n#:', count)

            except StaleElementReferenceException:
                try:
                    action.move_to_element(i).perform()
                    action.click(i).perform()
                except StaleElementReferenceException:
                    pass

        print(count, 'number of filter elements clicked')

    def check_month_limit(year, month):
        if browser.find_elements(By.XPATH, f"//a[contains(@class,'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw') and contains(@aria-label, {year}) and contains(@aria-label, {month})]") is not NoSuchElementException:
            return True
        else:
            return False

    def view_more(browser):
        browser.execute_script(
            "window.scrollTo(0, -document.body.scrollHeight);")
        time.sleep(4)
        moreComment = browser.find_elements(
            By.XPATH, "//div[contains(@class,'oajrlxb2 g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 mg4g778l p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb n00je7tq arfg74bv qs9ysxi8 k77z8yql pq6dq46d btwxx1t3 abiwlrkh lzcic4wl bp9cbjyn m9osqain buofh1pr g5gj957u p8fzw8mz gpro0wi8')]")

        if len(moreComment) > 0:

            oldmoreComment = []
            n = 0
            for j in moreComment:
                n += 1
                oldmoreComment.append(j)
                try:
                    browser.execute_script(
                        "arguments[0].click();", j)
                    print('clicked', n)

                except StaleElementReferenceException:
                    pass
                    print('skipped!!!', n)

            moreComment = browser.find_elements(
                By.XPATH, "//div[contains(@class,'oajrlxb2 g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 mg4g778l p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb n00je7tq arfg74bv qs9ysxi8 k77z8yql pq6dq46d btwxx1t3 abiwlrkh lzcic4wl bp9cbjyn m9osqain buofh1pr g5gj957u p8fzw8mz gpro0wi8')]")

        else:
            moreComment = browser.find_elements(
                By.XPATH, "//div[contains(@class,'oajrlxb2 g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 mg4g778l p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb n00je7tq arfg74bv qs9ysxi8 k77z8yql pq6dq46d btwxx1t3 abiwlrkh lzcic4wl bp9cbjyn m9osqain buofh1pr g5gj957u p8fzw8mz gpro0wi8')]")

    def getBack(browser):
        if not browser.current_url.endswith(f'{i}'):
            print('redirected!!!')
            browser.back()
            print('got back!!!')

    def archiveAtEnd(browser):
        # scroll back to the top
        browser.execute_script(
            "window.scrollTo(0, -document.body.scrollHeight);")
        time.sleep(3)

        with open(r'C:/path/web_scrap'+f"{i}.html", "w", encoding="utf-8") as file:
            source_data = browser.page_source
            bs_data = bs(source_data, 'html.parser')
            file.write(str(bs_data.prettify()))

        print('archived: ', f'{i}', '!!')

    ## CONTENT ANALYSIS ##
    count = 0
    switch = True
    old_numReviews = 0
    specifiedYear = '2019'  # stop date
    stopYear = '2019'
    stopMonth = 'December'

    def check_date_limit():
        try:
            browser.find_element(
                By.XPATH, f"//a[contains(@class,'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw') and contains(@aria-label, {specifiedYear})]")
        except NoSuchElementException:
            return False
        return True

    element = browser.find_element(By.TAG_NAME, 'body')
    last_height = browser.execute_script(
        "return document.body.scrollHeight")

    while switch:
        count += 1
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        new_height = browser.execute_script(
            "return document.body.scrollHeight")
        if new_height == last_height:
            browser.execute_script(
                "window.scrollBy(0, -1500);")
            print('help im stuckkk!!!')
        new_height = last_height

        if check_date_limit() is True:
            switch = False

    wait = WebDriverWait(browser, 10)

    filter = browser.find_elements(
        By.XPATH, "//div[contains(@class,'rq0escxv l9j0dhe7 du4w35lb bp9cbjyn pq6dq46d sf5mxxl7')]")

    filter_comments(browser, filter)
    getBack(browser)

    filter_all_comments(browser, filter)
    getBack(browser)

    # Loop clicking on view_more until reaching target post date
    while check_month_limit(stopYear, stopMonth) is False:
        view_more(browser)
        getBack(browser)
    view_more(browser)
    print('finished fetching comments!!')
    archiveAtEnd(browser)
    time.sleep(3)
    browser.quit()
    time.sleep(3)
