# Based on code by Howard Eglowstein, Science Buddies, 2014 that was updated by Ben Finio, Science Buddies, 2017

# import libraries sys, time, hashlib, and * from array
import sys
import time
from array import *

# Ask the user if they want to see instructions on what the program is doing
yesno = input("Do you want the program to pause at each step so you have time to read the instructions?(type y or n): ")
if yesno == "no" or yesno == "n" or yesno == "NO" or yesno == "N":
    show_instructions = False
    print("Okay, then once you start the program it will run without pausing.")
else:
    show_instructions = True
    print("Okay, the program will display more information as it runs and pause at each step.")
    input("Press enter to continue.")

# --------------- global variables we expect will be used by any function -----------
#
# a number from 1 to 6 selects which password we'll be trying to guess from
# a selection below.
which_password = 0

# Password here is not the password that is being checked don't change this area of the code
password0 = ""  # remember, do not edit password0 here! scroll down to the "main" function!
password1 = ""
password2 = ""
password3 = ""
password4 = ""
password5 = ""
password6 = ""

# total number of guesses we had to make to find it
totalguesses = 0


# --------------- extra helper functions -------------------
# These will be used by our search routines later on. We'll get these defined and out
# of the way. The actual search program is called "main" and will be the last one
# defined. Once it's defined, the last statement in the file runs it.
# Takes a number from 0 on up and the number of digits we want it to have. It uses that
# number of digits to make a string like "0000" if we wanted 4 or "00000" if we wanted
# 5, converts our input number to a character string, sticks them together and then returns
# the number we started with, with extra zeroes stuck on the beginning. 
def leading_zeroes(n, zeroes):
    t = ("0" * zeroes) + str(n)
    t = t[-zeroes:]
    return t


# This function checks if the MD5 hash value of the password you have guessed equals
# the MD5 hash value of the real password.
def check_userpass(which_password, password):
    global password0, password1, password2, password3
    global password4, password5, password6

    result = False

    if 1 == which_password:
        if password == password0:
            result = True

    if 2 == which_password:
        if password == password1:
            result = True

    if 3 == which_password:
        if password == password2:
            result = True

    if 4 == which_password:
        if password == password3:
            result = True

    if 5 == which_password:
        if password == password4:
            result = True

    if 6 == which_password:
        if password == password5:
            result = True

    if 7 == which_password:
        if password == password6:
            result = True

    return result


# This displays the results of a search including tests per second when possible
def report_search_time(tests, seconds):
    if seconds > 0.000001:
        print("The search took " + make_human_readable(seconds) + " seconds for " + make_human_readable(
            tests) + " tests\n" + make_human_readable(tests / seconds) + " tests per second.")
    else:
        print("The search took " + make_human_readable(seconds) + " seconds for " + make_human_readable(
            tests) + " tests.")
    return


# This function takes in numbers, rounds them to the nearest integer and puts
# commas in to make it more easily read by humans
def make_human_readable(n):
    if n >= 1:
        result = ""
        temp = str(int(n + 0.5))
        while temp != "":
            result = temp[-3:] + result
            temp = temp[:-3]
            if temp != "":
                result = "," + result
    else:
        temp = int(n * 100)
        temp = temp / 100
        result = str(temp)
    return result


# A little helper program to remove any weird formatting in the file
def cleanup(s):
    s = s.strip()
    return s


# A little helper program that capitalizes the first letter of a word
def cap(s: object) -> object:
    s = s.upper()[0] + s[1:]
    return s


# --------------------- password guessing functions ----------------------------
'''
 *** METHOD 1 ***

 search method 1 will try using digits as the password.
 first it will guess 0, 1, 2, 3...9, then it will try 00, 01, 02...99, etc.
'''


