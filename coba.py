import cv2
import numpy as np
import scipy
from scipy.misc import imread
from tkinter import *
from PIL import ImageTk, Image
import pickle
import random
import os
import matplotlib.pyplot as plt


# Feature extractor
def extract_features(image_path, vector_size=24):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    # crop img 300x300
    image = image[0:300, 0:300]

    alg = cv2.KAZE_create()
    # keypoints
    keypoints = alg.detect(image)
    keypoints = sorted(keypoints, key=lambda x: -x.response)[:vector_size]
    keypoints, dsc = alg.compute(image, keypoints)
    dsc = dsc.flatten()
    # Making descriptor of same size
    # Descriptor vector size is 64
    needed_size = (vector_size * 64)
    if dsc.size < needed_size:
        # if we have less the 32 descriptors then just adding zeros at the
        # end of our feature vector
        dsc = np.concatenate([dsc, np.zeros(needed_size - dsc.size)])

    return dsc


def batch_extractor(images_path, pickled_db_path="features.pck"):
    files = []

    folders = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]
    for subfolder in folders:
        files += [os.path.join(subfolder, p) for p in sorted(os.listdir(subfolder))]

    result = {}
    i = 1
    for f in files:
        print(str(100*i/len(files))[:5]+'%')
        i += 1
        name = f.split('/')[-1].lower()
        result[name] = extract_features(f)

    # simpan data hasil ekstraksi ke file pickle external
    with open(pickled_db_path, 'wb') as fp:
        pickle.dump(result, fp)

def show_img(path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    img = img[0:300, 0:300]
    cv2.imshow(path,img)
    cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # plt.imshow(img)
    # plt.show()

def cosdist(v1, v2):
    dotpro = np.sum(np.multiply(v1,v2))

    norm1 = np.sum(np.square(v1))
    norm1 = np.sqrt(norm1)

    norm2 = np.sum(np.square(v2))
    norm2 = np.sqrt(norm2)

    cosdis = 1-dotpro/(norm1*norm2)

    return cosdis

def eucdist(v1, v2):
    # v1 = [(x1-y1)^2, (x2-y2)^2, (x3-y3)^2, (x4-y4)^2]
    v1 = np.square(np.subtract(v2,v1))
    edis = np.sum(v1)
    edis = np.sqrt(edis)

    return edis


def load_database(pickled_db_path="features.pck"):
    with open(pickled_db_path, "rb") as fp:
        data = pickle.load(fp)

    # return a dictionary
    return data.items()

def matching(imgpath, db, cosine=True, top=5):
    imgvec = extract_features(imgpath)
    tuplearr = []

    for k, v in db:
        if(cosine):
            dist = cosdist(imgvec, v)
        else:
            dist = eucdist(imgvec, v)

        tuplearr.append((k,dist))

    return sorted(tuplearr, key=lambda x: x[1])[:top]


def pic_name(path):
    return path.split('\\')[0].split('/')[-1][5:]

def run():

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
    
    m_open.after(1500, m_open.destroy) #tampil sebentar
    m_open.mainloop()


    # untuk menu utama : random atau pilih foto
    m_menu = Tk()
    m_menu.title('M U K A K U K A M U') #engga keliatan krn frame windowsnya dihapus wkwk
    m_menu.wm_iconbitmap('./guiresources/icon.ico') #engga keliatan krn frame windowsnya dihapus wkwk
    m_menu.geometry('350x350+350+200')
    m_menu.resizable(0,0)
    m_menu.overrideredirect(1)

    main_msg = "\nSelidikilah kemiripan mukamu di MUKAKUKAMU!\nYou can pick your photo OR we can choose it for you!\n" 
    m_message = Message(m_menu, text=main_msg, font=("Montserrat",12))
    m_message.pack()
        
    random1 = Button(m_menu, command=m_menu.destroy) 
    img1 = PhotoImage(file = "./guiresources/opt1.png") #file path disesuaikan
    random1.config(image=img1)
    random1.pack()
        
    random2 = Button(m_menu, command=m_menu.destroy )
    img2 = PhotoImage(file = "./guiresources/opt2.png") #file path disesuaikan
    random2.config(image=img2)
    random2.pack()

    m_menu.mainloop()

    # menu ecluidean dan cosine
    m_method = Tk()
    m_method.title('M U K A K U K A M U')
    m_method.wm_iconbitmap('./guiresources/icon.ico')
    m_method.geometry('350x350+500+200')

    msg_method = "\nPilih metode yang Anda inginkan\n"
    m_method.message = Message(m_method, text=msg_method,font=("Montserrat",12))
    m_method.message.pack()

    euc_button = Button(m_method, command=m_method.destroy)
    img3 = PhotoImage(file="./guiresources//euc.png")
    euc_button.config(image=img3)
    euc_button.pack()

    cos_button = Button(m_method, command=m_method.destroy)
    img4 = PhotoImage(file="./guiresources//cos.png")
    cos_button.config(image=img4)
    cos_button.pack()

    m_method.mainloop()

    images_path = 'resources/PINS/'

    files = []

    folders = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]
    for subfolder in folders:
        files += [os.path.join(subfolder, p) for p in sorted(os.listdir(subfolder))]
    # files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]
    # getting 3 random images 
    sample = random.sample(files, 1)
    # sample = ['resources/saya.jpg'];
    # batch_extractor(images_path)
    # print(sample)
    
    db = load_database()
    
    for s in sample:
        print()
        # print('Query image ==========================================')
        show_img(s)
        # names, match = ma.match(s, topn=2)
        matches = matching(s, db, top=2, cosine=True)
        print(pic_name(s).lower())
        # print('Result images ========================================')
        for i in range(1,2):
            print('Match %s' % (matches[i][1]))
            print(pic_name(os.path.join(images_path, matches[i][0])).lower())
            show_img(os.path.join(images_path, matches[i][0]))
                # break;    

    
run()