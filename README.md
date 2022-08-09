# Тестовое задание
Работа с базой данных и Python
# Установка и запуск
1. Вам нужно клонировать данный репозиторий\
`git clone https://github.com/18BD/Data-Engineer-test-task.git`
2. После клонирования проекта вам также необходимо установить зависимости с помощью команды pip install -r requirements.txt из корневой папки проекта\
`pip install -r requirements.txt`
3. Для запуска откройте командную строку в корневой папке проекта и выполните следующую команду\
`python test_tasks.py`\
(Для корректной работы скрипта нужно подключиться к своей базе MongoDB в функции connect_mongo())
# Функции
- create_dataframe()
```python
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
```
Данная функция создаёт DataFrame используя библиотеку pandas
- create_excel()
```python
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
```
Данная функция принимает два параметра и конвертирует полученный из параметра 'dataframe' DataFrame в Excel (xlsx формат) с названием параметра filename через библиотеку pyexcelerate\
![alt text](https://i.imgur.com/dBuRSXr.png)
- connect_mongodb()
```python
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
```
(В переменной cluster изменить ссылку для подключения к базе данных на свою)\
Данная функция принимает два параметра и через библиотеку pymongo создаёт новую коллекцию с названием параметра collection_name и записывает туда тот основной DataFrame полученный из параметра dataframe\
![alt text](https://i.imgur.com/jEmXNJT.png)
- between_18_and_21()
```python
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
```
Данная функция добавляет новый столбец 'TimeToEnter' куда записывает время, во сколько должен приходить тот или иной сотрудник, создаёт excel файл с названием функции, а также создаёт коллекцию в mongodb с названием '18MoreAnd21andLess' и добавляет в неё данные из созданного DataFrame\
В функции указано условие, что те, кто работают в отделе Разработки(Developers) и те кому больше 
18 лет и меньше или равно 21, должны приходить ровно 09.00 каждое 
утро, а остальные работники, которые работают в отделе Разработки
(Developers) они могут опаздывать максимум на 15 минут 
- more_or_equal_35()
```python
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
```
Данная функция добавляет новый столбец 'TimeToEnter' куда записывает время, во сколько должен приходить тот или иной сотрудник, создаёт excel файл с названием функции, а также создаёт коллекцию в mongodb с названием '35AndMore' и добавляет в неё данные из созданного DataFrame\
В функции указано условие, что те кто работают в отделе помимо Разработки(Developers) и 
Менеджмент(Managers) и те кому больше или равно 35 лет, должны 
приходить ровно 11.00 каждое утро, а остальные работники они могут 
опаздывать как максимум 30 минут
- architects_time()
```python
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
```
Данная функция добавляет новый столбец 'TimeToEnter' куда записывает время, во сколько должен приходить тот или иной сотрудник, создаёт excel файл с названием функции, а также создаёт коллекцию в mongodb с названием 'ArchitectEnterTime' и добавляет в неё данные из созданного DataFrame\
В функции указано условие, что сотрудники должности Architect должны приходить ровно 10.30 
каждое утро, а остальные работники они могут опаздывать как максимум 
10 минут
