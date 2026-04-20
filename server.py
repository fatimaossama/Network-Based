import socket
import threading
import os
from tkinter import *

# إعدادات ريلواي
PORT = int(os.environ.get("PORT", 55555))
HOST = '0.0.0.0'

def receive_messages():
    global conn
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            chat_box.insert(END, f"Client: {data.decode()}\n")
            chat_box.yview(END)
        except:
            break

def send_message():
    message = msg_entry.get()
    if message and conn:
        try:
            chat_box.insert(END, f"You: {message}\n")
            conn.sendall(message.encode())
            msg_entry.delete(0, END)
            chat_box.yview(END)
        except:
            chat_box.insert(END, "Error: Connection lost.\n")

def start_server():
    global conn
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    chat_box.insert(END, f"Server started on port {PORT}...\nWaiting for client...\n")
    
    conn, addr = server_socket.accept()
    chat_box.insert(END, f"Connected by {addr}\n")
    # بعد ما العميل يتصل، نبدأ خيط الاستقبال
    threading.Thread(target=receive_messages, daemon=True).start()

# إعداد الواجهة
root = Tk()
root.title("WhatsApp Server Style")
chat_box = Text(root, height=20, width=50)
chat_box.pack(padx=10, pady=10)
msg_entry = Entry(root, width=40)
msg_entry.pack(side=LEFT, padx=10)
Button(root, text="Send", command=send_message, bg="#25D366", fg="white").pack(side=RIGHT, padx=10)

conn = None
# تشغيل السيرفر في Thread عشان الـ UI ما يتجمدش
threading.Thread(target=start_server, daemon=True).start()

root.mainloop()