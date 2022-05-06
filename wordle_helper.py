import json, difflib
from pprint import pprint as pp


def load_words(source='../../resources/json/words_dictionary.json', as_list=True):
    with open(source, 'r') as word_file:
        valid_words = json.loads(word_file.read())

    word_file.close()
    return list(valid_words.keys()) if as_list else valid_words.keys()


def get_five_letter_words(words):
    return [word for word in words if len(word) == 5]


def filter_five_letter_words(fives, word_pattern='-----', includes=[], exclude_pattern='-----', excludes=[]):
    filtered_word_list = []

    # This flow control is intentionally verbose to make the logic easier to read and understand.
    for word in fives:
        matches_exclude_pattern = any([c for idx, c in enumerate([*exclude_pattern]) if word[idx] == exclude_pattern[idx]])

        if not matches_exclude_pattern:
            matches_word_pattern = any([c for idx, c in enumerate([*word_pattern]) if word[idx] == word_pattern[idx]])

            if matches_word_pattern:
                has_correct_includes = any([c for c in includes if c in word])

                if has_correct_includes:
                    contains_excludes = any([c for c in excludes if c in word])
            
                    if not contains_excludes:
                        filtered_word_list.append(word)


    return filtered_word_list


if __name__ == '__main__':
    words = load_words()

    five_letter_words = get_five_letter_words(words)

    word_pattern = '-a---'
    includes = ['e']
    exclude_pattern = '---e-'
    excludes = ['o', 't', 'h', 'r', 'n', 'i', 'l', 's']

    filtered_fives = filter_five_letter_words(five_letter_words,
                                              word_pattern=word_pattern, 
                                              includes=includes, 
                                              exclude_pattern=exclude_pattern,
                                              excludes=excludes) 
    pp(filtered_fives)
