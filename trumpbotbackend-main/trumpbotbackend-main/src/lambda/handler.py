import json,re,random,sys
from operator import itemgetter
sys.path.append('vendor')
import markovify

topics = ["obama", "democrats", "china", "deal", "the mainstream media", "election", "campaign", "interview", "fox", "fake", "news", "fake news", "make america great", "keep america great", "@ cnn",
           "#", "thank you", "congratulations", "hillary", "america", "jobs", "congress", "senator"]

#these groups are a reprensentation for our clusters
group_1 = {"overtopic": "election", "count": 0, "subtopics": topics[:7], "file": "data/gruppe1.txt"}
group_2 = {"overtopic": "news", "count": 0, "subtopics": topics[7:14], "file": "data/gruppe2.txt"}
group_3 = {"overtopic": "people", "count": 0, "subtopics": topics[14:18], "file": "data/gruppe3.txt"}
group_4 = {"overtopic": "politics", "count": 0, "subtopics": topics[18:], "file": "data/gruppe4.txt"}

def handler(event, context):
    body = json.loads(event["body"])
    user_input = body["user_input"]
    fake_tweet = body["fake_tweet"]

    #def output of lambda function
    output = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Credentials": True,
            "Access-Control-Allow-Origin": "*",
        },
        "body": ""
    }
    
    #if user types !help, return all available topics to the bot
    if (user_input == "!help"):
        
        output["body"] = json.dumps({
                "flavor_text": "I make a very gold conversation on these numerous topics: " + return_topics(),
                "last_tweet": "",
                "fake_tweet": "exit" 
            })
            
        return output
    
    #react to user responding if a tweet is from trump or generated
    elif (user_input == "!fake" and fake_tweet != "exit"):
        
        if (fake_tweet == "true"):

            output["body"] = json.dumps({
                "flavor_text": "This story is just another made up by Fake News tale that is told only to damage me. 100% Correct. Thank you.", #user correct - tweet generated
                "last_tweet": "",
                "fake_tweet": "exit" 
            })

            return output

        else:

            output["body"] = json.dumps({
                    "flavor_text": "I am full of honesty and sincerity on the other hand you are a total liar. You got it wrong!", #user incorrect - tweet real
                    "last_tweet": "",
                    "fake_tweet": "exit"  
                })

            return output
     
    elif (user_input == "!real" and fake_tweet != "exit"):
        
        if (fake_tweet == "true"):

            output["body"] = json.dumps({
                "flavor_text": "Haha, that was a fake tweet! Get this liar out of the White House.", #user incorrect - tweet generated
                "last_tweet": "",
                "fake_tweet": "exit" 
            })

            return output

        else:

            output["body"] = json.dumps({
                    "flavor_text": "I dictated this tweet to my executive assistant and she posted it. True!", #user correct - tweet real
                    "last_tweet": "",
                    "fake_tweet": "exit"  
                })

            return output
    
    else:
        topics_retrieved = retrieve_topics(user_input)
        
        if (topics_retrieved == None):
            
            output["body"] = json.dumps({
                    "flavor_text": "FILE THIS UNDER SH!T you can’t make up YET ITS NOT FAKE NEWS!!!!!! (no valid topic)",
                    "last_tweet": "",
                    "fake_tweet": "exit"                    
            })
            
            return output
            
        else:
            matched_group_topics = matching_group(topics_retrieved)

            tweet_function_list = [generate_fake_tweet(matched_group_topics, topics_retrieved), return_real_tweet(matched_group_topics, topics_retrieved)]

            tweet = random.choice(tweet_function_list)
 
            output["body"] = json.dumps({
                    "flavor_text": "Some very interesting topics -- here is my tweet:",
                    "last_tweet": tweet["tweet"],
                    "fake_tweet": tweet["fake_tweet"]
            })
            
            return output


def return_topics():
    return ", ".join(topics)


