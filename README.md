#

## How to use the Messenger Program (A6.py)
#

### **The Main GUI File is A6.py**



When the program is run, the user will see 3 large text-boxes on the screen: 

* The box on the far left is for selecting the existing users. Clicking on one of the usernames will open and load all of the messages between the user and the other client.

* The box in the middle of the screen will show the user the messages that have been sent from the other client.

* The box on the far right is an entry box where the user can write messages that he would like to send.

There are 3 buttons located at the bottom of the GUI:
* **Add User**: Allows the user to add other clients that they would like to message. This button will send a message to the DSU server to connect and allow the user to send messages to the other client.
* **Fun Fact Mode**: This fun fact mode generates a random fun fact for the user and is the "flourish" feature in the program.
* **Send**: This send button sends a message to another user after a message has been written in the text-box.

On startup, the program will automatically load in messages from the other users once their username is clicked.

* We have implemented security features in our program as well. Two users are only able to communicate when **both parties send a message to one another**. This way, users cannot recieve messages from unknown strangers and are only able to send messages to someone who sends a message back to them. This also eliminates any miscommunication/accidental messaging when trying to message another user. The GUI will only update when the user you have sent a message to responds back to you, in order to ensure privacy and security for both users.