from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import schedule
import time

driver = webdriver.Firefox()

driver.get("https://hub.ucd.ie/usis/W_HU_MENU.P_PUBLISH?p_tag=GYMBOOK")

assert "Gym" in driver.title

reattempting = False


def setBooking(gymtime, user):
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
        driver.get(filtertimes[0].find_element_by_tag_name(
            "a").get_attribute("href"))
    except:
        print("Missed it.. trying to book later")
        if not reattempting:
            schedule.every(20).seconds.until(gymtime).do(
                setBooking, gymtime).tag(gymtime)
            reattempting = True
        return

    schedule.clear(gymtime)

    bar = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.NAME, "MEMBER_NO")))

    url = driver.current_url

    bar.send_keys(user)
    bar.send_keys(Keys.RETURN)

    WebDriverWait(driver, 7).until(EC.url_changes(url))

    # try:
    #     driver.execute_script(
    #         "arguments[0].style.display='none'", driver.find_element_by_id("onetrust-consent-sdk"))
    # except:
    #     allgood = True

    confirm = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.CLASS_NAME, "menubutton")))

    driver.get(confirm.get_attribute("href"))

    time.sleep(2)


schedule.every().tuesday.at("12:45").do(
    setBooking, gymtime="15:45", user="21372821")
setBooking("09:30", "21372821")

while True:
    schedule.run_pending()
    time.sleep(1)
