import hashlib
import itertools
import string
import time
import random
import fileinput
import re


allowed_chars = string.ascii_lowercase
max_length = 8
password = "sonne"

def hash(pw):
    """Return the SHA-256 hash for a given password"""
    return hashlib.sha256(pw.encode()).hexdigest()

### Different password generators

def password_generator_random():
    """Randomly generate passwords of maximal length max_length

    Choose a random length between 1 and max_length, then choose 
    as many random elements from allowed_chars and return them as string
    """
    while True:
        length = random.randint(1, max_length)
        yield ''.join(random.choices(allowed_chars, k=length))

def password_generator_list():
    """Systematically generate passwords of maximal length max_length

    Start with length 1 passwords, then length 2, ...
    """
    for l in range(1, max_length):
        # see https://docs.python.org/3/library/itertools.html#itertools.product
        for p in itertools.product(allowed_chars, repeat=l):
            yield ''.join(p)

def pin_generator_random():
    """Randomly generate a PIN of maximal length max_length

    Choose a random length between 1 and max_length, then choose 
    a random number between 1 and 10**length, pad it with leading 
    zeros and return as a string
    """
    while True:
        length = random.randint(1, max_length)
        yield f"{random.randint(0, 10**length):0{length}}"  # see https://fstring.help/cheat

def pin_generator_list():
    """Systematically generate PINs of maximal length max_length"""
    pass

def pin_generator_hibp():
    """Generate PINs according to frequency to the HIBP leaks

    This only includes PINs with 1,2,3,4,5 and 6 digits.
    """
    for line in fileinput.input('hibp.txt'):
        yield line.rstrip()

def crack_password(hashed_pw):
    """Crack a password

    Given **only** a hashed password, try to find a password leading to the same
    hash value by a lot of guessing.
    """
    # use a password generator to generate fresh passwords
    pw_gen = password_generator_list()
    for guess in pw_gen:
        hashed_guess = hash(guess)
        print_hash_and_pw(hashed_guess, guess, end="\r") # print on the same line
        if hashed_guess == hashed_pw:
            print()
            return guess
    print()
    return None  # no matching password found

def print_hash_and_pw(h, p, end="\n"):
    """Print a hash and a password in one line

    Helper function to pretty print a hash and a password.
    Use end="\r" to always print on the same line.
    """
    # {h:<66} is print h left aligned in a 66 character area
    print(f"{h:<66}{p:<20}", end=end)

def main():
    # check if we obey our own rules
    if not(len(password) <= max_length and all(c in allowed_chars for c in password)):
        print("WARNING: Password is not within max_length and allowed_chars!")
    # calculate the hash value of the given password
    hashed_pw = hash(password)
   
    # output given hash and password 
    print_hash_and_pw("hashed password", "password")  # header
    print_hash_and_pw(hashed_pw, password)            # data
    
    # start the timed area
    start_time = time.time()
    pw = crack_password(hashed_pw)
    if pw:
        print("Password successfully cracked!")
    else:
        print("Cannot crack password")
    end_time = time.time()

    print(f"Time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
