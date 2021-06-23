from tkinter import messagebox, Button, Tk
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy 
import turtle


def init_data():
    Base = declarative_base()
    engine = create_engine('sqlite:////home/hyx/Computer/database/database/video_share_platform.db')
    Base.metadata.create_all(engine)

    user_to_video = Table(
            "user_to_video",
            base.metadata,
            Column("user_id",ForeignKey("user.user_id")),
            Column("video_id",ForeignKey("video.video_id")),
            )

    video_to_comment = Table(
            "video_to_comment ",
            base.metadata,
            Column("video_id",ForeignKey("video.video_id")),
            Column("comment_id",ForeignKey("comment.comment_id")),
            )

    user_to_comment = Table(
            "user_to_comment ",
            base.metadata,
            Column("user_id",ForeignKey("user.user_id")),
            Column("comment_id",ForeignKey("comment.comment_id")),
            )

    class user_id(Base):
        __tablename__ = "user"
        user_id = Column(Integer,primary_key=True)
        user_name = Column(String)
        user_passwd = Colmn(String)

#should return user_id
def register():
    pass
def log_in(user_name,passwd):
    pass

def log_out():
    return True

def upload_video():
    window = Tk()
    window.title("service")
    window.geometry('400x200')
    logout = Button(text="log out", command=log_out).pack()
    window.mainloop()

def search_video():
    pass
def my_video_list():
    pass
def upload_comment():
    pass
def download_vides_and_comment():
    pass
def withdraw_comment():
    pass
def delete_videos():
    pass

#return service_type
def service_list():
    logout = False
    while not logout:
        window = Tk()
        window.title("service")
        window.geometry('400x200')
        Button(text="upload_video", command=upload_video).pack()
        Button(text="search_video", command=search_video).pack()
        Button(text="watch_video", command=download_vides_and_comment).pack()
        Button(text="my_video", command=my_video_list).pack()
        Button(text="log out", command=log_out).pack()
        window.mainloop()
        window.destroy()
    

service_list()

def user_interface():
    user_name = turtle.textinput("login","username")
    passwd = turtle.textinput("login","username")
    user_id = login(user_name,passwd)
    if user_id == None:
        messagebox.showerror("login_fail","wrong user_name or password")
    else:
        service_list()



    

def main():
    engine = sqlalchemy.create_engine("sqlite:////home/hyx/Computer/database/database/video_share_platform.db")
    session_schma = sessionmaker(engine)
    session_schma.configure(bind = engine)
    session = session_schma()
    user_interface()


