import os
from flask import Flask,url_for,request,render_template,request
import flask
import requests
import tweepy
import json
from random import randint
import random

session =dict()
db=dict()
app = Flask(__name__,instance_relative_config=True)



#print something
def search(text,api):
    return api.search(q=text+" ;) -filter:links",lang="en",count=10,include_entities=True)

#globals 
a = ["computer science","technology","smartphone","data","graphs","Windows 10","internet","data science","android","iphone","Internet of Things"]
used=[0]*12
count =0

def getURL(idNum):
    link="https://twitter.com/statuses/"+str(idNum)
    return link
def checkURL(idNum):
    gettyURL = "http://media.gettyimages.com/photos/-id"
    #gets twitter handle
    request = requests.get(gettyURL+idNum)
    
    #checks to see if the user exists
    if(request.status_code != 200):
        return 'fail'
    else:
        print("The url is valid!")
        return gettyURL+idNum
#function to get image id
def getId(searchTerm):

    headers = {
    'Api-Key': os.getenv("GETTY_KEY"),
    }
    r=requests.get('https://api.gettyimages.com/v3/search/images?fields=id,title,thumb,referral_destinations&sort_order=best&phrase='+str(searchTerm), headers=headers)
    request_image=r.json()
    try:
        return request_image
    except (IndexError, KeyError):
        # key or index is missing, handle an unexpected response
        return "No image found"

#guarantees random usage 
def isUsed(i):
    global used
    return used[i]
#sets search term that has been used to 1
def setUsed(i):
    global used
    used[i]=1
#reset used search terms
def reset():
    global count 
    global used
    count=0
    used = [0]*12
    print used
        
        
@app.route('/')
def setTweet():
    #sets up authentication to use api
    auth = tweepy.OAuthHandler(os.getenv("TWEEPY_CONSUMER_KEY"),os.getenv("TWEEPY_CONSUMER_SECRET"))
    auth.set_access_token(os.getenv("TWEEPY_ACCESS_TOKEN_KEY"), os.getenv("TWEEPY_ACCESS_TOKEN_SECRET"))
    api = tweepy.API(auth)
    global count
    #get random search term
    searchText=random.choice(a)
    #get a different search term if already used
    while isUsed(a.index(searchText))==1:
        searchText=random.choice(a)
    setUsed(a.index(searchText))
    #count number of page loads
    count=count+1
    print count
    #reset used searches
    if count>=10:
        reset()
        
    print "this is count:"+str(count)
    request_image=getId(searchText)
    #get image id
    uri_work=checkURL(request_image["images"][0]["id"])
    #get url for image
    other=random.choice(request_image["images"])
    #check for validity of url
    other=checkURL(other["id"])
    #search for tweet
    public_tweets=search(searchText,api)
    #choose random tweet
    twitterObj=random.choice(public_tweets)
    #get username
    twitterHandle=twitterObj.user.name
    #get text of tweet
    tweet=twitterObj.text
    tweetId=getURL(twitterObj.id)
    #set data
    user=twitterHandle
    quote=tweet
    return render_template('hello.html',quote=quote,author=user,image=other,attr=tweetId)
  
with app.test_request_context():
    url_for('static', filename='style.css')
app.run(debug=True,host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
