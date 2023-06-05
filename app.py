#importing flask
from flask import Flask, render_template,request
#Importing the summarizer
from summarizer import Summarizer
from summarizer.sbert import SBertSummarizer
import openai


openai.api_key = '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'
# Using an instance of SBERT to create the model
model = SBertSummarizer('paraphrase-MiniLM-L6-v2')

app = Flask(__name__)

@app.route("/")
def msg():
    return render_template('index.html')

@app.route("/summarize", methods=['POST','GET'])
def getSummary():
    body=request.form['data']
    result = model(body, num_sentences=5)
    return render_template('summary.html',result=result)

@app.route("/chatbot",methods=["POST"])
def chatbot():
    user_input = request.form["message"]
    prompt=f"User :{user_input}\nChatbot:"
    chat_history=[]
    response= openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0,
        stop=["\nUser:","\nChatbot:"]
    )
    bot_response =response.choices[0].text.strip()
    chat_history.append(f"User: {user_input}\nChatbot: {bot_response}")

    return render_template(
        "chatbot.html",
        user_input=user_input,
        bot_response=bot_response,
    )





if __name__ =="__main__":
    app.run(debug=True,port=5000)