import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import date
import numpy as np

def tweet_scraper(account, start_time, end_time, scraping_type = 'replies'):
  """
  this function is used to mine data 
  account: name of the account (ex. elonmusk)
  scraping_type: 
  if "replies", in returns all the replies to the account
  if "owner", it only returns the tweets made by the account 
  """
  tweets = []
  if scraping_type == 'replies':
    query = 'to:' + account + ' since:'+ start_time +' until:' + str(end_time)
  elif scraping_type == 'owner':
    query = 'from:' + account + ' since:'+ start_time +' until:' + str(end_time)

  for i,tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
      
      if i>100000:
          break
      tweets.append([tweet.date,  tweet.conversationId, tweet.rawContent, tweet.user.username])

  tweets_Dataframe = pd.DataFrame(tweets, columns=['Datetime', 'conversation Id' ,'Text', 'Username'])
  return tweets_Dataframe


def tweet_cleaning (tweet):
  """
  removes the tokens starting with @ as well as URL from text.
  """
  temp = ' '.join(word for word in tweet.split(' ') if not word.startswith('@'))
  return ' '.join(word for word in temp.split(' ') if not word.startswith('http'))

def data_update(data_repo, account, model, scraping_type = 'replies'):
    """
    this function is used to keep the data set of thweets updated. It downloads new tweets, calculate their sentiment scores, and adds them to exsisting dataset.
    data_repo: data dataframe of the tweets collected so far
    account: the name of the account as a string (EX. @elonmusk)
    model: the name of the sentiment classifier model. model must take the text and output a list of three scores
    """
    end_time = date.today()
    start_time = str(end_time.year)+'-'+str(end_time.month)+'-'+str(end_time.day-1)
    data = tweet_scraper(account, start_time, end_time, scraping_type)
    index = np.where(data_repo['Datetime'][0]==data['Datetime'][:])
    if any(index):
      data_repo = pd.concat([data[:int(np.array(index[0]))], data_repo])
    else :
      data_repo = pd.concat([data, data_repo])

    sentiment_scores = []
    for i in range(data.shape[0]):

      score = model.forward(tweet_cleaning(data['Text'][i]))
      sentiment_scores.append(score)
    data_repo['sentiment'][:data.shape[0]] = sentiment_scores
    data_repo.index = range(data_repo.shape[0])

    return data_repo
    
# data_concatenator(data1, '@cathiedwood', model, scraping_type = 'replies')
    
def active_audience(data, alpha):
  """alpha: percentage of top active users (ex. 5)
  data: data as a dataframe and must include a "sentiment" column
  """
  data = data['Username'].groupby(data['Username'].tolist()).size()
  sorted_data = data.sort_values()
  data = sorted_data[int((1-(alpha/100))*sorted_data.shape[0]):]
    
  username = data.index
  number_of_replies = data.values
  return   pd.DataFrame({'username': username, 'number of replies': number_of_replies})

# active_audience(data1,5)

def Polarity_Score(data):
  """
  this function calculates polarity score between n data point (n list of three scores). 
  this function is used to aggregate or calculate sentiment of all replies, or all tweets made by the account owner. 
  """
  # Aggregate the sentiment scores for each tweet
  total_positive = sum(score[2] for score in data)
  total_negative = sum(score[0] for score in data)
  total_neutral = sum(score[1] for score in data)

  # Compute the overall sentiment score
  sentiment_score = (total_positive - total_negative) / (total_positive + total_negative + total_neutral)
  return sentiment_score
# Polarity_Score(data1['sentiment']) gets the output of the sentiment_sum function

def sentiment_sum ( data, column= 'conversation Id'):
  if column == 'conversation Id':

    output = pd.DataFrame([])
    setniment_sum = []
    conversation_Id = []
    data = data.sort_values(by=['conversation Id'])
    data.index = range(data.shape[0])
    for i in range (0, data.shape[0]-1):
      
      if( data['conversation Id'][i+1] != data['conversation Id'][i]):
        setniment_sum.append(data['sentiment'].loc[(data['conversation Id'])== ((data['conversation Id'])[i])].sum())
        conversation_Id.append(data['conversation Id'][i])
    output['sentiment sum'] = setniment_sum
    output['conversation_Id'] = conversation_Id
  elif column == 'Username':
    output = data['sentiment'].sum()
  return output
#sentiment_sum(data2, column = 'conversation Id')

  