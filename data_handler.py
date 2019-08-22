import string
import random


def get_data(text):
    with open(text, "r") as file:
        file_in_list = "".join(file.readlines()).split("\n")
        data_to_return = [item.split(";") for item in file_in_list]
        data_to_return.pop(-1)
        return data_to_return


def save_data(text, data):
    with open(text, "w") as file:
        for inner_list in data:
            line = ";".join(inner_list)
            file.write(line + "\n")


def get_row_by_id(table, id_):
    row_we_want = None

    for row in table:
        if row[0] == id_:
            row_we_want = row

    return row_we_want


def add_element(text, list_to_save):
    with open(text, "a") as file:
        file.write(";".join(list_to_save) + "\n")


def edit_element(updated_list, table):
    return [updated_list if inner_list[0] == updated_list[0] else inner_list for inner_list in table]


def remove_element(table, id_):
    return [inner_list for inner_list in table if inner_list[0] != id_]


def generate_id(table):
    random_id = table[0][0]
    while random_id in [inner_list[0] for inner_list in table]:
        random_id = "##" + str(random.randint(1, 99)) + random.choice(string.ascii_lowercase)
    return random_id



