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

            # iterate through each word in the list of passwords
            for p_word in p_words.keys():

                # if the password's letter is a match, then add to group
                if p_word[char_i] == letter and p_words[p_word] < 0:
                    grouping.append(p_word)

            if len(grouping) > 1:
                groupings.append(grouping)  # if two or more words match, then save the grouping

    r_words = dict()  # declare a dictionary to store the passwords, ranked by score

    for p_word in [p for p in p_words.keys() if p_words[p] < 0]:  # iterate through each unchosen password

        counter = 0

        for grouping in groupings:
            if p_word in grouping:
                counter += 1

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


# for each un-chosen word, find a set of substrings that satisfy each chosen password, then check they don't contradict
def print_possible():

    possible_p_words = []   # define the list of possible passwords

    # if some passwords have been chosen, then we can determine valid and invalid ones
    if len(chosen_words) != 0:

        print("\n" + Fore.BLUE + "[!] Finding possible word matches" + Style.RESET_ALL)

        # iterate over each password that hasn't been checked yet
        for possible_p_word in un_chosen_words:

            print(Fore.BLUE + " > Trying un-chosen word " + possible_p_word + Style.RESET_ALL)

            # define a set of matching substring sets, which contain a list of matching substrings for each chosen word
            matching_substring_sets = []

            # iterate over each chosen word, and its number of correct characters
            for word, score in chosen_words:

                matching_substring_set = []  # define a list of substrings of possible_p_word that pass "word"

                print(Fore.BLUE + "     > Checking against chosen word " + word + " with score " + str(
                    score) + Style.RESET_ALL)

                # matching password choices which a non negative score, and so contain a valid substring
                if score > 0:

                    # iterate through all possible char positions which could be the valid substring
                    for substring_i in itertools.permutations(range(word_length), score):

                        possible_password = True    # define a boolean value, to specify if it is a valid password

                        # iterate through each position in the substring, checking if the possible word matches it
                        for char_i in substring_i:

                            # if the characters in that position contradict, then it isn't a valid substring
                            if possible_p_word[char_i] != word[char_i]:
                                possible_password = False
                                break

                        # if we have found a satisfying substring, then we need to get a string value for it
                        if possible_password:

                            substring = ""  # define an empty string which will hold the substring

                            # iterate through each index in the possible password string
                            for possible_p_word_i in range(len(possible_p_word)):

                                # if this index is in the substring, then add the char in that index
                                if possible_p_word_i in substring_i:
                                    substring += possible_p_word[possible_p_word_i]

                                # otherwise, we don't care what character it is so just add an underscore
                                else:
                                    substring += "_"

                            print(Fore.GREEN + "    Matching substring: "+substring)

                            # if the substring isn't the same as another substring we found, then add it to our list
                            if substring not in matching_substring_set:
                                matching_substring_set.append(substring)

                #  otherwise, the password's score is 0 and so it should not match a possible password in any position
                else:
                    possible_password = True    # define a boolean value, to specify if it is a valid password

                    # iterate through each index in the word
                    for char_i in range(len(word)):

                        # if the characters match in this position, then we know it can't be a valid password
                        if possible_p_word[char_i] == word[char_i]:
                            possible_password = False   # update the boolean flag
                            break

                    # this is a valid password as it doesn't match the 0-scored password in any position
                    if possible_password:
                        matching_substring_set.append("".join("_" for x in range(word_length)))

                # add the list of passing substrings for this chosen and unchosen password combination
                matching_substring_sets.append(matching_substring_set)

            # now, we have a list of passing substrings for each chosen (and scored) password
            # so we must now find a set of substrings, one from each list of passing substrings, which don't contradict
            # therefore, the possible password satisfies all the scored passwords and so COULD be a password

            possible_password = True    # define a boolean value, to specify if it is a valid password

            # iterate through each set of passing substrings for a given password
            for subset in matching_substring_sets:

                # if there are no passing substrings for a given password, then this password isn't possible
                if len(subset) == 0:
                    possible_password = False

            # if there are words to check...
            if possible_password:
                for initial_substring in matching_substring_sets[0]:
                    if p_word_recurse(initial_substring, matching_substring_sets[1:]):
                        possible_p_words.append(possible_p_word)
                        break

    print(Fore.GREEN + ", ".join(possible_p_words) + " are possible passwords")


def p_word_recurse(current_string, substring_lists):
    if len(substring_lists) == 0:
        return True
    elif len(substring_lists[0]) == 0:
        return False
    else:
        for word in substring_lists[0]:
            branching_substring = True

            # check the substrings don't contradict each other, iterate through each char in the substrings
            for char_i in range(len(current_string)):

                # print(Fore.BLUE + current_string[char_i] + " -> " + word[char_i])

                if word[char_i] != current_string[char_i] and \
                        not (word[char_i] != "_" or current_string != "_"):
                    branching_substring = False
                    break

            if branching_substring:
                if len(substring_lists) == 1:
                    return True
                elif p_word_recurse(current_string, substring_lists[1:]):
                    return True


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
        return False

    p_words[word] = word_score

    return True


if __name__ == "__main__":

    print("\n--- Fallout Terminal Solver --- ")

    print("\n" + Fore.BLUE + "[!] Reading in passwords..." + Style.RESET_ALL)

    # if no command line arguments are given, then keep prompting for password input
    if len(sys.argv) == 1:
        print("Taking passwords as user input")

        p_word_in = str(input("> Password; ")).strip()

        while p_word_in != "":
            p_words[p_word_in] = -1
            p_word_in = str(input("> Password; ")).strip()

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

    cant_stop_wont_stop_flag = True

    while cant_stop_wont_stop_flag:
        un_chosen_words = [p for p in p_words.keys() if p_words[p] < 0]
        chosen_words = [(p, p_words[p]) for p in p_words if p_words[p] >= 0]
        print("\n" + Fore.GREEN + "[!] Possible Words: {}".format(", ".join(un_chosen_words)) + Style.RESET_ALL)
        print(Fore.RED + "[!] Chosen Words: {}".format(
            ", ".join([word + " " + str(score) for word, score in chosen_words])) + Style.RESET_ALL)

        rank_words()
        print_possible()
        cant_stop_wont_stop_flag = score_word()

    deinit()
