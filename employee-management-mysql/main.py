import re
from tkinter import *
from tkinter import messagebox 
from tkinter import ttk
from sqlClient import PostgreSqlClient
import json

file = open('config.json', 'r')
configData = json.load(file)

sqlClient = PostgreSqlClient(username=configData['user'], password=configData['pass'], host=configData['host'], database=configData['database'])

window = Tk()

screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()

windowWidth = int(screenWidth * 0.7)
windowHeight = int(screenHeight * 0.7)

window.geometry(f"{windowWidth}x{windowHeight}")

window.title("Управление сотрудниками")

def homeScreen():
    for widget in window.winfo_children():
        widget.destroy()
    frame = Frame(window)
    frame.pack()
    opetionsFrame =LabelFrame(frame, text="Настройки")
    opetionsFrame.grid(row= 0, column=0, padx=20, pady=10)
    addButton = Button(opetionsFrame, text='Добавить нового сотрудника',height=2, width=22, padx=20, pady=20, font='lucida 10 normal', command=addScreen)
    addButton.pack(padx=10, pady=10)
    addButton = Button(opetionsFrame,text='Удалить сотрудника',height=2, width=22, padx=20, pady=20, font='lucida 10 normal', command=deleteScreen)
    addButton.pack(padx=10, pady=10)
    addButton = Button(opetionsFrame, text='Обновить информацию о сотруднике',height=2, width=22, padx=20, pady=20, font='lucida 10 normal', command=updateScreen)
    addButton.pack(padx=10, pady=10)
    addButton = Button(opetionsFrame,text='Просмотреть всех сотрудников',height=2, width=22, padx=20, pady=20, font='lucida 10 normal', command=allEmployeeScreen)
    addButton.pack(padx=10, pady=10)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

