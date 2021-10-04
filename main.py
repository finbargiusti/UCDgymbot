from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import schedule
import time

driver = webdriver.Firefox()

driver.get("https://hub.ucd.ie/usis/W_HU_MENU.P_PUBLISH?p_tag=GYMBOOK")

assert "Gym" in driver.title

reattempting = False


def setBooking(gymtime):
    global reattempting

    driver.refresh()

    timeslots = driver.find_element_by_class_name(
        "datadisplaytable").find_elements_by_tag_name("tr")

    filtertimes = []

    for timeslot in timeslots:
        row = timeslot.find_elements_by_tag_name("td")
        if len(row) > 0:
            if row[0].text == gymtime and row[1].text == "Performance gym":
                filtertimes.append(timeslot)

    try:
        filtertimes[0].find_element_by_tag_name("a").click()
    except:
        print("Missed it.. trying to book later")
        if not reattempting:
            schedule.every(20).seconds.until(gymtime).do(
                setBooking, gymtime).tag(gymtime)
            reattempting = True
        return

    schedule.clear(gymtime)

    bar = driver.find_element_by_name("MEMBER_NO")
    try:
        blocker = driver.find_element_by_id("onetrust-consent-sdk")
        driver.execute_script("arguments[0].style.display='none'", blocker)
    except:
        print("cookies not required")

    bar.send_keys("21372821")
    bar.send_keys(Keys.RETURN)

    time.sleep(1.5)

    try:
        blocker = driver.find_element_by_id("onetrust-consent-sdk")
        driver.execute_script("arguments[0].style.display='none'", blocker)
    except:
        print("cookies not required")

    confirm = driver.find_element_by_class_name("menubutton")

    confirm.click()

    time.sleep(2)


schedule.every().monday.at("17:47").do(setBooking, "20:45")
schedule.every().tuesday.at("15:45").do(setBooking, "18:45")
setBooking("20:45")

while True:
    schedule.run_pending()
    time.sleep(1)
