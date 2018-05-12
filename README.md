# cli-chat
A simple command line chat program for linux and windows written in python  
Currently the windows client is written in python 2 whereas the linux client is written in python 3

The messages are stored unencrypted on: http://waksmemes.x10host.com/mess/  
  
## Usage:  
### Entering chat rooms:  
To start chatting in the main chat room:  
`python chat.py`  
  
To start chatting in a chat room called "different_chat_room":  
`python chat.py different_chat_room`
  
### Sending messages  
After all a chat room's messages are printed a '> ' symbol is printed. This final line of text is called the _input line_.
To send a message simply type your message on the input line and press enter.  
If the user presses enter without typing a message, no message is sent
If the user runs a command no message is sent

### Reading messages
New messages are fetched every time the user presses enter on the input line, regardless of whether or not they sent a message  
To automatically reload the chat (fetch messages without having to press enter) you can start the script in _auto-reloading read-only mode_.  
  
To start in auto-reloading read-only mode:  
`python chat.py -r`
  
To start in auto-reloading read-only mode in a chat room called "different_chat_room":  
`python chat.py -r different_chat_room`

### Commands  
Commands begin with a backslash (\\) and are issued on the input line in a similar fashion to shell commands. Commands can take any number of arguments.  
#### The set command
set is used to configure your user settings. User settings are saved in a local configuration file that is automatically generated when the set command is used. These settings are sent along with every message you send so that other clients can use them.
  
Usage:  
`\set setting value`

Types of settings:  

|Setting name | Purpose                                                                                                      |
| ----------- |:------------------------------------------------------------------------------------------------------------:|
| name        | Sets your name so you're no longer identified by your IP                                                     |
| color       | Sets the color of your name. The only possible colors so far are red, green, purple, blue, yellow and cyan   |

#### Other commands  

|Command name | Args                | Explanation                                   | Example           |
| ----------- |:-------------------:|:---------------------------------------------:|:------------------:
| room        | (1) roomname        | Switches the room to roomname                 | \room other_room  |
| read        | (0) No arguments    | Swithces into auto-reloading read-only mode   | \read             |
