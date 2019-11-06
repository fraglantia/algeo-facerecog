from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
import random
import os
import cv2
from matcher import *

def open():
    global m_open
    global m_menu
    # ditambahin di run dulu ya gui nya --fu
    # untuk opening 'aplikasi' ala2 microsoft word
    m_open = Tk()
    m_open.overrideredirect(1) #menghapus frame windows
    m_open.geometry('350x350+500+200')
    logo_path = './guiresources/title_logo.png' #path diseuaikan
    img = PhotoImage(file=logo_path)
    panel = Label(m_open, image = img)
    panel.pack()

    open_text = "M U K A K U K A M U"
    m_open.message = Message(m_open, text=open_text, font=("Montserrat",20), width=350)
    m_open.message.pack()

    m_open.after(800, m_open.destroy) #tampil sebentar
    m_open.mainloop()

def menu():
    global v
    global fn
    global m_open
    global m_menu

    def chooserandom():
        images_path = testpath
        files = []
        folders = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]
        for subfolder in folders:
            files += [os.path.join(subfolder, p) for p in sorted(os.listdir(subfolder))]
        sample = random.sample(files, 1)
        return sample[0]

    def chooseimg():
        fn = filedialog.askopenfilename(initialdir = "./resources/TEST",title = "Select file", filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        return fn

    def choose_img_option(choose=True):
        global fn
        if(choose):
            fn = chooseimg()
            if(fn == ''):
                return
        else:
            fn = chooserandom()
        m_menu.destroy()

    # untuk menu utama : random atau pilih foto
    m_menu = Tk()
    m_menu.title('M U K A K U K A M U') #engga keliatan krn frame windowsnya dihapus wkwk
    m_menu.wm_iconbitmap('./guiresources/icon.ico') #engga keliatan krn frame windowsnya dihapus wkwk
    m_menu.geometry('350x350+500+200')
    m_menu.resizable(0,0)
    m_menu.overrideredirect(1)

    logo_path = './guiresources/title_logo.png' #path diseuaikan
    img = PhotoImage(file=logo_path)
    panel = Label(m_menu, image = img)

    backimg = PhotoImage(file='./guiresources/m_back.png')
    Label(m_menu, image=backimg).place(x=0,y=0)

    #choose image
    c_img = Button(m_menu, command=lambda:choose_img_option(True), border=0, bg='#f3ede8') 
    img1 = PhotoImage(file = "./guiresources/opt1.png") #file path disesuaikan
    c_img.config(image=img1)
    c_img.place(x=70, y=150)

    #randomize
    r_img = Button(m_menu, command=lambda:choose_img_option(False), border=0, bg='#f3ede8')
    img2 = PhotoImage(file = "./guiresources/opt2.png") #file path disesuaikan
    r_img.config(image=img2)
    r_img.place(x=70, y=220)

    m_menu.mainloop()

    # print(v.get())
    # print(fn)

def method():
    global fn
    global v
    global matches
    global maximg

    # cos/euc dan threshold
    m_method = Tk()
    m_method.geometry('350x350+500+200')
    m_method.title('M U K A K U K A M U')
    mth_bg = PhotoImage(file='./guiresources/m_choosemethod.png')
    Label(m_method, image=mth_bg).place(x=0,y=0)
    v=IntVar()
    v.set(1)

    Label(m_method, text="""Pilih metode yang Anda inginkan:""", justify = LEFT, padx = 20, pady=10, font=("Montserrat 8 bold"), bg='#ffffff').place(y = 100)
    Radiobutton(m_method, text="Euclidean Distance", padx = 50, variable=v, value=1, font=("Montserrat",10), bg='#ffffff').place(y = 130)
    Radiobutton(m_method, text="Cosine Similarity", padx = 50, variable=v, value=2, font=("Montserrat",10), bg='#ffffff').place(y = 150)
    m_method.wm_iconbitmap('./guiresources/icon.ico')
    m_method.resizable(0,0)
    m_method.overrideredirect(1)

    def_thres = StringVar(m_method)
    def_thres.set('10')

    Label(m_method, text="""Tentukan nilai threshold yang Anda inginkan:""",justify = LEFT, padx = 20, pady=10, font=("Montserrat 8 bold"), bg='#ffffff').place(y = 180)
    t_value = Spinbox(m_method, from_=1 ,to=20,textvariable=def_thres)
    t_value.place(x=60, y = 220)

    ok = Button(m_method, command=lambda:m_method.destroy(), border=0, bg='#ffffff')
    img3 = PhotoImage(file='./guiresources/ok.png')
    ok.config(image=img3)
    ok.place(x=70, y= 260)

    m_method.mainloop()

    maximg = int(def_thres.get())
    if(maximg>20):
        maximg = 20
    if(maximg<1):
        maximg = 1

    matches = matching(fn, db, top=maximg, cosine=(v.get()==2))
    counter = 0

def img():
    global matches
    global counter
    global fn
    global v

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

    def ret2home():
        global reset
        reset = True
        m_img.destroy()

    def exit():
        global reset
        reset = False
        m_img.destroy()

    m_img = Tk()
    m_img.title('M U K A K U K A M U') #engga keliatan krn frame windowsnya dihapus wkwk
    m_img.geometry('800x450+200+150')
    m_img.wm_iconbitmap('./guiresources/icon.ico') #engga keliatan krn frame windowsnya dihapus wkwk
    m_img.resizable(0,0)
    m_img.overrideredirect(1)

    personname1 = fn.split('/')[3].split('\\')[0]
    l_name1 = Label(m_img, text=personname1, font=("Montserrat", 8))
    l_name1.place(x=150, y=35)

    canvas1 = Canvas(m_img, width = 300, height = 300)
    canvas1.place(x=50,y=50)
    img1 = ImageTk.PhotoImage(Image.open(fn))
    imgArea2 = canvas1.create_image(20,20, anchor=NW, image=img1)

    personname2 = (refpath+matches[counter][0]).split('/')[3].split('\\')[0]
    l_name2 = Label(m_img, text=personname2, font=("Montserrat", 8))
    l_name2.place(x=500, y=30)

    canvas2 = Canvas(m_img, width = 300, height = 300)
    canvas2.place(x=400,y=50)
    img2 = ImageTk.PhotoImage(Image.open(refpath+matches[counter][0]))
    imgArea2 = canvas2.create_image(20,20, anchor=NW, image=img2)      

    bt1 = Button(m_img, text=">>", command=lambda:changeimg(matches, pos=True), state=NORMAL)
    bt2 = Button(m_img, text="<<", command=lambda:changeimg(matches, pos=False), state=DISABLED)
    bt1.place(x=400,y=370)
    bt2.place(x=350,y=370)

    if counter == maximg-1:
        bt1.configure(state=DISABLED)
    if counter == 0:
        bt2.configure(state=DISABLED)

    l_count = Label(m_img, text="1", font=("Montserrat", 11))
    l_count.place(x=380,y=370)

    backhome = Button(m_img,text="Back To Home", command=lambda:ret2home(), border=0)
    img5 = PhotoImage(file='./guiresources/reset.png')
    backhome.config(image=img5)    
    backhome.place(x=280,y=410)

    exitbtn = Button(m_img, command=lambda:exit(), border=0)
    img4 = PhotoImage(file='./guiresources/exit.png')
    exitbtn.config(image=img4)
    exitbtn.place(x=400,y=410)

    m_img.mainloop()


refpath = './resources/REF/'
testpath = './resources/TEST/'

db = load_database() #load db data
reset = True
open()

while reset:
    matches = []
    counter = 0
    fn = ''

    menu()
    method()
    img()
