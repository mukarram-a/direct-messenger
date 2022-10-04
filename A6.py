'''

Direct Messaging Program
- Supports full messaging between 2 users.
- Features graphical interface for easy use.
- Loads pre-existing conversations and saves when program is quit.

In collaboration with Kyle T. and Nicholas G.

'''
# Mukarram A.
# Kyle T.
# Nicholas G.
 
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import font
from profile import Post, Profile
from ds_messenger import DirectMessenger
import random as rdm
from pathlib import Path
 
class ServerVals:
    """
    Custom class that does not need initialization.
    Stores values of server address and pre-existing
    username and password.

    """
    dsuserver = "168.235.86.101"
    username = "test5"
    password = "123"
 
test_messenger = DirectMessenger(ServerVals.dsuserver, ServerVals.username, ServerVals.password) #The Direct Messenger that is used with values from ServerVals
 
try:
    full_response = test_messenger.retrieve_all()               #Retrieves all messages from JSON dictionaries
    global all_recipients                                       #Initializes list of recipients
    all_recipients = []
    for entry in full_response["response"]["messages"]:         #Collects all specific recipients from JSON dictionaries
        if entry["from"] not in all_recipients:
            all_recipients.append(entry["from"])
except:
    print("We're sorry. The messages could not be retrieved at this time.")
 
 
class Body(tk.Frame):
    """
    Class for our Tkinter body
    Opens all loaded widgets and graphical interface

    """
    def __init__(self, root, select_callback=None):
        """
        Initialize the Tkinter window.
        Allows Body to be run by the MainApp class.

        """
        #Initializes with root functionality from tk.
        tk.Frame.__init__(self, root)
        self.root = root
        try:
            self._draw()                                        #Draws the GUI canvas
        except:
            print("We're sorry. The GUI could not be drawn at this time")
   
    global response_with_recipient                              #Initializes a list to be accessed for all responses with a specific recipient
    response_with_recipient = []
 
    def node_select(self, event):
        """
        This function occurs when the user selects a node
        from the Point Tree on the far left of the Tkinter window.

        """
        try:
            self.post_history.delete('1.0', tk.END)             #Initalizes each of the two textboxes blank
            self.entry_editor.delete('1.0', tk.END)
        except:
            print("The content could not be deleted.")
 
        try:
            index = int(self.posts_tree.selection()[0][-1]) - 1 #Sets proper index for a user selection of a name on the point tree
            self.recipient_name = all_recipients[index]         #Gets the name using that index
        except:
            print("We're sorry. There was an issue with the Username Point Tree. Please Try Again Later")
 
        try:
            full_response = test_messenger.retrieve_all()       #Retrieves all messages from that particular user
        except:
            print("We're sorry. The messages could not be retrieved at this time.")
 
        try:
            response_with_recipient = []                        #Begins with a list that will record which responses are from the assigned recipient
            for entry in full_response["response"]["messages"]: #Extracts the responses from the json file
                if entry["from"] == self.recipient_name:
                    response_with_recipient.append(entry["message"])
        except:
            print("We're sorry. The messages could not be extracted from the database at this time.")
 
        self.update()                                           #Updates the GUI canvas
 
        try:
            for i in range(len(response_with_recipient)):       #Prints each message with the sender's username
                self.post_history.insert('1.0', self.recipient_name + ": " + response_with_recipient[i] + "\n")
        except:
            print("We're sorry. The messages could not be printed on screen at this time.")
       
        self.update() #Updates the GUI canvas
 
    def set_text_entry(self, text:str):
        """
        Clears/deletes content from "Post History"
        and "Entry Editor" text boxes.
        
        """
        try:
            self.post_history.delete('1.0','end')               #Deletes the content from the Post History Box
            self.post_history.insert('1.0', text)
            self.entry_editor.delete('1.0','end')               #Deletes the content from the Entry Editor Box
            self.entry_editor.insert('1.0', text)
        except:
            print("We're sorry. The content could not be changed at this time.")
   
    def add_user(self):
        """
        Allows current user to add another user to message.

        """
        try:
            self.add_user_mode = True                           #Sets the mode to true whenever the user presses the button
            self.recipient = ""                                 #Clears the existing data
            self.post_history.delete('1.0', tk.END)
            self.entry_editor.delete('1.0', tk.END)
            self.post_history.insert('1.0', "Please enter the New Username in the Opposite Textbox.\nPress 'Send' to Confirm.") #Asks the user to enter the new Username in the Entry Editor Box.
        except:
            print("We're sorry. The new username could not be added here.")
 
    def send(self):
        """
        Sends message to another user based on "Entry Editor" input.

        If the user is in the process of entering another user,
        then "Entry Editor" input is added as a username to the
        point tree instead of sending a message.

        """
        if not self.add_user_mode:                                          #If the user means to send
            try:
                message_to_be_sent = self.entry_editor.get('1.0', tk.END)   #Gets message from box
           
                #Gets rid of any lingering newlines in the name or message
                if "\n" in message_to_be_sent:
                    message_to_be_sent = message_to_be_sent[:-1]
           
                if "\n" in self.recipient_name:
                    self.recipient_name = self.recipient_name[:-1]
   
                test_messenger.send(message_to_be_sent, self.recipient_name) #Sends the message
                self.node_select(None)                                       #Updates the GUI via the node_select method
            except:
                print("We're sorry. The messages could not be sent to the recipient at this time.")
 
        elif self.add_user_mode:                                             #If the user means to add a new username
            try:
                new_username = self.entry_editor.get('1.0', tk.END)          #Gets the username
                all_recipients.append(new_username)                          #Adds the name to a list
                if "\n" in new_username:                                     #Gets rid of lingering new lines
                    new_username = new_username[:-1]
                self.posts_tree.insert("", tk.END, text=new_username)        #Inserts into a post tree
                self.recipient_name = new_username                           #Assigns new username to appropriate variables
                self.set_text_entry("")                                      #Clears the Boxes
                self.update()                                                #Updates the Canvas
                self.add_user_mode = False                                   #Puts back to default mode
            except:
                print("We're sorry. The new username could not be added to the Username Point Tree.")
 
    def insert_post(self):
        """
        Inserts "post tree" contents into the GUI. 
        According to all recipients the GUI receives, 
        the post tree will vary in size.
        
        """
        try:
            self.all_recipients = all_recipients                            #Sets toa class wide varaible
            for entry in all_recipients:                                    #Inserts each happening onto the point tree
                if len(entry) > 25:                                         #Shortens to ... if the entry is too long.
                    entry = entry[:24] + "..."    
                self.posts_tree.insert("", tk.END, text=str(entry))
        except:
            print("We're sorry. The post could not be inserted onto the Point Tree.")
 
 
    def changer(self):
        """
        Generates fun facts based on user prompts on the GUI.
        A random selection of fun facts are selected and shared with the user
        when the button is pressed. 

        This mode can be turned off if the button is pressed again.

        """
        try:
            self.fun_fact_mode = not self.fun_fact_mode                     #Switches the modes
            fun_fact = rdm.randint(0,4)                                     #Picks random index of facts
            fact_list = ["The scientific name of the water buffalo is Bubalus Bubalis.",
            "Did you know that Python was originally created by Guido Van Rossum?",
            "Cooper is one of the best tortoises that the world has ever seen!",
            "Zulip and Discord are both excellent chatting services!",
            "ICS 32 is a great class and we highly recommend it be taken!"] #List of fun facts to be shared
            if self.fun_fact_mode:                                          #If we are in fun fact mode
                self.set_text_entry("")                                     #Reset the screen
                self.post_history.insert('1.0', "Fun Fact:\n" + fact_list[fun_fact]) #Shares the Fun Fact
            elif not self.fun_fact_mode:
                self.set_text_entry("")                                     #Reset the screen
                self.node_select(None)                                      #Update via node_select()
        except:
            print("We're sorry. The Fun Facts could not be shared at this time.")
       
    def _draw(self):
        """
        Draws each of the widgets to specific sizes and allows
        the rest of the class to access the widgets.
    
        """
        #Sets the post frame on which the post tree will be placed
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)
 
        #Inserts the post tree onto the GUI
        self.posts_tree = ttk.Treeview(posts_frame)
        self.insert_post()
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)
 
        #Enters entry frame onto which the other widgets will be placed
        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
       
        #Enters editor frame onto which the two text boxes will be placed
        editor_frame = tk.Frame(master=entry_frame, bg="")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
 
        #Places send button onto the GUI
        send_button = tk.Button(master=self, text="Send", width=20)
        send_button.configure(command=self.send)
        send_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)
 
        #Places add user button onto the GUI
        add_user_button = tk.Button(master=self, text="Add User", width=20)
        add_user_button.configure(command=self.add_user)
        add_user_button.pack(fill=tk.BOTH, side=tk.LEFT, padx=5, pady=5)
        self.add_user_mode = False #Sets default mode of pressing this button to false
 
        #Places fun fact button onto the GUI
        fun_fact = tk.Button(master=self, text="Fun Fact Mode On/Off", width=20)
        fun_fact.configure(command=self.changer)
        fun_fact.pack(fill=tk.BOTH, side=tk.BOTTOM, padx=5, pady=5)
        self.fun_fact_mode = False #Sets default mode of pressing this button to false
       
        #Places Entry Editor text box onto the GUI
        self.entry_editor = tk.Text(editor_frame, width=0)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True, padx=5, pady=5)
 
        #Places Post History text box onto the GUI
        self.post_history = tk.Text(editor_frame, width=0)
        self.post_history.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=5, pady=5)
 
 
