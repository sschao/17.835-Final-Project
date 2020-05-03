import os

import pandas as pd
import twint


# nest_asyncio.apply()
# could potentially remove this. It was running into looping errors on my setup without this

def followers(username, num_followers):
    """
    :param username: twitter username of candidate
    :param num_followers: number of follower to pull at once
    :return: list that has the username of the follower

    This code seems to be less reliable. It often breaks but its easier to use since the list is already stored
    """
    c = twint.Config()
    c.Limit = num_followers
    c.Username = username
    c.Pandas = True

    twint.run.Followers(c)

    Followers_df = twint.storage.panda.Follow_df
    list_of_followers = Followers_df['followers'][username]
    return list_of_followers


def followers_to_csv(username, num_followers): #preferred method
    """

    :param username: twitter username of candidate
    :param num_followers: number of followers to pull at once
    :return: nothing explicitly but csv with followers will be in '/{c.Output}/username.csv'

    this functions puts the followers' usernames in a csv rather storing it in memory
    """
    c = twint.Config()

    c.Username = username
    c.Custom["tweet"] = ["id"]
    c.Custom["user"] = ["bio"]
    c.Limit = num_followers
    c.Store_csv = True
    c.Output = "Twitter_Data" #folder that is created
    #the csv is called username
    twint.run.Followers(c)

def retrieve_tweets(username, num_tweets):
    """

    :param username: twitter username
    :param num_tweets: number of tweets to pull at a time (this might be a bit broken)
    :return: pandas dataframe of tweets and its information
    """
    c = twint.Config()
    c.Limit = num_tweets
    c.Username = username
    c.Pandas = True
    twint.run.Search(c)
    Tweets_df = twint.storage.panda.Tweets_df
    return(Tweets_df)


def tweets_from_relevant_usernames(num_tweets, file_path = None, usernames = False):
    """

    :param num_tweets: number of tweets to fetch per username
    :param file_path: file path of csv file (including the csv file name plus .csv) return from followers_to_csv (optional)
    :param usernames: list of usernames (optional)
    :return: combined pandas dataframe of tweets from each relevant username

    IMPORTANT: One of file_path and usernames has to have a tangible input. Otherwise there is nothing to lookup.
    It prioritizes looking for csv if both have tangible inputs
    """
    df_tweets = pd.DataFrame()
    if file_path != None:
        df_username = pd.read_csv(file_path)
        usernames = list(df_username['username'])
    for username in usernames:
        tweets = retrieve_tweets(username, num_tweets)
        df_tweets = df_tweets.append(tweets, ignore_index = True)
    return df_tweets




if __name__ == "__main__":
    # userfollowers = followers("berniesanders", 100)
    # tweets = retrieve_tweets('berniesanders', 10)
    # followers_to_csv("berniesanders", 10000)
    follow = {}
    q = ["realDonaldTrump", "JoeBiden", "ewarren", "berniesanders", "amyklobuchar", "JoinRocky", "MikeBloomberg",
         "PeteButtigeig", "KamalaHarris", "TulsiGabbard", "AndrewYang", "TomSteyer",
         "SenatorBennet", "GovBillWeld", "WalshFreedom"]

    while len(q) > 0:
        person = q.pop(0)
        try:
            print(person)
            followers_to_csv(person, 5000)
            os.rename("Twitter_Data/usernames.csv", "Twitter_Data/" + person + ".csv")
        except:
            q.append(person)

    # while not len(people) == 0:
    #     name = people.pop(0)
    #     try:
    #         follow[name] = followers(name, 1000)
    #         df = tweets_from_relevant_usernames(5, file_path=None, usernames=follow[name])
    #         with open(name+".pkl", "wb") as f:
    #             pickle.dump(df, f)
    #             f.close()
    #     except:
    #         people.append(name)
    #         time.sleep(120)

    # df = rel_tweets = tweets_from_relevant_usernames(5, file_path = "Twitter_Data/usernames.csv", usernames=False)
    # import pickle
    # with open("tweets.pkl", "wb") as f:
    #     pickle.dump(df, f)
    #     f.close()
    # print(rel_tweets)
    # print(tweets.columns)
    #print(rel_tweets['tweet'])
