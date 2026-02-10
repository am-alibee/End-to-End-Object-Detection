import random
import yaml
import getpass

def read_yaml(filepath: str):
    with open(filepath, "r") as f:
        return yaml.safe_load(f)

config = read_yaml("game_config.yaml")

min = config["range"]["min"]
max = config["range"]["max"]
guesses_allowed = config["guesses"]
mode = config["mode"]

solved = False

if mode == "single":
    correct_no = random.randint(min, max)
elif mode == "multi":
    correct_no = int(getpass.getpass("Player 2, enter the no to guess "))
else:
    print("Invalid config")
    exit()

for i in range(guesses_allowed):
    guess = int(input("Enter your guess: "))

    if guess == correct_no:
        print(f"Correct! you needed {i+1} tries")
        solved = True
        break
    elif guess < correct_no:
        print("Too Low")
    else:
        print("Too High")


if not solved:
    print(f"You lost!!! The no is {correct_no}")