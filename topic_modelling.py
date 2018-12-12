#Importing Libraries
import string
import gensim
from gensim import corpora
import csv
import pandas as pd
import os
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from gensim.models.coherencemodel import CoherenceModel
stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

# cleaning the data by removing stop words and lemmatizing the data
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

# reading the data set into a dataframe
df = pd.read_csv(os.path.expanduser(r"~/Desktop/google/google_app_reviews.csv"), encoding='unicode_escape', sep=",")
main_pol_list = []
main_sub_list =[]
Perplexity = []
Coherence = []
Topic = []
i = 0
if __name__ == '__main__':
    # Itterating through each row
    for rows in df.reviews:
        if __name__ == '__main__':
            doc_complete = rows.split(',')
            doc_clean = [clean(doc).split() for doc in doc_complete]
            # defining dictionary
            dictionary = corpora.Dictionary(doc_clean)
            doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
            # defining model
            Lda = gensim.models.ldamodel.LdaModel
            # executing the model
            ldamodel = Lda(doc_term_matrix, num_topics=3, id2word = dictionary, passes=50)
            t = ldamodel.print_topics(num_topics=3, num_words=3)
            Topic.append(t)
            # calculating perplexity of the model
            p = ldamodel.log_perplexity(doc_term_matrix)
            Perplexity.append(p)
            # calculating coherance of the model
            cm = CoherenceModel(model=ldamodel, texts=doc_clean, dictionary=dictionary, coherence='c_v')
            c = cm.get_coherence()
            Coherence.append(c)
            print(Topic)

# Writing the dataframe back to the .csv file
if __name__ == '__main__':
    print(Topic)
    print(Perplexity)
    print(Coherence)
    df['Topic'] = Topic
    df['Perplexity'] = Perplexity
    df['Coherence'] = Coherence
    df.to_csv(os.path.expanduser(r"~/Desktop/google/google_app_reviews.csv"),index=False)

