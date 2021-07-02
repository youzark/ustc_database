import PySimpleGUI as sg

# sg.theme('LightBlue1')

# Scaled window
layout = [[sg.Text('')]]
scaling_window = sg.Window('Window Title', layout, no_titlebar=True, auto_close=False, alpha_channel=0).Finalize()
scaling_window.TKroot.tk.call('tk', 'scaling', 4)
scaling_window.close()

# Actual program you want
layout1 = [[sg.Text('Persistent window', key='Text1')],
          [sg.Input(key='-IN-')],
          [sg.Button('Read'), sg.Exit()]]

window = sg.Window('Window that stays open', layout1).Finalize()
print(window.TKroot.tk.call('tk', 'scaling'))
# window.refresh()

while True:                             # The Event Loop
    event, values = window.read()

    print(event, values)
    if event in (None, 'Exit'):
        break

window.close()
