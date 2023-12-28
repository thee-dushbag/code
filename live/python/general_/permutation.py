from string import ascii_letters
from tqdm import tqdm
from random import shuffle

true_password = "SimongasH50"
password = list(true_password)
shuffle(password)
password = "".join(password)


def createbox(passwd, msg):
    def safebox(testpasswd):
        if testpasswd == passwd:
            print(msg)
            return True

    return safebox


def recursive_perm(sequence):
    if len(sequence) == 1:
        yield sequence
        return
    for index, item in enumerate(sequence):
        others = sequence[:index] + sequence[index + 1 :]
        for subsequence in recursive_perm(others):
            yield item + subsequence


def unlockbox():
    box = createbox(true_password, "My name is Simon Nganga Njoroge and I'm 21 years old.")
    for possible_passwd in recursive_perm(password):
        print(f"Testing: {possible_passwd}")
        if box(possible_passwd):
            break


def main():
    from math import factorial

    for i in tqdm(range(1, 11)):
        size = factorial(i)
        perms = tuple(recursive_perm(ascii_letters[:i]))
        assert (
            len(perms) == size
        ), f"Expected {size} permutaions, got {len(perms)} permutaions"


if __name__ == "__main__":
    # main()
    unlockbox()
