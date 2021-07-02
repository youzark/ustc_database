import PySimpleGUI as sg
import DB as db

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
        sg.In(size=(25, 1), enable_events=True, key="-video_name-"),
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
        sg.In(size=(25, 1), enable_events=True, key="-upload_video_path-"),
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
            values=[], enable_events=True, size=(40, 20), key="-comment_list-"
        )
    ],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(login_column),
        sg.VSeperator(),
        sg.Column(video_viewer_column),
    ]
]

window = sg.Window("short video platform", layout)


# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "login":
        user_passwd = db.ac_query(values["-user_name-"])
        if not user_passwd == None:
            if user_passwd == values["-passwd-"]:
                window["-login_reg_status-"].update("login successfully")
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

window.close()
