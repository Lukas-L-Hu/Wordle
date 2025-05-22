import random
from collections import defaultdict
from collections import Counter

NUM_SIMULATIONS = 1000 # constant for how many simulations to run

def load_words(filename="words.txt"):
    # loads words from a text file
    with open(filename, "r") as f:
        return [line.strip().lower() for line in f if len(line.strip()) == 5]


def evaluate_guess(secret, guess):
    # Determines the color of each letter in the guess
    feedback = ['gray'] * 5
    secret_counts = Counter(secret)

    for i in range(5):
        if guess[i] == secret[i]:
            feedback[i] = 'green'
            secret_counts[guess[i]] -= 1

    for i in range(5):
        if feedback[i] == 'gray' and secret_counts[guess[i]] > 0:
            feedback[i] = 'yellow'
            secret_counts[guess[i]] -= 1

    return feedback



def update_constraints(guess, feedback, constraints):
    # Updates the constraints that guesses have to be within
    for i, (char, color) in enumerate(zip(guess, feedback)):
        if color == 'green':
            constraints['greens'][i] = char
        elif color == 'yellow':
            constraints['yellows'][char].add(i)
        elif color == 'gray':
            if (char not in constraints['greens'].values()
                    and char not in constraints['yellows']
                    and guess.count(char) == 1):  # Only add to grays if it only appeared once
                constraints['grays'].add(char)


def prune_words(word_list, constraints):
    # Eliminates words from consideration
    def is_valid(word):
        for i, c in constraints['greens'].items():
            if word[i] != c:
                return False
        for c, bad_positions in constraints['yellows'].items():
            if c not in word:
                return False
            if any(word[i] == c for i in bad_positions):
                return False
        for c in constraints['grays']:
            if c in word:
                return False
        return True

    return [word for word in word_list if is_valid(word)]


def select_guess(valid_words):
    if not valid_words:
        return None

    candidates = {}
    for _ in range(5):
        new_word = random.choice(valid_words)
        candidates[new_word] = unique_letters(new_word)
    best_score = max(candidates.values())
    for word in candidates:
        if candidates[word] == best_score:
            return word



def unique_letters(word):
    # Checks how many unique letters are in a word
    letters = set()
    unique_letters = 5
    for letter in word:
        if letter in letters:
            unique_letters -= 1
        else:
            letters.add(letter)
    return unique_letters


def print_guess_feedback(guess, feedback, past_guesses):
    # Prints out the letters based on what color they are
    # spaced_guess = ' '.join(guess.upper())

    symbols = {
        'green': 'G',
        'yellow': 'Y',
        'gray': '.'
    }
    spaced_feedback = ' '.join(symbols[f] for f in feedback)
    for guess in past_guesses:
        print(' '.join(guess))
    # print(spaced_guess)
    print(spaced_feedback)
    print()


def run_simulation(secret_word, word_list):
    # Runs the wordle simulation
    constraints = {
        'greens': {},
        'yellows': defaultdict(set),
        'grays': set()
    }

    valid_words = word_list[:]
    previous_guesses = []
    for attempt in range(1, 7):
        guess = select_guess(valid_words)
        print(f"Attempt {attempt}:")
        feedback = evaluate_guess(secret_word, guess)
        previous_guesses.append(guess.upper())
        print_guess_feedback(guess, feedback, previous_guesses)

        if guess == secret_word:
            print(f"Solved in {attempt} tries!")
            return attempt

        update_constraints(guess, feedback, constraints)
        valid_words = prune_words(valid_words, constraints)

    print(f"Failed to guess the word: {secret_word}")
    return False

if __name__ == "__main__":
    # word_list = load_words("words.txt")
    # secret = random.choice(word_list)
    # run_simulation(secret, word_list)

    correct = 0
    incorrect_words = []
    total_attempts = 0

    for _ in range(NUM_SIMULATIONS):
        word_list = load_words("words.txt")
        secret = random.choice(word_list)
        attempts = run_simulation(secret, word_list)
        if attempts:
            correct += 1
            total_attempts += attempts
        else:
            incorrect_words.append(secret)

    print(f'Correct: {correct}\n'
          f'Incorrect: {NUM_SIMULATIONS-correct}\n'
          f'Correct rate: {correct / NUM_SIMULATIONS * 100}%\n'
          f'Avg. # attempts (on guessed words): {total_attempts / correct}\n'
          f'Incorrect words: {incorrect_words}')