class MainApp(tk.Frame):
    """
    MainApp Class which allows the Body widgets 
    to be added in a uniform manner to the GUI.

    """
    def __init__(self, root):
        """
        Initializes the MainApp class.
        A root is specified from which a proper GUI can be generated.

        """
        #Initializes with root functionality from tk.
        tk.Frame.__init__(self, root)
        self.root = root
        try:
            self._draw()
        except:
            print("We're sorry. The GUI could not be drawn at this time")
   
    def check_something(self):
        """
        Updates GUI automatically every 5 seconds.

        """
        #Updates and checks every 5 seconds.
        try:
            self.update()
            self.root.after(5000,self.check_something)
        except:
            print("We're sorry. The automated checking does not work at this time.")
 
    def _draw(self):
        """
        Draws the GUI widgets defined in 
        the Body class to the GUI properly.

        """
        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
 
 
if __name__ == "__main__":
    # root widnow
    main = tk.Tk()
 
    # 'title' assigns a text value to the Title Bar of a window.
    main.title("Messenger")
 
    # size for window
    main.geometry("720x480")
 
    # adding this option removes some legacy behavior with menus that modern OS's don't support.
    main.option_add('*tearOff', False)
    mainApp = MainApp(main)
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height()) #min size for GUI Canvas
    try:
        main.after(5000, mainApp.check_something) #Checks for progress in main loop every 5 seconds.
    except:
        print("We're sorry. The automated checking does not work at this time.")
    main.mainloop()
 