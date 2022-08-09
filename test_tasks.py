import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from pyexcelerate import Workbook


# Создание DataFrame
def create_dataframe():
    data = {"id": [1, 2, 3, 4, 5, 6, 7],
            "Name": ["Alex", "Justin", "Set", "Carlos", "Gareth", "John", "Bob"],
            "Surname": ["Smur", "Forman", "Carey", "Carey", "Chapman", "James", "James"],
            "Age": [21, 25, 35, 40, 19, 27, 25],
            "Job": ["Python Developer", 
                    "Java Developer", 
                    "Project Manager", 
                    "Enterprise Architect", 
                    "Python Developer", 
                    "IOS Developer", 
                    "Python Developer"],
            "Datetime": [datetime(2022, 1, 1, 9, 45, 12), 
                         datetime(2022, 1, 1, 11, 50, 25), 
                         datetime(2022, 1, 1, 10, 0, 45), 
                         datetime(2022, 1, 1, 9, 7, 36), 
                         datetime(2022, 1, 1, 11, 54, 10), 
                         datetime(2022, 1, 1, 9, 56, 40), 
                         datetime(2022, 1, 1, 9, 52, 45)]}
    df = pd.DataFrame(data, index=None)
    return df


# Добавление нового столбца и фильтрация данных
def between_18_and_21():
    table = create_dataframe()
    time = []
    jobs = table["Job"].tolist()
    ages = table["Age"].tolist()
    for i in range(len(jobs)):
        if "Developer" in jobs[i] and (18 < ages[i] <= 21):
            time.append("09:00")
        elif "Developer" in jobs[i] and ages[i] >= 21:
            time.append("09:15")
        else:
            time.append(None)
    table["TimeToEnter"] = time
    create_excel(table, "between_18_and_21")
    connect_mongodb(table, "18MoreAnd21andLess")
    return table


# Добавление нового столбца и фильтрация данных
def more_or_equal_35():
    table = create_dataframe()
    time = []
    jobs = table["Job"].tolist()
    ages = table["Age"].tolist()
    for i in range(len(jobs)):
        if ("Developer" in jobs[i] or "Manager" in jobs[i]) and ages[i] >= 35:
            time.append("11:00")
        else:
            time.append("11:30")
    table["TimeToEnter"] = time
    create_excel(table, "more_or_equal_35")
    connect_mongodb(table, "35AndMore")
    return table


# Добавление нового столбца и фильтрация данных
def architects_time():
    table = create_dataframe()
    time = []
    jobs = table["Job"].tolist()
    for i in range(len(jobs)):
        if "Architect" in jobs[i]:
            time.append("10:30")
        else:
            time.append("10:10")
    table["TimeToEnter"] = time
    create_excel(table, "architects_time")
    connect_mongodb(table, "ArchitectEnterTime")
    return table


# Создание excel файла
def create_excel(dataframe, filename):
    table = dataframe
    data = []
    titles = []
    for title in table:
        titles.append(title)
    data.append(titles)
    for i in range(len(table)):
        row = []
        for value in table.loc[i]:
            if str(value).isnumeric():
                row.append(value)
            else:
                row.append(str(value))
        data.append(row)
    wb = Workbook()
    wb.new_sheet('task', data=data)
    wb.save(f'{filename}.xlsx')


# Подключение к mongodb, создание коллекции и добавление данных в неё
def connect_mongodb(dataframe, collection_name):
    cluster = MongoClient("mongodb+srv://user:password@cluster0.cm4dtfz.mongodb.net/?retryWrites=true&w=majority")
    db = cluster["workers"]
    collection = db[collection_name]
    table = dataframe
    data = []
    for i in range(len(table)):
        row = []
        for value in table.loc[i]:
            row.append(str(value))
        collection.insert_one({"Id": row[0], 
                               "Name": row[1], 
                               "Surname": row[2], 
                               "Age": row[3], 
                               "Job": row[4], 
                               "Datetime": row[5], 
                               "TimeToEnter": row[6]})


between_18_and_21()
more_or_equal_35()
architects_time()