def search_method_1(num_digits):
    global totalguesses
    result = False
    a = 0
    # num_digits = 3    # How many digits to try. 1 = 0 to 9, 2 = 00 to 99, etc.
    starttime = time.time()
    tests = 0
    still_searching = True
    print("\nUsing method 1 and searching for " + str(num_digits) + " digit numbers...")
    while still_searching and a < (10 ** num_digits):
        ourguess = leading_zeroes(a, num_digits)
        # uncomment the next line to print each guess, for debugging
        # print(ourguess)
        tests = tests + 1
        totalguesses = totalguesses + 1
        if (check_userpass(which_password, ourguess)):
            print("Success! Password " + str(which_password) + " is " + ourguess)
            still_searching = False  # we can stop now - we found it!
            result = True
        # else:
        # print("Aw Man! "  +  ourguess  +  " is NOT the password.")
        a = a + 1

    seconds = time.time() - starttime
    report_search_time(tests, seconds)
    return result


"""
*** METHOD 2 ***

 search method 2 is a simulation of a letter-style combination lock. Each 'wheel' has the
 letters A-Z, a-z and 0-9 on it as well as a blank. The idea is that we have a number of
 wheels for a user name and password and we try each possible combination.

 Method 2 takes a while to run
"""


def search_method_2(num_pass_wheels):
    global totalguesses
    result = False
    starttime = time.time()
    tests = 0
    still_searching = True
    print("\nUsing method 2 and searching with " + str(num_pass_wheels) + " characters.")
    # going to try all the letters, symbols, and numbers
    wheel = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789~!@#$%^&*()_-+={}[]:<>,./X?"
    # we only allow up to 8 wheels for each password for now
    if (num_pass_wheels > 8):
        print("Unable to handle the request. No more than 8 characters for a password")
        still_searching = False
    else:
        if show_instructions:
            print("WARNING: a brute-force search can take a long time to run!")
            print("Try letting this part of the program run for a while (even overnight).")
            print("Press ctrl + C to stop the program.")
            print("Read the comments in Method 2 of the program for more information.")
            print()

    # set all the wheels to the first position
    pass_wheel_array = array('i', [1, 0, 0, 0, 0, 0, 0, 0, 0])

    while still_searching:
        ourguess_pass = ""
        for i in range(0, num_pass_wheels):  # once for each wheel
            if pass_wheel_array[i] > 0:
                ourguess_pass = wheel[pass_wheel_array[i]] + ourguess_pass
        # Uncomment the next line if you want to see how many guesses are used
        # print("trying [" + ourguess_pass + "]")
        if (check_userpass(which_password, ourguess_pass)):
            print("Success! Password  " + str(which_password) + " is " + ourguess_pass)
            still_searching = False  # we can stop now - we found it!
            result = True
        # else:
        # print ("Aw Man! "  +  ourguess  +  " is NOT the password.")
        tests = tests + 1
        totalguesses = totalguesses + 1

        # spin the rightmost wheel and if it changes, spin the next one over and so on
        carry = 1
        for i in range(0, num_pass_wheels):  # once for each wheel
            pass_wheel_array[i] = pass_wheel_array[i] + carry
            carry = 0
            if pass_wheel_array[i] > 89:
                pass_wheel_array[i] = 1
                carry = 1
                if i == (num_pass_wheels - 1):
                    still_searching = False

    seconds = time.time() - starttime
    report_search_time(tests, seconds)
    return result


"""
*** METHOD 3 ***

search method 3 uses a list of dictionary words. 
"""


