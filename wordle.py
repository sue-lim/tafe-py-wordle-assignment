"""Guess-My-Word is a single player game to guess a 5 letter word.
Author: P Lim
Company: WordGamesRUs
Copyright: 2023
"""
import random
from rich import print
from rich.console import Console
from rich.theme import Theme


console = Console(width=100, theme=Theme({"warning": " bold white on red"}))
console.rule(f"[bold white]:memo: Wordle :memo:\n")

# def refresh_page(headline):
#     console.clear()
# console.rule(f"[bold blue]:leafy_green: {headline}: leafy_green:")


# from pathlib import Path
# import enum

TARGET_WORDS = "./word-bank/target_words.txt"
VALID_WORDS = "./word-bank/all_words.txt"
CONGRATULATORY_MSGS = "wordle_congrats_messages.txt"


# USED FOR THE GUESS_SCORE FUNCTION
# class target_word_score(enum.Enum):
#     wrong_letters = 0
#     misplaced_letters = 1
#     correct_letters = 2


def greet():
    """Welcomes user and requests for an player name input
    Returns:
        str: player_name

    Example:

    """
    player_name = str(
        input(
            "\nWelcome to Wordle\nLet's get to know each other a little more before we get started!\nWhat's your name? "
        )
    )
    print(f"\n:waving_hand: Hey {player_name}... Nice to E-Meet you!\n")


# FUNCTION TO CONTAIN THE GAME INTRODUCTION
def game_introduction():
    """Displays instructions
    Args: None

    Returns: str game instructions

    Example:
    >>> print(game_introduction())
        "Wordle is a single-player game\n\nA player has to guess a five-letter hidden word...\nYou have 6 attempts\nYour Progress Guide\n\nIndicates that the letter at that position is in the hidden word but in a different position (TO BE UPDATED)\nIndicates that the letter at that position is in the hidden word...(TO BE UPDATED)\n"
    True
    """
    console.print(f"[bold_underlined]:white_exclamation_mark: Instructions\n")
    console.print(
        f":white_exclamation_mark: Wordle is a single-player game\n\n:white_exclamation_mark: A player has to guess a five-letter hidden word...\n:white_exclamation_mark: You have 6 attempts\n\n:white_exclamation_mark: Your Progress Guide\n\n:white_exclamation_mark: :green_square:  Indicates that the letter at that position is in the hidden word\n:white_exclamation_mark: :yellow_square:  Indicates that the letter at that position is in the hidden word but in a different position\n:white_exclamation_mark: :red_square:  Indicates the letter is not in the word...\n\n:four_leaf_clover:  Goodluck  :four_leaf_clover:\n "
    )

    console.print(f"Let's play...\n")


def get_target_word(file_path):
    """Reads through a file and picks a random word from TARGET_WORDS
    Args:
        file_path (str): the path to the file containing the words
    Returns:
        str or None: a random word from the file

    Examples:
    >>> file_path = "./word-bank/target_words.txt"
    >>> target_word = get_target_word(file_path)
    >>> assert target_word is not None, "File reading failed"
    >>> print("File has been successfully read.")
    """

    try:
        target_words_file = open(file_path, "r")
        target_words_content = target_words_file.readlines()
        target_words_file.close()
        target_words_list = []

        for target_word in target_words_content:
            updated_target_word = target_word.strip()
            if updated_target_word:
                uppercase_target_word = updated_target_word.upper()
                target_words_list.append(uppercase_target_word)

        random_word = random.choice(target_words_list)
        return random_word

    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None


# FUNCTION TO SHOW WHAT USER GUESSED LETTERS ARE IN THE CORRECT SPOT,
# MISPLACED OR NOT CORRECT
def show_guess(guess, target_word):
    """Set Function to return how many correct letters, misplaced letters, wrong letters
    have been guessed.

    Example:
    >>> show_guess("SQUID","SQUIB")
    Correct letters: I, Q, S, U
    Misplaced letters:
    Wrong letters: D
    """
    guessed_letters = []

    correct_letters = {
        letter for letter, correct in zip(guess, target_word) if letter == correct
    }
    misplaced_letters = set(guess) & set(target_word) - correct_letters
    wrong_letters = set(guess) - set(target_word)
    # this is required as it's part of the set
    # removing this will affect the "else" statement below

    for letter, correct in zip(guess, target_word):
        if letter == correct:
            guessed_letters.append(f"[b white on green]{letter:^3}[/b white on green]")
        elif letter in misplaced_letters:
            guessed_letters.append(f"[white on yellow]{letter:^3}[/white on yellow]")
        else:
            guessed_letters.append(f"[white on red]{letter:^3}[/white on red]")

    print(*guessed_letters, sep=" ")
    return show_guess


# FUNCTION TO IMPLEMENT A SCORING ALGORITHM FOR WORD AND CORRECTLY GUESSED LETTERS
def guess_score(guess, target_word):
    """
    Given two strings of equal length, returns a list of integers representing the score of the guess
    against the target word (MISS, MISPLACED, or EXACT).

    Args:
    - guess (str): The user's guess.
    - target_word (str): The target word to be guessed against.

    Returns:
    - list: A list of integers representing the score for each character in the guess.

    Example:
    >>> guess_score("HELLO", "WORLD")
    [0, 0, 1, 2, 1]
    """

    correct_letters = 2
    misplaced_letters = 1
    wrong_letters = 0

    numeric_score = []
    formatted_score = []

    for target_char, guess_char in zip(target_word, guess.upper()):
        if target_char == guess_char:
            numeric_score.append(correct_letters)  # SCORE OF 2
            formatted_score.append("🟩")  # SCORE OF 2
        elif guess_char in target_word:
            numeric_score.append(misplaced_letters)  # SCORE OF 1
            formatted_score.append("🟨")  # SCORE OF 1
        else:
            numeric_score.append(wrong_letters)  # SCORE OF 0
            formatted_score.append("🟥")  # SCORE OF 0

    """ Test print to screen """
    # print(numeric_score)
    # print(*formatted_score, sep="")
    return numeric_score


