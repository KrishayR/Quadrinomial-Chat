import tkinter as tk
import tkmacosx as tkm
import tkinter.scrolledtext
import socket
import threading
from tkinter import simpledialog

HOST = '127.0.0.1' # Enter IP
PORT = 9090 # Enter Port


class Client():
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tk.Tk()
        msg.withdraw()
        
        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent=msg)
        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)


        gui_thread.start()
        receive_thread.start()
        msg.mainloop()

    def gui_loop(self):
        self.window = tk.Tk()
        self.window.config(background='#2f333b')
        self.window.geometry("1200x700")
        self.window.title("Quadrinomial")
        self.window.grid_rowconfigure(1,weight=1)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.window, background='#2f333b',fg="#ff574e")
        self.text_area.grid(row=0, column=0, sticky='n')
        self.text_area.config(state='disabled')
        
        self.input_area = tk.Text(self.window, fg="#ff574e", height=2, width=105)
        self.input_area.grid(row=1, column=0, sticky="s")
        self.input_area.configure(font=("Courier", 16))

        self.send_button = tkm.Button(
                                 self.window,
                                 highlightbackground="#ff574e",
                                 borderless=1,
                                 focuscolor='',
                                 bg="#ff574e",
                                 activebackground='#ff574e',
                                 fg="black",
                                 text="Send",
                                 height=44,
                                 width=140,
                                 command=self.write
                                 )
        self.send_button.grid(row=1, column=1, sticky="s")
        self.gui_done = True
        self.window.protocol("WM_DELETE_WINDOW", self.stop)
        self.window.mainloop()

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.window.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024)
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state="normal")
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
                        
            except ConnectionAbortedError:
                break
            except:
                print("Something happened error")
                self.sock.close()
                break
            
client = Client(HOST, PORT)
                    
            
        

        



