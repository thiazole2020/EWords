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


def init_data(file_name, main_sep, less_sep, syn_sep, encoding_type='utf-8'):
    dictionary = {}
    lessons = {}
    with open(file_name, "r", encoding=encoding_type) as words_file:
        word_id = 1
        lesson_id = 1
        lesson_words_id = []

        for line in words_file.readlines():
            if line == '\n':
                continue
            elif line.strip() == less_sep:
                lessons[lesson_id] = lesson_words_id
                lesson_id += 1
                lesson_words_id = []
                continue
            else:
                lesson_words_id.append(word_id)
                e_v_word, r_v_words = line.split(sep=main_sep)
                e_v_word = e_v_word.strip()
                r_v_words = list(map(lambda x: x.strip(), r_v_words.split(sep=syn_sep)))
                dictionary[word_id] = [e_v_word, r_v_words]
                word_id += 1

        lessons[lesson_id] = lesson_words_id
    return dictionary, lessons


def output_expression_gen(input_data):
    return f'{input_data}\n'


def words_generator(words_dictionary, curr_key, mode, start_comm_sep, end_comm_sep):
    if mode == 'e -> r':
        init_word = words_dictionary[curr_key][0]
        trans_words = words_dictionary[curr_key][1]
        trans_words_str = ''
        for i in trans_words:
            trans_words_str += i
            trans_words_str += ', '
        trans_words_str = trans_words_str[:-2]
        output_str = output_expression_gen(trans_words_str)
    elif mode == 'r -> e':
        init_word = random.sample(words_dictionary[curr_key][1], 1)[0]
        trans_word = words_dictionary[curr_key][0]
        output_str = output_expression_gen(trans_word)

    answ_str = ''
    upper = False
    for i in init_word:
        if i == start_comm_sep:
            upper = True
        elif i == end_comm_sep:
            upper = False

        if upper:
            answ_str += i.lower()
        else:
            answ_str += i.upper()

    next_step = str(input(answ_str))
    print(output_str)
    return next_step


# SETTINGS
words_dictionary, lessons = None, None
mode1_dict = {
    'words': 'words.txt',
    'stable expressions': 'stable_expressions.txt',
    'prepositions': 'prepositions.txt',
}
separator_dict = {
    'main_sep': '/',
    'lesson_sep': '#',
    'syn_sep': ',',
    'start_comm_sep': '(',
    'end_comm_sep': ')',
}
encoding_type = 'utf-8'

# MAIN CODE
print("Hello!\nIt's the program for improve your English!\nDeveloper: Anshin V.S., ver 1.1\n")
while True:
    mode_1 = input("Select word's type.\n"
                   "Input a character to continue.\n"
                   "'1' or nothing      - single word;\n"
                   "'2' or any string   - stable expressions;\n"
                   "'3'                 - prepositions.\n:")
    if mode_1:
        if mode_1.strip() == '1':
            mode1 = 'words'
        elif mode_1.strip() == '3':
            mode1 = 'prepositions'
        else:
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

    words_dictionary, lessons = init_data(mode1_dict[mode1], separator_dict['main_sep'],
                                          separator_dict['lesson_sep'], separator_dict['syn_sep'], encoding_type)

    if mode2 == 'all words':
        words_keys_list = list(words_dictionary.keys())
    elif mode2 == "last lesson's words":
        words_keys_list = lessons[max(list(lessons.keys()))]

    print("\nDo you wish next word? Yes - don't enter symbol, No - enter any symbol")
    init_key = min(words_keys_list)
    finall_key = max(words_keys_list)
    while True:
        curr_key = random.randint(init_key, finall_key)
        next_step = words_generator(words_dictionary, curr_key, mode3,
                                    separator_dict['start_comm_sep'], separator_dict['end_comm_sep'])
        if next_step:
            print('You have rebooted the program! Please, select modes.')
            break
