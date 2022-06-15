from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def parse_all_groups():
    path = 'http://newtimetable.sfu-kras.ru/main'

    driver = webdriver.Chrome('../chrome_driver_for_parse/chromedriver.exe')
    driver.get(path)

    time.sleep(1)

    institutions = driver.find_elements(By.CLASS_NAME, 'instItemLabel')
    print(len(institutions))

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
            groups_of_courses.append(groups_titles)
            print(groups_titles)

    driver.close()


if __name__ == 'main':
    parse_all_groups()
