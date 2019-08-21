import csv


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
        if int(row[0]) == id_:
            row_we_want = row

    return row_we_want


def append_table(table, row):
    with open(table, mode="a") as file:
        row_writer = csv.writer(file, delimiter=";", lineterminator="\n")
        row_writer.writerow(row)


def update_row_in_table_by_id(table, row, id_):
    table[id_-1] = row
    with open(TABLE, mode="w") as file:
        row_writer = csv.writer(file, delimiter=";", lineterminator="\n")
        for actual_row in table:
            row_writer.writerow(actual_row)
