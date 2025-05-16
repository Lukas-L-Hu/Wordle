import random
from collections import defaultdict

def load_words(filename="words.txt"):
    with open(filename, "r") as f:
        return [line.strip().lower() for line in f if len(line.strip()) == 5]


def evaluate_guess(secret, guess):
    feedback = ['gray'] * 5
    secret_letters = list(secret)

    # First pass for greens
    for i in range(5):
        if guess[i] == secret[i]:
            feedback[i] = 'green'
            secret_letters[i] = None  # prevent reuse

    # Second pass for yellows
    for i in range(5):
        if feedback[i] == 'gray' and guess[i] in secret_letters:
            feedback[i] = 'yellow'
            secret_letters[secret_letters.index(guess[i])] = None

    return feedback


def update_constraints(guess, feedback, constraints):
    for i, (char, color) in enumerate(zip(guess, feedback)):
        if color == 'green':
            constraints['greens'][i] = char
        elif color == 'yellow':
            constraints['yellows'][char].add(i)
        elif color == 'gray':
            if char not in constraints['greens'].values() and char not in constraints['yellows']:
                constraints['grays'].add(char)


def prune_words(word_list, constraints):
    def is_valid(word):
        # Green check
        for i, c in constraints['greens'].items():
            if word[i] != c:
                return False
        # Yellow check
        for c, bad_positions in constraints['yellows'].items():
            if c not in word:
                return False
            if any(word[i] == c for i in bad_positions):
                return False
        # Gray check
        for c in constraints['grays']:
            if c in word:
                return False
        return True

    return [word for word in word_list if is_valid(word)]


def select_guess(valid_words):
    candidates = dict()
    for i in range(5):
        new_word = random.choice(valid_words)
        candidates[new_word] = unique_letters(new_word)
    best_score = max(candidates.values())
    for word in candidates:
        if candidates[word] == best_score:
            return word
    # return random.choice(valid_words) if valid_words else None


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


def print_guess_feedback(guess, feedback):
    # Make letters uppercase and space them out
    spaced_guess = ' '.join(guess.upper())

    # Map feedback to symbols and space them out to align with letters
    symbols = {
        'green': 'G',
        'yellow': 'Y',
        'gray': '.'
    }
    spaced_feedback = ' '.join(symbols[f] for f in feedback)

    # Print both lines
    print(spaced_guess)
    print(spaced_feedback)
    print()

# ----------------------------
# Main simulation loop
# ----------------------------
def run_simulation(secret_word, word_list):
    constraints = {
        'greens': {},              # pos → char
        'yellows': defaultdict(set), # char → bad positions
        'grays': set()
    }

    valid_words = word_list[:]
    for attempt in range(1, 7):
        guess = select_guess(valid_words)
        print(f"Attempt {attempt}:")
        feedback = evaluate_guess(secret_word, guess)
        print_guess_feedback(guess, feedback)

        if guess == secret_word:
            print(f"Solved in {attempt} tries!")
            return

        update_constraints(guess, feedback, constraints)
        valid_words = prune_words(valid_words, constraints)

    print(f"Failed to guess the word: {secret_word}")

if __name__ == "__main__":
    word_list = load_words("words.txt")
    secret = random.choice(word_list)
    run_simulation(secret, word_list)