# FUNCTION TO RETURN THE BEST MATCHING HINT WORD BASED ON WHAT USER HAS ENTERED
def find_matching_hint(guess_letters, file_path, target_word):
    """Function to read through a file_path and return the best hint
    Args:
        guess_letters (str): Letters used for guessing.
        file_path (str): The path to the file containing the words.
        target_word (str): The target word to match against.

    Returns:
        str or None: A hint word from the file.

    Examples:

    """
    try:
        hint_word_file = open(file_path, "r")
        hint_word_file_content = hint_word_file.readlines()
        best_match_hint = None
        best_match_score = 0

        hint_word_file.close()

        for hint_word in hint_word_file_content:
            hint_word = hint_word.strip().upper()  # strip and uppercase

            # Ensure the word is at least 3 characters long and count any two matching letters
            if len(hint_word) > 2:
                match_score = 0
                for letter in guess_letters:
                    if letter in hint_word:
                        match_score += 1

                # Check if the current word has a higher match score than the best match
                if match_score >= 2 and match_score > best_match_score:
                    # Update the best match hint and score
                    best_match_hint = hint_word
                    best_match_score = match_score

        return best_match_hint

    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None


def get_random_congratulatory_message(file_path):
    """Reads through a file and returns a random congratulatory message for Wordle from a file.
    Args:
        file_path (str): The path to the file containing sentences.
    Returns:
        str or None: A sentence from the file, or None if file reading fails.

    Example:
    >>> file_path = CONGRATULATORY_MSGS
    >>> congrats_messages = get_random_congratulatory_message(file_path)
    >>> assert message is not None, "File reading failed"
    >>> print("File has been successfully read.")
    """
    try:
        congrats_message_file = open(file_path, "r")
        congrats_message_content = congrats_message_file.readlines()
        congrats_message_file.close()
        congrats_message_list = []

        for message in congrats_message_content:
            congrats_message = message.strip()
            if congrats_message:
                congrats_message_list.append(congrats_message)

        random_congrats_msg = random.choice(congrats_message_list)
        return random_congrats_msg

    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None


# FUNCTION FOR THE END OF THE GAME
def game_over(target_word):
    """Function to call the target word at the end of the game
    to be displayed on the screen

    Returns:
        str:

    """
    print(f"The word was {target_word}")
    return game_over


def update_statistics(target_word, guess_counter, total_guesses, total_games_played):
    """Function to update wordle game statistics in a CSV file.

    Args:
        target_word (str): The target word.
        guess_counter (int): Number of guesses made in the game.
        total_guesses (int): Total number of guesses so far.
        total_games_played (int): Total number of games played.

    Returns:
        int, int: Updated total_guesses and total_games_played.
    """
    try:
        guess_statistics_file = open("wordle_statistics.csv", "a")
        guess_statistics_file.write(f"{target_word}:{guess_counter}\n")
        guess_statistics_file.close()

        # Update the total guesses and total games played
        total_guesses += guess_counter
        total_games_played += 1

        return total_guesses, total_games_played

    except Exception as e:
        print(f"Error: {e}")
        return total_guesses, total_games_played


# MAIN GAME
def main():
    greet()
    game_introduction()
    # PRE-PROCESS
    total_games_played = 0
    # PROCESS (MAIN LOOP)

    total_games_played = 0
    total_guesses = 0
    # total_games_played = get_total_games_played()

    while True:
        target_word = get_target_word(TARGET_WORDS)
        congratulation_msg = get_random_congratulatory_message(CONGRATULATORY_MSGS)
        print("TARGET_WORD - ", target_word)

        guess_num = 1
        guess_counter = 0

        while guess_num < 6:
            guess = console.input(f"\n:lock: Guess {guess_num}: ").upper()
            best_match_hint = find_matching_hint(guess, VALID_WORDS, target_word)
            if not len(guess) == 5 and guess.isalpha():
                print(
                    "Sorry! try again... Please use a word with 5 characters only!  A-Z "
                )
                continue
            else:
                guess_num += 1
                guess_counter += 1
                show_guess(guess, target_word)
                if best_match_hint:
                    console.print("\n:gift:  Hint:", best_match_hint)
                else:
                    console.print(":x:  Sorry there is no hint word for this.")
                guess_score(guess, target_word)
            if guess == target_word:
                # print(f"*** ATTEMPTS - {guess_counter} ")
                console.print(f"\n:mailbox: {congratulation_msg}")
                console.print(f"\n:tada: Yipee! You guess the word correctly!\n")
                break

            # POST-PROCESS (is the word needed to clean up the main loop)
        else:
            game_over(target_word)

        total_guesses, total_games_played = update_statistics(
            target_word, guess_counter, total_guesses, total_games_played
        )

        print(f"Games played: {total_games_played}")

        # print(total_guesses)

        answer = input("\nDo you want to play again? Y/N ")
        if answer.lower() not in ("y", "yes"):
            if total_games_played > 0:
                average_guesses = total_guesses / total_games_played
                console.print(
                    f"\n:video_game: Your Game Statistics\n\n:video_game: Average guesses attempts per game: {average_guesses}"
                )

            print(
                "\nThanks for playing, hope to see you again for another challenge!\n"
            )
            break


# THIS LINE MAKES SURE YOUR CODE IS CALLED WHEN THE FILE IS EXECUTED
if __name__ == "__main__":
    main()
