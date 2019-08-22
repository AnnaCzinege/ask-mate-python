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
        if str(row[0]) == str(id_):
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
    while True:
        random_id = "##" + str(random.randint(1, 99)) + random.choice(string.ascii_lowercase)
        if random_id not in [inner_list[0] for inner_list in table]:
            return random_id
