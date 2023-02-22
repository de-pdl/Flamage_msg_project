import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from tkinter import *

HOST = "10.216.49.111"
PORT = 62996

print(HOST)
#riwaj is a dumbass

class Client:

    def __init__(self, host, port):

        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent = msg)

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        recieve_thread = threading.Thread(target=self.recieve)

        gui_thread.start()
        recieve_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")
        self.win.minsize(500, 800)
        self.win.title("Flamage Chat Service")
        

        def bind_enter(event):
            self.write()
        self.win.bind('<Return>', bind_enter)

        self.title = tkinter.Label(self.win, text="flamage.", font=("Courier", 20), anchor=CENTER, bg="lightgray")
        self.title.place(relx=0.35, rely=0.02, relheight=0.06, relwidth=0.3)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.place(relx=0.05, rely=0.1, relheight = 0.70, relwidth= 0.9)
        self.text_area.config(state='disabled')

        self.client_chat_text = Text(self.win, relief = RAISED, width = 20, font=("Courier", 12))
        self.client_chat_text.place(relx= 0.05, rely= 0.85, relheight= 0.1, relwidth= 0.65)

        self.client_chat_label = Label(self.win, text = "message:", font=("Courier", 12), bg="lightgray")
        self.client_chat_label.place(relx=0.04, rely= 0.8, relheight= 0.05, relwidth= 0.2)

        self.sendbutton = Button(self.win, text = "send", font=("Courier", 12), command=self.write)
        self.sendbutton.place(relx= 0.75, rely= 0.9, relheight= 0.05, relwidth= 0.20)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)
    
        self.win.mainloop()

    
    def write(self):
        message = f"{self.nickname}: {self.client_chat_text.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.client_chat_text.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)


    def recieve(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state = 'disabled')
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break

client = Client(HOST, PORT)

