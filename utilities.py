def read_line(line_arr):
    line = ""
    for word in line_arr[:-1]:
        line += word + " "
    return line[:-1]

def read_lines(filename):
    with open(filename, 'r') as file:
         input_lines = [line.strip() for line in file]
    return input_lines

def select_lines(input_lines, start_index, num_lines):
    arr = []
    for i in range(num_lines):
        arr.append(input_lines[start_index + i])
    return arr

def read_responses():
    input_lines = read_lines('quotes.txt')
    index = 0
    responses = {}
    while (index < len(input_lines)):
        line_arr = input_lines[index].split(' ')
        response_length = int(line_arr[-1])
        key = read_line(line_arr).lower()
        responses[key] = select_lines(input_lines, index + 1, response_length)
        index = index + response_length + 1
    return responses

def read_character_quotes(character_list):
    for character in character_list:
        input_lines = read_lines('characters/'+ character + '.txt')

def read_character_aliases():
    input_lines = read_lines('characters/characters.txt')
    index = 0
    aliases = {}
    while (index < len(input_lines)):
        line_arr = input_lines[index].split(' ')
        num_aliases = int(line_arr[-1])
        key = read_line(line_arr).lower()
        lines = select_lines(input_lines, index, num_aliases)
        lines[0] = lines[0][:-2]
        for line in lines:
            aliases[line.lower()] = key
        index = index + num_aliases
    return aliases
