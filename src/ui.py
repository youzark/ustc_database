import PySimpleGUI as sg
import DB as db
import datetime

#this is used to scale the window
#this function init a window and invoke tk func to scale all windows
#and close the window
layout = [[sg.Text('')]]
scaling_window = sg.Window('Window Title', layout, no_titlebar=True, auto_close=False, alpha_channel=0).Finalize()
scaling_window.TKroot.tk.call('tk', 'scaling', 3)
scaling_window.close()

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
        sg.Text("Open video by name")
    ],
    [
        sg.In(size=(25, 1), enable_events=True, key="-open_video_name-"),
        sg.Button("open")
    ],
    [
        sg.Text("your video list")
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(60, 30), key="-private_video_list-"
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
        sg.Text("friend list")
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(60, 10), key="-friend_list-"
        )
    ],
    [
        sg.Text("send add friend message")
    ],
    [
        sg.Text("new friend name"),
        sg.In(size=(25, 1), enable_events=True, key="-add_friend_name-"),
        sg.Button("add")
        ],
    [
        sg.Text("friend invitation list")
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(60, 10), key="-friend_invitation_list-"
        )
    ],
    [
        sg.In(size=(25, 1), enable_events=True, key="-accept_friend_name-"),
        sg.Button("accept")
    ],
    [
        sg.Text(size=(40, 1), key="-new_friend_info-"),
    ],
    [
        sg.Text("delete video")
    ],
    [
        sg.In(size=(25, 1), enable_events=True, key="-delete_video_name-"),
        sg.Button("delete video")
    ],
    [
        sg.Text(size=(40, 1), key="-delete_video_info-"),
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
                # update login user name
                window["-login_reg_status-"].update("login successfully")
                user_name_inst = login_user_name
                window["-user_name_info-"].update(user_name_inst)
                # update login user info : video list
                video_list = db.video_user_query(user_name_inst)
                user_video_list = []
                for video in video_list:
                    user_video = f'{video[0]}  time:{video[2]}'
                    user_video_list.append(user_video)
                window["-private_video_list-"].update(user_video_list)
                # update friend invitation
                message_list = db.message_query(user_name_inst)
                friend_invitation_list = []
                for message in message_list:
                    if message[1][0] == "~":
                        friend_invitation = f'username:{message[0]},time:{message[2]}'
                        friend_invitation_list.append(friend_invitation)
                window["-friend_invitation_list-"].update(friend_invitation_list)
                # update friend list
                friend_list = db.friends_list_query(user_name_inst)
                window["-friend_list-"].update(friend_list)
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

    if event == "open":
        if not user_name_inst == None:
            name = values["-open_video_name-"]
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
            window["-upload_comment_info-"].update("please login first")

    if event == "add":
        if not user_name_inst == None:
            add_friend_name = values["-add_friend_name-"]
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            add_friend_message = f'~{user_name_inst}'
            db.send_email(user_name_inst,add_friend_name,add_friend_message,time)
            window["-new_friend_info-"].update("please wait response")
        else:
            window["-new_friend_info-"].update("please login first")

    if event == "accept":
        if not user_name_inst == None:
            accept_friend_name = values["-accept_friend_name-"]
            message_list = db.message_query(user_name_inst)
            accept_suss = False
            for message in message_list:
                if message[1][0] == "~" and message[0] == accept_friend_name:
                    db.friendship_insert(user_name_inst,accept_friend_name)
                    db.friendship_insert(accept_friend_name,user_name_inst)
                    window["-new_friend_info-"].update("add friend successfully")
                    db.email_delete(message[3])
                    accept_suss = True
            if accept_suss:
                window["-new_friend_info-"].update("wrong user name")
        else:
            window["-new_friend_info-"].update("please login first")

    if event == "delete video":
        if not user_name_inst == None:
            delete_video_name = values["delete_video_name"]
            delete_video_id = db.video_name_query(delete_video_name)[3]
            delete_video_user = db.video_id_query(delete_video_id)[2]
            if delete_video_user == user_name_inst:
                db.video_delete(delete_video_id)
                window["-delete_video_info-"].update("video delete successfully")
            else:
                window["-delete_video_info-"].update("you are not the owner")
        else:
            window["-delete_video_info-"].update("please login first")

window.close()
