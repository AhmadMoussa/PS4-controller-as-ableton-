__If this helped you in some way or you find this interesting consider dropping a star, or sending me an email. If you have suggestions for this also consider sending me an email.__

# PS4-controller-as-ableton-
Enables you to use your PS4 controller as a MIDI controller for ableton

## Dependencies
You're gonna have to install two packages:
`pip install pygame`
`pip install rtmidi`

## How it works:

A problem with `pygame` was that it can detect which button was pressed, but it can not tell you which button released (aybe it does, but I couldn't find anything about it). But that can be easily solved by implementing two button states and comparing, to see which button has been released or pressed.

Dict that maps buttons to notes. You can simply change which button triggers which note, by changing the number value that represents that note in MIDI.

## TO-DO:
* Implement button mapping in json file
* Smoothen pitch bend with analogue stick
* Implement vibrato with second analogue stick
* Two button press implementation
* Implement Velocity control with touchpad
* upload demo video
* fix code structure and function/variable names
* think about how this could be useful
