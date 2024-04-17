from customtkinter import *
import cv2
from PIL import Image, ImageTk
from io import BytesIO
import random
import requests
import webbrowser


#creating class for setting up a video as background and playing it in loop. 
class VideoBg:
    def __init__(self, window, video_src):
        self.window = window
        self.video_src = video_src

        self.cap = cv2.VideoCapture(self.video_src)
        self.canvas = CTkCanvas(window, width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()
        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            self.photo = ImageTk.PhotoImage(image=frame)
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0) 
        self.window.after(30, self.update_frame)


root=CTk()
root.geometry('420x595')
root.title('Potter World App')
from CTkMessagebox import CTkMessagebox

#function to switch frames
def switch_frame(frame):
    frame.tkraise()

def aboutPopup():
    CTkMessagebox(title='About the app', message=f"This application explores the Harry potter world. Explore the 7 wonders of the Hp world in this application ", option_1='Let\'s go!')

def infoPopup():
    CTkMessagebox(title='Navigation Info', message=f"To explore books, please click \"Get a Book\" button. It will generate one of the 7 Harry Potter titles. Click the button again to change the book title. Click \"View the Book\" to check the given title's book details", option_1='Let\'s go!', icon='question')


def getBook():
    url = f"https://api.potterdb.com/v1/books"  
    response = requests.get(url)
    data = response.json()

    l_num = random.randint(0, len(data['data']))

   
    book_title = data['data'][l_num]['attributes']['title']
    bookLabel.configure(text=book_title)
    book_name.configure(text=f"Title\t  :  {book_title}")

    bookAuthor = data['data'][l_num]['attributes']['author']
    book_author.configure(text=f"Author\t  :  {bookAuthor}")

    bookDate = data['data'][l_num]['attributes']['release_date']
    book_date.configure(text=f"Date of Release:  {bookDate}")

    bookPages = data['data'][l_num]['attributes']['pages']
    book_pages.configure(text=f"Pages\t  :  {bookPages}")

    bookWiki = data['data'][l_num]['attributes']['wiki']
    from textwrap import wrap
    bookwiki_new = '\n'.join(wrap(bookWiki, width=40))
    book_wiki.configure(text=f": {bookwiki_new}")
    book_wiki.bind('<Button-1>', lambda x:webbrowser.open_new(f"\"{bookWiki}\""))
    
    img_url = data['data'][l_num]['attributes']['cover']
    img_res = requests.get(img_url)
    if img_res.status_code == 200:
        img = CTkImage(Image.open(BytesIO(img_res.content)), size=(212, 303.5))
        cover_label = CTkLabel(home_frame, image=img, text="")
        cover_label.image = (
            img  #keep a reference to the image to prevent garbage collection
        )
        cover_label.place(x=99.5, y=164.7)
        
        #To request and place the cover photo of the selected book in details frame
        img2 = CTkImage(Image.open(BytesIO(img_res.content)), size=(199.8, 286.1))
        cover_label2 = CTkLabel(details_frame, image=img2, text="")
        cover_label2.image = (
            img2  # keep a reference to the image to prevent garbage collection
        )
        cover_label2.place(x=110.1, y=145.6)


    


#main frame for introducing the application
main_frame = CTkFrame(root, width=420, height=595)
main_frame.place(x=0, y=0)

#setting the video as bg for main frame
video_source = "Video assets\hp bg.mp4"
app = VideoBg(main_frame, video_source)

#home frame to display books
home_frame=CTkFrame(root, width=420, height=595)
home_frame.place(x=0, y=0)

#setting the video as bg for home frame
video_source = "Video assets\hp bg2.mp4"
app = VideoBg(home_frame, video_source)


#details_frame to display details of the clicked book
details_frame=CTkFrame(root, width=420, height=595)
details_frame.place(x=0, y=0)

#setting the video as bg for details frame
video_source = "Video assets\hp bg3.mp4"
app = VideoBg(details_frame, video_source)


#buttons on main frame. Explore button switches the frame to home frame. 
aboutbtn = CTkButton(main_frame, text="About", command=aboutPopup ,fg_color="#751807", corner_radius=40, bg_color="#F59F14", text_color="#F59F14", hover_color="#b5250b", font=("Georgia", 20), width=150, height=50)
aboutbtn.place(x=50, y=500)

explorebtn = CTkButton(main_frame, text="Explore", command= lambda:switch_frame(home_frame), fg_color="#751807", corner_radius=40, bg_color="#F59F14", text_color="#F59F14", hover_color="#b5250b", font=("Georgia", 20), width=150, height=50)
explorebtn.place(x=220, y=500)
#button on home frame
viewbtn = CTkButton(home_frame, text=" View the Book ", command=lambda:[switch_frame(details_frame), getBook] ,fg_color="#751807",  bg_color="#F59F14", text_color="#F59F14", hover_color="#b5250b", font=("Georgia", 20), width=150, height=50, corner_radius=0)
viewbtn.place(x=42, y=527.2)

nextbtn = CTkButton(home_frame, text=" Get a book " , command=getBook ,fg_color="#751807",  bg_color="#F59F14", text_color="#F59F14", hover_color="#b5250b", font=("Georgia", 20), width=150, height=50, corner_radius=0)
nextbtn.place(x=220, y=527.2)

bookLabel = CTkLabel(home_frame, text="", font=("Georgia", 14, 'bold'), text_color="#751807", bg_color="#F59F14")
bookLabel.place(x=60, y=470)

book_name =  CTkLabel(details_frame, text="", font=("Georgia", 14), text_color="#751807", bg_color="#F59F14")
book_name.place(x=42, y=444.4)

book_author = CTkLabel(details_frame, text="", font=("Georgia", 14), text_color="#751807", bg_color="#F59F14")
book_author.place(x=42, y=468.6)

book_date = CTkLabel(details_frame, text="", font=("Georgia", 14), text_color="#751807", bg_color="#F59F14")
book_date.place(x=42, y=492.7)

book_pages = CTkLabel(details_frame, text="", font=("Georgia", 14), text_color="#751807", bg_color="#F59F14")
book_pages.place(x=42, y=516.7)

book_wiki = CTkLabel(details_frame, text="", font=("Georgia", 14, UNDERLINE), text_color="#751807", bg_color="#F59F14", )
book_wiki.place(x=120, y=544.8)

wiki_label = CTkLabel(details_frame, text='Wiki',font=("Georgia", 14), text_color="#751807", bg_color="#F59F14" )
wiki_label.place(x=42, y=540.8)

back=CTkImage(Image.open("Image Assets\Previous_icon.png"), size=(40, 40))
backbtn=CTkButton(home_frame, image=back, text='', width=30 , fg_color="#F59F14",  bg_color="#F59F14", hover=False, command=lambda: switch_frame(main_frame))
backbtn.place(x=17.1, y=23.4)
backbtn2=CTkButton(details_frame, image=back, text='', width=30 , fg_color="#F59F14",  bg_color="#F59F14", hover=False, command=lambda: switch_frame(home_frame) )
backbtn2.place(x=17.1, y=23.4)

info=CTkImage(Image.open("Image Assets\q_icon.png"), size=(40, 40))
infobtn=CTkButton(home_frame, image=info, text='', width=30 , fg_color="#F59F14",  bg_color="#F59F14", hover=False, command= infoPopup )
infobtn.place(x=359, y=23.4)

switch_frame(main_frame)
root.mainloop()
