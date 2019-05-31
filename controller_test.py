import pygame
import rtmidi

pygame.init()
midiout = rtmidi.MidiOut()

ports = midiout.get_ports()
midiout.open_port(1)

j = pygame.joystick.Joystick(0)
j.init()
controller_on = 1

print(j.get_numaxes())

button_names = {'0': "SQUARE",
                '1': "X",
                '2': "CIRCLE",
                '3': "TRIANGLE",
                '4': "L1",
                '5': "R1",
                '6': "L2",
                '7': "R2",
                '8': "SHARE",
                '9': "OPTIONS",
                '10': "LEFT ANALOG PRESS",
                '11': "RIGHT ANALOG PRESS",
                '12': "PS4 ON BUTTON",
                '13': "TOUCHPAD PRESS",
                }

button_notes = {'0': 60,
                '1': 62,
                '2': 63,
                '3': 65,
                '4': 60,
                '5': 63,
                '6': 67,
                '7': 68,
                '8': 60,
                '9': 63,
                '10': 65,
                '11': 67,
                '12': 0,
                '13': 1,
                }

current_button_state = {'0': 0,
                        '1': 0,
                        '2': 0,
                        '3': 0,
                        '4': 0,
                        '5': 0,
                        '6': 0,
                        '7': 0,
                        '8': 0,
                        '9': 0,
                        '10': 0,
                        '11': 0,
                        '12': 0,
                        '13': 0,
                    }
previous_button_state = current_button_state.copy()

# returns a dict that is the difference between current and previous state
def get_difference(p, c):
    different_items = {k: c[k] for k in c if k in p and c[k] != p[k]}
    return different_items

# makes current and previous state equal
def update_states(current, previous):
    updates = get_difference(previous, current)
    for k, val in enumerate(updates):
        previous['{}'.format(val)] = updates[val]

# returns a dict that shows which button was pressed and updates the current state
def check_which_button_was_pressed(j, current, previous):
    for i in range(14):
        if j.get_button(i):
            current['{}'.format(i)] = 1
    return get_difference(current,previous)

# returns a dict that shows which button was released and updates the current state
def check_which_button_was_released(j, current, previous):
    for i in range(14):
        if j.get_button(i) == 0 and previous['{}'.format(i)] == 1:
            current['{}'.format(i)] = 0
    return get_difference(current,previous)

# send a midi note, where note is an array of shape (3)
def send_note_on(midiout, note):
    midiout.send_message(note)

# send a midi note with velocity 0, where note is an array of shape (3)
def send_note_off(midiout, note):
    midiout.send_message(note)

# takes input from check_which_button_was_pressed or check_which_button_was_released and returns the notes mapped to the according buttons
def button_to_note(events, button_notes):
    return {k: button_notes[k] for k in events}

def midi_handler(midiout, button_notes, pressed_buttons = 0, released_buttons = 0):
    print(pressed_buttons)
    if pressed_buttons:
        notes_to_be_sent = button_to_note(pressed_buttons, button_notes)
        for note in notes_to_be_sent.values():
            send_note_on(midiout, [0x90,note,60])
    if released_buttons:
        notes_to_be_sent = button_to_note(released_buttons, button_notes)
        for note in notes_to_be_sent.values():
            send_note_on(midiout, [0x90,note,0])

current_axis_val = 0
previous_axis_val = 0

def check_which_axis_changed(j):
    for i in range(6):
        print(j.get_axis(i))


def check_axis_change(current_axis_val, previous_axis_val):
    pass

def run_loop(j, current_button_state, previous_button_state, controller_on, midiout):
    while controller_on:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                pressed_buttons = check_which_button_was_pressed(j, current_button_state, previous_button_state)
                if current_button_state['12'] == 1:
                    controller_on = 0
                midi_handler(midiout, button_notes, pressed_buttons = pressed_buttons)
                update_states(current_button_state, previous_button_state)
                print(current_button_state)
            elif event.type == pygame.JOYBUTTONUP:
                midi_handler(midiout, button_notes, released_buttons = check_which_button_was_released(j, current_button_state, previous_button_state))
                update_states(current_button_state, previous_button_state)
                print(current_button_state)
            if event.type == pygame.JOYAXISMOTION:
                axs = j.get_axis(0)
                if axs > 0.05:
                    midiout.send_message([0xE0, 0, axs*65])
                if axs < -0.05:
                    midiout.send_message([0xE0, 0, 60 - axs*65])
            if event.type == pygame.JOYHATMOTION:
                if event.hat == 0:
                    if event.value == (1, 0):
                        print("right")
                    if event.value == (-1, 0):
                        print("left")
                    if event.value == (0, 1):
                        print("up")
                        for key, val in button_notes.items():
                            button_notes[key] = val + 12
                    if event.value == (0, -1):
                        print("down")
                        for key, val in button_notes.items():
                            button_notes[key] = val - 12




run_loop(j, current_button_state, previous_button_state, controller_on, midiout)
j.quit()
