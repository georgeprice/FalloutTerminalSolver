import sys
import string
import itertools
import operator

p_words = dict()                # declare the dictionary of (password => matching characters)
word_length = len(sys.argv[1])  # get the length of the passwords

for p_word in sys.argv[1:]:
    p_words[string.lower(p_word)] = -1  # setup the dictionary, using the arguments provided

# ranks words based on how many letters they share with other words - more common words = more info deduced from result
def rank_words():
    print("\n[!] Ranking words based on common characters.")

    groupings = list()                              # declare the list of groupings of words

    for char in range(0, word_length):              # iterate through each character position in the words
        for letter in string.ascii_lowercase:       # iterate through each possible letter
            grouping = list()                       # initialise a grouping of words with matching letters

            for p_word in p_words.keys():           # iterate through each word in the list of passwords

                # if the password's letter is a match, then add to group
                if p_word[char] == letter and p_words[p_word] < 0:
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

    for (a,b) in itertools.combinations([p for p in p_words.keys() if p_words[p] < 0], 2):
        counter = 0
        for char_i in range(len(a)):
            if a[char_i] == b[char_i]:
                counter += 1
        lcs_combs[(a,b)] = counter

    for key, value in reversed(sorted(lcs_combs.items(), key=operator.itemgetter(1))):
        print ("%s: %s" % (key, value))


# prints out the list of unchosen passwords which could still be the actual password
def print_possible():

    unchosen_p_words = [p for p in p_words.keys() if p_words[p] < 0]  # define the list of unchosen passwords
    chosen_p_words = [(p, p_words[p]) for p in p_words if p_words[p] >= 0]  # define the list of chosen passwords
    possible_p_words = list()  # define the list of possible passwords

    if len(chosen_p_words) != 0:

        print("\n[!] Finding possible word matches")


        possiblePassword = True
        
        # iterate through each word that hasn't been selected yet (and so could be the password)        
        for possible_p_word in unchosen_p_words:

            print(" Trying unchosen word "+possible_p_word)
            
            # iterate through each word that has been chosen and scored so far
            for chosen_p_word, score in chosen_p_words:

                print("     Checking against chosen word "+chosen_p_word+" with score "+str(score))
                
                # if the chosen word has a score greater than zero, then it must contain score number matching chars
                if score > 0:
                    
                    # iterate over all possible substrings in the chosen password, which could be the valid chars
                    for substring_i in itertools.permutations([i for i in range(word_length)], score):

                        print("         Trying permutation "+str(substring_i))
                        
                        # iterate through each position in the substring, checking if the possible word matches it
                        for char_i in substring_i:
                            if possible_p_word[char_i] != chosen_p_word[char_i]:
                                possiblePassword = False
                                break
                                
                        # if the password could be the actual one, based on the
                        if possiblePassword:
                            break
                            
                # if the 
                else:
                    for char_i in range(len(chosen_p_word)):
                        if possible_p_word[char_i] == chosen_p_word[char_i]:
                            possiblePassword = False
                            break
            if possiblePassword:
                possible_p_words.append(possible_p_word)


        '''

        for possible_p_word in unchosen_p_words:

            p_word_match_flag = True

            for chosen_p_word, score in chosen_p_words:

                if score > 0:
                    for valid_substring_i in itertools.permutations([i for i in range(0, word_length)], score):

                        sub_match_flag = True
                        for valid_char in valid_substring_i:

                            if possible_p_word[valid_char] != chosen_p_word[valid_char]:
                                sub_match_flag = False
                                break

                        if sub_match_flag:
                            break
                else:

                    sub_match_flag = True

                    for char_i in range(0, len(chosen_p_word)):
                        if possible_p_word[char_i] == chosen_p_word[char_i]:
                            sub_match_flag = False
                            break


                p_word_match_flag = sub_match_flag

            if p_word_match_flag:
                possible_p_words.append(possible_p_word)

        '''

        print (possible_p_word)

    else:
        print("\n[!] No password attempts have been made yet, so any could be the password!")

# updates the score for each word as input by the user
def score_word():

    print("\n[!] Please enter the word you selected on the terminal.")
    word = ""       # declare the string password (from the possible selection) that is chosen by the user

    while(word not in p_words.keys()):  # keep prompting for a password choice until a valid one is given

        try:
            word_input = str(input("> Word choice; "))  # take input from the user

            print (word_input)

            # check that this word hasn't already been scored
            if p_words[word_input] >= 0:          print ("This word has already been scored.")
            else:                                 word = word_input

        except KeyError as k:
            print("This is not a valid choice, please enter a possible password.")
        except NameError as n:
            print("Please write your input as a string, using the ' ' or "+' " " symbols around it.')
        except KeyboardInterrupt as ki:
            print("\nI see that you no longer want to use the terminal solver :(")
            sys.exit(1)

    word_score = int(input("> Score; "))

    if word_score == word_length: sys.exit("Congratulations, you've got the password.")

    p_words[word] = word_score

print("\n--- Fallout Terminal Solver --- ")

while(True):
    print("\n[!] Possible Words: "+str([p for p in p_words.keys() if p_words[p] < 0]))
    print("[!] Chosen Words: "+str([(p, p_words[p]) for p in p_words if p_words[p] >= 0]))

    rank_words()
    print_possible()
    longest_substring()
    score_word()