def retrieve_topics(user_input):
    array_of_topics = []
    
    if (type(user_input) == str):
        
        user_input = re.sub(r'[^A-Za-z0-9 ]', '', user_input)
        user_input = user_input.lower()
        
        if (re.search(r'(obama|barack.?obama|barack)', user_input)):
            array_of_topics.append("barack obama")
            
        if (re.search(r'(democrat.*|part(y|ies))', user_input)):
            array_of_topics.append("democrats")
            
        if (re.search(r'(china|peking|xi( jinping)?)', user_input)):
            array_of_topics.append("china")
            
        if (re.search(r'(deals?|trade deal|contract)', user_input)):
            array_of_topics.append("deal")
            
        if (re.search(r'(medias?|television|tv|radio|news)', user_input)):
            array_of_topics.append("media")
            
        if (re.search(r'elections?|ballot.*|polls?', user_input)):
            array_of_topics.append("election")
        
        if (re.search(r'campaign.*', user_input)):
            array_of_topics.append("campaign")
            
        if (re.search(r'(interview.?|meet.*|press( conference)?|statements?)', user_input)):
            array_of_topics.append("interview")
        
        if (re.search(r'fox( news)?', user_input)):
            array_of_topics.append("fox")
            
        if (re.search(r'(fake( news)?|hoax|scam.*|trick.*|fraud)', user_input)):
            array_of_topics.append("fake")
            
        if (re.search(r'(news|report.*|state(ment)?|rumor.*|report.*)', user_input)):
            array_of_topics.append("news")
            
        if (re.search(r'cnn', user_input)):
            array_of_topics.append("cnn")
            
        if (re.search(r'nbc', user_input)):
            array_of_topics.append("nbc")
            
        if (re.search(r'obamagate', user_input)):
            array_of_topics.append("obamagate")
            
        if (re.search(r'(provocat.*|affront|insult.*)', user_input)):
            array_of_topics.append("provocation")
            
        if (re.search(r'(maga|make america great again)', user_input)):
            array_of_topics.append("make america great again")
            
        if (re.search(r'(kag(2020)?|keep america great)', user_input)):
            array_of_topics.append("keep america great")
            
        if (re.search(r'(thanks?(you)?|prais.*|grateful|appreciat.*)', user_input)):
            array_of_topics.append("thank you")
            
        if (re.search(r'(congrat.*|compliments?|bless.*)', user_input)):
            array_of_topics.append("congrats")
            
        if (re.search(r'(hillary|crook.*|clinton)', user_input)):
            array_of_topics.append("hillary")
            
        if (re.search(r'(usa|america.*|land|states)', user_input)):
            array_of_topics.append("america")
        
        if (re.search(r'(work|job.*|business|career|office|profession|task.*)', user_input)):
            array_of_topics.append("jobs")
            
        if (re.search(r'state of the union', user_input)):
            array_of_topics.append("state of the union")
            
        if (re.search(r'(announc.*|advertis.*|messag.*|publica.*)', user_input)):
            array_of_topics.append("announcement")
            
        if (re.search(r'congress.*', user_input)):
            array_of_topics.append("congress")
            
        if (re.search(r'senat.*', user_input)):
            array_of_topics.append("senator")
            
            
        #return none if no match was found    
        if(len(array_of_topics) == 0):
            return None
        else:       
            return array_of_topics
        
    else:
        return None

    
def matching_group(topics):
    group_1["count"] = 0
    group_2["count"] = 0
    group_3["count"] = 0
    group_4["count"] = 0
    
    for word in topics:
        
        if (word in group_1["subtopics"]):
            group_1["count"] += 1
        
        if (word in group_2["subtopics"]):
            group_2["count"] += 1
            
        if (word in group_3["subtopics"]):
            group_3["count"] += 1
            
        if (word in group_4["subtopics"]):
            group_4["count"] += 1

    group = max([group_1, group_2, group_3, group_4], key=itemgetter('count'))
            
    return group
  
    
def generate_fake_tweet(matched_group, topics):
    tweets = []

    with open(matched_group["file"], encoding="utf8") as txt_file:   
        for line in txt_file:
            clean_line = re.sub("\n", "", line)
            tweets.append(clean_line)

    model = markovify.Text(tweets, state_size = 3, well_formed = False)
    
    output = []
    retries = 0

    while (retries < 2 and len(output) < 1):
        retries += 1
        
        for topic in topics:
            
            if(topic == "media"):
                topic = "the mainstream media"
            if(topic == "maga"):
                topic = "make america great"
            if(topic == "make america great again"):
                topic = "make america great"
            if(topic == "kag2020"):
                topic = "keep america great"
            
            try:
                sentence = model.make_sentence_with_start(topic)
                
                if (sentence != None):
                    output.append(sentence)
                
            except:
                output.append("error")
    
    try:
        return {"tweet": random.choice(output), "fake_tweet": "true"}
        
    except:
        output.append("error")
        return {"tweet": output[0], "fake_tweet": "true"}

def return_real_tweet(matched_group, topics):
    tweets = []
    
    with open(matched_group["file"], encoding="utf8") as txt_file:   
        for line in txt_file:
            clean_line = re.sub("\n", "", line)
            tweets.append(clean_line)

    try:
        possible_tweets = []
        for tweet in tweets:
            for topic in topics:
                
                if(topic == "media"):
                    topic = "the mainstream media"
                if(topic == "maga"):
                    topic = "make america great"
                if(topic == "make america great again"):
                    topic = "make america great"
                if(topic == "kag2020"):
                    topic = "keep america great"
                
                if topic in tweet:
                    if (re.search(rf'^{topic}', tweet)):
                        possible_tweets.append(tweet)
        
        return {"tweet": random.choice(possible_tweets), "fake_tweet": "false"}
    except:
        return {"tweet": random.choice(tweets), "fake_tweet": "false"}