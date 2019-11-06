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
    # untuk opening 
    m_open = Tk()
    m_open.overrideredirect(1) #menghapus frame windows
    m_open.geometry('350x350+500+200')
    logo_path = './guiresources/title_logo.png'
    img = PhotoImage(file=logo_path)
    panel = Label(m_open, image = img)
    panel.pack()

    open_text = "M U K A K U K A M U"
    m_open.message = Message(m_open, text=open_text, font=("Montserrat",20), width=350)
    m_open.message.pack()

    m_open.after(900, m_open.destroy) #tampil sebentar
    m_open.mainloop()

def menu():
    global v
    global fn
    global m_open
    global m_menu
    global is_continue

    is_continue = False

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
        return './' + fn[fn.find('resources'):] #relpath

    def choose_img_option(choose=True):
        global fn
        global is_continue
        if(choose):
            fn = chooseimg()
            if(fn == ''):
                return
        else:
            fn = chooserandom()
        is_continue = True
        m_menu.destroy()

    # untuk menu utama : random atau pilih foto
    m_menu = Tk()
    m_menu.title('M U K A K U K A M U')
    m_menu.wm_iconbitmap('./guiresources/icon.ico')
    m_menu.geometry('350x350+500+200')
    m_menu.resizable(0,0)

    logo_path = './guiresources/title_logo.png' #path diseuaikan
    img = PhotoImage(file=logo_path)
    panel = Label(m_menu, image = img)

    backimg = PhotoImage(file='./guiresources/m_back.png')
    Label(m_menu, image=backimg).pack()

    #button : choose image
    c_img = Button(m_menu, command=lambda:choose_img_option(True), border=0,bg='#e5e0d9') 
    img1 = PhotoImage(file = "./guiresources/opt1.png") #file path disesuaikan
    c_img.config(image=img1)
    c_img.place(x=70, y=150)

    #button : randomize
    r_img = Button(m_menu, command=lambda:choose_img_option(False), border=0,bg='#e5e0d9')
    img2 = PhotoImage(file = "./guiresources/opt2.png") #file path disesuaikan
    r_img.config(image=img2)
    r_img.place(x=70, y=220)

    m_menu.mainloop()

def method():
    global fn
    global v
    global matches
    global maximg
    global is_continue

    is_continue = False

    def next():
        global is_continue
        is_continue = True
        m_method.destroy()

    # windows untuk meminta input metode metriks dan nilai threshold
    m_method = Tk()
    m_method.geometry('350x350+500+200')
    m_method.title('M U K A K U K A M U')

    mth_bg = PhotoImage(file='./guiresources/m_choosemethod.png')
    Label(m_method, image=mth_bg).pack()

    v=IntVar()
    v.set(1)

    Radiobutton(m_method, text="Euclidean Distance", padx = 50, variable=v, value=1, font=("Montserrat",10),bg='#e5e0d9').place(y = 130)
    Radiobutton(m_method, text="Cosine Similarity", padx = 50, variable=v, value=2, font=("Montserrat",10),bg='#e5e0d9').place(y = 150)
    m_method.wm_iconbitmap('./guiresources/icon.ico')
    m_method.resizable(0,0)

    def_thres = StringVar(m_method)
    def_thres.set('10')

    t_value = Spinbox(m_method, from_=1 ,to=20,textvariable=def_thres)
    t_value.place(x=60, y = 220)

    ok = Button(m_method, command=lambda:next(), border=0 ,bg='#e5e0d9')
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
    global is_continue

    is_continue = False

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
        global is_continue
        reset = True
        is_continue = True
        m_img.destroy()

    def exit():
        global reset
        reset = False
        m_img.destroy()

    # windows yang menampilkan image (pilihan dan hasil uji)
    m_img = Tk()
    m_img.title('M U K A K U K A M U')
    m_img.geometry('800x450+200+150')
    m_img.wm_iconbitmap('./guiresources/icon.ico')
    m_img.resizable(0,0)

    # background windows image
    match_bg = PhotoImage(file='./guiresources/matchpage.png')
    Label(m_img, image=match_bg).pack()

    #foto yang ingin diuji
    canvas1 = Canvas(m_img, width = 300, height = 300,bd=0, highlightthickness=0,bg='#e5e0d9')
    canvas1.place(x=50,y=50)
    img1 = ImageTk.PhotoImage(Image.open(fn))
    imgArea2 = canvas1.create_image(20,20, anchor=NW, image=img1)

    personname1 = fn.split('/')[3].split('\\')[0]
    l_name1 = Label(m_img, text=personname1, font=("Montserrat", 10),bg='#e5e0d9')
    l_name1.place(x=150, y=35)

    #hasil uji, ditampilkan sebanyak nilai threshold
    canvas2 = Canvas(m_img, width = 300, height = 300,bd=0, highlightthickness=0,bg='#e5e0d9')
    canvas2.place(x=400,y=50)
    img2 = ImageTk.PhotoImage(Image.open(refpath+matches[counter][0]))
    imgArea2 = canvas2.create_image(20,20, anchor=NW, image=img2)      

    personname2 = (refpath+matches[counter][0]).split('/')[3].split('\\')[0]
    l_name2 = Label(m_img, text=personname2, font=("Montserrat", 10),bg='#e5e0d9')
    l_name2.place(x=500, y=35)

    # button prev dan next
    bt1 = Button(m_img, command=lambda:changeimg(matches, pos=True), state=NORMAL,bg='#e5e0d9',bd=0)
    bt2 = Button(m_img, command=lambda:changeimg(matches, pos=False), state=DISABLED,bg='#e5e0d9',bd=0)
    
    imgbt1 = PhotoImage(file='./guiresources/nextbtn.png')
    bt1.config(image=imgbt1)
    imgbt2 = PhotoImage(file='./guiresources/prevbtn.png')
    bt2.config(image=imgbt2)
    
    bt1.place(x=590,y=370) # button next image
    bt2.place(x=500,y=370) # button previous image

    if counter == maximg-1:
        bt1.configure(state=DISABLED)
    if counter == 0:
        bt2.configure(state=DISABLED)

    # menunjukkan foto ke berapa
    l_count = Label(m_img, text="1", font=("Montserrat", 11),bg='#e5e0d9')
    l_count.place(x=555,y=370)

    # kembali ke menu awal
    backhome = Button(m_img, command=lambda:ret2home(), border=0,bg='#e5e0d9')
    img5 = PhotoImage(file='./guiresources/reset.png')
    backhome.config(image=img5)    
    backhome.place(x=40,y=400)

    # keluar program
    exitbtn = Button(m_img, command=lambda:exit(), border=0,bg='#e5e0d9')
    img4 = PhotoImage(file='./guiresources/exit.png')
    exitbtn.config(image=img4)
    exitbtn.place(x=660,y=400)

    m_img.mainloop()


refpath = './resources/REF/'
testpath = './resources/TEST/'

db = load_database() #load db data
reset = True
is_continue = True
open()

while reset:
    matches = []
    counter = 0
    fn = ''

    if(is_continue):
        menu()
    if(is_continue):
        method()
    if(is_continue):
        img()
