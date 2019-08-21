def get_data(data):
    with open(data, "r") as file:
        file_in_list = "".join(file.readlines()).split("\n")
        data_to_return = [item.split(";") for item in file_in_list]
        data_to_return.pop(-1)
        return data_to_return


def save_data(data):
    with open("data.csv", "w") as file:
        for inner_list in data:
            line = ";".join(inner_list)
            file.write(line + "\n")