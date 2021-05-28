# About API </br></br>

This API can be used by users by users to provide to ask a question and fetch an automated answer from the system depending on NLP model used.</br></br>

# API URL </br></br>

# Dependencies </br></br>

# Steps to build and run the API locally via doicker or FLask</br></br>

# Available Routes</br></br>

<b>List Available Models :</b> This route allows a user to obtain a list of the models currently loaded into the server and available for inference.</br>
Method and path: GET /models</br>
Response Type : JSON</br>
Sample Response Format:</br>
[</br>
    {</br>
        "name": "distilled-bert",</br>
         "tokenizer": "distilbert-base-uncased-distilled-squad",</br>
          "model": "distilbert-base-uncased-distilled-squad"</br>
    },</br>
    {</br>
         "name": "deepset-roberta",</br>
         "tokenizer": "deepset/roberta-base-squad2",</br>
         "model": "deepset/roberta-base-squad2"</br>
    }</br>
]</br></br>


<b>Add a Model :</b> This route allows a user to add a new model into the server and make it available for inference.</br>
Method and path: PUT /models</br>
Response Type : JSON</br></br>
Sample Request Body Format: </br>
{</br>
"name": "bert-tiny",</br>
"tokenizer": "mrm8488/bert-tiny-5-finetuned-squadv2",</br>
"model": "mrm8488/bert-tiny-5-finetuned-squadv2"</br>
}</br></br>
Sample Response Format:</br>
[</br>
{</br>
"name": "distilled-bert",</br>
"tokenizer": "distilbert-base-uncased-distilled-squad",</br>
"model": "distilbert-base-uncased-distilled-squad"</br>
},</br>
{</br>
"name": "deepset-roberta",</br>
"tokenizer": "deepset/roberta-base-squad2",</br>
"model": "deepset/roberta-base-squad2"</br>
},</br>
{</br>
"name": "bert-tiny",</br>
"tokenizer": "mrm8488/bert-tiny-5-finetuned-squadv2",</br>
"model": "mrm8488/bert-tiny-5-finetuned-squadv2"</br>
}</br>
]</br>


<b>Delete a Model :</b> This route allows a user to delete an existing model on the server such that it is no longer
available for inference and returns the remaining list of models as a response. </br>
Method and path: DELETE /models?model=<model name></br>
Query Parameters:</br> - <model name> (required) - The name of the model to be deleted</br>
Response Type : JSON</br>
Sample Response Format:</br>
[</br>
    {</br>
        "name": "distilled-bert",</br>
         "tokenizer": "distilbert-base-uncased-distilled-squad",</br>
          "model": "distilbert-base-uncased-distilled-squad"</br>
    },</br>
    {</br>
         "name": "deepset-roberta",</br>
         "tokenizer": "deepset/roberta-base-squad2",</br>
         "model": "deepset/roberta-base-squad2"</br>
    }</br>
]</br></br>

<b>Answer a Question :</b> This route uses one of the available models to answer a question, given the context provided in
the JSON payload.</br>
</br>
    - Method and path: POST /answer?model=<model name></br>
</br>
    - Query Parameters:  
        - <model name> (optional) - The name of the model to be used in answering the</br>
</br>
question. If no model name is provided use a default model. </br>
</br>
    - Response Type : JSON</br>
</br>
Sample Request Body Format: </br>
{ </br>
"question": "who did holly matthews play in waterloo rd?", </br>
"context": "She attended the British drama school East 15 in 2005, </br>
and left after winning a high-profile role in the BBC drama Waterloo </br>
Road, playing the bully Leigh-Ann Galloway.[6] Since that role, </br>
Matthews has continued to act in BBC's Doctors, playing Connie </br>
Whitfield; in ITV's The Bill playing drug addict Josie Clarke; and </br>
she was back in the BBC soap Doctors in 2009, playing Tansy Flack." </br>
} </br>

Sample Response Format:</br>
</br>
{</br>
"timestamp": 1621602784,</br>
"model": "deepset-roberta",</br>
"answer": "Leigh-Ann Galloway",</br>
"question": "who did holly matthews play in waterloo rd?",</br>
"context": "She attended the British drama school East 15 in 2005,</br>
and left after winning a high-profile role in the BBC drama Waterloo</br>
Road, playing the bully Leigh-Ann Galloway.[6] Since that role,</br>
Matthews has continued to act in BBC's Doctors, playing Connie</br>
Whitfield; in ITV's The Bill playing drug addict Josie Clarke; and</br>
she was back in the BBC soap Doctors in 2009, playing Tansy Flack."</br>
}
</br></br>

<b>List Recently Answered Questions :</b> This route returns recently answered questions.</br>
Method and path: GET /answer?model=<model name>&start=<start timestamp>&end=<end</br>
timestamp></br>
    </br>
   - Query Parameters:</br>
        - <model name> (optional) - Filter the results by providing a certain model name, such</br>
        that the results only include answered questions that were answered using the provided</br>
        model.</br>
       - <start timestamp> (required) - The starting timestamp, such that answers to questions</br>
          prior to this timestamp won't be returned.</br>
       - <end timestamp> (required) - The ending timestamp, such that answers to questions</br>
         after this timestamp won't be returned.</br>
     
Sample Response :

        [
{
"timestamp": 1621602784,
"model": "deepset-roberta",
"answer": "Leigh-Ann Galloway",
"question": "who did holly matthews play in waterloo rd?",
"context": "She attended the British drama school East 15 in
2005, and left after winning a high-profile role in the BBC drama
Waterloo Road, playing the bully Leigh-Ann Galloway.[6] Since that
role, Matthews has continued to act in BBC's Doctors, playing Connie
Whitfield; in ITV's The Bill playing drug addict Josie Clarke; and
she was back in the BBC soap Doctors in 2009, playing Tansy Flack."
},
{
"timestamp": 1621602930,
"model": "distilled-bert",
"answer": "Travis Pastrana",
"question": "who did the first double backflip on a dirt bike?",
"context": "2006 brought footage of Travis Pastrana completing a
double backflip on an uphill/sand setup on his popular /"Nitro
Circus/" Freestyle Motocross movies. On August 4, 2006, at X Games 12
in Los Angeles, he became the first rider to land a double backflip
in competition. Having landed another trick that many had considered
impossible, he vowed never to do it again."
}
]
