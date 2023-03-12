

### How to run:
## Step 1:
- install all packages in requirement.txt
## step 2:
- run main.py in terminal
## step 3:
- go to the local host adress that appears in the terminal (EX. http://127.0.0.1:5000/). This is the main IP. you can access APIs using this adress. 
while code is running, you can connect to the API using this local host (EX. http://127.0.0.1:5000/accounts).

### Files description:
- transformer.py: the sentiment classification model, in this code I load roberta (BERT variation) from hugging face API.
- functions.py: contains several function for cleaning, preprocessing, and preparing the data, the tweet crawler model, sentiment combiner method. 
- main.py: genrates the API using flask-restapi package.
- .pkl files are the collected data of three users until march 11th.

## Attention:
When getting sentiment JSON file, the sentiment are returned as a scaler number between -1 = negative and +1 = positive. 