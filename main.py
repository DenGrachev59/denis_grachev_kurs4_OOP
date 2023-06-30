from classes import HHApi, SJApi


if __name__ == "__main__":
    # user_interaction()
    v_hh = HHApi()
    v_sj = SJApi()

    # print (v_sj.get_vacancies('Python'))
    print(v_hh.get_vacancies("Python"))