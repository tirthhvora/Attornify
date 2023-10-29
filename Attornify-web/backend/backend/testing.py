import requests
data={'prompt':"hi dear sir @ madam i am work enterprises shop casher my owner my big bother my owner all cosmer money take and leave in city all cosmer tarcher and attack me and my family what i do sir", "language":""}
 
response = requests.post(url='http://127.0.0.1:5001/get_response', data=data)
print(response.json())