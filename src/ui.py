import PySimpleGUI as sg
import DB as db
import datetime

login_column = [
    [
        sg.Text("username"),
        sg.In(size=(25, 1), enable_events=True, key="-user_name-"),
    ],
    [
        sg.Text("password"),
        sg.In(size=(25, 1), enable_events=True, key="-passwd-"),
    ],
    [
        sg.Button("login"),
        sg.Button("register")
    ],
    [
        sg.Text(size=(40, 1), key="-login_reg_status-")
    ],
    [
        sg.Text("Search video by name")
    ],
    [
        sg.In(size=(25, 1), enable_events=True, key="-search_video_name-"),
        sg.Button("search")
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-video_list-"
        )
    ],
]


# For now will only show the name of the file that was chosen
video_viewer_column = [
    [
        sg.Text("upload video")
    ],
    [
        sg.Text("videoname"),
        sg.In(size=(25, 1), enable_events=True, key="-upload_video_name-"),
    ],
    [
        sg.Text("videopath"),
        sg.In(size=(25, 1), enable_events=True, key="-upload_video_path-"),
    ],
    [
        sg.Text(size=(40, 1), key="-vider_submit_info-")
    ],
    [
        sg.Button("submit")
    ],
    [
        sg.Text("video path")
    ],
    [
        sg.Text(size=(40, 1), key="-video_path-")
    ],
    [
        sg.Text("comment")
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(60, 20), key="-comment_list-"
        )
    ],
    [
        sg.Text("leave your comment")
    ],
    [
        sg.In(size=(25, 1), enable_events=True, key="-upload_comment-"),
    ],
    [
        sg.Button("comment")
    ],
    [
        sg.Text(size=(40, 1), key="-upload_comment_info-")
    ],
]

user_info_column =[
    [
        sg.Text("user name:")
    ],
    [
        sg.Text("please login first",key="-user_name_info-")
    ],
    [
        sg.Text("your video list")
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(60, 20), key="-private_video_list-"
        )
    ],

]
# ----- Full layout -----
layout = [
    [
        sg.Column(login_column),
        sg.VSeperator(),
        sg.Column(video_viewer_column),
        sg.VSeperator(),
        sg.Column(user_info_column)
    ]
]

window = sg.Window("short video platform", layout)


user_name_inst = None
current_open_video_id = None

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == "login":
        login_user_name = values["-user_name-"]
        user_passwd = db.ac_query(login_user_name)
        if not user_passwd == None:
            if user_passwd == values["-passwd-"]:
                window["-login_reg_status-"].update("login successfully")
                user_name_inst = login_user_name
                window["-user_name_info-"].update(user_name_inst)
                video_list = db.video_user_query(user_name_inst)
                user_video_list = []
                for video in video_list:
                    user_video = f'{video[0]}  time:{video[2]}'
                    user_video_list.append(user_video)
                window["-private_video_list-"].update(user_video_list)
        

            else:
                window["-login_reg_status-"].update("wrong password")
        else:
            window["-login_reg_status-"].update("username not exist")
            
    if event == "register":
        user_passwd = db.ac_query(values["-user_name-"])
        if not user_passwd == None:
            window["-login_reg_status-"].update("username already existed")
        else:
            db.ac_insert(values["-user_name-"],values["-passwd-"])
            window["-login_reg_status-"].update("register successfully")

    if event == "submit":
        if not user_name_inst == None:
            name = values["-upload_video_name-"]
            filename = values["-upload_video_path-"]
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db.video_insert(name, filename, user_name_inst, time)
            window["-vider_submit_info-"].update("submit successfully")
        else:
            window["-vider_submit_info-"].update("please login first")

    if event == "search":
        if not user_name_inst == None:
            name = values["-search_video_name-"]
            video_list = db.video_name_query(name)
            window["-video_path-"].update(video_list[0][1])
            current_open_video_id = video_list[0][3]
            comment_list = db.video_comments_query(current_open_video_id)
            show_comment_list = []
            for comment_item in comment_list:
                show_comment = f'{comment_item[1]} by:{comment_item[0]} time:{comment_item[2]}'
                show_comment_list.append(show_comment)
            window["-comment_list-"].update(show_comment_list)
        else:
            window["-vider_submit_info-"].update("please login first")

    if event == "comment":
        if not user_name_inst == None:
            comment = values["-upload_comment-"]
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if not current_open_video_id == None:
                db.video_comments_insert(current_open_video_id,user_name_inst,comment,time)
                window["-upload_comment_info-"].update("upload comment successfully")
            else:
                window["-upload_comment_info-"].update("open a video first")
                

        else:
            window["-vider_submit_info-"].update("please login first")




window.close()