def addScreen():
    for widget in window.winfo_children():
        widget.destroy()


    def enterData():
        firstname = firstNameEntry.get()
        lastname = lastNameEntry.get()
        phoneNumber = phoneNumberEntry.get()
        email = emailEntry.get()
        country = countryVar.get()
        city = cityVar.get()
        salary = salaryEntry.get()

        
        phone_pattern = r'^\+?\d{10,15}$' 
        email_pattern = r'^[^@]+@[^@]+\.[^@]+$'

        if not firstname or not lastname or not phoneNumber or not email or not country or not city or not salary:
            messagebox.showwarning(title="Ошибка", message="Все поля должны быть заполнены.")
        elif not re.match(phone_pattern, phoneNumber):
            messagebox.showwarning(title="Ошибка", message="Некорректный номер телефона. Введите только цифры и, при необходимости, '+' в начале.")
        elif not re.match(email_pattern, email):
            messagebox.showwarning(title="Ошибка", message="Некорректный адрес электронной почты. Убедитесь, что адрес содержит '@' и домен.")
        else:
            sqlClient.insertEmployee(
                name=f'{firstname.capitalize()} {lastname.capitalize()}',
                phoneNumber=phoneNumber,
                email=email,
                country=country,
                city=city,
                salary=salary
            )
            messagebox.showinfo(title="Успешно", message="Данные о новом сотруднике успешно добавлены.")
            clear_entries()

    def clear_entries():
        for entry in [firstNameEntry, lastNameEntry, phoneNumberEntry, emailEntry, salaryEntry]:
            entry.delete(0, END)
        countryVar.set(countryOptions[0])
        cityVar.set(cityOptions[countryOptions[0]][0])

    def update_cities(*args):
        selected_country = countryVar.get()
        cityVar.set(cityOptions[selected_country][0])
        cityMenu['menu'].delete(0, 'end')
        for city in cityOptions[selected_country]:
            cityMenu['menu'].add_command(label=city, command=lambda value=city: cityVar.set(value))

    frame = Frame(window)
    frame.pack()

    employeeDetailsFrame = LabelFrame(frame, text="Добавить нового сотрудника")
    employeeDetailsFrame.grid(row=0, column=0, padx=20, pady=10)

    firstNameLabel = Label(employeeDetailsFrame, text="Имя")
    firstNameLabel.grid(row=0, column=0)
    lastNameLabel = Label(employeeDetailsFrame, text="Фамилия")
    lastNameLabel.grid(row=0, column=1)
    phoneNumberLabel = Label(employeeDetailsFrame, text="Номер телефона")
    phoneNumberLabel.grid(row=0, column=2)
    emailLabel = Label(employeeDetailsFrame, text="Электронная почта")
    emailLabel.grid(row=2, column=0)
    countryLabel = Label(employeeDetailsFrame, text="Страна")
    countryLabel.grid(row=2, column=1)
    cityLabel = Label(employeeDetailsFrame, text="Город")
    cityLabel.grid(row=2, column=2)
    salaryLabel = Label(employeeDetailsFrame, text="Зарплата")
    salaryLabel.grid(row=4, column=0)

    firstNameEntry = Entry(employeeDetailsFrame)
    firstNameEntry.grid(row=1, column=0)
    lastNameEntry = Entry(employeeDetailsFrame)
    lastNameEntry.grid(row=1, column=1)
    phoneNumberEntry = Entry(employeeDetailsFrame)
    phoneNumberEntry.grid(row=1, column=2)
    emailEntry = Entry(employeeDetailsFrame)
    emailEntry.grid(row=3, column=0)
    salaryEntry = Entry(employeeDetailsFrame)
    salaryEntry.grid(row=5, column=0)

    countryOptions = ["Казахстан", "США", "Канада", "Германия", "Франция", "Япония"]
    cityOptions = {
        "Казахстан": ["Алматы", "Астана", "Шымкент"],
        "США": ["Нью-Йорк", "Лос-Анджелес", "Чикаго"],
        "Канада": ["Торонто", "Монреаль", "Ванкувер"],
        "Германия": ["Берлин", "Гамбург", "Мюнхен"],
        "Франция": ["Париж", "Лион", "Марсель"],
        "Япония": ["Токио", "Осака", "Киото"]
    }

    countryVar = StringVar(employeeDetailsFrame)
    countryVar.set(countryOptions[0])
    countryVar.trace('w', update_cities)

    cityVar = StringVar(employeeDetailsFrame)
    cityVar.set(cityOptions[countryOptions[0]][0])

    countryMenu = OptionMenu(employeeDetailsFrame, countryVar, *countryOptions)
    countryMenu.grid(row=3, column=1)
    cityMenu = OptionMenu(employeeDetailsFrame, cityVar, *cityOptions[countryOptions[0]])
    cityMenu.grid(row=3, column=2)

    for widget in employeeDetailsFrame.winfo_children():
        widget.grid_configure(padx=10, pady=5)

    saveButton = Button(frame, text="Сохранить данные сотрудника", command=enterData)
    saveButton.grid(row=6, column=0, sticky="news", padx=20, pady=10)
    cancelButton = Button(frame, text="Отмена", command=homeScreen)
    cancelButton.grid(row=7, column=0, sticky="news", padx=20, pady=10)

    frame.place(relx=0.5, rely=0.5, anchor=CENTER)


