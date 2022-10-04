'''

Sends and recieves messages to communicate with the other user.
Allows user to send messages, receive new messages, or get
all messages sent. Called in 'a6.py'

'''

# Mukarram A.
# Kyle T.
# Nicholas G.
 
import socket, json, time
from unittest.mock import NonCallableMagicMock
from ds_message_protocol import *
 
#IP Address// Server : 168.235.86.101
#Port: 3021
 
#User1 = 'test5', '123'
#User2 = 'gel', '123'
#User3 =
 
class DirectMessage:
    '''
    Stores values for recipient, message, and timestamp as class attributes of the DirectMessage class
   
    '''
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None
   
class DirectMessageEx():
    '''
    Special Exception Class 
    Used when an error has occured for sending a direct message

    '''
 
    def __init__(self, message="OH NO! An error has occured for DirectMessage."):
        self.message = message
 
    def __str__(self):
        final_message = f"Exception occured --> {self.message}"
        return final_message
 
 
class DirectMessenger:
    '''
    Communicates with the DSU server and allows a user to send direct messages
    to another user, retrieve a list of new messages, and retrieve all messages
    
    '''
    def __init__(self, dsuserver=None, username=None, password=None):
        '''
        Creates class attributes for server token, dsuserver address, username, and password
       
        '''
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
 
    def check_error(self, dsuserver=None, username=None, password=None):
        '''
        Checks to confirm all parameters are valid using conditional statements before joining the DSU server
       
        returns: if a parameter is invalid, return False
       
        '''
        if dsuserver is not None:
            if type(dsuserver) != str:                                             #checks if server parameter is a string
                DirectMessageEx('TypeError. Server should be a string. Returning...')
                return False

        elif dsuserver is None:
            DirectMessageEx('Server address is not valid. Returning...')
            return False

        if username is None:
            DirectMessageEx('Username can not be empty. Returning...')
            return False
   
        if type(username) != str:                                                  #checks if username parameter is a string
            DirectMessageEx('TypeError. Username should be a string. Returning...')
            return False
   
        if username == '':
            DirectMessageEx('Username can not be empty. Returning...')             #checks if the username parameter is blank
            return False
   
        if ' ' in username:                                                        #checks if there is whitespace in the username parameter
            DirectMessageEx('Username can not contain whitespace. Returning...')
            return False
   
        if password is None:
            DirectMessageEx('Password can not be empty. Returning...')
            return False
   
        elif password is not None:
            if type(password) != str:                                              #checks if the password parameter is a string
                DirectMessageEx('TypeError. Password should be a string. Returning...')
                return False
   
            if password == '':
                DirectMessageEx('Password can not be empty. Returning...')         #checks if the password parameter is blank
                return False
   
            if ' ' in password:                                                    #checks if there is whitespace in the password parameter
                DirectMessageEx('Password can not contain whitespace. Returning...')
                return False
 
 
    def send(self, message:str, recipient:str) -> bool:
        '''
        Sends a direct message to another user
       
        returns: if the direct message is successfully sent, return True. if not successfully sent, return False
       
        '''
        if self.check_error(self.dsuserver, self.username, self.password) == False:
            return False
       
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            try:
                client.connect((self.dsuserver, 3021))                             #connects to the server using the server and port input parameters
            except (socket.gaierror, OSError):
                print('Connection refused, check ip and port. Returning...')
                return False
       
            self.token = join(client, self.username, self.password)
       
            dict_resp = directmessage(client, self.token, message, recipient)      #Returns a dictionary with the server response
            print(dict_resp['response']['message'])                                #Prints the message response from the server
            check = dict_resp['response']['type']                                  #Stores the "type" value from the server response
           
            if check == 'ok':                                                      #Checks if the server has sucessfully sent the direct message
                return True                                                        #Cerver has successfully sent the direct message. Return True
           
            else:
                return False                                                       #An issue occured when sending the direct message. Return False


    def retrieve_new(self) -> list:
        '''
        Joins the DSU server using the existing self.username and self.password class attributes and retrieves a list of new messages
        Before joining the server, check_error() is called to confirm if the existing variables are valid
       
        returns: list of new messages that have been sent to the user
       
        '''
        if self.check_error(self.dsuserver, self.username, self.password) == False:
            return False
       
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            try:
                client.connect((self.dsuserver, 3021))                            #connects to the server using the server and port input parameters
            except (socket.gaierror, OSError):
                print('Connection refused, check ip and port. Returning...')
                return False
       
            self.token = join(client, self.username, self.password)
            dict_resp = new_msg(client, self.token)                              #Stores dictionary from unread() function as a variable
            return dict_resp                                                     #Returns a list of all new messages
       
       
    def retrieve_all(self) -> list:
        '''
        Joins the DSU server using the existing self.username and self.password class attributes and retrieves a list of all messages
        Before joining the server, check_error() is called to confirm if the existing variables are valid.
       
        returns: list of all messages that have been sent to the user
       
        '''
        if self.check_error(self.dsuserver, self.username, self.password) == False:
            return False
       
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            try:
                client.connect((self.dsuserver, 3021))                          #connects to the server using the server and port input parameters
            except (socket.gaierror, OSError):
                print('Connection refused, check ip and port. Returning...')
                return False
       
            self.token = join(client, self.username, self.password)
            dict_resp = all_msg(client, self.token)                             #Stores dictionary from all_msg() function as a variable

            return dict_resp
