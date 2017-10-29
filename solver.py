# fallout terminal solver

import itertools
import operator
import sys

from colorama import Style, Fore
from colorama import init

# Colorama colour conventions
# Blue - Info
# Yellow - Warning
# Red - Error / Certain non-password
# Green - Possible password

init(autoreset=True)

p_words = {}  # declare the dictionary of passwords on the fallout terminal
un_chosen_words = []
chosen_words = []


# ranks words based on how many letters they share with other words
def rank_words():
    print("\n" + Fore.BLUE + "[!] Ranking words based on common characters." + Style.RESET_ALL)

    # groups words into lists if they share a character in the same position

    groupings = []  # declare the list of groupings of words

    # iterate through each character index in a password, then group the passwords which
    for char_i in range(word_length):  # iterate through each character position in the words
        for letter in [chr(x) for x in range(97, 123)]:  # iterate through each possible letter

            grouping = []  # initialise a grouping of words with matching letters

            for p_word in p_words.keys():  # iterate through each word in the list of passwords

                # if the password's letter is a match, then add to group
                if p_word[char_i] == letter and p_words[p_word] < 0:
                    grouping.append(p_word)

            if len(grouping) > 1:   groupings.append(grouping)  # if two or more words match, then save the grouping

    r_words = dict()  # declare a dictionary to store the passwords, ranked by score

    for p_word in [p for p in p_words.keys() if p_words[p] < 0]:  # iterate through each unchosen password

        counter = 0

        for grouping in groupings:
            if p_word in grouping: counter += 1

        # the score for a password is the number of characters it shares with another password
        # save the (password, score) value into the dictionary
        r_words[p_word] = counter

    r_words = sorted(r_words.items(), key=operator.itemgetter(1))  # sort into desc score order

    for word in reversed(r_words):
        print(Fore.BLUE + "    > Password " + word[0] + ", has shared characters: " + str(word[1]) + Style.RESET_ALL)


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
            print(Fore.BLUE + "{}: {}".format(key, value) + Style.RESET_ALL)


def print_possible_alt():

    possible_p_words = []   # define the list of possible passwords

    if len(chosen_words) != 0:  # if some passwords have been chosen, then we can determine valid and invalid ones

        print("\n" + Fore.BLUE + "[!] Finding (alt) possible word matches" + Style.RESET_ALL)

        for possible_p_word in un_chosen_words: # iterate over each password that hasn't been checked yet

            print(Fore.BLUE + " Trying un-chosen word " + possible_p_word + Style.RESET_ALL)

            # define a set of matching substring sets, which contain a list of matching substrings for each chosen word
            matching_substring_sets = []

            for word, score in chosen_words:    # iterate over each chosen word, and its number of correct characters

                matching_substring_set = []  # define a list of substrings of possible_p_word that pass "word"

                print(Fore.BLUE + "     Checking against chosen word " + word + " with score " + str(
                    score) + Style.RESET_ALL)

                if score > 0:

                    for substring_i in itertools.permutations(range(word_length), score):

                        possible_password = True

                        # iterate through each position in the substring, checking if the possible word matches it
                        for char_i in substring_i:
                            # print(char_i)
                            if possible_p_word[char_i] != word[char_i]:
                                # print(possible_p_word[char_i])
                                # print(word[char_i])
                                possible_password = False
                                break

                        # if the password could be the actual one, based on the
                        if possible_password:
                            substring = ""
                            for possible_p_word_i in range(len(possible_p_word)):
                                if possible_p_word_i in substring_i:
                                    substring += possible_p_word[possible_p_word_i]
                                else:
                                    substring += "_"
                            print(Fore.GREEN + "    Matching substring: "+substring)
                            if substring not in matching_substring_set:
                                matching_substring_set.append(substring)

                else:
                    possible_password = True
                    for char_i in range(len(word)):
                        if possible_p_word[char_i] == word[char_i]:
                            possible_password = False
                            break
                    if possible_password:
                        matching_substring_set.append("".join("_" for x in range(word_length)))

                matching_substring_sets.append(matching_substring_set)

            possible_password = True

            for subset in matching_substring_sets:
                if len(subset) == 0:
                    possible_password = False

            def recurse(current_string, substring_lists):
                print(Fore.BLUE + "RECURSE: " + current_string + ", " + str(substring_lists))
                if len(substring_lists) == 0:
                    return True
                else:
                    for word in substring_lists[0]:
                        print(Fore.BLUE + "  Attempting to branch into substring;" + word)

                        branching_substring = True

                        # check the substrings don't contradict each other, iterate through each char in the substrings
                        for char_i in range(len(current_string)):

                            # print(Fore.BLUE + current_string[char_i] + " -> " + word[char_i])

                            if word[char_i] != current_string[char_i] and \
                                    not (word[char_i] != "_" or current_string != "_"):
                                branching_substring = False
                                print(Fore.BLUE + "FAIL")
                                break

                        if branching_substring:
                            print(Fore.BLUE + "  Found a fitting substring;" + word)
                            if len(substring_lists) == 1 or recurse(current_string, substring_lists[1:]):
                                return True

            # if there are words to check...
            if possible_password:
                # print(matching_substring_sets)
                possible_password = False
                for initial_substring in matching_substring_sets[0]:
                    if recurse(initial_substring, matching_substring_sets[1:]):
                        possible_password = True
                        break

            if possible_password:
                print(Fore.GREEN + possible_p_word + " is a valid possible password")
            else:
                print(Fore.RED + possible_p_word + " is not a valid possible password")



