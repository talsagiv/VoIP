import sys
import socket
import select
import base64
import sqlite3
import hashlib


#connect to database and setup socket. (GLOBALS)
conn = sqlite3.connect('test.db')
cur = conn.cursor()
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 23))
server_socket.listen(20)
open_client_sockets = []
messages_to_send = []



#register function
def reg(lst, soc):
    cur.execute("SELECT * FROM USERS WHERE NAME=" +lst[1])
    if cur.fetchone() is None:
        cur.execute("INSERT INTO USERS (NAME, PASS, ADDR, ONLINE) \
            VALUES (" + lst[1] + ", " + hashlib.sha256(lst[2]).hexdigest() + ", " + soc.gethostbyname(soc.gethostname()) + ", TRUE )")
        #TODO check if operation successful
        cur.commit()
        messages_to_send.append((soc, "SUCCEED"))
        #COMMAND|NAME|PASSWORD for register
    else:
        messages_to_send.append((soc, "FAILED"))



#login function
def lgn(lst, soc):
    cur.execute("SELECT PASS FROM USERS WHERE NAME=" +lst[1])
    password = cur.fetchone()
    if hashlib.sha256(lst[2]).hexdigest() == password:
        cur.execute("UPDATE USERES SET ONLINE=TRUE, ADDR="+ soc.gethostbyname(soc.gethostname()) +" \
            WHERE USER="+ lst[1])
        cur.commit()
        #TODO check if operation successful
        messages_to_send.append((soc, "SUCCEED"))
        #COMMAND|NAME|PASSWORD for login
    else:
        messages_to_send.append((soc, "FAILED"))



#disconnect
def dis(soc):
    cur.execute("UPDATE USERS set ONLINE = FALSE where ADDR=" + soc.getsockname()[0] + "")
    cur.commit()

#invitation to a call function
def inv(lst):
    pass


#accept invitation to call and initiate call function
def acp(lst):
    pass


#ignore invitation or terminate call
def bye(lst):
    pass


#return connected users
def usr(lst):
    pass







#Break the message into a list (COM NAME ....)
def prot_to_list(prot):
    command = prot[:3]
    prot = prot[3:]
    prot_lst = prot.split("|")
    lst = []
    lst.append(command)
    for data in prot_lst:
        lst.append(base64.b64decode(data))
    return lst


#function dictionary
function_protocol ={'REG': reg,

                                }




#send messages
def send_waiting_messages(wlist):
    for message in messages_to_send:
        (client_socket, data) = message
        if client_socket in wlist:
            client_socket.send(data)
            messages_to_send.remove(message)


def run_select():
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 23))
    server_socket.listen(20)
    open_client_sockets = []
    messages_to_send = []
    while True:

        rlist, wlist, xlist = select.select( [server_socket] + open_client_sockets, [], [] )

        for current_socket in rlist:

            #New Client
            if current_socket is server_socket:
                (new_socket, address) = server_socket.accept()
                open_client_sockets.append(new_socket)

            #New data for existing client
            else:

                #recieve data
                data = current_socket.recv(1024)

                #terminate connection
                if data == "":
                    open_client_sockets.remove(current_socket)
                    function_protocol["dis"](current_socket)

                #handle data
                else:
                    #Break the message into a list
                    lst = prot_to_list(data)

                    #call the function based on the command
                    function_protocol[lst[0]](lst)





    #send messages
    send_waiting_messages(wlist)




def main():
    run_select()



if __name__ is "__main__":
    main()