''' Insert heading comments here.'''
import math, string

# Define constants for punctuation and alphanumeric characters
#  string.punctuation is a string constant that contains all the punctuation characters on the keyboard.
#  except space is not included in this string
PUNCTUATION = string.punctuation

#  string.ascii_lowercase is a string constant that contains all the lowercase letters in the alphabet.
#  string.digits is a string constant that contains all the digits 0-9.
ALPHA_NUM = string.ascii_lowercase + string.digits


BANNER = ''' Welcome to the world of 'dumbcrypt,' where cryptography meets comedy! 
    We're combining Affine Cipher with Caesar Cipher to create a code 
    so 'dumb,' it's brilliant. 
    Remember, in 'dumbcrypt,' spaces are as rare as a unicorn wearing a top hat! 
    Let's dive into this cryptographic comedy adventure!             
    '''


def print_banner(message):
    '''Display the message as a banner.
    It formats the message inside a border of asterisks, creating the banner effect.'''
    border = '*' * 50
    print(border)
    print(f'* {message} *')
    print(border)
    print()

def multiplicative_inverse(A, M):
    '''Return the multiplicative inverse for A given M.
       Find it by trying possibilities until one is found.
        Args:
        A (int): The number for which the inverse is to be found.
        M (int): The modulo value.
        Returns:
            int: The multiplicative inverse of A modulo M.
    '''
    for x in range(M):
        if (A * x) % M == 1:
            return x


def check_co_prime(num, M):
    co_prime_check = math.gcd(num, M)

    if co_prime_check == 1:
        return True
    else:
        return False


def get_smallest_co_prime(M):
     for i in range(2, M):
        if math.gcd(M, i) == 1:
            return i


def caesar_cipher_encryption(ch, N, alphabet):
    index = alphabet.find(ch)
    M = len(alphabet)

    formula = (index+N) % M

    for x, letter in enumerate(alphabet):
        if formula == x:
            return(letter)


def caesar_cipher_decryption(ch, N, alphabet):
    index = alphabet.find(ch)
    M = len(alphabet)

    formula = (index-N) % M

    for x, letter in enumerate(alphabet):
        if formula == x:
            return(letter)


def affine_cipher_encryption(ch, N, alphabet):
    M = len(alphabet)
    A = get_smallest_co_prime(len(alphabet))
    encrypted = ""
    for i in ch:

        index = alphabet.find(i)
        formula = ((A * index) + N) % M

        for x, letter in enumerate(alphabet):
            if formula == x:
                encrypted += letter
    return encrypted


def affine_cipher_decryption(ch, N, alphabet):
    decrypted = ''
    M = len(alphabet)
    A = get_smallest_co_prime(M)
    A_inverse = multiplicative_inverse(A,M)

    for i in ch:

        for x, letter in enumerate(alphabet):
            if letter == i:
                index = x

                formula = (A_inverse * (index - N)) % M

                decrypted += alphabet[formula]
    return decrypted



def main():
    print_banner(BANNER)



    rotation = input("Input a rotation (int): ")
    while rotation.isdigit() == False:
        print("\nError; rotation must be an integer.")
        rotation = input("Input a rotation (int): ")

    rotation = int(rotation)

    asking = input("\n\nInput a command (e)ncrypt, (d)ecrypt, (q)uit: ")

    while asking != "q":


        if asking == "e":
            string_to_encrypt = input("\nInput a string to encrypt: ")
            string_to_encrypt_lower = string_to_encrypt.lower()
            encrypted = ""
            check = False
            for i in string_to_encrypt_lower:
                if i.isalnum():
                    encryption = affine_cipher_encryption(i,rotation,ALPHA_NUM)
                    encrypted += encryption


                elif i in PUNCTUATION:
                    encryption = caesar_cipher_encryption(i,rotation,PUNCTUATION)
                    encrypted += encryption


                else:
                    print("\nError with character: " + i)
                    print("Cannot encrypt this string.")
                    check = True

            if check == False:
                print("\nPlain text: " + string_to_encrypt)
                print("\nCipher text: "+ encrypted)


        elif asking == "d":
            string_to_decrypt = input("\nInput a string to decrypt: ")
            decrypted = ""

            check = False
            for i in string_to_decrypt:
                if i.isalnum():
                    decryption = affine_cipher_decryption(i,rotation,ALPHA_NUM)
                    decrypted += decryption

                elif i in PUNCTUATION:
                    decryption = caesar_cipher_decryption(i,rotation,PUNCTUATION)
                    decrypted += decryption

                else:
                    print("\nError with character: " + i)
                    print("Cannot encrypt this string.")
                    check = True

            if check == False:
                print("\nCipher text: " + string_to_decrypt)
                print("\nPlain text: " + decrypted)

        else:
            print(    "\nCommand not recognized.")


        asking = input("\n\nInput a command (e)ncrypt, (d)ecrypt, (q)uit: ")








# These two lines allow this program to be imported into other codes
# such as our function tests code allowing other functions to be run
# and tested without 'main' running.  However, when this program is
# run alone, 'main' will execute.
# DO NOT CHANGE THESE 2 lines or Do NOT add code to them. Everything
# you add should be in the 'main' function above.
if __name__ == '__main__':
    main()

