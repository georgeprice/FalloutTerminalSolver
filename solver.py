# fallout terminal solver

import sys
import string
import itertools
import operator
import colorama as col
from colorama import init
init(autoreset=True)

p_words = dict()                # declare the dictionary of passwords on the fallout terminal
un_chosen_words = list()
chosen_words = list()


# ranks words based on how many letters they share with other words
def rank_words():
    print("\n[!] Ranking words based on common characters.")

    # groups words into lists if they share a character in the same position

    groupings = list()                              # declare the list of groupings of words

    # iterate through each character index in a password, then group the passwords which
    for char_i in range(word_length):              # iterate through each character position in the words
        for letter in string.ascii_lowercase:       # iterate through each possible letter

            grouping = list()                       # initialise a grouping of words with matching letters

            for p_word in p_words.keys():           # iterate through each word in the list of passwords

                # if the password's letter is a match, then add to group
                if p_word[char_i] == letter and p_words[p_word] < 0:
                    grouping.append(p_word)

            if len(grouping) > 1:   groupings.append(grouping)  # if two or more words match, then save the grouping

    r_words = dict()                                # declare a dictionary to store the passwords, ranked by score

    for p_word in [p for p in p_words.keys() if p_words[p] < 0]:    # iterate through each unchosen password

        counter = 0

        for grouping in groupings:
            if p_word in grouping: counter += 1

        # the score for a password is the number of characters it shares with another password
        # save the (password, score) value into the dictionary
        r_words[p_word] = counter

    r_words = sorted(r_words.items(), key=operator.itemgetter(1))   # sort into desc score order

    for word in reversed(r_words): print("    > Password "+word[0]+", has shared characters: "+str(word[1]))


def longest_substring():

    lcs_combs = dict()

    for (a, b) in itertools.combinations([p for p in p_words.keys() if p_words[p] < 0], 2):
        counter = 0
        for char_i in range(len(a)):
            if a[char_i] == b[char_i]:
                counter += 1
        lcs_combs[(a, b)] = counter

    for key, value in reversed(sorted(lcs_combs.items(), key=operator.itemgetter(1))):
        if value > 0:
            print ("%s: %s" % (key, value))


# prints out the list of unchosen passwords which could still be the actual password
def print_possible():

    possible_p_words = list()  # define the list of possible passwords

    if len(chosen_words) != 0:

        print("\n[!] Finding possible word matches")

        possible_password = True
        
        # iterate through each word that hasn't been selected yet (and so could be the password)        
        for possible_p_word in un_chosen_words:

            print(" Trying un-chosen word "+possible_p_word)
            
            # iterate through each word that has been chosen and scored so far
            for chosen_p_word in chosen_words:

                score = p_words[chosen_p_word]

                print("     Checking against chosen word "+chosen_p_word+" with score "+str(score))
                
                # if the chosen word has a score greater than zero, then it must contain score number matching chars
                if score > 0:
                    
                    # iterate over all possible sub-strings in the chosen password, which could be the valid chars
                    for substring_i in itertools.permutations([i for i in range(word_length)], score):

                        print("         Trying permutation "+str(substring_i))
                        
                        # iterate through each position in the substring, checking if the possible word matches it
                        for char_i in substring_i:
                            if possible_p_word[char_i] != chosen_p_word[char_i]:
                                possible_password = False
                                break
                                
                        # if the password could be the actual one, based on the
                        if possible_password:
                            break
                            
                # if the 
                else:
                    for char_i in range(len(chosen_p_word)):
                        if possible_p_word[char_i] == chosen_p_word[char_i]:
                            possible_password = False
                            break
            if possible_password:
                possible_p_words.append(possible_p_word)

            print(possible_p_word)

    else:
        print("\n[!] No password attempts have been made yet, so any could be the password!")


# updates the score for each word as input by the user
def score_word():

    print("\n[!] Please enter the word you selected on the terminal.")
    word = ""       # declare the string password (from the possible selection) that is chosen by the user

    while word not in p_words.keys():  # keep prompting for a password choice until a valid one is given

        try:
            word_input = str(input("> Word choice; "))  # take input from the user

            # check that this word hasn't already been scored
            if p_words[word_input] >= 0:
                print ("This word has already been scored.")
            else:
                word = word_input

        except KeyError as k:
            print("This is not a valid choice, please enter a possible password.")
        except NameError as n:
            print("Please write your input as a string, using the ' ' or "+' " " symbols around it.')
        except KeyboardInterrupt as ki:
            print("\nI see that you no longer want to use the terminal solver :(")
            sys.exit(1)

    word_score = int(input("> Score; "))

    if word_score == word_length:
        sys.exit("Congratulations, you've got the password.")

    p_words[word] = word_score


print("\n--- Fallout Terminal Solver --- ")

print("\n[!] Reading in passwords...")

# if no command line arguments are given, then keep prompting for password input
if len(sys.argv) == 1:
    print("Taking passwords as user input")
    p_word_in = " "
    while p_word_in != "":
        p_word_in = str(input("> Password; "))
        p_words[p_word_in] = -1

# if a single command line argument, of a text file is given, then use that
elif len(sys.argv) == 3 and ".txt" in sys.argv[1]:
    print("Reading passwords from a text file")

    with open('p_words.txt', 'r') as file:
        for x in range(int(sys.argv[2])):
            file.readline()
        for word in file.readline().split(" "):
            p_words[str(word).replace("\n", "")] = - 1
        file.close()

# otherwise, use the command line arguments as the passwords
else:
    print("Taking passwords from command line arguments")
    for p_word in sys.argv[1:]:
        p_words[p_word] = -1

print("[!] Passwords ; "+str(p_words.keys()))

word_length = len(list(p_words.keys())[0])

while True:
    un_chosen_words = str([p for p in p_words.keys() if p_words[p] < 0])
    chosen_words = str([(p, p_words[p]) for p in p_words if p_words[p] >= 0])
    print("\n[!] Possible Words: " + un_chosen_words)
    print("[!] Chosen Words: "+chosen_words)

    rank_words()
    print_possible()
    longest_substring()
    score_word()
