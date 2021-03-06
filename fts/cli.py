# fallout terminal solver

import fts.helpers.string as string_helper
import sys

from colorama import Style, Fore
from colorama import init, deinit
from fts.helpers.graph import Graph

# Colorama colour conventions
# Blue - Info
# Yellow - Warning
# Red - Error / Certain non-password
# Green - Possible password

init(autoreset=True)


def get_passwords() -> [str]:
    """
    Gets the password from either user input, or from an external file and line selector
    :return: a list of password strings
    """

    print("\n" + Fore.BLUE + "[!] Reading in passwords..." + Style.RESET_ALL)

    passwords = []

    # if no command line arguments are given, then keep prompting for password input
    if len(sys.argv) == 1:

        print("[!] Taking passwords as user input")

        p_word_in = str(input("> Password; ")).strip()

        while p_word_in != "":
            passwords.append(p_word_in)
            p_word_in = str(input("> Password; ")).strip()

    elif len(sys.argv) == 2:
        print(Fore.RED + "[!] 1 or 3 arguments only" + Style.RESET_ALL)
        sys.exit(0)

    # if a single command line argument, of a text file is given, then use that
    elif len(sys.argv) == 3 and sys.argv[1].endswith(".txt"):
        print(Fore.BLUE + "[!] Reading passwords from a text file" + Style.RESET_ALL)

        with open('p_words.txt', 'r') as file:

            for x in range(int(sys.argv[2])):   file.readline()

            passwords = [str(word).replace("\n", "") for word in file.readline().split(" ")]
            file.close()

    # otherwise, use the command line arguments as the passwords
    else:
        print(Fore.BLUE + "[!] Taking passwords from command line arguments" + Style.RESET_ALL)

        passwords = sys.argv[1:]

    return passwords


if __name__ == "__main__":

    print("\n--- Fallout Terminal Solver --- ")

    password_graph = Graph(get_passwords(), string_helper.matching_characters)

    print("[!] Possible passwords = {}".format(password_graph.get_nodes()))

    in_word = " "
    score = 0

    while score != len(in_word) and len(list(password_graph.get_connected_nodes())) > 1:

        in_word = input('[?] Enter password attempt ')

        while in_word not in password_graph.get_connected_nodes():
            in_word = input('[?] Enter password attempt (must match possible password) ')

        score = int(input('[?] Enter chosen password score '))

        password_graph.prune_nodes(lambda n: n != in_word and password_graph.get_node_edges(n)[in_word] != score)
        password_graph.delete_node(in_word)

        print("[!] Possible passwords = {}".format(password_graph.get_nodes()))

        recommended = sorted(password_graph.get_nodes(),
                             key=lambda node: len(set(password_graph.get_node_edges(node).values())), reverse=True)

        if len(recommended):
            print("[!] Recommended password = {}".format(recommended[0]))

    print("[!] FTS finished.")
    deinit()