def search_method_3(file_name):
    global totalguesses
    result = False

    # Start by reading the list of words into a Python list
    f = open(file_name)
    words = f.readlines()
    f.close()
    # We need to know how many there are
    number_of_words = len(words)
    print()
    print("Using method 3 with a list of " + str(number_of_words) + " words...")

    # Depending on the file system, there may be extra characters before
    # or after the words.
    for i in range(0, number_of_words):
        words[i] = cleanup(words[i])

    # Let's try each one as the password and see what happens
    starttime = time.time()
    tests = 0
    still_searching = True
    word1count = 0  # Which word we'll try next

    while still_searching:
        ourguess_pass = words[word1count]
        # uncomment the next line to print the current guess
        # print("Guessing: " + ourguess_pass)
        # Try it the way it is in the word list
        if (check_userpass(which_password, ourguess_pass)):
            print("Success! Password " + str(which_password) + " is " + ourguess_pass)
            still_searching = False  # we can stop now - we found it!
            result = True
        # else:
        # print ("Aw Man! "  +  ourguess_pass  +  " is NOT the password.")
        tests = tests + 1
        totalguesses = totalguesses + 1
        # Now let's try it with the first letter capitalized
        if still_searching:
            ourguess_pass = ourguess_pass.capitalize()
            # uncomment the next line to print the current guess
            # print("Guessing: " + ourguess_pass)
            if (check_userpass(which_password, ourguess_pass)):
                print("Success! Password " + str(which_password) + " is " + ourguess_pass)
                still_searching = False  # we can stop now - we found it!
                result = True
            # else:
            # print ("Aw Man! "  +  ourguess_pass  +  " is NOT the password.")
            tests = tests + 1
            totalguesses = totalguesses + 1

        # Check it with all the letters capitalized
        if still_searching:
            ourguess_pass = ourguess_pass.upper()
            # uncomment the next line to print the current guess
            # print("Guessing: " + ourguess_pass)
            if (check_userpass(which_password, ourguess_pass)):
                print("Success! Password " + str(which_password) + " is " + ourguess_pass)
                still_searching = False  # we can stop now - we found it!
                result = True
            # else:
            # print ("Aw Man! "  +  ourguess_pass  +  " is NOT the password.")
            tests = tests + 1
            totalguesses = totalguesses + 1

        # Now lets check it with the guess having alternate lower and higher case
        if still_searching:
            # Using list comprehension
            # Alternate cases in String
            ourguess_pass = [ele.upper() if not idx % 2 else ele.lower()
                             for idx, ele in enumerate(ourguess_pass)]
            ourguess_pass = "".join(ourguess_pass)
        # uncomment the next line to print the current guess
        # print("Guessing: " + ourguess_pass)
        if (check_userpass(which_password, ourguess_pass)):
            print("Success! Password " + str(which_password) + " is " + ourguess_pass)
            still_searching = False  # we can stop now - we found it!
            result = True
        # else:
        # print ("Aw Man! "  +  ourguess_pass  +  " is NOT the password.")
        tests = tests + 1
        totalguesses = totalguesses + 1

        # Now lets check it with the words backwards
        if still_searching:
            ourguess_pass = ourguess_pass[::-1]
            # uncomment the next line to print the current guess
            # print("Guessing: " + ourguess_pass)
            if (check_userpass(which_password, ourguess_pass)):
                print("Success! Password " + str(which_password) + " is " + ourguess_pass)
                still_searching = False  # we can stop now - we found it!
                result = True
            # else:
            # print ("Aw Man! "  +  ourguess_pass  +  " is NOT the password.")
            tests = tests + 1
            totalguesses = totalguesses + 1

        word1count = word1count + 1
        if (word1count >= number_of_words):
            still_searching = False

    seconds = time.time() - starttime
    report_search_time(tests, seconds)
    return result


'''
 *** METHOD 4 ***     
 Search method 4 is similar to 3 in that it uses the dictionary, but it tries two
 two words separated by a punctuation character.
'''


