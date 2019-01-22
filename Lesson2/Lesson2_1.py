import re
import csv

# @dikkini
def get_data():
    file_list = ["info_1.txt", "info_2.txt", "info_3.txt"]
    main_data = [["Изготовитель системы", "Название ОС", "Код продукта", "Тип системы"]]
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []

    os_prod_com = re.compile("(?<=Изготовитель системы:).*")
    os_name_com = re.compile("(?<=Название ОС:).*")
    os_code_com = re.compile("(?<=Код продукта:).*")
    os_type_com = re.compile("(?<=Тип системы:).*")

    for fi in file_list:
        with open(fi, encoding='windows-1251') as info:
            for iline in info:
                find = os_prod_com.search(iline)
                if find is not None:
                    os_prod_list.append(find[0].strip())

                find = os_name_com.search(iline)
                if find is not None:
                    os_name_list.append(find[0].strip())

                find = os_code_com.search(iline)
                if find is not None:
                    os_code_list.append(find[0].strip())

                find = os_type_com.search(iline)
                if find is not None:
                    os_type_list.append(find[0].strip())

    for i in range(len(os_prod_list)):
        main_data.append([os_prod_list[i], os_name_list[i], os_code_list[i], os_type_list[i]])

    return main_data


def write_to_csv():
    with open('main_data.csv', 'w') as f_n:
        f_n_writer = csv.writer(f_n)
        for row in get_data():
            f_n_writer.writerow(row)


write_to_csv()
