### Intallation of Required Libraries

import tweepy
from tweepy import OAuthHandler
import pandas as pd
import time
import datetime


### Defination of Twitter API Credentials

# Obtain the twitter credentials from your twitter developer account


api_key = 'XXX'
api_secret = 'XXX'

access_token_ = 'XXX'
access_token_secret = 'XXX'


# Pass your twitter credentials to tweepy via its OAuthHandler
auth = OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token_, access_token_secret)
api = tweepy.API(auth)

# Test The Twitter API Tokens
try:
    redirect_url = auth.get_authorization_url()
    print('Successfully loaded!!!')
except tweepy.TweepError:
    print('Error! Failed to get request token.')


### Scraping The Tweets

def conf_and_scrape(last_date,search_words,date_since,numTweets,cols):

    print('Starting new scraping from {}'.format(last_date))
        
    #check the date    
    if last_date>date_since:
        try:
            tweets=tweepy.Cursor(api.search_full_archive,environment_name='hashtag', query=search_words, toDate=last_date).items(numTweets)
            tweet_list = [tweet for tweet in tweets]

            print("Totaly {} tweets scraped under the '{}' keyword/hashtag - from {}".format(len(tweet_list),search_words, last_date))
            analyze_and_save(tweet_list,search_words,date_since,numTweets,cols)
        except:
            print("Problem about API!!!")
        
    else:
        print('All planned tweets are scraped!!!')
    
    return None



