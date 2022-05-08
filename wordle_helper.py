import json, difflib
from pprint import pprint as pp


class WordleHelper:

    def __init__(self):
        defaults = {
            'words': self.load_words(),
            'word_pattern': '-----',
            'exclude_pattern': '-ti-s',
            'includes': ['t', 'i', 's'],
            'excludes': ['o', 'h', 'e', 'r', 'n', 'a', 'l'],
            'filtered_word_list': []
        }

        self.settings_string = ''

        for key, value in defaults.items():
            setattr(self, key, defaults.get(key, value))
            if key != 'words':
                self.settings_string += "{key}: {value}\n".format(key=key, value=value)

        self.__print_settings()

    def __print_settings(self):
        print("\nCurrent settings")
        print("----------------")
        print(self.settings_string)

    @staticmethod
    def load_words(source='../../resources/json/words_dictionary.json', as_list=True):
        with open(source, 'r') as word_file:
            valid_words = json.loads(word_file.read())

        word_file.close()
        return [word for word in list(valid_words.keys()) if len(word) == 5] if as_list else valid_words.keys()

    @DeprecationWarning
    def get_five_letter_words(self):
        return [word for word in self.words if len(word) == 5]

    def filter_five_letter_words(self):

        # This flow control is intentionally verbose to make the logic easier to read and understand.
        for word in self.words:
            matches_exclude_pattern = any([c for idx, c in enumerate([*self.exclude_pattern]) if word[idx] == self.exclude_pattern[idx]])

            if not matches_exclude_pattern:
                matches_word_pattern = any([c for idx, c in enumerate([*self.word_pattern]) if word[idx] == self.word_pattern[idx]])

                if matches_word_pattern or self.word_pattern == '-----':
                    has_correct_includes = all([c in word for c in self.includes])

                    if has_correct_includes:
                        contains_excludes = any([c in word for c in self.excludes])
                
                        if not contains_excludes:
                            self.filtered_word_list.append(word)


        return self.filtered_word_list


if __name__ == '__main__':
    helper = WordleHelper()
    filtered_fives = helper.filter_five_letter_words()
    pp(filtered_fives)
