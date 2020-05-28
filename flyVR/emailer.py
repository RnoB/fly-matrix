#MIT License

#Copyright (c) 20120 Renaud Bastien

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
###########

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


