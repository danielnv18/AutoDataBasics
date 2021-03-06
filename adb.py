from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from os import path
import csv

def runDataBasics(db_url, username, password, timesheet_lines_all, alias={}):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome('./chromedriver', desired_capabilities=chrome_options.to_capabilities())
    driver.get(db_url)

    print("Filling Username...")
    login_username = driver.find_element_by_id("username-input")
    login_username.send_keys(username)
    login_username.send_keys(Keys.RETURN)

    sleep(2)

    print("Filling Password...")
    login_pw = driver.find_element_by_id("password-input")
    login_pw.send_keys(password)
    login_pw.send_keys(Keys.RETURN)

    sleep(5)

    print("Entering Current Timesheet...")
    current_ts_link = driver.find_element_by_class_name("tm-grid-current-timesheet")
    current_ts_link.click()

    sleep(10)

    print("Important: We're going to create entries in chunks of 5 to avoid scroll issues :)")
    for i in range(0, len(timesheet_lines_all), 5):
        timesheet_lines = timesheet_lines_all[i:i+5]

        print("Switching to Favorites View...")
        favorites_tab = driver.find_element_by_class_name("vertTab-timesheet-template-icon")
        favorites_tab.click()

        sleep(2)

        icon_adds = driver.find_elements_by_class_name("icon-add")

        print("Creating Entry Lines %s to %s..." % (i+1,i+len(timesheet_lines)))
        for line in timesheet_lines:
            try:
                row = int(line["fav"])
            except:
                row = alias[line["fav"]]

            icon_adds[row].click()
            sleep(3)

        x_row_editors = driver.find_elements_by_id("lineNo")

        print("Closing Favorites View...")
        timesheet_tab = driver.find_element_by_class_name("vertTab-report-icon-count")
        timesheet_tab.click()

        print("Filling Lines...")
        timesheet_lines.reverse()
        for row in range(len(timesheet_lines)):
            web_row = x_row_editors[row]
            entry = timesheet_lines[row]
            web_row.click()
            sleep(0.3)

            for day in range(3,8):
                slot = driver.find_element_by_id("timefield"+str(day))
                slot.send_keys(entry["times"][day-3])

            add_note_btn = driver.find_element_by_id("addTimeLineNewNotes")
            add_note_btn.click()
            sleep(0.8)

            driver.find_element_by_xpath('//button[text()="Yes"]').click()
            sleep(1)

            text_area = driver.find_elements_by_class_name("x-form-textarea")[0]
            text_area.click()

            sleep(0.3)

            text_area.send_keys(entry["note"])

            driver.find_element_by_xpath('//button[text()="SAVE & CLOSE"]').click()
            sleep(0.8)

    print("Done! Review and submit your timesheet! :)")

if __name__ == "__main__":
    with open("auth.txt") as auth:
        auth_txt = auth.read().split("\n")
        db_url = auth_txt[0]
        username = auth_txt[1]
        password = auth_txt[2]

    alias_dict = dict()
    if(path.exists("alias.txt")):
        with open("alias.txt") as alias:
            i = 0
            for line in alias.read().split("\n"):
                if(line.strip() != ""):
                    alias_dict[line] = i
                i += 1

    with open("timesheet.txt") as ts:
        csv_reader = csv.reader(ts)
        timesheet_lines = []
        for row in csv_reader:
            timesheet_lines.append({"fav":row[0].strip(),
            "note":row[1].strip(),
            "times":[x.strip() for x in row[2:]]})

    runDataBasics(db_url, username, password, timesheet_lines, alias=alias_dict)
