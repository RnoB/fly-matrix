
import tweepy
import datetime
import keys


def twitter_api():

    auth = tweepy.OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
    auth.set_access_token(keys.ACCESS_KEY, keys.ACCESS_SECRET)
    api = tweepy.API(auth)
    return api




def twitStatus(expId,status = 0, t=0,filename=''):
    try:
        api = twitter_api()
        if status ==0:
            now = datetime.datetime.now()
            endTime = now + datetime.timedelta(minutes = int(t))
            message = "the experiment " + str(expId) + " has started. Should end at "+str(endTime.strftime("%H:%M"))
            
        elif status ==1:
            message = "the experiment " + str(expId) + " is ending in "+str(t)+" minutes."
            
        elif status ==2:
            message = "the experiment " + str(expId) + " is done."
            
        elif status == 3:
            #media = api.upload_chunked(filename)
            message = "The Fly Matrix is ready to serve."
            
        api.update_status(message)    
    except ValueError:
        print(ValueError)


