from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import pickle
import sys
from collections import namedtuple
sentimentTuple = namedtuple("Sentiment", field_names=["sentiment", "p_pos", "p_neg"])
n = NaiveBayesAnalyzer()
for file in sys.argv[1:]:
    with open(file, "rb") as f:
        df = pickle.load(f)
    l = []
    for i, tweet in enumerate(df['tweet']):
        #print("{}/{}".format(i, len(df['tweet'])))
        s = n.analyze(tweet)

        l.append((s.classification, s.p_pos, s.p_neg))
    pos = len(list(filter(lambda x: x[0] == 'pos', l)))
    neg = len(list(filter(lambda x: x[0] == 'neg', l)))
    print("Candidate Name: "+file)
    print("Total positive tweets: {}".format(pos))
    print("Total negative tweets: {}".format(neg))
    print('negative to total ratio: {}'.format(neg / (neg + pos)))
    with open(file.replace(".pkl", "")+"Sentiment.pkl", "wb") as f:
        pickle.dump(l, f)
        f.close()
