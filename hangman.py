import hangman_helper

CHAR_A = 97
CHAR_Z = 122
UNDERLINE = "_"

# Part a


def update_word_pattern(word, pattern, letter):
    """This function get a word, the current pattern and a letter. If the
    letter is in the word, the function return a new pattern including
    the letter."""

    for i in range(len(word)):
        if letter == word[i]:
            pattern = pattern[:i] + letter + pattern[i+1:]
    return pattern


def main():
    """This function start a game. While the player want to keep playing, new
    game will start."""

    words_lst = hangman_helper.load_words()
    run_single_game(words_lst)
    move = hangman_helper.get_input()

    while move[0] == hangman_helper.PLAY_AGAIN and move[1]:
        run_single_game(words_lst)
        move = hangman_helper.get_input()


def run_single_game(words_list):
    """This function run a single hangman game."""

    the_word = hangman_helper.get_random_word(words_list)
    pattern = "_" * len(the_word)
    wrong_guess_lst = list()
    error_count = 0
    msg = hangman_helper.DEFAULT_MSG
    ask_play = False

    while error_count < hangman_helper.MAX_ERRORS and pattern != the_word:
        error_count, pattern, msg = the_game(ask_play, error_count, msg,
            pattern, the_word, wrong_guess_lst, words_list)

    end_game(ask_play, error_count, msg, pattern, the_word, wrong_guess_lst)


def the_game(ask_play, error_count, msg, pattern, the_word, wrong_guess_lst,
             words_list):
    """This function check if the player want to guess a letter or to ask for
    a hint. If the player guessed a letter, the function check if it is a valid
    letter. If he want a hint, it gives him one."""

    hangman_helper.display_state(pattern, error_count, wrong_guess_lst, msg,
        ask_play)
    move = hangman_helper.get_input()

    # If the player chose to put a letter in -
    if move[0] == hangman_helper.LETTER:
        letter = move[1]
        if len(letter) == 1 and letter.islower():
            error_count, pattern, msg = good_letter(error_count, letter,
                pattern, the_word, wrong_guess_lst)
        else:
            msg = hangman_helper.NON_VALID_MSG

    # If the player ask for a hint
    elif move[0] == hangman_helper.HINT:
        filter_list = filter_words_list(words_list, pattern, wrong_guess_lst)
        hint = choose_letter(filter_list, pattern)
        msg = hangman_helper.HINT_MSG + hint
    return error_count, pattern, msg


def good_letter(error_count, letter, pattern, the_word, wrong_guess_lst):
    """This function check if the letter is in the word. if not, the function
    add the letter to the wrong guess list. """

    if letter in pattern or letter in wrong_guess_lst:
        msg = hangman_helper.ALREADY_CHOSEN_MSG + letter
    elif letter in the_word:
        pattern = update_word_pattern(the_word, pattern, letter)
        msg = hangman_helper.DEFAULT_MSG
    else:
        wrong_guess_lst.append(letter)
        error_count += 1
        msg = hangman_helper.DEFAULT_MSG
    return error_count, pattern, msg


def end_game(ask_play, error_count, msg, pattern, the_word, wrong_guess_lst):
    """When the games ends, this function tell the player if he won or lose and
    what was the word."""

    if error_count == hangman_helper.MAX_ERRORS:
        msg = hangman_helper.LOSS_MSG + the_word
        ask_play = True
    elif pattern == the_word:
        msg = hangman_helper.WIN_MSG
        ask_play = True

    hangman_helper.display_state(pattern, error_count, wrong_guess_lst, msg,
                                 ask_play)


# Part b


def filter_words_list(words, pattern, wrong_guess_lst):
    """This function filter the words list, and return a new list of all the
    words that this pattern and wrong guess list can feet them."""

    word_length = len(pattern)
    filtered_words = list()

    for word in words:
        if len(word) == word_length and same_right_letters(word, pattern) and \
                same_wrong_letters(word, wrong_guess_lst):
            filtered_words.append(word)
    return filtered_words


def same_right_letters(word, pattern):
    """This function get a word and a pattern, and return True if this pattern
    can feet the word."""
    for i in range(len(word)):
        if pattern[i] != UNDERLINE:
            if word[i] != pattern[i]:
                return False
        elif word[i] in pattern:
            return False
    return True


def same_wrong_letters(word, wrong_guess_lst):
    """This function get a word and wrong guess list, and return True if the
    wrong guess list can feet the word."""

    for letter in wrong_guess_lst:
        if letter not in word:
            continue
        else:
            return False
    return True


def choose_letter(words, pattern):
    """This function get a list of words and a pattern. and return the most
    frequent letter in the words list that doesn't appear in the pattern."""

    maximum = 0
    max_letter = " "

    for i in range(CHAR_A, CHAR_Z+1):
        char_i_times = 0
        for j in range(len(words)):
            for letter in words[j]:
                if letter == chr(i):
                    char_i_times += 1
        if char_i_times > maximum and chr(i) not in pattern:
            maximum = char_i_times
            max_letter = chr(i)
    return max_letter


if __name__ == "__main__":
    hangman_helper.start_gui_and_call_main(main)
    hangman_helper.close_gui()

