

### How to run:
## Step 1:
- install all packages in requirement.txt
## step 2:
- run main.py in terminal
## step 3:
- while code is runningon a remote host, you can connect to the API using this ermote host (EX. <IP of the remote host>/accounts).

### Files description:
- transformer.py: the sentiment classification model, in this code I load roberta (BERT variation) from hugging face API.
- functions.py: contains several function for cleaning, preprocessing, and preparing the data, the tweet crawler model, sentiment combiner method. 
- main.py: genrates the API using flask-restapi package.
- datasets contains the collected data of three users, which are updated every 6 hours.

## Attention:
When getting sentiment JSON file, the sentiment are returned as a scaler number between -1 = negative and +1 = positive. 

use this two commands to show your json file in a pretty manner:

parsed = json.loads(name_of_the_json_file);
 
json.dumps(parsed, indent=4)

### the API is live for a while. you can access it and fetch data from following endpoints:
 
## 1- list of all tracked accounts:
 
74.249.25.211:5000/accounts
 
## 2- user's conversation threads since the start: 
 
74.249.25.211:5000/tweets/taylorlorenz
 
74.249.25.211:5000/tweets/ylecun
 
74.249.25.211:5000/tweets/cathiedwood
 
## 3- information about the audience for a user's account:
 
74.249.25.211:5000/audience/cathiedwood
 
74.249.25.211:5000/audience/ylecun
 
74.249.25.211:5000/audience/taylorlorenz
 
## 4- sentiment information of an account (thread level):
 
74.249.25.211:5000/sentiment/taylorlorenz
 
74.249.25.211:5000/sentiment/ylecun
 
74.249.25.211:5000/sentiment/cathiedwood
