'''
    Data structure in the txt-files
    'english_word' / 'русский_аналог_вар._1', 'русский_аналог_вар._2', ...
    ...
    # - lessons delimiter
    'english_word' / 'русский_аналог_вар._1', 'русский_аналог_вар._2', ...
    ...

    Data structure in the txt-files for irregular verbs
    'english_word'*'irregular_form_1'*'irregular_form_2' / 'русский_аналог_вар._1', 'русский_аналог_вар._2', ...

    Data structure in the script
        words_dictionary = {
            1: ['e_ver', ['r_ver_1', 'r_ver_2', ...], ['irr_form_1',  'irr_form_2', ...]],
            2: [...],
            ...
        }
    
        lessons_structure = {
                1:[1,5],
                ...
            }
'''

import random


def init_data(file_name, main_sep, less_sep, syn_sep, irr_verb_sep,
              encoding_type='utf-8', start_dictionary=None, start_word_id=1):
    if start_dictionary is None:
        dictionary = {}
    else:
        dictionary = start_dictionary
    lessons = {}
    with open(file_name, "r", encoding=encoding_type) as words_file:
        word_id = start_word_id
        lesson_id = 1
        lesson_words_id = []

        for line in words_file.readlines():
            if line.strip() == '\n' or line.strip() == '':
                continue
            elif line.strip() == less_sep:
                lessons[lesson_id] = lesson_words_id
                lesson_id += 1
                lesson_words_id = []
                continue
            else:
                lesson_words_id.append(word_id)
                e_v_word, r_v_words = line.split(sep=main_sep)
                e_v_word_forms = string_sep(e_v_word, irr_verb_sep)
                e_v_word = e_v_word_forms[0]
                e_v_word_irr_forms = e_v_word_forms[1:]

                r_v_words = string_sep(r_v_words, syn_sep)

                dictionary[word_id] = [e_v_word, r_v_words, e_v_word_irr_forms]
                word_id += 1

        lessons[lesson_id] = lesson_words_id
    return dictionary, lessons, word_id


def output_expression_gen(input_str):
    return f'{input_str}\n'


def string_sep(input_data, sep):
    return list(map(lambda x: x.strip(), input_data.split(sep=sep)))


def irr_forms_str_gen(irr_forms_list):
    irr_forms_str = ' - '
    for i in irr_forms_list:
        irr_forms_str += f'{i} - '
    return irr_forms_str[:-3]


def words_generator(words_dictionary, curr_key, mode, start_comm_sep, end_comm_sep, irr_forms=False):
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
        if irr_forms:
            irr_forms_str = irr_forms_str_gen(words_dictionary[curr_key][2])
        else:
            irr_forms_str = ''
        trans_word = words_dictionary[curr_key][0] + irr_forms_str
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

def print_dict(words_dictionary, init_key, finall_key, irr_form=False):
    for i in range(init_key, finall_key+1):
        russian_str = ''
        irr_form_str = ''
        for j in words_dictionary[i][1]:
            russian_str += f'{j}, '
        if irr_form:
            for j in words_dictionary[i][2]:
                irr_form_str += f'/{j}'
        print(f'> {words_dictionary[i][0]}{irr_form_str} - {russian_str[:-2]}')


# SETTINGS
words_dictionary, lessons = None, None
mode1_dict = {
    'words': ['words.txt'],
    'stable expressions': ['stable_expressions.txt'],
    'prepositions': ['prepositions.txt'],
    'irregular verbs': ['irregular_verbs.txt'],
    'oppression mode': ['words.txt', 'stable_expressions.txt', 'prepositions.txt']
}
separator_dict = {
    'main_sep': '/',
    'lesson_sep': '#',
    'syn_sep': ',',
    'start_comm_sep': '(',
    'end_comm_sep': ')',
    'irr_verb_sep': '*',
}
encoding_type = 'utf-8'
console_command = {
    'all_words_in_dict': 'ALL*',
    'all_words_in_last_lessons': 'ALL',
}

# MAIN CODE
print("Hello!\nIt's the program for improve your English!\nDeveloper: Anshin V.S., ver 1.3\n")
while True:
    mode_1 = input("Select word's type.\n"
                   "Input a character to continue.\n"
                   "'1' or nothing    - single word;\n"
                   "'2' or any string - stable expressions;\n"
                   "'3'               - prepositions;\n"
                   "'4'               - irregular verbs;\n>"
                   "'5'               - oppression mode.\n>")
    irr_forms = False
    select_over_mode = True
    if mode_1:
        mode_1 = mode_1.strip()
        if mode_1 == '1':
            mode1 = 'words'
        elif mode_1 == '3':
            mode1 = 'prepositions'
        elif mode_1 == '4':
            mode1, mode2, mode3 = 'irregular verbs', 'all words', 'r -> e'
            irr_forms = True
            select_over_mode = False
        elif mode_1 == '5':
            mode1, mode2, mode3 = 'oppression mode', 'all words', 'r -> e'
            select_over_mode = False
        else:
            mode1 = 'stable expressions'
    else:
        mode1 = 'words'
    print('\n')

    if select_over_mode:
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

    word_id = 1
    dictionary = None
    for i in mode1_dict[mode1]:
        dictionary, lessons, word_id = init_data(i, separator_dict['main_sep'],
                                              separator_dict['lesson_sep'], separator_dict['syn_sep'],
                                              separator_dict['irr_verb_sep'], encoding_type,
                                              start_dictionary=dictionary, start_word_id=word_id)
    words_dictionary = dictionary

    if mode2 == 'all words':
        words_keys_list = list(words_dictionary.keys())
    elif mode2 == "last lesson's words":
        words_keys_list = lessons[max(list(lessons.keys()))]

    print("Next word - don't enter any symbol\n"
          f"Show last lesson's dictionary - enter '{console_command['all_words_in_last_lessons']}'\n"
          f"Show whole dictionary - enter '{console_command['all_words_in_dict']}'\n"
          "Reboot program - enter any other string")
    last_lesson_init_key = min(lessons[max(list(lessons.keys()))])
    init_key = min(words_keys_list)
    finall_key = max(words_keys_list)

    while True:
        curr_key = random.randint(init_key, finall_key)
        next_step = words_generator(words_dictionary, curr_key, mode3,
                                    separator_dict['start_comm_sep'], separator_dict['end_comm_sep'], irr_forms)
        if next_step:
            input_command = next_step.strip().upper()
            if input_command == console_command['all_words_in_last_lessons']:
                print_dict(words_dictionary, last_lesson_init_key, finall_key, irr_forms)
            elif input_command == console_command['all_words_in_dict']:
                print_dict(words_dictionary, 1, finall_key, irr_forms)
            else:
                print('You have rebooted the program! Please, select modes.')
                break
