# welcome to my rhythm game

this was written as a favour to a friend who needed a game for a music course
(hi phoenix)

it's written with python 3.8 and pygame 2.0.1

the game is a fairly simple rhythm / touch typing game that can be configured
quite easily by editing config.json

letters come in from the right side of the screen and you press the key as it hits the left side of the screen.

## configuring the game
the configuration options are as follows
* bpm - this one controls the speed of the game (and the reason for using this is because it's supposed to be simple enough to be configured be even a _musician_)
* rhythm_pattern - this one is a list of intervals between the letters. a list of 1s is one letter every beat. a list of 2s is one letter every other beat. don't make the numbers too small or the letters start getting rendered on top of one another
* alphabet - this is the list of letters that can come on the screen. if you're finding the game too hard, you can always make it so you only need to push the letter A.
* runtime - this is the time, in seconds, that the program will run for.

## changing the music
create a new file called game_music.wav just swap the game_music.wav file here for something better than a metronome click. or something worse. i don't care.