def deleteScreen():
    for widget in window.winfo_children():
        widget.destroy()
    frame = Frame(window)
    frame.pack()

    findEmployeeFrame = LabelFrame(frame, text="Удалить сотрудника")
    findEmployeeFrame.grid(row=0, column=0, padx=20, pady=10)

    options = [
        "Id",
        "Имя",
        "Номер телефона",
        "Электронная почта",
        "Страна",
        "Город",
        "Зарплата",
    ]

    usingOpt = StringVar(findEmployeeFrame)
    usingOpt.set("Найти сотрудника используя:")

    menu = OptionMenu(findEmployeeFrame, usingOpt, *options)
    menu.grid(row=0, column=0, padx=10, pady=10)

    def nextDelete():
        def find():
            def delete():
                selectedEmployee = tree.selection()
                if not selectedEmployee:
                    messagebox.showwarning(title="Ошибка", message="Сначала выберите сотрудника.")
                else:
                    for item in selectedEmployee:
                        itemValue = tree.item(item, 'values')
                        ind = options.index(usingOptValue)
                        sqlClient.deleteEmployee(method=usingOptValue, value=itemValue[ind])
                        deleteScreen()
                        messagebox.showinfo(title="Успешно", message="Информация о сотруднике была удалена.")
            
            employees = sqlClient.findEmployee(method=usingOptValue, value=valueEntry.get())
            if not employees:
                messagebox.showwarning(title="Ошибка", message="Нет совпадений.")
            else:
                tree = ttk.Treeview(nextDeleteFrame, columns=("ID", "Имя", "Телефон", "Почта", "Страна", "Город", "Зарплата"))
                tree.heading("#0", text="", anchor="center")
                tree.heading("ID", text="ID", anchor="center")
                tree.heading("Имя", text="Имя", anchor="center")
                tree.heading("Телефон", text="Телефон", anchor="center")
                tree.heading("Почта", text="Почта", anchor="center")
                tree.heading("Страна", text="Страна", anchor="center")
                tree.heading("Город", text="Город", anchor="center")
                tree.heading("Зарплата", text="Зарплата", anchor="center")

                tree.column("#0", width=0, stretch=NO)
                tree.column("ID", width=50, anchor="center")
                tree.column("Имя", width=150, anchor="center")
                tree.column("Телефон", width=100, anchor="center")
                tree.column("Почта", width=150, anchor="center")
                tree.column("Страна", width=100, anchor="center")
                tree.column("Город", width=100, anchor="center")
                tree.column("Зарплата", width=100, anchor="center")

                for row in employees:
                    tree.insert("", "end", values=row)

                tree.grid(row=4, column=0, padx=20, pady=10)
                deleteButton = Button(nextDeleteFrame, text="Удалить", command=delete)
                deleteButton.grid(row=5, column=0, padx=20, pady=10)

        usingOptValue = usingOpt.get()
        if usingOptValue == 'Найти сотрудника используя:':
            messagebox.showwarning(title="Ошибка", message="Сначала выберите вариант.")
        else:
            for widget in window.winfo_children():
                widget.destroy()
            frame = Frame(window)
            frame.pack()

            nextDeleteFrame = LabelFrame(frame, text="Удалить сотрудника")
            nextDeleteFrame.grid(row=0, column=0, padx=20, pady=10)

            valueLabel = Label(nextDeleteFrame, text=f"Введите {usingOptValue}")
            valueLabel.grid(row=0, column=0)
            valueEntry = Entry(nextDeleteFrame, width=100)
            valueEntry.grid(row=1, column=0, padx=10, pady=10)

            findButton = Button(nextDeleteFrame, text="Найти", command=find)
            findButton.grid(row=2, column=0, sticky="news", padx=10, pady=10)
            backButton = Button(nextDeleteFrame, text="Назад", command=deleteScreen)
            backButton.grid(row=3, column=0, sticky="news", padx=10, pady=10)

            frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    nextButton = Button(findEmployeeFrame, text="Дальше", command=nextDelete, width=25)
    nextButton.grid(row=1, column=0, sticky="news", padx=10, pady=10)
    cancelButton = Button(findEmployeeFrame, text="Отмена", command=homeScreen)
    cancelButton.grid(row=2, column=0, sticky="news", padx=10, pady=10)

    frame.place(relx=0.5, rely=0.5, anchor=CENTER)