def search_method_4(file_name):
    global totalguesses
    result = False

    # Start by reading the list of words into a Python list
    f = open(file_name)
    words = f.readlines()
    # We need to know how many there are
    number_of_words = len(words)

    # Depending on the file system, there may be extra characters before
    # or after the words. 
    for i in range(0, number_of_words):
        words[i] = cleanup(words[i])

    # Let's try each one as the password and see what happens
    starttime = time.time()
    tests = 0
    still_searching = True
    word1count = 0  # Which word we'll try next
    punc_count = 0
    word2count = 0

    punctuation = "~!@#$%^&*()_- + ={}[]:<>,./X?"  # X is a special case where we omit
    # the punctuation to run the words together

    number_of_puncs = len(punctuation)
    print()
    print("Using method 4 with " + str(number_of_puncs) + " punctuation characters and " + str(
        number_of_words) + " words...")

    while still_searching:
        if ("X" == punctuation[punc_count]):
            # If we're at the end of the string and found the 'X', leave it out
            ourguess_pass = words[word1count] + words[word2count]
        else:
            ourguess_pass = words[word1count] + punctuation[punc_count] + words[word2count]
        # uncomment the next line to print the current guess
        # print("Guessing: " + ourguess_pass)
        # Try it the way they are in the word list
        if (check_userpass(which_password, ourguess_pass)):
            print("Success! Password " + str(which_password) + " is " + ourguess_pass)
            still_searching = False  # we can stop now - we found it!
            result = True
        # else:
        # print ("Aw Man! "  +  ourguess_pass  +  " is NOT the password.")
        tests = tests + 1
        totalguesses = totalguesses + 1
        # Now let's try it with the first letter of the first word capitalized
        if still_searching:
            ourguess_pass = cap(words[word1count]) + punctuation[punc_count] + words[word2count]
            # uncomment the next line to print the current guess
            # print("Guessing: " + ourguess_pass)
            if (check_userpass(which_password, ourguess_pass)):
                print("Success! Passwword " + str(which_password) + " is " + ourguess_pass)
                still_searching = False  # we can stop now - we found it!
                result = True
            # else:
            # print ("Aw Man! "  +  ourguess_pass  +  " is NOT the password.")
            tests = tests + 1
            totalguesses = totalguesses + 1
        # Now let's try it with the first letter of the second word capitalized
        if still_searching:
            ourguess_pass = words[word1count] + punctuation[punc_count] + cap(words[word2count])
            # uncomment the next line to print the current guess
            # print("Guessing: " + ourguess_pass)
            if (check_userpass(which_password, ourguess_pass)):
                print("Success! Password " + str(which_password) + " is " + ourguess_pass)
                still_searching = False  # we can stop now - we found it!
                result = True
            # else:
            # print ("Aw Man! "  +  ourguess_pass  +  " is NOT the password.")
            tests = tests + 1
            totalguesses = totalguesses + 1
        # Now let's try it with the both words capitalized
        if still_searching:
            ourguess_pass = cap(words[word1count]) + punctuation[punc_count] + cap(words[word2count])
            # uncomment the next line to print the current guess
            # print("Guessing: " + ourguess_pass)
            if (check_userpass(which_password, ourguess_pass)):
                print("Success! Password " + str(which_password) + " is " + ourguess_pass)
                still_searching = False  # we can stop now - we found it!
                result = True
            # else:
            # print ("Aw Man! "  +  ourguess_pass  +  " is NOT the password.")
            tests = tests + 1
            totalguesses = totalguesses + 1

        word1count = word1count + 1
        if (word1count >= number_of_words):
            word1count = 0
            punc_count = punc_count + 1
            if (punc_count >= number_of_puncs):
                punc_count = 0
                word2count = word2count + 1
                if (word2count >= number_of_words):
                    still_searching = False

    seconds = time.time() - starttime
    report_search_time(tests, seconds)
    return result


'''
 *** METHOD 1&3 ***

 search method 1 & 3 will use a common password number and a number to guess the password
'''


