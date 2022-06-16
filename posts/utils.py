from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time


def get_all_groups_sfu():
    path = 'http://newtimetable.sfu-kras.ru/main'

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(path)

    time.sleep(2)

    institutions = driver.find_elements(By.CLASS_NAME, 'instItemLabel')

    print('parsing groups start')

    groups_of_courses = []

    for institute_count in range(len(institutions)):
        js_script = f'document.getElementsByClassName("instItemContainer")[{institute_count}].click();'

        time.sleep(0.2)

        driver.execute_script(js_script)

        courses = driver.find_elements(By.CLASS_NAME, 'instItemCoursesItem')
        for course_count in range(len(courses)):
            js_script = f'document.getElementsByClassName("instItemCoursesItem")[{course_count}].click();'

            time.sleep(0.2)

            driver.execute_script(js_script)

            groups = driver.find_elements(By.CLASS_NAME, 'instItemGroupItem')
            groups_titles = [group.text.split(' ')[0] for group in groups]
            groups_of_courses += groups_titles

    groups_of_courses = set(groups_of_courses)
    driver.close()
    return groups_of_courses
