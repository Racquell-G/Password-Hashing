import hashlib
import itertools
import matplotlib.pyplot as plt
import numpy as np
import time
import random

# PART 1: Read words from the password_file.txt (DICTIONARY)
def read_dictionary(file_name):
    with open(file_name, 'r') as file:
        words = file.read().splitlines()
    return words

# PART 2: Hash user input w/ SHA256 & SHA512
def hash_input(password):
    # Hashes the user inputted password in sha256 and sha512
    hash256 = hashlib.sha256(password.encode()).hexdigest()
    hash512 = hashlib.sha512(password.encode()).hexdigest()
    password_length = len(password)
    return hash256, hash512, password_length

# PART 3 & 4: Perfrom the dictionary attack
def dictionary_attack(password_hashes, dict, password_length):
    # Starts the timer and attempts
    attempts = 0
    start_time = time.time()
    # Every word in the dictionary will be encoded in SHA256 & SHA512
    for word in dict:
        if len(word) == password_length:
            word_hash256 = hashlib.sha256(word.encode()).hexdigest()
            word_hash512 = hashlib.sha512(word.encode()).hexdigest()
            # If either word hashes are in the password hashes return the newly found data (word, time, etc.)
            attempts += 1
            if word_hash256 in password_hashes or word_hash512 in password_hashes:
                end_time = time.time()
                return True, word, end_time - start_time, word_hash256, word_hash512, attempts
    # Else do this
    end_time = time.time()
    return False, None, end_time - start_time, None, None, None

# main
if __name__ == "__main__":
    # PART 1: READS WORDS FROM THE FILE
    dictionary = read_dictionary("/home/ugrads/majors/racquellg/CS2104/W13_Class_Project/dictionary.txt")
    results = []
    difficult_passwords = []
    INDENT = (" "*4)
    
    # This is for the 10 difficult passwords we need to obtain, so that we can plot
    random.shuffle(dictionary)
    for _ in range(10):
        word1 = random.choice(dictionary)
        word2 = random.choice(dictionary)
        word3 = random.choice(dictionary)
        merged_word = word1 + word2 + word3
        difficult_passwords.append(merged_word)

    # Hashes the 10 generated difficult passwords
    for password in difficult_passwords:
        hash256, hash512, pwlength = hash_input(password)
        password_hashes = [hash256, hash512]
        dictionary_size = len(dictionary)

    # PART 2: USER INPUT
    while True:
        user_input = input("Enter password: ")
        if user_input.lower() == 'q':
            break
        user_passwords = user_input.split()
        passwords_info = []

# PART 3: Hashes user input
        for password in user_passwords:
            password_three_combo = []
            # ASK TA again if I handled this correctly, it should make the three password combination I was messing up earlier
            for r in range (1, min(4, len(dictionary) + 1)):
                password_three_combo.extend([''.join(combo) for combo in itertools.permutations(dictionary, r)])                            
            hash256, hash512, pwlength = hash_input(password)
            print(f" ")
            print(f"{INDENT}SHA256: {hash256}")
            print(f"{INDENT}SHA512: {hash512}")
            print(f" ")
            password_hashes = [hash256, hash512]
            passwords = [password + " (SHA256)", password + " (SHA512)"]
            times = []
# PART 4: DICTIONARY
            for password_hash, password in zip(password_hashes, passwords):
                is_found, guessed_password, time_taken, hash256, hash512, attempts = dictionary_attack([password_hash], dictionary, pwlength)
                if is_found:
                    hash_type = "SHA256" if "SHA256" in password else "SHA512"
                    if hash_type == "SHA256":
                        print(f"Cracked SHA256: {guessed_password}")
                        print(f"Time to crack: {time_taken * 100000}")
                        print(f" ")
                    else:
                        print(f"Cracked SHA512: {guessed_password}")
                        print(f"Time to crack: {time_taken * 100000}")
                        print(f" ")
                        print(f"Attempts: {attempts}")
                        print(f" ")
                    times.append(time_taken)
                    passwords_info.append((passwords, times))
                    results.append({"Password": password, 
                        "Hash Type": hash_type,
                        "Dictionary Size": dictionary_size, 
                        "Time to crack": sum(times), 
                        "Number of Attempts": attempts
                        })
                else:
                    print(f"Wrong Password!")
    # So when q is pressed it breaks the while and heads down here
    # I begin by getting the results for the SHA256 10 difficult passwords
    passwords = [result["Password"] for result in results if "(SHA256)" in result["Password"]]
    crack_time = [result["Time to crack"] for result in results]
    tries = [result["Number of Attempts"] for result in results]

    # Plots the data
    # Most of the stuff down here is pretty self explanatory and follows the basic terminology of graphs
    # I believe the graph they wanted is a scatter plot so that is why plt.scatter is used
    plt.figure(figsize=(10,6))
    time_taken_difficult_pwords = []
    for i, password in enumerate(difficult_passwords):
        sha256_hash, _, _= hash_input(password)
        start_time = time.time()
        is_found, _, _, _, _, _, = dictionary_attack([sha256_hash], dictionary, pwlength)
        end_time = time.time()
        time_taken = end_time - start_time
        time_taken_difficult_pwords.append(time_taken)
        plt.scatter(i, time_taken_difficult_pwords[i], label=f"('{password}', '{time_taken:.5f} sec')")

    plt.xlabel('Password Difficulty')
    plt.ylabel('Time taken to crack SHA256 (seconds)')
    plt.title('Password Difficulty vs Time Taken to Crack SHA256')
    plt.xticks(range(len(difficult_passwords)))
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    plt.figtext(0.5, 0.9, f'Dictionary Size: {len(dictionary)} words')
    plt.show()    