def updateScreen():
    for widget in window.winfo_children():
        widget.destroy()
    frame = Frame(window)
    frame.pack()

    findEmployeeFrame = LabelFrame(frame, text="Обновить информацию о сотруднике")
    findEmployeeFrame.grid(row=0, column=0, padx=20, pady=10)

    options = [
        "Id",
        "Имя",
        "Номер телефона",
        "Электронная почта",
        "Страна",
        "Город",
        "Зарплата",
    ]

    usingOpt = StringVar(findEmployeeFrame)
    usingOpt.set("Найти сотрудника используя:")

    menu = OptionMenu(findEmployeeFrame, usingOpt, *options)
    menu.grid(row=0, column=0, padx=10, pady=10)

    def nextUpdate():
        def find():
            def update():
                selectedEmployee = tree.selection()
                if not selectedEmployee:
                    messagebox.showwarning(title="Ошибка", message="Сначала выберите сотрудника.")
                else:
                    for item in selectedEmployee:
                        itemValue = tree.item(item, 'values')
                        ind = options.index(usingOptValue)

                    for widget in window.winfo_children():
                        widget.destroy()

                    def enterData():
                        phone = phoneEntry.get()
                        email = emailEntry.get()
                        country = countryEntry.get()
                        city = cityEntry.get()
                        salary = salaryEntry.get()

                        if phone and email and country and city and salary:
                            sqlClient.updateEmployee(
                                method=usingOptValue,
                                value=itemValue[ind],
                                newValue=(
                                    itemValue[0],
                                    phone,
                                    email,
                                    country,
                                    city,
                                    salary,
                                )
                            )
                            messagebox.showinfo(title="Успешно", message="Информация о сотруднике была обновлена")
                            updateScreen()
                        else:
                            messagebox.showwarning(title="Ошибка", message="Все поля должны быть заполнены.")

                    frame = Frame(window)
                    frame.pack()

                    employeeDetailsFrame = LabelFrame(frame, text="Обновить информацию о сотруднике")
                    employeeDetailsFrame.grid(row=0, column=0, padx=20, pady=10)

                    phoneLabel = Label(employeeDetailsFrame, text="Телефон")
                    phoneLabel.grid(row=0, column=0)
                    emailLabel = Label(employeeDetailsFrame, text="Электронная почта")
                    emailLabel.grid(row=0, column=1)
                    countryLabel = Label(employeeDetailsFrame, text="Страна")
                    countryLabel.grid(row=2, column=0)
                    cityLabel = Label(employeeDetailsFrame, text="Город")
                    cityLabel.grid(row=2, column=1)
                    salaryLabel = Label(employeeDetailsFrame, text="Зарплата")
                    salaryLabel.grid(row=2, column=2)

                    phoneEntry = Entry(employeeDetailsFrame)
                    phoneEntry.insert(0, itemValue[2])
                    emailEntry = Entry(employeeDetailsFrame)
                    emailEntry.insert(0, itemValue[3])
                    countryEntry = Entry(employeeDetailsFrame)
                    countryEntry.insert(0, itemValue[4])
                    cityEntry = Entry(employeeDetailsFrame)
                    cityEntry.insert(0, itemValue[5])
                    salaryEntry = Entry(employeeDetailsFrame)
                    salaryEntry.insert(0, itemValue[6])

                    phoneEntry.grid(row=1, column=0)
                    emailEntry.grid(row=1, column=1)
                    countryEntry.grid(row=3, column=0)
                    cityEntry.grid(row=3, column=1)
                    salaryEntry.grid(row=3, column=2)

                    for widget in employeeDetailsFrame.winfo_children():
                        widget.grid_configure(padx=10, pady=5)

                    button = Button(frame, text="Обновить информацию о сотруднике", command=enterData)
                    button.grid(row=3, column=0, sticky="news", padx=20, pady=10)
                    button = Button(frame, text="Отмена", command=homeScreen)
                    button.grid(row=4, column=0, sticky="news", padx=20, pady=10)
                    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

            employees = sqlClient.findEmployee(method=usingOptValue, value=valueEntry.get())
            if not employees:
                messagebox.showwarning(title="Ошибка", message="Нет совпадений.")
            else:
                tree = ttk.Treeview(nextUpdateFrame, columns=("ID", "Имя", "Телефон", "Почта", "Страна", "Город", "Зарплата"))
                tree.heading("#0", text="", anchor="center")
                tree.heading("ID", text="ID", anchor="center")
                tree.heading("Имя", text="Имя", anchor="center")
                tree.heading("Телефон", text="Телефон", anchor="center")
                tree.heading("Почта", text="Почта", anchor="center")
                tree.heading("Страна", text="Страна", anchor="center")
                tree.heading("Город", text="Город", anchor="center")
                tree.heading("Зарплата", text="Зарплата", anchor="center")

                tree.column("#0", width=0, anchor="center")
                tree.column("ID", width=50, anchor="center")
                tree.column("Имя", width=150, anchor="center")
                tree.column("Телефон", width=100, anchor="center")
                tree.column("Почта", width=150, anchor="center")
                tree.column("Страна", width=100, anchor="center")
                tree.column("Город", width=100, anchor="center")
                tree.column("Зарплата", width=100, anchor="center")

                for row in employees:
                    tree.insert("", "end", values=row)

                tree.grid(row=4, column=0, padx=20, pady=10)
                updateButton = Button(nextUpdateFrame, text="Выбрать", command=update)
                updateButton.grid(row=5, column=0, padx=20, pady=10)

        usingOptValue = usingOpt.get()
        if usingOptValue == 'Найти сотрудника используя:':
            messagebox.showwarning(title="Ошибка", message="Сначала выберите вариант.")
        else:
            for widget in window.winfo_children():
                widget.destroy()

            frame = Frame(window)
            frame.pack()

            nextUpdateFrame = LabelFrame(frame, text="Обновить информацию о сотруднике")
            nextUpdateFrame.grid(row=0, column=0, padx=20, pady=10)

            valueLabel = Label(nextUpdateFrame, text=f"Введите {usingOptValue}")
            valueLabel.grid(row=0, column=0)
            valueEntry = Entry(nextUpdateFrame, width=100)
            valueEntry.grid(row=1, column=0, padx=10, pady=10)
            findButton = Button(nextUpdateFrame, text="Найти", command=find)
            findButton.grid(row=2, column=0, sticky="news", padx=10, pady=10)
            backButton = Button(nextUpdateFrame, text="Назад", command=updateScreen)
            backButton.grid(row=3, column=0, sticky="news", padx=10, pady=10)

            frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    nextButton = Button(findEmployeeFrame, text="Дальше", command=nextUpdate, width=25)
    nextButton.grid(row=1, column=0, sticky="news", padx=10, pady=10)
    cancelButton = Button(findEmployeeFrame, text="Отмена", command=homeScreen)
    cancelButton.grid(row=2, column=0, sticky="news", padx=10, pady=10)

    frame.place(relx=0.5, rely=0.5, anchor=CENTER)