def search_method_1_and_3(file_name, num_digits):
    global totalguesses
    result = False
    a = 0
    # Start by reading the list of words into a Python list
    f = open(file_name)
    words = f.readlines()
    # We need to know how many there are
    number_of_words = len(words)
    print()
    print("Using method 3 with a list of " + str(number_of_words) + " words and " + str(
        num_digits) + " digits of numbers...")

    # Depending on the file system, there may be extra characters before
    # or after the words. 
    for i in range(0, number_of_words):
        words[i] = cleanup(words[i])

    # Let's try each one as the password with a number and see what happens
    starttime = time.time()
    tests = 0
    still_searching = True
    word1count = 0  # Which word we'll try next

    while still_searching:
        # Reset number to zero now that the word is changed
        a = 0
        # Check if the number didn't finish going through all the digits
        while a < (10 ** num_digits):
            ourguess_word = words[word1count]
            ourguess_num = leading_zeroes(a, num_digits)
            ourguess_pass = ourguess_word + str(ourguess_num)
            # uncomment the next line to print the current guess
            # print("Guessing: "+ourguess_word + str(ourguess_num))
            # Try it the way it is in the word list
            if (check_userpass(which_password, ourguess_pass)):
                print("Success! Password " + str(which_password) + " is " + ourguess_pass)
                still_searching = False  # we can stop now - we found it!
                result = True
            # else:
            # print ("Aw Man! " + ourguess_pass + " is NOT the password.")
            tests = tests + 1
            totalguesses = totalguesses + 1
            # Now let's try it with the first letter capitalized with the numbers at the end
            if still_searching:
                ourguess_pass = ourguess_word.capitalize() + str(ourguess_num)
                # uncomment the next line to print the current guess
                # print("Guessing: "+ourguess_pass)
                if (check_userpass(which_password, ourguess_pass)):
                    print("Success! Password " + str(which_password) + " is " + ourguess_pass)
                    still_searching = False  # we can stop now - we found it!
                    result = True
                # else:
                # print ("Aw Man! " + ourguess_pass + " is NOT the password.")
                tests = tests + 1
                totalguesses = totalguesses + 1

            # Check it with all the letters capitalized with the number
            if still_searching:
                ourguess_pass = ourguess_word.upper() + str(ourguess_num)
                # uncomment the next line to print the current guess
                # print("Guessing: "+ourguess_pass)
                if (check_userpass(which_password, ourguess_pass)):
                    print("Success! Password " + str(which_password) + " is " + ourguess_pass)
                    still_searching = False  # we can stop now - we found it!
                    result = True
                # else:
                # print ("Aw Man! " + ourguess_pass + " is NOT the password.")
                tests = tests + 1
                totalguesses = totalguesses + 1

            # Now lets check it with the guess having alternate lower and higher case
            if still_searching:
                # Using list comprehension
                # Alternate cases in String
                ourguess_word = [ele.upper() if not idx % 2 else ele.lower()
                                 for idx, ele in enumerate(ourguess_word)]
                ourguess_word = "".join(ourguess_word)
                # Put the word and the number together
                ourguess_pass = ourguess_word + str(ourguess_num)

                # uncomment the next line to print the current guess
                # print("Guessing: "+ ourguess_pass)
                if (check_userpass(which_password, ourguess_pass)):
                    print("Success! Password " + str(which_password) + " is " + ourguess_pass)
                    still_searching = False  # we can stop now - we found it!
                    result = True
                # else:
                # print ("Aw Man! " + ourguess_pass + " is NOT the password.")
                tests = tests + 1
                totalguesses = totalguesses + 1
                
            # Now lets check it with the words backwards
            if still_searching:
                ourguess_word = ourguessword.lower()
                ourguess_word = ourguess_word[::-1]
                ourguess_pass = ourguess_word + str(ourguess_num)
                # uncomment the next line to print the current guess
                # print("Guessing: "+ourguess_pass)
                if (check_userpass(which_password, ourguess_pass)):
                    print("Success! Password " + str(which_password) + " is " + ourguess_pass)
                    still_searching = False  # we can stop now - we found it!
                    result = True
                # else:
                # print ("Aw Man! " + ourguess_pass + " is NOT the password.")
                tests = tests + 1
                totalguesses = totalguesses + 1
            # Add one to the number and run it again with the same word
            a = a + 1

        word1count = word1count + 1
        if (word1count >= number_of_words):
            still_searching = False

    seconds = time.time() - starttime
    report_search_time(tests, seconds)
    return result


# -------------------------- main function ----------------------------

