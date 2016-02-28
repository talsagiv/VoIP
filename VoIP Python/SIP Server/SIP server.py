import socket
import select



server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 23))
server_socket.listen(20)
open_client_sockets = []
messages_to_send = []

def send_waiting_messages(wlist):
    for message in messages_to_send:
        (client_socket, data) = message
        if client_socket in wlist:
            client_socket.send(data)
            messages_to_send.remove(message)


def run_select():
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
                #handle data
                else:
                    pass

    #send messages
    send_waiting_messages(wlist)




def main():
    run_select()



if __name__ is "__main__":
    main()