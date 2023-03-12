from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

class SentimentClassifier():
  def __init__(self):
    self.roberta = "cardiffnlp/twitter-roberta-base-sentiment"
    self.model = AutoModelForSequenceClassification.from_pretrained(self.roberta)
    self.tokenizer = AutoTokenizer.from_pretrained(self.roberta)
  def forward(self, tweet):
    encoded_tweet = self.tokenizer(tweet, return_tensors='pt')
    output = self.model(**encoded_tweet)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    return  scores  

