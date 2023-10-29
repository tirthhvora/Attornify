from flask import Flask, request, jsonify
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
import openai
import pickle
# with open('embeddings.pkl' , 'rb') as f:
#     embeddings = pickle.load(f)
from langchain.embeddings.openai import OpenAIEmbeddings
from googletrans import Translator 
from flask import Flask, jsonify, request,send_file
import speech_recognition as sr
from gtts import gTTS
from flask_cors import CORS
from pydub import AudioSegment
import os

embeddings = OpenAIEmbeddings(openai_api_key="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")
vectorstore = FAISS.load_local("main-vectordb",embeddings)
llm = OpenAI(openai_api_key="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", model_name='gpt-3.5-turbo')
retriever = vectorstore.as_retriever(search_kwargs={"k":5})
recognizer = sr.Recognizer()
admin_prompt =  "INSTRUCTIONS: You are an expert lawyer who if gets a naive query can give technical query out of it. You will get a user query. The user doesnt know much about law, but he or she desperately wants legal advice. i have a dataset of lawyers with these attributes: Lawyer Names, Experience, Practice Areas, Client Feedback, Jurisdiction, Hourly Rate, Avg Days for Disposal, Languages, Pro Bono Services, Client Demographics. in the form of a vectordatabase. Convert the user query into a query using or linking the attributes i gave you that i can give my vectordatabase for semantic search. give a single string as output"


app = Flask(__name__)
CORS(app)


@app.route('/get_audio_response', methods=['GET', 'POST'])
def get_audio_response():
    vectorstore = FAISS.load_local("main-vectordb",embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k":15})
    print("request received")
    if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
   
    audio_file = request.files['file']
    print("audio received")

        # Check if the file is present and has an allowed extension
    if audio_file and allowed_file(audio_file.filename):
            # Convert the audio file to WAV format (if not already)
            audio = convert_to_wav(audio_file)

            # Perform speech recognition on the converted WAV file
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio) as source:
                audio_data = recognizer.record(source)

            # Recognize the speech
            naive_prompt = recognizer.recognize_google(audio_data)

            translated=  openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "you will be given hindi or gujarati text. translate it to pure english"},
                            {"role": "user", "content": naive_prompt}
            ], temperature=0)
            translated_prompt = translated["choices"][0]['message']['content']
            print("translation", translated_prompt)
            naive_prompt = "QUERY: " + translated_prompt + " INSTRUCTIONS: understand the query deeply and map with possible lawyer attributes. lawyer should be highly experienced and in similar practice area"
            print(naive_prompt)

            lawyer_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": admin_prompt},
                            {"role": "user", "content": naive_prompt}
            ], temperature=0)

            a = lawyer_response["choices"][0]['message']['content']
            relevant_docs = retriever.get_relevant_documents(a)
            print(f"There are {len(relevant_docs)} number of docs ")
            lawyer_info =[]
            for i in range(len(relevant_docs)):
                lawyer_info.append(relevant_docs[i].to_json()['kwargs']['page_content'])
            print(lawyer_info)
            string = ', '.join(lawyer_info)
            
            print(string[:6])
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": f"given a list of lawyer names and their complete information, starting from first, you will understand the name of the lawyers and give 6 lawyers containing 3 male and 3 female. response should only contain names separated by comma. "},
                            {"role": "user", "content": string}
            ], temperature=0)

            names = response["choices"][0]['message']['content']
            print("names", names)
            names_list = [name.strip() for name in names.split(',')]
            print(names_list)
            lawyer_information = {}

            # Iterate through the lawyer information strings
            for lawyer_info in lawyer_info:
                # Split the lawyer info into lines
                lines = lawyer_info.split('\n')
                
                # Extract the lawyer name from the first line
                lawyer_name = lines[0].replace('Lawyer Names: ', '')
                print(lawyer_name)
                # Check if this lawyer is in the names list
                if lawyer_name in names_list:
                    # Extract information for this lawyer
                    start_index = lawyer_info.find('Information:')
                    if start_index != -1:
                        # Extract information after 'Information:'
                        lawyer_infor = lawyer_info[start_index + len('Information:'):].strip()
                        # Store the information in the dictionary
                        lawyer_information[lawyer_name] = lawyer_infor
            print(lawyer_information)   
            return jsonify(lawyer_information)
    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'wav', 'flac', 'aiff', 'aifc'}

def convert_to_wav(audio_file):
    # Convert audio to WAV format (assuming it's not already in WAV)
    audio = AudioSegment.from_file(audio_file)
    wav_file = os.path.splitext(audio_file.filename)[0] + '.wav'
    audio.export(wav_file, format='wav')
    return wav_file

@app.route('/update_db', methods=['GET', 'POST'])
def update_db():
    data = request.form
    print("FORM recieved")
    text1 = data.get("text1")
    hi = vectorstore.add_embeddings([(text1,embeddings.embed_query(text1)),(text2,embeddings.embed_query(text2)),(text3,embeddings.embed_query(text3))])
    vectorstore.save_local("main-vectordb")
    return jsonify({'result':"success"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)


