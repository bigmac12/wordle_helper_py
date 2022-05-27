import json
import cmd
from pprint import pprint as pp


class WordleHelper:
    def __init__(self):
        self.DEBUG = True
        self.display_width = 80

        defaults = {
            'words': self.load_words(),
            'word_pattern': 't-a--',
            'exclude_pattern': '-r-i-',
            'includes': ['a', 'i', 't', 'r'],
            'excludes': ['n', 'l', 's', 'o', 'h', 'e'],
            'filtered_word_list': []
        }

        self.settings_string = ''

        for key, value in defaults.items():
            setattr(self, key, defaults.get(key, value))

            if key not in ['words', 'filtered_word_list']:
                key_str = "{}:".format(key).ljust(19, ' ')
                self.settings_string += "{key_str} {value}\n".format(key_str=key_str, value=value)

        if self.DEBUG:
            self.__print_settings()

    def __print_heading(self, heading):
        print("\n{heading}".format(heading=heading))
        print(''.join(['-' for char in heading]))

    def __print_settings(self):
        self.__print_heading("Current settings")
        print(self.settings_string)

    def __column_print(self, data):
        cli = cmd.Cmd()
        cli.columnize(data, displaywidth=self.display_width)

    @staticmethod
    def load_words(source='../../resources/json/wordle_words.json', as_list=True):
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
            matches_exclude_pattern = any([char for idx, char in enumerate([*self.exclude_pattern]) if word[idx] == self.exclude_pattern[idx]])
            
            if not matches_exclude_pattern:
                matches_word_pattern = any([char for idx, char in enumerate([*self.word_pattern]) if word[idx] == self.word_pattern[idx]])

                if matches_word_pattern or self.word_pattern == '-----':
                    has_correct_includes = all([char in word for char in self.includes])

                    if has_correct_includes:
                        contains_excludes = any([char in word for char in self.excludes])
                
                        if not contains_excludes:
                            self.filtered_word_list.append(word)

        return self.filtered_word_list

    def print_results(self):
        self.__print_heading("Possible matches")
        self.__column_print(self.filter_five_letter_words())


@DeprecationWarning
def column_print_old(data):
    for a, b, c in zip(data[::3], data[1::3], data[2::3]):
        print('{:<30}{:<30}{:<}'.format(a, b, c))


if __name__ == '__main__':
    helper = WordleHelper()
    helper.print_results()
