from flask import Flask, request, jsonify
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
import openai
import pickle
from flask_cors import CORS
import pandas as pd
# with open('embeddings.pkl' , 'rb') as f:
#     embeddings = pickle.load(f)
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from googletrans import Translator 
from flask import Flask, jsonify, request,send_file
import speech_recognition as sr
from gtts import gTTS
from flask_cors import CORS
from pydub import AudioSegment
import os
openai_key = "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"
embeddings = OpenAIEmbeddings(openai_api_key=openai_key)
llm = OpenAI(openai_api_key=openai_key, model_name='gpt-3.5-turbo')
admin_prompt =  "INSTRUCTIONS: You are an expert lawyer. You will get a user query or a client situation. you also have a dataset of lawyers in the form of a vectordatabase with these attributes: Lawyer Names, lawyer Experience, Practice Areas, Client Feedback, Jurisdiction, Hourly Rate, Avg Days for Disposal, Languages, Pro Bono Services, Client Demographics. you understand the query or situation given by user, and link it to the dataset lawyer attributes and give output of what attributes values of lawyers will be applicable for the query. Convert the user query into a query using or linking the attributes i gave you that i can give my vectordatabase for semantic search. give a single string as output"
    
#  who if gets a client query or a situation, you can give technical query out of it

app = Flask(__name__)

CORS(app)

@app.route('/get_response', methods=['GET', 'POST'])
def get_response():
    vectorstore = FAISS.load_local("main-vectordb",embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k":20})
    data = request.json
    print("FORM recieved")
    naive_prompt = data.get("prompt")
    naive_prompt = "QUERY: " + naive_prompt + " INSTRUCTIONS: understand the query deeply and map with possible lawyer attributes. lawyer should be highly experienced and in similar practice area"
    language = data.get('language')
    print(language)
    print("data received")
    lawyer_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": admin_prompt},
                        {"role": "user", "content": naive_prompt}
        ], temperature=0)
    a = lawyer_response["choices"][0]['message']['content']
    relevant_docs = retriever.get_relevant_documents(a)
    relevant_docs[0].to_json()['kwargs']['page_content']

    lawyer_info =[]
    for i in range(len(relevant_docs)):
        lawyer_info.append(relevant_docs[i].to_json()['kwargs']['page_content'])
    string = "".join(lawyer_info) + f"COMPULSUORY: picked lawyer should speak {language}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": f"given a list of lawyer names and their complete information, starting from first, you will understand the name of the lawyers and give 6 lawyers containing 3 male and 3 female. response should only contain names separated by comma.COMPULSUORY: picked lawyer should speak {language} "},
                        {"role": "user", "content": string }
        ], temperature=0)

    names = response["choices"][0]['message']['content']

    names_list = [name.strip() for name in names.split(',')]

    lawyer_information = {}

    # Iterate through the lawyer information strings
    for lawyer_info in lawyer_info:
        # Split the lawyer info into lines
        lines = lawyer_info.split('\n')
        
        # Extract the lawyer name from the first line
        lawyer_name = lines[0].replace('Lawyer Names: ', '')
        
        # Check if this lawyer is in the names list
        if lawyer_name in names_list:
            # Extract information for this lawyer
            start_index = lawyer_info.find('Information:')
            if start_index != -1:
                # Extract information after 'Information:'
                lawyer_infor = lawyer_info[start_index + len('Information:'):].strip()
                # Store the information in the dictionary
                lawyer_information[lawyer_name] = lawyer_infor
    
    return jsonify(lawyer_information)

@app.route('/update_db', methods=['GET', 'POST'])
def upload_file():
    embeddings = OpenAIEmbeddings(openai_api_key=openai_key)
    vectorstore = FAISS.load_local("main-vectordb",embeddings)

    # Check if a file is included in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file included in the request"})
 
    file = request.files['file']
    print('file recieved')
    # Check if the file has an allowed extension (e.g., .csv or .xlsx)
    allowed_extensions = {'csv', 'xlsx'}
    if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
        # Read the file using pandas
        if file.filename.rsplit('.', 1)[1].lower() == 'csv':
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
 
        # Generate text strings for each row
        texts = []
        text_embeddings=[]
        for index, row in df.iterrows():
            lawyer_name = row['Name']
            description = row['Information']
            text = f"{lawyer_name}\n{description}"
            texts.append(text)
        for text in texts:
            embedding = embeddings.embed_query(text)
            text_embeddings.append((text, embedding))
        print("embeddings successfully created")   
        hi = vectorstore.add_embeddings(text_embeddings)
        vectorstore.save_local("main-vectordb")
        print("new data added to the database")
        return jsonify({'result':"success"})
    
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
           
            naive_prompt = "QUERY: " + translated_prompt + " INSTRUCTIONS: understand the query deeply and map with possible lawyer attributes. lawyer should be highly experienced and in similar practice area"
        

            lawyer_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": admin_prompt},
                            {"role": "user", "content": naive_prompt}
            ], temperature=0)

            a = lawyer_response["choices"][0]['message']['content']
            relevant_docs = retriever.get_relevant_documents(a)
 
            lawyer_info =[]
            for i in range(len(relevant_docs)):
                lawyer_info.append(relevant_docs[i].to_json()['kwargs']['page_content'])
        
            string = ', '.join(lawyer_info)
 
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": f"given a list of lawyer names and their complete information, starting from first, you will understand the name of the lawyers and give 6 lawyers containing 3 male and 3 female. response should only contain names separated by comma. "},
                            {"role": "user", "content": string}
            ], temperature=0)

            names = response["choices"][0]['message']['content']
   
            names_list = [name.strip() for name in names.split(',')]
            print(names_list)
            lawyer_information = {}

            # Iterate through the lawyer information strings
            for lawyer_info in lawyer_info:
                # Split the lawyer info into lines
                lines = lawyer_info.split('\n')
                
                # Extract the lawyer name from the first line
                lawyer_name = lines[0].replace('Lawyer Names: ', '')
                
                # Check if this lawyer is in the names list
                if lawyer_name in names_list:
                    # Extract information for this lawyer
                    start_index = lawyer_info.find('Information:')
                    if start_index != -1:
                        # Extract information after 'Information:'
                        lawyer_infor = lawyer_info[start_index + len('Information:'):].strip()
                        # Store the information in the dictionary
                        lawyer_information[lawyer_name] = lawyer_infor
     

            return jsonify(lawyer_information)
    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'wav', 'flac', 'aiff', 'aifc'}

def convert_to_wav(audio_file):
    # Convert audio to WAV format (assuming it's not already in WAV)
    audio = AudioSegment.from_file(audio_file)
    wav_file = os.path.splitext(audio_file.filename)[0] + '.wav'
    audio.export(wav_file, format='wav')
    return wav_file

 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)