def analyze_and_save(tweet_list,search_words,date_since,numTweets,cols):
    
    
    #Creating DF for saving the results in tabular format 
    df= pd.DataFrame(columns=cols, index=range(len(tweet_list)))


    #Extracting The Results
    for n,tweet in enumerate(tweet_list):
        tweet_id=tweet.id
        user_id=tweet.user.id
        username = tweet.user.screen_name #unique
        displayname = tweet.user.name #not unique
        user_create_date = tweet.user.created_at
        user_description = tweet.user.description
        user_location_manuel = tweet.user.location
        user_url_in_bio=tweet.user.url 
        geo_enable=tweet.user.geo_enabled #When true, indicates that the user has enabled the possibility of geotagging their Tweets.
        following_num = tweet.user.friends_count
        followers_num = tweet.user.followers_count
        total_tweets = tweet.user.statuses_count
        total_likes = tweet.user.favourites_count   
        protected_account = tweet.user.protected
        verified_account = tweet.user.verified
        user_translator = tweet.user.is_translator
        user_profile_photo = tweet.user.profile_image_url
        try:
            user_banner_photo = tweet.user.profile_banner_url
        except:
            user_banner_photo = None
        user_default_photo = tweet.user.default_profile_image #egg account  
        tweet_create_date = tweet.created_at
        tweet_language = tweet.lang
        tweet_geo = tweet.geo
        tweet_location = tweet.coordinates
        tweet_retweeted = tweet.retweeted #this tweet is retweeted?
        try:
            tweet_status = 'ORIGINAL' if  tweet.user.screen_name==tweet.retweeted_status.user.screen_name else 'RETWEETED'
        except:
            tweet_status = 'ORIGINAL'
        tweet_source = tweet.source #platform source for tweet

        try:
            tweet_text = tweet.retweeted_status.extended_tweet['full_text']
            tweet_original_username = tweet.retweeted_status.user.screen_name
            tweet_original_displayname = tweet.retweeted_status.user.name
            tweet_original_user_id = tweet.retweeted_status.user.id
            tweet_original_user_create_date = tweet.retweeted_status.user.created_at
            tweet_original_retweets_num = tweet.retweeted_status.retweet_count
            tweet_original_likes_num = tweet.retweeted_status.favorite_count

        except AttributeError:  # Not a Retweet

            try:
                tweet_text = tweet.extended_tweet['full_text']
            except: # Not an extended tweet
                tweet_text = tweet.text
            tweet_original_username = tweet.user.screen_name
            tweet_original_displayname = tweet.user.name
            tweet_original_user_id = tweet.user.id
            tweet_original_user_create_date = tweet.created_at
            tweet_original_retweets_num = tweet.retweet_count
            tweet_original_likes_num = tweet.favorite_count

        #Save The Cleaned Data
        df.loc[n].tweet_id = tweet_id
        df.loc[n].user_id = user_id
        df.loc[n].username = username
        df.loc[n].displayname = displayname
        df.loc[n].user_create_date = user_create_date
        df.loc[n].user_description = user_description
        df.loc[n].user_location_manuel = user_location_manuel
        df.loc[n].user_location_manuel = user_location_manuel
        df.loc[n].geo_enable = geo_enable
        df.loc[n].following_num = following_num
        df.loc[n].followers_num = followers_num
        df.loc[n].total_tweets = total_tweets
        df.loc[n].total_likes = total_likes  
        df.loc[n].protected_account = protected_account
        df.loc[n].verified_account = verified_account
        df.loc[n].user_translator = user_translator 
        df.loc[n].user_profile_photo = user_profile_photo
        df.loc[n].user_banner_photo = user_banner_photo
        df.loc[n].user_default_photo = user_default_photo
        df.loc[n].tweet_create_date = tweet_create_date
        df.loc[n].tweet_language = tweet_language
        df.loc[n].tweet_geo = tweet_geo
        df.loc[n].tweet_location = tweet_location
        df.loc[n].tweet_retweeted = tweet_retweeted
        df.loc[n].tweet_source = tweet_source
        df.loc[n].tweet_status = tweet_status
        df.loc[n].tweet_text = tweet_text
        df.loc[n].tweet_original_username = tweet_original_username
        df.loc[n].tweet_original_displayname = tweet_original_displayname
        df.loc[n].tweet_original_user_id = tweet_original_user_id
        df.loc[n].tweet_original_user_create_date = tweet_original_user_create_date
        df.loc[n].tweet_original_retweets_num = tweet_original_retweets_num
        df.loc[n].tweet_original_likes_num = tweet_original_likes_num

    #Open Existing CSV
    df_tot = pd.read_csv('twitter{}.csv'.format(search_words), sep=';')
    
    #Concat two df
    df_tot = pd.concat([df_tot, df])
    df_tot.to_csv('twitter{}.csv'.format(search_words),sep=';',encoding='utf-8-sig',index=False) 

    #defination
    last_date = df.iloc[-1,:]['tweet_create_date'].strftime('%Y%m%d%H%M')
    
    print('Data Saved!!! Last date of the current data is: {}'.format(last_date))
    
    #Wait 5 seconds
    time.sleep(5)
    
    conf_and_scrape(last_date,search_words,date_since,numTweets,cols)

    return df


if __name__ == "__main__":
    
    #defination
    search_words ='#Kanaleneiland' #>>>>> and '#schilderswijk'
    date_since = "202009130000" ## start date of collecting
    numTweets = 100
    
    #Creating empty DF for saving the results in tabular format 
    cols = ['tweet_id', 'user_id', 'username', 'displayname', 'user_create_date', 'user_description', 'user_location_manuel', 
            'user_url_in_bio', 'geo_enable', 'following_num', 'followers_num', 'total_tweets', 'total_likes', 'protected_account',
            'verified_account', 'user_translator', 'user_profile_photo', 'user_banner_photo', 'user_default_photo','tweet_create_date',
            'tweet_language', 'tweet_geo', 'tweet_location', 'tweet_retweeted', 'tweet_status', 'tweet_source', 'tweet_text', 
            'tweet_original_username', 'tweet_original_displayname', 'tweet_original_user_id', 'tweet_original_user_create_date',
            'tweet_original_retweets_num', 'tweet_original_likes_num' ]

    df_empty= pd.DataFrame(columns=cols)
    
    df_empty.to_csv('twitter{}.csv'.format(search_words),sep=';',encoding='utf-8-sig',index=False)

    conf_and_scrape((datetime.datetime.now() - datetime.timedelta(hours = 2)).strftime("%Y%m%d%H%M"),
                    search_words,date_since,numTweets,cols) 

