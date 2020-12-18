import re
from bs4 import BeautifulSoup
import requests

def run_scraper():
    print_opening()
    lists = []
    lists = get_letter_lists()
    choice = input("Enter 1 to play yesterday's puzzle, or enter 2 for solutions to today's puzzle: ")
    while(choice != "1" and choice != "2"):
        choice = input("Please enter either 1 or 2 to continue: ")
    if(choice == "1"):
        yesterday_puzzle(lists[1])
    else:
        today_puzzle(lists[0])   

def yesterday_puzzle(list):
    print()
    letters = ""
    for character in list:
        if(character != '"' and character != ',' and character != " "):
            letters = letters + character
    print("Yesterday's letters, with the center letter first, are: " + letters)
    print()
    answer_list = get_yesterdays_words()
    play_game(letters, answer_list)

def play_game(letters, answer_list):
    print("If at any point you give up, please type 'i give up'")
    all_words_found = False
    words_found = []
    points = 0
    players_input = ""
    while(all_words_found == False and players_input != 'i give up'):
        print("These are the words you have found so far: " + str(words_found))
        print("Score: " + str(points))
        print("Today's letters are: " + letters)
        players_input = input("Enter your word: ")
        if(players_input in answer_list and players_input not in words_found):
           words_found.append(players_input)
           points = points + get_points(players_input, letters)
        if(all(word in words_found for word in answer_list)):
            all_words_found = True
            print("You found all the words!") 
    if(players_input == 'i give up'):
        print("You found " + str(len(words_found)) + " out of " + str(len(answer_list)) + " words!")
        print("These are the words: " + str(answer_list))

def get_points(word, letters):
    if(all(letter in word for letter in letters)):
        print()
        print(word + " is a pangram!")
        return len(word) + 7
    else:
        if len(word) == 4:
            return 1
        else: 
            return len(word)
 
def today_puzzle(list):
    print()
    letters = ""
    for character in list:
        if(character != '"' and character != ',' and character != " "):
            letters = letters + character
    print("Today's letters, with the center letter first, are: " + letters)
    print()
    print("The list of words from our database is as follows:")
    print()
    get_today_puzzle_word_list(letters) 

def get_today_puzzle_word_list(letters):
    all_words = set(open('words_alpha.txt').read().split())
    word_set = set()
    for word in all_words:
        if len(word) > 3 and letters[0] in word and all([letter in letters for letter in word])    :
            word_set.add(word)
    for word in word_set:
        print(word)
    print("The number of words found is: " + str(len(word_set)))

def get_letter_lists():
    url = "https://www.nytimes.com/puzzles/spelling-bee"
    r = requests.get(url)
    data = r.text
   
    soup = BeautifulSoup(data, 'html.parser')
    lines = soup.get_text()
    letter_lists = []
    for i in range(len(lines)):
        if(lines[i] == 'v' and lines[i+1] == 'a' and lines[i+2] == 'l' and lines[i+3]=='i' and lines[i+4] == 'd' and lines[i+5]=="L"):
            list = lines[i+15:i+42]
            letter_lists.append(list)
    return letter_lists

def get_yesterdays_words():
    url = "https://www.nytimes.com/puzzles/spelling-bee"
    r = requests.get(url)
    data = r.text
   
    soup = BeautifulSoup(data, 'html.parser')
    lines = soup.get_text()
    yesterday_word_list = []
    answers_list_start = 0
    for i in range(len(lines)):
        if(lines[i] == 'a' and lines[i+1] == 'n' and lines[i+2] == 's' and lines[i+3] == 'w'):
            answers_list_start = i + 7
    index = answers_list_start + 4
    answers_list = []
    while(lines[index] != ']'):
        answers_list.append(lines[index])
        index = index + 1
    answers_list = [x for x in answers_list if x != '"']
    final_answers = []
    word = ""
    for character in answers_list:
        if character != ',':
            word = word + character
        else:
            final_answers.append(word)
            word = ""
    final_answers.append(word)
    add_words_to_dictionary(final_answers)
    return final_answers

def add_words_to_dictionary(answers_from_yesterday):
    all_words = set(open('words_alpha.txt').read().split())
    file = open('words_alpha.txt', 'a')
    for word in answers_from_yesterday:
        if not word in all_words:
           file.write("\n" + word) 

def print_opening():
    print()
    print("Welcome to the NYTimes Spelling Bee!")
    print()
    print("This app can set up yesterday's puzzle using the official")
    print()
    print("word list from the NYTimes,")
    print()
    print("Or, it can give a list of words from our database to solve the current puzzle!")
    print()

run_scraper()
