import itertools

from typing import Mapping


def matching_characters(a: str, b: str) -> int:
    """
    Returns the number of matching characters for a given pair of strings
    :param a: the first string
    :param b: the second string
    :return: the number of indices with matching character values in the two strings
    """
    return sum(map(lambda p: 1 if p[0] == p[1] else 0, [x for x in zip(a, b)]))


def matching_character_pairs(words: [str]) -> Mapping[str, str]:
    """
    Sorts the strings by their number of matching characters and prints them out
    :param words: the list of words to pair up, and find matching character counts for
    :return: a dictionary mapping word pairings to their number of matching characters
    """
    return {(a, b): matching_characters(a, b) for (a, b) in itertools.combinations(words, 2)}


def satisfiable(a: str, b: str) -> bool:
    """
    Returns whether two strings can both be satisfying passwords
    :param a: the first string
    :param b: the second string
    :return: True if they can both be satisfying passwords, otherwise False
    """
    for (a_char, b_char) in zip(a, b):
        if a_char != b_char and not (a_char != "_" or b_char != "_"):
            return False
    return True
