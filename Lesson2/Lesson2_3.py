import yaml

dict = {
    "list": ["Изготовитель системы", "Название ОС", "Код продукта", "Тип системы"],
    "quantity": 4,
    "dict2": {"Я": 1071, "Ч": 1063, "Ю": 1070, "Б":1041 }
}

with open('file.yaml', 'w') as f_n:
    yaml.dump(dict, f_n, default_flow_style=False, allow_unicode = True)

with open('file.yaml', encoding="utf-8") as f_n:
    print(f_n.read())
