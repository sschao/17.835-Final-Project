import os
import pickle
import random
import re
import string

import nltk
from nltk import NaiveBayesClassifier
from nltk.corpus import twitter_samples, stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize


def remove_noise(tweet_tokens, stop_words=()):
    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token


def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)


nltk.download('twitter_samples')  # only need to run once
nltk.download('punkt')  # only need to run once (used for tokenization)
nltk.download('wordnet')  # only need to run once (used for normalization)
nltk.download('averaged_perceptron_tagger')  # only need to run once (used for normalization)
nltk.download('stopwords')  # only need to run once (used for removing noise)

# get training data
positive_tweets = twitter_samples.strings('positive_tweets.json')
negative_tweets = twitter_samples.strings('negative_tweets.json')
neutral_tweets = twitter_samples.strings('tweets.20150430-223406.json')

# words to ignore
stop_words = stopwords.words('english')

# tokenize training data
positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

# clean tokenized training data
positive_cleaned_tokens_list = []
negative_cleaned_tokens_list = []

for tokens in positive_tweet_tokens:
    positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

for tokens in negative_tweet_tokens:
    negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

# change format to prepare for model
positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

positive_dataset = [(tweet_dict, "Positive") for tweet_dict in positive_tokens_for_model]
negative_dataset = [(tweet_dict, "Negative") for tweet_dict in negative_tokens_for_model]

train_data = positive_dataset + negative_dataset
random.shuffle(train_data)

# create classifier
classifier = NaiveBayesClassifier.train(train_data)
print("HERE")
for file in os.listdir("Followers of Candidates/"):
    with open("Followers of Candidates/" + file, "rb") as f:
        df = pickle.load(f)
    l = []
    for i, tweet in enumerate(df['tweet']):
        # print("{}/{}".format(i, len(df['tweet'])))
        custom_tokens = remove_noise(word_tokenize(tweet))
        s = classifier.classify(dict([token, True] for token in custom_tokens))
        if s == 'Positive':
            l.append(('pos',))
        else:
            l.append(('neg',))
        # l.append((s.classification, s.p_pos, s.p_neg))
    pos = len(list(filter(lambda x: x[0] == 'pos', l)))
    neg = len(list(filter(lambda x: x[0] == 'neg', l)))
    print("Candidate Name: "+file)
    print("Total positive tweets: {}".format(pos))
    print("Total negative tweets: {}".format(neg))
    print(file, pos, neg)
    print('negative to total ratio: {}'.format(neg / (neg + pos)))
    with open(file.replace(".pkl", "")+"Sentiment.pkl", "wb") as f:
        pickle.dump(l, f)
        f.close()