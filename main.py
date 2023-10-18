'''
    Data structure in the txt-files
    
    'english_word' / 'русский_аналог_вар._1', 'русский_аналог_вар._2', ...
    ...
    # - lessons delimiter
    'english_word' / 'русский_аналог_вар._1', 'русский_аналог_вар._2', ...
    ...
    
    Data structure in the script
    
    words_dictionary = {
            1: ['e_ver', ['r_ver_1', 'r_ver_2', ...]],
            2: [...],
            ...
        }
    
    lessons_structure = {
            1:[1,5],
            ...
        }
'''

import random

def init_data(file_name):
    dictionary = {}
    lessons = {}
    with open(file_name, "r", encoding='utf-8') as words_file:
        word_id = 1
        lesson_id = 1
        lesson_words_id = []

        for line in words_file.readlines():
            if line == '\n':
                continue
            elif line.strip() == '#':
                lessons[lesson_id] = lesson_words_id
                lesson_id += 1
                lesson_words_id = []
                continue
            else:
                lesson_words_id.append(word_id)
                e_v_word, r_v_words = line.split(sep='/')
                e_v_word = e_v_word.strip()
                r_v_words = list(map(lambda x: x.strip(), r_v_words.split(sep=',')))
                dictionary[word_id] = [e_v_word, r_v_words]
                word_id += 1

        lessons[lesson_id] = lesson_words_id
    return dictionary, lessons

def words_generator(words_dictionary, curr_key, mode):
    if mode == 'e -> r':
        init_word = words_dictionary[curr_key][0]
        trans_words = words_dictionary[curr_key][1]
        trans_words_str = ''
        for i in trans_words:
            trans_words_str += i
            trans_words_str += ', '
        trans_words_str = trans_words_str[:-2]
        output_str = f'{init_word} - {trans_words_str}\n'
    elif mode == 'r -> e':
        init_word = random.sample(words_dictionary[curr_key][1], 1)[0]
        trans_word = words_dictionary[curr_key][0]
        output_str = f'{init_word} - {trans_word}\n'

    next_step = str(input(init_word.upper()))
    print(output_str)
    return next_step

print("Hello!\nIt's the programm for learning english words and stable expressions\nDeveloper: Anshin V.S., ver 1.0\n")
while True:
    mode_1 = input("Select word's type. Single word - don't enter symbol, Expressions - enter any symbol: ")
    if mode_1:
        mode1 = 'stable expressions'
    else:
        mode1 = 'words'
    print('\n')
    
    mode_2 = input("Select sample size. All words - don't enter symbol, Last lesson's words - enter any symbol: ")
    if mode_2:
        mode2 = "last lesson's words"
    else:
        mode2 = 'all words'
    print('\n')
    
    mode_3 = input("Select direction of translation. Rus -> Eng - don't enter symbol, Eng -> Rus - enter any symbol: ")
    if mode_3:
        mode3 = 'e -> r'
    else:
        mode3 = 'r -> e'
    
    
    words_dictionary, lessons = None, None

    if mode1 == 'words':
        words_dictionary, lessons = init_data('words.txt')
    elif mode1 == 'stable expressions':
        words_dictionary, lessons = init_data('stable_expressions.txt')

    if mode2 == 'all words':
        words_keys_list = list(words_dictionary.keys())
    elif mode2 == "last lesson's words":
        words_keys_list = lessons[max(list(lessons.keys()))]

    print("\nDo you wish next word? Yes - don't enter symbol, No - enter any symbol")
    while True:
        curr_key = random.sample(words_keys_list, 1)[0]
        next_step = words_generator(words_dictionary, curr_key, mode3)
        if next_step:
            print('You have rebooted the programm! Please, select modes.')
            break


