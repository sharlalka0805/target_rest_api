# About API </br>

This API can be used by users by users to provide to ask a question and fetch an automated answer from the system depending on NLP model used.</br></br>

# API URL </br>
https://mgmt-rest-api-shipra-yu4izdrwlq-uc.a.run.app/

# Dependencies </br>

### Flask: 
We used flask to produce the rest API

### Torch: 
We used torch as a dependency for transformers

### Transformers: 
We used this dependency for answering question.

You need to install all the dependencies avaailable in requirements.txt

# Steps to build and run the API locally via Docker or Flask</br>

1. To build the API locally , install FLASK,Tensorflow,Pytorch</br>
2. Clone the above githib code to your local machine</br>
3. Open the cloned code in PyCharm and go to main.py</br>
4. Set main.py in Run COnfigurations and trigger the build </br>
5. Your local port will be picked and API will be hosted on the same.</br>
6. You may then your broweser to test this API </br>
  
# Available Routes</br>

<b>List Available Models :</b> This route allows a user to obtain a list of the models currently loaded into the server and available for inference.
</br>Service URL : https://mgmt-rest-api-shipra-yu4izdrwlq-uc.a.run.app/models   
</br>Method and path: GET /models</br>
Response Type : JSON</br>
Sample Response Format:</br>

      [
          {
              "name": "distilled-bert",
               "tokenizer": "distilbert-base-uncased-distilled-squad",
                "model": "distilbert-base-uncased-distilled-squad"
          },
          {
               "name": "deepset-roberta",
               "tokenizer": "deepset/roberta-base-squad2",
               "model": "deepset/roberta-base-squad2"
          }<
      ]
</br></br>

<b>Add a Model :</b> This route allows a user to add a new model into the server and make it available for inference.</br>

Service URL : https://mgmt-rest-api-shipra-yu4izdrwlq-uc.a.run.app/models  

Method and path: PUT /models</br>
Response Type : JSON</br>
Sample Request Body Format: </br>

     {
        "name": "bert-tiny",
        "tokenizer": "mrm8488/bert-tiny-5-finetuned-squadv2",
        "model": "mrm8488/bert-tiny-5-finetuned-squadv2"
      }
    
Sample Response Format:</br>
 
     [
          {
              "name": "distilled-bert",
              "tokenizer": "distilbert-base-uncased-distilled-squad",
              "model": "distilbert-base-uncased-distilled-squad"
          },
          {
              "name": "deepset-roberta",
              "tokenizer": "deepset/roberta-base-squad2",
              "model": "deepset/roberta-base-squad2"
          },
          {
              "name": "bert-tiny",</br>
              "tokenizer": "mrm8488/bert-tiny-5-finetuned-squadv2",</br>
              "model": "mrm8488/bert-tiny-5-finetuned-squadv2"</br>
          }
     ]
 </br></br>

<b>Delete a Model :</b> This route allows a user to delete an existing model on the server such that it is no longer
available for inference and returns the remaining list of models as a response. </br>

Service URL : https://mgmt-rest-api-shipra-yu4izdrwlq-uc.a.run.app/models?model=bert-base-multilingual-uncased 

Method and path: DELETE /models?model=<model name></br>
Query Parameters: - <model name> (required) - The name of the model to be deleted</br>
Response Type : JSON</br>

Sample Response Format:</br>

      [
        {
            "name": "distilled-bert",
             "tokenizer": "distilbert-base-uncased-distilled-squad",
              "model": "distilbert-base-uncased-distilled-squad"
        },
        {
             "name": "deepset-roberta",</br>
             "tokenizer": "deepset/roberta-base-squad2",
             "model": "deepset/roberta-base-squad2"
        }
    ]
    
 </br></br>

<b>Answer a Question :</b> This route uses one of the available models to answer a question, given the context provided in
the JSON payload.</br>
Service URL : https://mgmt-rest-api-shipra-yu4izdrwlq-uc.a.run.app/answer?model=bert-base-multilingual-uncased

Method and path: POST /answer?model=<model name></br>
Query Parameters:  
        - <model name> (optional) - The name of the model to be used in answering the question. If no model name is provided use a default model. </br>
Response Type : JSON</br>

Sample Request Body Format: </br>

          { 
                "question": "who did holly matthews play in waterloo rd?",
                "context": "She attended the British drama school East 15 in 2005,
                            and left after winning a high-profile role in the BBC drama Waterloo 
                            Road, playing the bully Leigh-Ann Galloway.[6] Since that role, 
                            Matthews has continued to act in BBC's Doctors, playing Connie
                           Whitfield; in ITV's The Bill playing drug addict Josie Clarke; and
                            she was back in the BBC soap Doctors in 2009, playing Tansy Flack."
          }
          
 </br>
   Sample Response Format:</br>

    {
          "timestamp": 1621602784,
           "model": "deepset-roberta",
          "answer": "Leigh-Ann Galloway",
          "question": "who did holly matthews play in waterloo rd?",
          "context": "She attended the British drama school East 15 in 2005,
                      and left after winning a high-profile role in the BBC drama Waterloo
                    Road, playing the bully Leigh-Ann Galloway.[6] Since that role,
                  Matthews has continued to act in BBC's Doctors, playing Connie
                  Whitfield; in ITV's The Bill playing drug addict Josie Clarke; and
                she was back in the BBC soap Doctors in 2009, playing Tansy Flack."
    }
    
</br></br>

<b>List Recently Answered Questions :</b> This route returns recently answered questions.</br>

Method and path: GET /answer?model=<model name>&start=<start timestamp>&end=<end timestamp></br>
Query Parameters:</br>
         - <model name> (optional) - Filter the results by providing a certain model name, such
                                    that the results only include answered questions that were answered using the provided
                                    model.</br>
       - <start timestamp> (required) - The starting timestamp, such that answers to questions
                                        prior to this timestamp won't be returned.</br>
       - <end timestamp> (required) -  The ending timestamp, such that answers to questions
                                         after this timestamp won't be returned.</br>
     
Sample Request:

          {
             "timestamp": 1621602784,
             "model": "deepset-roberta",
              "answer": "Leigh-Ann Galloway",
             "question": "who did holly matthews play in waterloo rd?",
             "context": "She attended the British drama school East 15 in 2005,
                    and left after winning a high-profile role in the BBC drama Waterlo
                    Road, playing the bully Leigh-Ann Galloway.[6] Since that role,
                    Matthews has continued to act in BBC's Doctors, playing Connie
                    Whitfield; in ITV's The Bill playing drug addict Josie Clarke; and
                    she was back in the BBC soap Doctors in 2009, playing Tansy Flack."
    }
