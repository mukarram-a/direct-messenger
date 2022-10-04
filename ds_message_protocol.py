'''

Creates JSON-formatted dictionaries to send to 'ds_messagenger.py'.
JSON-formatted dictionaries allow the user to log on to the 
server, send messages, convert messages into JSON, edit their biography,
and open a new message to new users.

'''

# Mukarram A.
# Kyle T.
# Nicholas G.
  
import json
from profile import *
import time
 
def to_json(obj:dict) -> str:

    """
    Serializes a Python dictionary object to a JSON-formatted string
    
    returns: None if object cannot be serialized to JSON
    """
    try:
       json_obj = json.dumps(obj)                               #Uses json.dumps() in order to un-json the object
       return json_obj                                          #Returns the object
    except:
       return None

 
def from_json(obj:str) -> any:                                  #Turns a Python-readable string into json format

    """
    Deserializes a JSON-formatted string to a python type.
    The return type depends on JSON structure.
    
    returns: None if string cannot be deserialized from JSON
    """
    try:
        python_obj = json.loads(obj)                            #Uses json.loads() to json-ify the object
        return python_obj                                       #Returns the object
    except:
        return None
 
def join(client, username:str, password:str) -> str:
    '''
    Sends a join message to the DSU server by creating a JSON formatted dictionary
   
    returns: Server Token
   
    '''
    join_dict = {"join": {"username": username,"password": password, "token":""}}
    join_msg = to_json(join_dict)
    send = client.makefile('w')                                 #Uses client in order to create a write file to be used later
    recv = client.makefile('r')                                 #Uses client in order to create a read file to be used later
    send.write(join_msg + '\r\n')
    send.flush()
    resp = recv.readline()
    resp_python = from_json(resp)
    user_token = resp_python['response']['token']
    return user_token                                           #Returns the token
 
 
def post(client, user_token:str, message:str) -> dict:
    '''
    Sends a post to publish on the DSU server by creating a JSON formatted dictionary
   
    returns: dictionary (server's response message)
   
    '''
    timeNow = time.time()
    post_dict = {"token": user_token, "post": {"entry": message,"timestamp": timeNow}}
    post_msg = to_json(post_dict)
    send = client.makefile('w')                                 #Uses client in order to create a write file to be used later
    recv = client.makefile('r')                                 #Uses client in order to create a read file to be used later
    send.write(post_msg + '\r\n')
    send.flush()
    resp = recv.readline()
    resp_python = from_json(resp)
    return resp_python                                          #Returns the dictionary with confirmation or error message
 
 
def bioFun(client, user_token:str, bio:str) -> dict:
    '''
    Sends a bio to the DSU server by creating a JSON formatted dictionary
   
    returns: dictionary (server's response message)
   
    '''
    timeNow = time.time()
    bio_dict = {"token": user_token, "bio": {"entry": bio,"timestamp": timeNow}} #Appropriate dictionary layout to be compatible with JSON serialization
    bio_msg = to_json(bio_dict)                                 #Turns the dictionary into JSON format
    send = client.makefile('w')                                 #Uses client in order to create a write file to be used later
    recv = client.makefile('r')                                 #Uses client in order to create a read file to be used later
    send.write(bio_msg + '\r\n')
    send.flush()
    resp = recv.readline()
    resp_python = from_json(resp)
    return resp_python                                          #Returns the dictionary with confirmation or error message
 
 
def directmessage(client, user_token:str, dmessage:str, recipient:str) -> dict:
    '''
    Sends a direct message to another user by creating a JSON formatted dictionary
    returns: dictionary (server's response message)
   
    '''
    timeNow = time.time()
    dmDict = {"token": user_token, "directmessage": {"entry": dmessage, "recipient": recipient, "timestamp": timeNow}}
    dm_msg = to_json(dmDict)                                    #Turns the dictionary into json format
 
    send = client.makefile('w')                                 #Uses client in order to create a write file to be used later
    recv = client.makefile('r')                                 #Uses client in order to create a read file to be used later
    send.write(dm_msg + '\r\n')                                 
    send.flush()                                                
    resp = recv.readline()                                      
    resp_python = from_json(resp)                               
    return resp_python                                          #Returns the dictionary with confirmation or error message
   
 
def new_msg(client, token:str) -> dict:
    '''
    Sends a "new message" request to the server by creating a JSON formatted dictionary
   
    returns: a dictionary of all new messages that have been sent to the user
   
    '''
    dmDict = {"token": token, "directmessage": "new"}
    dm_msg = to_json(dmDict)
   
    send = client.makefile('w')                                 #Uses client in order to create a write file to be used later
    recv = client.makefile('r')                                 #Uses client in order to create a read file to be used later
    send.write(dm_msg + '\r\n')                                 #Returns carriage and adds new line to the message, and writes this combination to the write file
    send.flush()
    resp = recv.readline()
    resp_python = from_json(resp)
    return resp_python                                          #Returns the dictionary with all new messages
 
 
def all_msg(client, token:str) -> dict:
    '''
    Sends a "all messages" request to the server by creating a JSON formatted dictionary
   
    returns: a dictionary of all messages that have been sent to the user
   
    '''
    dmDict = {"token": token, "directmessage": "all"}
    dm_msg = to_json(dmDict)
   
    send = client.makefile('w')                                #Uses client in order to create a write file to be used later
    recv = client.makefile('r')                                #Uses client in order to create a read file to be used later
    send.write(dm_msg + '\r\n')
    send.flush()
    resp = recv.readline()
    resp_python = from_json(resp)
    return resp_python                                         #Returns the dictionary with all messages from the sender