# prints out the list of unchosen passwords which could still be the actual password
def print_possible():
    possible_p_words = []  # define the list of possible passwords

    if len(chosen_words) != 0:

        print("\n" + Fore.BLUE + "[!] Finding possible word matches" + Style.RESET_ALL)

        # iterate through each word that hasn't been selected yet (and so could be the password)        
        for possible_p_word in un_chosen_words:

            print(Fore.BLUE + " Trying un-chosen word " + possible_p_word + Style.RESET_ALL)

            # iterate through each word that has been chosen and scored so far
            for word, score in chosen_words:

                score = p_words[word]

                print(Fore.BLUE + "     Checking against chosen word " + word + " with score " + str(
                    score) + Style.RESET_ALL)

                # if the chosen word has a score greater than zero, then it must contain score number matching chars
                if score > 0:

                    # iterate over all possible sub-strings in the chosen password, which could be the valid chars
                    for substring_i in itertools.permutations(range(word_length), score):
                        possible_password = True

                        # print("         Trying permutation " + str(substring_i) + " on " + word + " and " +
                        # possible_p_word)

                        # iterate through each position in the substring, checking if the possible word matches it
                        for char_i in substring_i:
                            # print(char_i)
                            if possible_p_word[char_i] != word[char_i]:
                                # print(possible_p_word[char_i])
                                # print(word[char_i])
                                possible_password = False
                                break

                        # if the password could be the actual one, based on the
                        if possible_password:
                            # print("permutation matched")
                            break

                # if the 
                else:
                    for char_i in range(len(word)):
                        if possible_p_word[char_i] == word[char_i]:
                            possible_password = False
                            break
            if possible_password:
                possible_p_words.append(possible_p_word)

        print(Fore.GREEN + "[!] Possible passwords: " + ", ".join(possible_p_words) + Style.RESET_ALL)

    else:
        print("\n" + Fore.BLUE + "[!] No password attempts have been made yet, so any could be the password!" +
              Style.RESET_ALL)


# updates the score for each word as input by the user
def score_word():
    print("\n" + Fore.BLUE + "[!] Please enter the word you selected on the terminal." + Style.RESET_ALL)
    word = ""  # declare the string password (from the possible selection) that is chosen by the user

    while word not in p_words.keys():  # keep prompting for a password choice until a valid one is given

        try:
            word_input = str(input("> Word choice; "))  # take input from the user

            # check that this word hasn't already been scored
            if p_words[word_input] >= 0:
                print(Fore.YELLOW + "This word has already been scored." + Style.RESET_ALL)
            else:
                word = word_input

        except KeyError as k:
            print(Fore.RED + "This is not a valid choice, please enter a possible password." + Style.RESET_ALL)
        except NameError as n:
            print(
                Fore.RED + "Please write your input as a string, using the ' ' or " + ' " " symbols around it.' + Style.RESET_ALL)
        except KeyboardInterrupt as ki:
            print("\n" + Fore.RED + "I see that you no longer want to use the terminal solver :(" + Style.RESET_ALL)
            sys.exit(1)

    word_score = int(input("> Score; "))

    if word_score == word_length:
        print(Fore.GREEN + "Congratulations, you've got the password." + Style.RESET_ALL)
        sys.exit(0)

    p_words[word] = word_score


print("\n--- Fallout Terminal Solver --- ")

print("\n" + Fore.BLUE + "[!] Reading in passwords..." + Style.RESET_ALL)

# if no command line arguments are given, then keep prompting for password input
if len(sys.argv) == 1:
    print("Taking passwords as user input")
    p_word_in = " "
    while p_word_in != "":
        p_word_in = str(input("> Password; ")).strip()
        p_words[p_word_in] = -1

elif len(sys.argv) == 2:
    print(Fore.RED + "1 or 3 arguments only" + Style.RESET_ALL)
    sys.exit(0)

# if a single command line argument, of a text file is given, then use that
elif len(sys.argv) == 3 and sys.argv[1].endswith(".txt"):
    print(Fore.BLUE + "Reading passwords from a text file" + Style.RESET_ALL)

    with open('p_words.txt', 'r') as file:
        for x in range(int(sys.argv[2])):
            file.readline()
        for word in file.readline().split(" "):
            p_words[str(word).replace("\n", "")] = - 1
        file.close()

# otherwise, use the command line arguments as the passwords
else:
    print(Fore.BLUE + "Taking passwords from command line arguments" + Style.RESET_ALL)
    for p_word in sys.argv[1:]:
        p_words[p_word] = -1

print(Fore.BLUE + "[!] Passwords ; " + str(p_words.keys()) + Style.RESET_ALL)

word_length = len(list(p_words.keys())[0])

while True:
    un_chosen_words = [p for p in p_words.keys() if p_words[p] < 0]
    chosen_words = [(p, p_words[p]) for p in p_words if p_words[p] >= 0]
    print("\n" + Fore.GREEN + "[!] Possible Words: {}".format(", ".join(un_chosen_words)) + Style.RESET_ALL)
    print(Fore.RED + "[!] Chosen Words: {}".format(
        ", ".join([word + " " + str(score) for word, score in chosen_words])) + Style.RESET_ALL)

    rank_words()
    print_possible()
    print_possible_alt()
    longest_substring()
    score_word()

deinit()
