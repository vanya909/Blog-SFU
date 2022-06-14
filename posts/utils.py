from selenium import webdriver
from selenium.webdriver.common.by import By
import time


path = 'http://newtimetable.sfu-kras.ru/main'

driver = webdriver.Chrome('../chrome_driver_for_parse/chromedriver.exe')
driver.get(path)

institutions = driver.find_elements(By.CLASS_NAME, 'instItemHead')

groups_of_courses = []

for institut_count in range(0, len(institutions)):
    js_script = f'document.getElementsByClassName("instItemContainer")[{institut_count}].click();'

    time.sleep(1)

    driver.execute_script(js_script)

    time.sleep(1)

    courses = driver.find_elements(By.CLASS_NAME, 'instItemCoursesItem')
    for course_count in range(0, len(courses)):
        js_script = f'document.getElementsByClassName("instItemCoursesItem")[{course_count}].click();'

        time.sleep(1)

        driver.execute_script(js_script)

        groups = driver.find_elements(By.CLASS_NAME, 'instItemGroupItem')
        groups_titles = [group.text for group in groups]
        groups_of_courses.append(groups_titles)
        print(groups_titles)