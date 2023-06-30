def get_vacancies_by_salary(list_vacancies: list, salary_from: int, salary_to: int = 0):
    """
    Обработка по заданному диапазону ЗП
    """
    new_list_vac = []
    for data in list_vacancies:
        if data.salary_to and data.salary_from:
            if data.salary_from >= salary_from and data.salary_to >= salary_to:
                new_list_vac.append(data)
                continue
        if data.salary_from and salary_to == 0:
            if data.salary_from >= salary_from:
                new_list_vac.append(data)
    return new_list_vac


def sort_from_minimum_salary(data: list, reverse_data=False):
    """
    Сортировка по зарплате
    """

    data = sorted(data, reverse=reverse_data)
    return data


def get_top_vacancies(list_vac: list, n: int = 1):
    """
    Нужное количество вакансий
    """
    fin_data = list_vac[0:n]
    return fin_data
