#Google play store top and free app ratinngs and reviews scraper

#Importing Libraries
#Import urllib
import urllib.request, os, csv, re, sys, datetime, urllib.parse, requests, sys, time
import time
from bs4 import BeautifulSoup
from selenium import webdriver

Title = 'global Title'
Category = 'global Category'
Developer = 'global Developer'
Temp_Category = 'global Temp_Category'
i = 'global i'
x = 'global x'
Temp = 'global Temp'
Size = 'global Size'
Downloads = 'global Downloads'
Content_rating = 'global Content_rating'
reviews = 'global reviews'
Temp_reviews = 'global Temp_reviews'
Cost = 'global Cost'
cat = 'global Cat'
m_Temp = 'global m_Temp'

#defining URL's
link_list = ["https://play.google.com/store/apps/collection/topselling_free?hl=en",
             "https://play.google.com/store/apps/collection/topselling_paid?hl=en",
             "https://play.google.com/store/apps/collection/topgrossing?hl=en",
             "https://play.google.com/store/apps/category/GAME/collection/topselling_free?hl=en",
             "https://play.google.com/store/apps/category/GAME/collection/topselling_paid?hl=en",
             "https://play.google.com/store/apps/category/GAME/collection/topgrossing?hl=en"]

# Itterating through each URL
for url in link_list:
    page_url = url
    driver = webdriver.Firefox(executable_path='C:\geckodriver.exe')
    driver.get(page_url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)
    page_html = driver.execute_script("return document.documentElement.outerHTML")
    driver.close()
    sel_page_soup = BeautifulSoup(page_html, "html.parser")

    all_tag_a = sel_page_soup.find_all(attrs={"class": "title"})
    #itterating through each link in the URL
    for links in all_tag_a:
        Title = ""
        Category = ""
        Developer = ""
        Temp_Category = ""
        i = 0
        x = 0
        Temp = ""
        Size = ""
        Downloads = ""
        Content_rating = ""
        reviews = ""
        Temp_reviews = ""
        Cost = ""
        Cat = ""
        m_Temp = ""

        #opening and reading each app and every link
        if links.get('href') is not None:

            prod_url = urllib.parse.urljoin('https://play.google.com',links.get('href'))
            prod_url_open = urllib.request.urlopen(prod_url)
            prod_readHtml = prod_url_open.read()
            prod_url_open.close()

            prod_soup = BeautifulSoup(prod_readHtml, "html.parser")

            rev_tag_a = prod_soup.find_all(attrs={"class": "title"})

            #Getting Title of the app from webpage
            Title = ""
            for containers1 in prod_soup.find_all(attrs={"class": "AHFaub"}):
                Title = containers1.span.text
                Title = Title.replace(",", "")

            #Getting Category and Developer of the app from webpage
            Category = ""
            Developer = ""
            Temp_Category = ""
            i = 1
            q = 1
            for containers2 in prod_soup.find_all(attrs={"class": "hrTbp R8zArc"}):
                if i == 1:
                    Developer = containers2.text
                    i += 1
                else:
                    Temp_Category = containers2.text
                    if q == 1:
                        Category = Temp_Category
                        q += 1
                    else:
                        Category = Category + " | " + Temp_Category
            Category = Category.replace(",", "")


            #Getting Size, Downloads and Content_rating of the app from webpage
            for containers3 in prod_soup.find_all(attrs={"class": "hAyfc"}):

                if containers3.div.text == "Size":
                    Size = containers3.span.div.span.text
                    Size = Size.replace(",", "")
                elif containers3.div.text == "Installs":
                    Downloads = containers3.span.div.span.text
                    Downloads = Downloads.replace(",", "")
                elif containers3.div.text == "Content Rating":
                    for containers6 in containers3.find_all('div'):
                        for containers7 in containers6.find_all(attrs={"class": "htlgb"}):
                            if containers7 is not None:
                                k = 0
                                for containers8 in containers7.find_all('div'):
                                    Content_rating_t = containers8.text
                                    if Content_rating_t != 'Learn More':
                                        if k == 0:
                                            Content_rating = Content_rating_t
                                            k += 1
                                        else:
                                            Content_rating = Content_rating + " | " + Content_rating_t
                                Content_rating = Content_rating.replace(","," ")


            #Getting Cost of the app from webpage
            Cost = ""
            for containers4 in prod_soup.find_all(attrs={"class": "LkLjZd ScJHi HPiPcc IfEcue "}):
                Cost = containers4.text
                Cost = Cost[0:len(Cost)-4]
                Cost = Cost.replace(",", "")
                if Cost == "Ins":
                    Cost = "$0.00"


            #opening and reading each app reviews
            reviews = []
            Temp_reviews = ""
            rev_url = urllib.parse.urljoin('https://play.google.com',links.get('href') + '&showAllReviews=true')
            driver = webdriver.Firefox(executable_path='C:\geckodriver.exe')
            driver.get(rev_url)
            html = driver.execute_script("return document.documentElement.outerHTML")
            sel_soup = BeautifulSoup(html, "html.parser")
            driver.close()
            Z = 0
            for containers5 in sel_soup.find_all(attrs={"class": "UD7Dzf"}):
                Temp_reviews = containers5.span.text
                Temp_reviews = Temp_reviews.replace(",", "")
                Temp_reviews = re.sub('[^a-zA-Z0-9| \n\.]', '', Temp_reviews)
                reviews.append(Temp_reviews)
        # Writing all values to a list
        if Title != "":
            Final_list = [Title,Developer,Category,Size,Downloads,Content_rating,Cost,reviews]
            print(Final_list)
            # Writing the list to a .CSV file
            with open(os.path.expanduser(r"~/Desktop/google/demo.csv"),"a",encoding='utf-8') as w_file:
                csv_app = csv.writer(w_file)
                csv_app.writerow(Final_list)

