import PySimpleGUI as sg
import DB

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
        sg.Text("Search video by name")
    ],
    [
        sg.In(size=(25, 1), enable_events=True, key="-video_name-"),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]

# For now will only show the name of the file that was chosen
video_viewer_column = [
    [
        sg.Text("video path")
    ],
    [
        sg.Text(size=(40, 1), key="-vider_path-")
    ],
    [
        sg.Text("comment")
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
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

window = sg.Window("Image Viewer", layout)

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "login":
        
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(filename=filename)

        except:
            pass

window.close()