def allEmployeeScreen():
    employees = sqlClient.getAllEmployees()
    if not employees:
        messagebox.showwarning(title="Ошибка", message="В базе данных нет сотрудников.")
    else:
        for widget in window.winfo_children():
            widget.destroy()
        frame = Frame(window)
        frame.pack()

        allEmployeeFrame = LabelFrame(frame, text="Список сотрудников")
        allEmployeeFrame.grid(row=0, column=0, padx=20, pady=10)

        tree = ttk.Treeview(
            allEmployeeFrame, 
            columns=("ID", "Имя", "Телефон", "Почта", "Страна", "Город", "Зарплата"),
            show="headings"
        )

        tree.heading("ID", text="ID", anchor="center")
        tree.heading("Имя", text="Имя", anchor="center")
        tree.heading("Телефон", text="Телефон", anchor="center")
        tree.heading("Почта", text="Почта", anchor="center")
        tree.heading("Страна", text="Страна", anchor="center")
        tree.heading("Город", text="Город", anchor="center")
        tree.heading("Зарплата", text="Зарплата", anchor="center")

        tree.column("ID", width=50, anchor="center")
        tree.column("Имя", width=150, anchor="center")
        tree.column("Телефон", width=100, anchor="center")
        tree.column("Почта", width=150, anchor="center")
        tree.column("Страна", width=100, anchor="center")
        tree.column("Город", width=100, anchor="center")
        tree.column("Зарплата", width=100, anchor="center")

        scrollbar = Scrollbar(allEmployeeFrame, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=scrollbar.set)
        scrollbar.grid(row=5, column=0, sticky="ew", padx=10)

        for row in employees:
            tree.insert("", "end", values=row)

        tree.grid(row=4, column=0, padx=20, pady=10)

        backButton = Button(allEmployeeFrame, text="Назад", command=homeScreen)
        backButton.grid(row=6, column=0, padx=20, pady=10)

        frame.place(relx=0.5, rely=0.5, anchor=CENTER)

homeScreen()

window.mainloop()