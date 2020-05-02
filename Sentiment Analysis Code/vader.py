import os
import pickle
from collections import namedtuple

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# pip install vaderSentiment

sentimentTuple = namedtuple("Sentiment", field_names=["sentiment", "p_pos", "p_neg"])  # ???
analyzer = SentimentIntensityAnalyzer()
for file in os.listdir("Followers of Candidates/"):
    with open("Followers of Candidates/" + file, "rb") as f:
        df = pickle.load(f)
    l = []
    for i, tweet in enumerate(df['tweet']):
        # print("{}/{}".format(i, len(df['tweet'])))
        s = analyzer.polarity_scores(tweet)['compound']
        if s > 0.05:
            l.append(('pos', s))
        elif s < -0.05:
            l.append(('neg', s))
        else:
            l.append(('neutral', s))
        # l.append((s.classification, s.p_pos, s.p_neg))
    pos = len(list(filter(lambda x: x[0] == 'pos', l)))
    neg = len(list(filter(lambda x: x[0] == 'neg', l)))
    print("Candidate Name: " + file)
    print("Total positive tweets: {}".format(pos))
    print("Total negative tweets: {}".format(neg))
    print('negative to total ratio: {}'.format(neg / (neg + pos)))
    with open(file.replace(".pkl", "") + "Sentiment.pkl", "wb") as f:
        pickle.dump(l, f)
        f.close()
