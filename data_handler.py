import string
import random


def get_data():
    with open('sample_data/question.csv', "r") as file:
        file_in_list = "".join(file.readlines()).split("\n")
        data_to_return = [item.split(";") for item in file_in_list]
        data_to_return.pop(-1)
        return data_to_return


def get_answers():
    with open('sample_data/answer.csv', "r") as file:
        file_in_list = "".join(file.readlines()).split("\n")
        file_in_matrix = [item.split(";") for item in file_in_list]
        file_in_matrix.pop(-1)
        return {item[0]: item[1:] for item in file_in_matrix}


def add_answers(id_, answer, table):
    if id_ in table.keys():
        table[id_].append(answer)
    else:
        table[id_] = [answer]
    with open('sample_data/answer.csv', "w") as file:
        for key, value in table.items():
            line = ";".join([key] + value)
            file.write(line + "\n")


def save_data(data):
    with open('sample_data/question.csv', "w") as file:
        for inner_list in data:
            line = ";".join(inner_list)
            file.write(line + "\n")


def get_row_by_id(table, id_):
    row_we_want = None

    for row in table:
        if str(row[0]) == str(id_):
            row_we_want = row

    return row_we_want


def get_list_from_dict(table, id_):
    if id_ in table.keys():
        return table[id_]
    else:
        return []


def add_element(list_to_save):
    with open('sample_data/question.csv', "a") as file:
        file.write(";".join(list_to_save) + "\n")


def edit_element(updated_list, table):
    return [updated_list if inner_list[0] == updated_list[0] else inner_list for inner_list in table]


def remove_element(table, id_):
    return [inner_list for inner_list in table if inner_list[0] != id_]


def generate_id(table):
    while True:
        random_id = "##" + str(random.randint(1, 99)) + random.choice(string.ascii_lowercase)
        if random_id not in [inner_list[0] for inner_list in table]:
            return random_id


def sort_columns(table, num, dir_):
    reverse_ = True
    if dir_ == "asc":
        reverse_ = False
    return sorted(table, key=lambda x: x[int(num)], reverse=reverse_)

