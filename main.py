from scr.classes import JSONSaver, HHApi, SJApi
from scr.utils import get_vacancies_by_salary, sort_from_minimum_salary, get_top_vacancies


def main():
    def user_interaction():
        print("Здравствуйте.")
        search_request = input("Введите ключевой запрос по вакансии: ")
        salary_min = int(input("Укажите минимальную ЗП "))
        top_n = int(input("Сколько вакансий вывести из топ выборки? Введите число: "))

        # Создание экземпляров классов
        hh_api = HHApi()
        sj_api = SJApi()

        # вакансии с сайтов
        hh_vacancies = hh_api.get_vacancies(search_request)
        sj_vacancies = sj_api.get_vacancies(search_request)

        # Сохранение файл
        json_saver_hh = JSONSaver(search_request, "hh")
        json_saver_hh.add_vacancy(hh_vacancies)

        json_saver_sj = JSONSaver(search_request, "sj")
        json_saver_sj.add_vacancy(sj_vacancies)

        # Отбор данных
        vac_hh = json_saver_hh.select()
        vac_sj = json_saver_sj.select()

        # Сортировка по указанной зарплате
        sort_vac_hh = get_vacancies_by_salary(vac_hh, salary_min)
        sort_vac_sj = get_vacancies_by_salary(vac_sj, salary_min)

        # Сортировка списка по убывающей
        sort_vac_hh = sort_from_minimum_salary(sort_vac_hh, True)
        sort_vac_sj = sort_from_minimum_salary(sort_vac_sj, True)

        # Выборка N количетсва из топ вакансий
        top_vac_hh = get_top_vacancies(sort_vac_hh, top_n)
        top_vac_sj = get_top_vacancies(sort_vac_sj, top_n)

        print("\n", "*" * 150, "\n")
        print("\n", "          ВАКАНСИИ с hh.ru", "\n")
        print("\n","*" * 150, "\n")
        for vacancy in top_vac_hh:
            print(vacancy)
            print("\n", "-" * 20, "\n")

        print("\n","*" * 150, "\n")
        print("\n", "          ВАКАНСИИ с superjob.ru", "\n")
        print("\n","*" * 150, "\n")
        for vacancy in top_vac_sj:
            print(vacancy)
            print("\n", "-" * 20, "\n")

    user_interaction()


if __name__ == "__main__":

    main()
