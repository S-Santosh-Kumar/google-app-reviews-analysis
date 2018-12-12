# importing libraries
import pandas as pd
import os, re
import ast
import csv
from textblob import TextBlob

# Reading the .csv file into a dataframe
df = pd.read_csv(os.path.expanduser(r"~/Desktop/google/google_app_reviews.csv"), encoding='unicode_escape', sep=",")

# Iterating through each row
for index, row in df.iterrows():
    app_title = row['Title']
    app_developer = row['Developer']
    app_review = row['reviews']
    item = app_review.split(',')
    for rev in item:
        print_list = []
        blob = TextBlob(rev)
        polarity = blob.polarity
        subjectivity = blob.subjectivity
        rev = re.sub('[^a-zA-Z0-9| \n\.]', '', rev)
        if polarity > 0:
            sentiment = "Positive"
        elif polarity < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        #Writing dataframe back to the .csv file
        print_list = [app_title, app_developer, rev, polarity, subjectivity, sentiment]
        with open(os.path.expanduser(r"~/Desktop/google/sentiment_google_app_reviews.csv"),"a",encoding='utf-8') as w_file:
                csv_app = csv.writer(w_file)
                csv_app.writerow(print_list)
