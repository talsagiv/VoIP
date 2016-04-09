import pyaudio
import Audio
import socket
import thread
import base64
from Tkinter import *


#globals
audio = Audio.Audio(CHANNELS=1,FORMAT=pyaudio.paInt16, RATE=44100, CHUNK=32, NOFFRAMES=0.2)
sock_server = socket.socket()
sock_server.connect(("127.0.0.1", 23)) #server ip




#get name and pass from gui, reg to the server and check if successful
def reg(x):
    def commitreg():
        name = namevar.get()
        password = passwordvar.get()
        datatosend = "reg|"+base64.b64encode(name)+"|"+base64.b64encode(password)
        sock_server.send(datatosend)
        answer = sock_server.recv(1024)
        regGUI.destroy()
        if answer[:7] is "SUCCEED":
            pass #TODO add after reg
        else:
            reg("prob")



    regGUI = Tk()
    namevar = StringVar()
    if(x!="normal"):
        problem = Label(master=regGUI, text='Name is already taken').pack()
    passwordvar = StringVar()
    namelable = Label(master=regGUI, text='Name:').pack()
    nameentry = Entry(master=regGUI, textvariable= namevar).pack()
    passlable = Label(master=regGUI, text='Password:').pack()
    passentry = Entry(master=regGUI, textvariable= passwordvar).pack()
    button = Button(master = regGUI, text="Connect", command=commitreg).pack()
    regGUI.mainloop()


def lgn(x):
    def commitlgn():
        name = namevar.get()
        password = passwordvar.get()
        datatosend = "lgn|"+base64.b64encode(name)+"|"+base64.b64encode(password)
        sock_server.send(datatosend)
        answer = sock_server.recv(1024)
        lgnGUI.destroy()
        if answer[:7] is "SUCCEED":
            pass #TODO add after lgn
        else:
            lgn("prob")



    lgnGUI = Tk()
    namevar = StringVar()
    if(x!="normal"):
        problem = Label(master=lgnGUI, text='Incorrect details').pack()
    passwordvar = StringVar()
    namelable = Label(master=lgnGUI, text='Name:').pack()
    nameentry = Entry(master=lgnGUI, textvariable=namevar).pack()
    passlable = Label(master=lgnGUI, text='Password:').pack()
    passentry = Entry(master=lgnGUI, textvariable=passwordvar).pack()
    button = Button(master = lgnGUI, text="Connect", command=commitlgn).pack()
    lgnGUI.mainloop()





def main():
    '''
    #get the ip addr from the gui and start conversation
    def start_talk():
        ip = ip_addr.get()
        print ip
        thread.start_new_thread(send_audio(ip))
        #thread.start_new_thread(receive_audio(ip))


    #GUI
    GUI = Tk()
    ip_addr = StringVar()
    GUI.geometry('450x450')
    GUI.title("VOIP")
    ip_entry = Entry(GUI, textvariable=ip_addr).pack()
    button = Button(GUI, text="Connect", command=start_talk).pack()
    GUI.mainloop()'''

    GUI = Tk()
    regbutton = Button(GUI, text="register", command=lambda :reg("normal")).pack()
    lgnbutton = Button(GUI, text="login", command=lambda :lgn("normal")).pack()
    GUI.mainloop()




#function to handle recording audio and sending it
def send_audio(ip):
    global audio
    send_socket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        audio_to_send = audio.record_to_string()
        send_socket.sendto(audio_to_send, (ip, 5000))


#function to handle receiving audio and playing it
def receive_audio(ip):
    global audio
    receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receive_socket.bind(('0.0.0.0', 5000))
    while True:
        data = receive_socket.recv(65536)
        print data
        audio.string_to_wave("bla.wav",data)




if __name__ == "__main__":
    main()