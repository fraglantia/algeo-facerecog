from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
import random
import os
import cv2
from coba import *

refpath = './resources/REF/'
testpath = './resources/TEST/'


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
db = load_database() #load db data
m_open.mainloop()

# untuk menu utama : random atau pilih foto
m_menu = Tk()
m_menu.title('M U K A K U K A M U') #engga keliatan krn frame windowsnya dihapus wkwk
m_menu.wm_iconbitmap('./guiresources/icon.ico') #engga keliatan krn frame windowsnya dihapus wkwk
m_menu.geometry('350x350+350+200')
m_menu.resizable(0,0)
# m_menu.overrideredirect(1)

main_msg = "\nMatch your photos in Mukakukamu\nYou can pick your photo OR we can choose it for you!\n" 
m_message = Message(m_menu, text=main_msg, font=("Montserrat",10))
m_message.pack()

threshold = 0
v = IntVar()
v.set(1)
fn = ''

def get_t_value():
    #get threshold value from spinbox
    global threshold
    threshold = int(t_value.get()) 

def choose_img_option(choose=True):
    global fn
    if(choose):
        fn = chooseimg()
    else:
        fn = chooserandom()
    m_menu.destroy()

def chooserandom():
    images_path = testpath
    files = []
    folders = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]
    for subfolder in folders:
        files += [os.path.join(subfolder, p) for p in sorted(os.listdir(subfolder))]
    sample = random.sample(files, 1)
    return sample[0]

def chooseimg():
    fn = filedialog.askopenfilename(initialdir = "./resources",title = "Select file", filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    return fn

#choose image
random1 = Button(m_menu, command=lambda:choose_img_option(True), border=0) 
img1 = PhotoImage(file = "./guiresources/opt1.png") #file path disesuaikan
random1.config(image=img1)
random1.pack(padx=10,pady=10)

#randomize
random2 = Button(m_menu, command=lambda:choose_img_option(False), border=0)
img2 = PhotoImage(file = "./guiresources/opt2.png") #file path disesuaikan
random2.config(image=img2)
random2.pack()

m_menu.mainloop()

# print(v.get())
# print(fn)

# cos/euc dan threshold
m_method = Tk()
m_method.geometry('350x350+350+200')
m_method.title('M U K A K U K A M U')
Label(m_method, text="""Pilih metode yang Anda inginkan:""", justify = LEFT, padx = 20, pady=10, font=("Montserrat 12 bold")).pack()
Radiobutton(m_method, text="Euclidean Distance", padx = 50, variable=v, value=1, font=("Montserrat",10)).pack(anchor=CENTER)
Radiobutton(m_method, text="Cosine Similarity", padx = 50, variable=v, value=2, font=("Montserrat",10)).pack(anchor=CENTER)
m_method.wm_iconbitmap('./guiresources/icon.ico')
m_method.resizable(0,0)

def_thres = StringVar(m_method)
def_thres.set('10')

Label(m_method, text="""Tentukan nilai threshold yang Anda inginkan:""",justify = LEFT, padx = 20, pady=10, font=("Montserrat 12 bold")).pack()
t_value = Spinbox(m_method, from_=1 ,to=20,textvariable=def_thres)
t_value.pack()

ok = Button(m_method, font=('Montserrat',12), command=lambda:[get_t_value() ,m_method.destroy()], border=0)
img3 = PhotoImage(file='./guiresources/ok.png')
ok.config(image=img3)
ok.pack(anchor=CENTER,padx=10, pady=20)


backhome = Button(m_method,text="Back To Home")
backhome.pack(side = BOTTOM, padx = 20, pady=10)

m_method.mainloop()

maximg = int(def_thres.get())

matches = matching(fn, db, top=maximg, cosine=(v.get()==2))
counter = 0


def changeimg(matches, pos=True):
    global maximg
    global counter
    # print 
    bt1.configure(state=NORMAL)
    bt2.configure(state=NORMAL)
    if pos:
        counter += 1
    else:
        counter -= 1

    # maxnya ganti ntar
    if counter == maximg-1:
        bt1.configure(state=DISABLED)
    if counter == 0:
        bt2.configure(state=DISABLED)

    img2 = ImageTk.PhotoImage(Image.open(refpath+matches[counter][0]))
    canvas2.itemconfig(imgArea2, image=img2)
    canvas2.image = img2
    l_count.configure(text=str(counter+1))
    personname2 = (refpath+matches[counter][0]).split('/')[3].split('\\')[0]
    l_name2.configure(text=personname2)


m_img = Tk()
m_img.title('M U K A K U K A M U') #engga keliatan krn frame windowsnya dihapus wkwk
m_img.geometry('1000x400')
m_img.wm_iconbitmap('./guiresources/icon.ico') #engga keliatan krn frame windowsnya dihapus wkwk
m_img.resizable(0,0)

personname1 = fn.split('/')[3].split('\\')[0]
l_name1 = Label(m_img, text=personname1, font=("Montserrat", 8))
l_name1.pack(side=LEFT)

canvas1 = Canvas(m_img, width = 300, height = 300)
canvas1.pack(side=LEFT)
img1 = ImageTk.PhotoImage(Image.open(fn))
imgArea2 = canvas1.create_image(20,20, anchor=NW, image=img1)


personname2 = (refpath+matches[counter][0]).split('/')[3].split('\\')[0]
l_name2 = Label(m_img, text=personname2, font=("Montserrat", 8))
l_name2.pack(side=LEFT)

canvas2 = Canvas(m_img, width = 300, height = 300)
canvas2.pack(side=LEFT)
img2 = ImageTk.PhotoImage(Image.open(refpath+matches[counter][0]))
imgArea2 = canvas2.create_image(20,20, anchor=NW, image=img2)      

bt1 = Button(m_img, text=">>", command=lambda:changeimg(matches, pos=True), state=NORMAL)
bt2 = Button(m_img, text="<<", command=lambda:changeimg(matches, pos=False), state=DISABLED)
if counter == maximg-1:
    bt1.configure(state=DISABLED)
if counter == 0:
    bt2.configure(state=DISABLED)

l_count = Label(m_img, text="1", font=("Montserrat", 11))
l_count.pack(side=BOTTOM)

backhome = Button(m_img,text="Back To Home")
backhome.pack(side = BOTTOM)

bt1.pack(side=BOTTOM)
bt2.pack(side=BOTTOM)



m_img.mainloop()
