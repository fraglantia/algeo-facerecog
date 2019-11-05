from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
import random
import os
import cv2
# import coba

# ditambahin di run dulu ya gui nya --fu
# untuk opening 'aplikasi' ala2 microsoft word
m_open = Tk()
m_open.overrideredirect(1) #menghapus frame windows
m_open.geometry('350x350+350+200')
logo_path = './guiresources/title_logo.png' #path diseuaikan
img = PhotoImage(file=logo_path)
panel = Label(m_open, image = img)
panel.pack()

open_text = "M U K A K U K A M U"
m_open.message = Message(m_open, text=open_text, font=("Montserrat",20), width=350)
m_open.message.pack()

m_open.after(500, m_open.destroy) #tampil sebentar
m_open.mainloop()

# untuk menu utama : random atau pilih foto
m_menu = Tk()
m_menu.title('M U K A K U K A M U') #engga keliatan krn frame windowsnya dihapus wkwk
m_menu.wm_iconbitmap('./guiresources/icon.ico') #engga keliatan krn frame windowsnya dihapus wkwk
m_menu.geometry('350x350+350+200')
m_menu.resizable(0,0)
m_menu.overrideredirect(1)

main_msg = "\nSelidikilah kemiripan mukamu di MUKAKUKAMU!\nYou can pick your photo OR we can choose it for you!\n" 
m_message = Message(m_menu, text=main_msg, font=("Montserrat",10))
m_message.pack()

v = IntVar()
v.set(1)
fn = ''

Label(m_menu, text="""Pilih metode yang Anda inginkan:""", justify = LEFT, padx = 20, font=("Montserrat",10)).pack()
Radiobutton(m_menu, text="Euclidean Distance", padx = 50, variable=v, value=1, font=("Montserrat",8)).pack(anchor=W)
Radiobutton(m_menu, text="Cosine Similarity", padx = 50, variable=v, value=2, font=("Montserrat",8)).pack(anchor=W)

def choose_img_option(choose=True):
    global fn
    if(choose):
        fn = chooseimg()
    else:
        fn = chooserandom()
    m_menu.destroy()

def chooserandom():
    images_path = 'resources/PINS/'
    files = []
    folders = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]
    for subfolder in folders:
        files += [os.path.join(subfolder, p) for p in sorted(os.listdir(subfolder))]
    sample = random.sample(files, 1)
    return sample[0]

def chooseimg():
    fn = filedialog.askopenfilename(initialdir = "./resources",title = "Select file", filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    return fn

random1 = Button(m_menu, command=lambda:choose_img_option(True)) 
img1 = PhotoImage(file = "./guiresources/opt1.png") #file path disesuaikan
random1.config(image=img1)
random1.pack()

random2 = Button(m_menu, command=lambda:choose_img_option(False))
img2 = PhotoImage(file = "./guiresources/opt2.png") #file path disesuaikan
random2.config(image=img2)
random2.pack()

m_menu.mainloop()

print(v.get())
print(fn)

m_img = Tk()
m_img.title('M U K A K U K A M U') #engga keliatan krn frame windowsnya dihapus wkwk
m_img.geometry('700x400')
m_img.wm_iconbitmap('./guiresources/icon.ico') #engga keliatan krn frame windowsnya dihapus wkwk
m_img.resizable(0,0)

canvas1 = Canvas(m_img, width = 300, height = 300)
canvas1.pack(side=LEFT)
img1 = ImageTk.PhotoImage(Image.open(fn))
imgArea2 = canvas1.create_image(20,20, anchor=NW, image=img1)    

canvas2 = Canvas(m_img, width = 300, height = 300)
canvas2.pack(side=LEFT)
img2 = ImageTk.PhotoImage(Image.open(chooserandom()))
imgArea2 = canvas2.create_image(20,20, anchor=NW, image=img2)      

bt = Button(m_img, text=">>")
bt.pack(side=BOTTOM)

m_img.mainloop()


# menu ecluidean dan cosine
# m_method = Tk()
# m_method.title('M U K A K U K A M U')
# m_method.wm_iconbitmap('./guiresources/icon.ico')
# m_method.geometry('350x350+500+200')

# msg_method = "\nPilih metode yang Anda inginkan\n"
# m_method.message = Message(m_method, text=msg_method,font=("Montserrat",12))
# m_method.message.pack()

# euc_button = Button(m_method, command=m_method.destroy)
# img3 = PhotoImage(file="./guiresources/euc.png")
# euc_button.config(image=img3)
# euc_button.pack()

# cos_button = Button(m_method, command=m_method.destroy)
# img4 = PhotoImage(file="./guiresources/cos.png")
# cos_button.config(image=img4)
# cos_button.pack()

# m_method.mainloop()