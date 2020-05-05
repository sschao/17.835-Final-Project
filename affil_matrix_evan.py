import pandas as pd
import twint
import os
from os import listdir
from os.path import isfile, join
import time
import random


path = os.path.abspath(os.getcwd()) +"\\candidate_follower_usernames" #path of original datafiles
file_names = [f for f in listdir(path) if isfile(join(path, f))] #file names in path
candidate_usernames = [file_name[:-4] for file_name in file_names] #take out csvs for twitter handles
usernames_df = pd.DataFrame()
for file_name in file_names:
    df_candidate_username = pd.read_csv(os.path.abspath(os.getcwd()) +"\\candidate_follower_usernames\\"+file_name)
    usernames_df = pd.concat([usernames_df,df_candidate_username]) #merge all dataframes of usernames together


# print(twitter_usernames)
# test = pd.read_pickle('Followers of Candidates/ewarren.pkl')
# print(len(test['username'].unique()))
# candidates = ["JoinRocky", "MikeBloomberg", "PeteButtigeig", "KamalaHarris", "TulsiGabbard",
#           "AndrewYang", "TomSteyer", "SenatorBennet", "GovBillWeld", "WalshFreedom", 'BernieSanders', 'RealDonaldTrump']
affil = pd.DataFrame(0, index=usernames_df.username, columns=candidate_usernames) #create initial all 0 matrix
affil = affil.loc[~affil.index.duplicated(keep='first')] #remove duplicate handles

def following(username, num_following):
    """
    :param username: twitter username of candidate
    :param num_followers: number of following to pull at once
    :return: list that has the username of the people following

    # This code seems to be less reliable. It often breaks but its easier to use since the list is already stored
    """
    c = twint.Config()
    c.Limit = num_following
    c.Username = username
    c.Pandas = True

    twint.run.Following(c)

    Following_df = twint.storage.panda.Follow_df
    print(Following_df.to_string())
    list_of_following = Following_df['following'][username]
    return list_of_following

affil.to_csv('affiliation_matrix_0.csv') #initial csv


success = 0
# affil_csv = pd.read_csv(f'affiliation_matrix_chao_{str(success)}.csv', index_col = 0)
# affil = affil_csv[0:33000] #Shawn's work
# affil = affil_csv[33000:] #Evan uncomment
affil = affil[33000:]
usernames_index_list = list(affil.index)
# original_length = len(usernames_index_list)
# for i in range(len(usernames_index_list)):

while len(usernames_index_list) != 0:
    user = usernames_index_list.pop(random.randint(0,len(usernames_index_list)-1)) #pop out the user
    try:
        if affil.loc[user].sum() == 0:
             # user = usernames_index_list.pop(0)
            followings_list = following(user, 5000)
            for followings in followings_list:
                if followings in candidate_usernames:
                    affil.loc[user][followings] += 1

            # print(user)
            # affil.to_csv(f'affiliation_matrix_{str(affil.index.get_loc(user))}.csv')
            # os.remove(f'affiliation_matrix_{str(affil.index.get_loc(user)-1)}.csv')
            # print(original_length, len(usernames_index_list))
            # print(len(usernames_index_list))
            # affil.to_csv(f'affiliation_matrix_{str(original_length-len(usernames_index_list))}.csv')
            # os.remove(f'affiliation_matrix_{str(original_length-len(usernames_index_list)-1)}.csv')
            success += 1
            affil.to_csv(f'affiliation_matrix_evan_{str(success)}.csv') #new file
            os.remove(f'affiliation_matrix_evan_{str(success-1)}.csv') #remove old file

    except:
        usernames_index_list.append(user) #add the user back in if we failed
        time.sleep(60) #pause