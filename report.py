import csv


def get_employees() -> list:
    """считываем файл и возвращаем список с информацией о каждом сотруднике"""
    rows = open('Corp Summary.csv', encoding="utf8").read().split("\n")
    employees = []
    for row in rows:
        employees.append(row.split(";"))
    return employees[1:-1]


def get_report(employees: list) -> dict:
    """возвращаем словарь с информацией по департаментам"""
    dep_info = {}
    for employee in employees:
        department, salary = employee[1], int(employee[5])
        if not dep_info.get(department):
            dep_info[department] = [1, salary, salary, salary]
        else:
            dep_info[department][0] += 1  # кол-во людей в департаменте
            dep_info[department][1] = min(dep_info[department][1], salary)  # минимальная зарплата
            dep_info[department][2] = max(dep_info[department][2], salary)  # маскимальная зарплата
            dep_info[department][3] += salary  # общая сумма зарплат
    for department in dep_info:
        dep_info[department][3] = round(dep_info[department][3] / dep_info[department][0], 2)
    return dep_info


def show_dep_hier():
    """выводим департаменты и все команды, которые в них входят"""
    employees = get_employees()
    dep_team = {}
    for employee in employees:
        department, team = employee[1], employee[2]
        if not dep_team.get(department):
            dep_team[department] = [team]
        elif team in dep_team[department]:
            continue
        else:
            dep_team[department].append(team)
    for department, list_of_teams in dep_team.items():
        print(department + ':')
        print(*list_of_teams, sep='; ')
        print()


def show_report():
    """выводим отчет по департаментам"""
    employees = get_employees()
    dep_info = get_report(employees)
    for department, info in dep_info.items():
        print(department + ':')
        print(f'Кол-во {info[0]} '
              f'Мин. з/п {info[1]} '
              f'Макс. з/п {info[2]} ',
              f'Средняя з/п {info[3]} ', sep='\t')


def save_report():
    """сохраняем отчет по департаментам в новом csv файле"""
    employees = get_employees()
    dep_info = get_report(employees)
    with open('./Consolidated report.csv', 'w') as f:
        out_file = csv.writer(f, delimiter=';')
        out_file.writerow(('Кол-во', 'Мин. з/п', 'Макс. з/п', 'Средняя з/п'))
        for department, info in dep_info.items():
            out_file.writerow((department, *info))


def start_report():
    """предлагаем пользователю выбрать пункт для выполнения"""
    print("Please choose an option:\n"
          "1: show department hierarchy\n"
          "2: show consolidated report\n"
          "3: save consolidated report\n")
    option = int(input())
    if option == 1:
        return show_dep_hier()
    elif option == 2:
        return show_report()
    elif option == 3:
        return save_report()
    else:
        print('Please choose one of the given options')
        start_report()


if __name__ == '__main__':
    start_report()
