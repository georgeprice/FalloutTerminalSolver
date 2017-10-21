# Fallout Terminal Solver
Helps you solve the terminal mini-games from Fallout 3, NV and 4.

## The Terminal Minigame
Given a set of words of the same length, you have 4 guesses to try and find the word that matches the terminal's unique password. With each incorrect guess, you are told the number of characters that this word shares with the password.

## Help solving it
This python script helps keep track of what words the password could be (based on the remaining available words), and the best words to choose.

## Using the script
If you want to be prompted for the words and type them in individually...
``` python
python solver.py
```

If you've got the words present on the terminal handy...
``` python
python solver.py word_a word_b word_c ...
```

If you've got a .txt file of the words...
``` python
python solver.py p_words.txt line_number_with_words
```

## Examples
Here are some examples of videos of people solving the Fallout terminal mini-game, alongwith the words used..

Terminal Difficulty | Link | Words Used
--------------------|------|-----------
Master | https://www.youtube.com/watch?v=Iux-pjzKjYs | processing recreating procession activating complexion descending intentions inevitably frequently equivalent aggressive specialize leaderless worthiness
? | https://www.youtube.com/watch?v=Sa4RUpXgzT4 | shot hurt sell give sure gear sent fire glow week ones sick
? | https://www.youtube.com/watch?v=IFXxm6AOa0U&t=49s | guns lets golf roof juke uses move doom busy late born