def main(argv=None):
    global password0, password1, password2, password3
    global password4, password5, password6, totalguesses
    global which_password

    # Here is where you change the passwords
    #Password 1
    password1 = "football"
    #Password 2
    password2 = "pass/star"
    #Password 3
    password3 = "92364829"
    #Password 4
    password4 = "frank834"
    #Password 5
    password5 = "tIwg2s@a""
    # Last two passwords for testing other passwords if wanted
    # Password 6
    password6 = ""
    #Password 7
    password7 = ""

    # start searching
    which_password = 1
    if show_instructions:
        input("\nPress enter to start the program.")
        print()
        print("This program will use several different algorithms to try and guess passwords.")
        print()
    which_password = int(input("Which password do you want to try to guess (1-7)? "))

    if show_instructions:
        print()
        print("The program will now automatically try to guess the password using several different methods:")
        print()
        print("Method 1 will only guess digits 0-9.")
        print("Method 2 will guess digits 0-9 as well as letters a-z and A-Z and symbols like ^#(@.")
        print("Method 3 will guess using a list of common passwords.")
        print("Method 4 will try combinations of common words with punctuation in between them.")
        print("Method 1 and 3 will guess using a list of common passwords followed by numbers.")
        # Press enter
        input("\nPress enter to continue.\n")

    overallstart = time.time()
    foundit = False
    print("Trying to guess password " + str(which_password) + "...")
    # Look through our list of common passwords first
    if not foundit:
        foundit = search_method_3("passwords.txt")
    # Still looking? Let's combine the common passwords 2 at a time
    if not foundit:
        print("Method 3 did not work!")
        if show_instructions:
            input("Press enter to continue.")
        foundit = search_method_4("passwords.txt")
    # Still looking? See if it's a single digit
    if not foundit:
        print("Method 4 did not work!")
        if show_instructions:
            input("Press enter to continue.")
        foundit = search_method_1(1)
    # Still looking? See if it's a 2 digit number
    if not foundit:
        print("Method 1 (1 digit) did not work!")
        if show_instructions:
            input("Press enter to continue.")
        foundit = search_method_1(2)
    # Still looking? See if it's a 3 digit number
    if not foundit:
        print("Method 1 (2 digit) did not work!")
        if show_instructions:
            input("Press enter to continue.")
        foundit = search_method_1(3)
    # Still looking? See if it's a 4 digit number
    if not foundit:
        print("Method 1 (3 digit) did not work!")
        if show_instructions:
            input("Press enter to continue.")
        foundit = search_method_1(4)
    # Still looking? Use words with numbers
    if not foundit:
        print("Method 1 (4 digits) didn't work!")
        if show_instructions:
            input("Press enter to continue.")
        foundit = search_method_1_and_3('passwords.txt', 1)
    if not foundit:
        print("Method 1 and 3 (1 digit) didn't work!")
        if show_instructions:
            input("Press enter to continue.")
        foundit = search_method_1_and_3('passwords.txt', 2)
    if not foundit:
        print("Method 1 and 3 (2 digits) didn't work!")
        if show_instructions:
            input("Press enter to continue.")
        foundit = search_method_1_and_3('passwords.txt', 3)
    if not foundit:
        print("Method 1 and 3 (3 digits) didn't work!")
        if show_instructions:
            input("Press enter to continue.")
        foundit = search_method_1_and_3('passwords.txt', 4)

    # Still looking? Use our rotary wheel simulation up to 6 wheels.
    # This should take care of any 5 digit number as well as letter
    # combinations up to 6 characters
    if not foundit:
        print("Method 1 and 3 (3 digits) didn't work!")
        if show_instructions:
            input("Press enter to continue.")
        foundit = search_method_2(6)
    # Still looking? Try 7 digit numbers
    if not foundit:
        print("Method 2 (6 digits) did not work!")
        if show_instructions:
            input("Press enter to continue.")
        foundit = search_method_1(7)
    # Still looking? Try 8 digit numbers
    if not foundit:
        print("Method 2 (7 digits) did not work!")
        if show_instructions:
            input("Press enter to continue.")
        foundit = search_method_1(8)
    seconds = time.time() - overallstart
    if (seconds < 0.00001):
        print("The total search for all methods took " + make_human_readable(
            seconds) + " seconds and " + make_human_readable(totalguesses) + " guesses.")
        print("(on some machines, Python doesn't know how long things actually took)")
    else:
        print("The total search for all methods took " + make_human_readable(
            seconds) + " seconds and " + make_human_readable(totalguesses) + " guesses.(" + make_human_readable(
            totalguesses / seconds) + " guesses per second)")
    print()
    if foundit:
        print("Lets goooo! \nThe password has been correctly guessed")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
