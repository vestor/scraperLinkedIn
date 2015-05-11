import csv
import selenium.webdriver.support.ui as ui
from selenium import webdriver
import time


def PrettyRelativeTime(time_diff_secs):
    # Each tuple in the sequence gives the name of a unit, and the number of
    # previous units which go into it.
    weeks_per_month = 365.242 / 12 / 7
    intervals = [('minute', 60), ('hour', 60), ('day', 24), ('week', 7),
                 ('month', weeks_per_month), ('year', 12)]

    unit, number = 'second', abs(time_diff_secs)
    for new_unit, ratio in intervals:
        new_number = float(number) / ratio
        # If the new number is too small, don't go to the next unit.
        if new_number < 2:
            break
        unit, number = new_unit, new_number
    shown_num = int(number)
    return '{} {}'.format(shown_num, unit + ('' if shown_num == 1 else 's'))


import os.path


def getAllAttributes(mydriver):
    wait = ui.WebDriverWait(mydriver, 35)
    wait.until(lambda mydriver: mydriver.find_elements_by_xpath("//div[@id='location']//span[@class='locality']//a"))
    location = mydriver.find_elements_by_xpath("//div[@id='location']//span[@class='locality']//a")[0].text
    experiences = mydriver.find_elements_by_xpath("//span[@class='experience-date-locale']")
    sum = 0
    try:
        currentCompany = \
            mydriver.find_elements_by_xpath(
                "//div[@class='editable-item section-item current-position']//h5//strong//a")[
                0].text
    except:
        currentCompany = ''

    try:
        currentPosition = \
            mydriver.find_elements_by_xpath("//div[@class='editable-item section-item current-position']//h4//a")[
                0].text
    except:
        currentPosition = ''
    sumYear = 0
    sumMonths = 0
    for e in experiences:
        try:
            text = e.text
            text = text[text.rfind('('):text.rfind(')')].replace('(', '').replace(')', '').strip()
            splits = text.split(' ')
            print splits

            if 'years' in splits or 'year' in splits:
                sumYear += int(splits[0])

            if 'months' in splits or 'month' in splits:
                sumMonths += int(splits[len(splits) - 2])
        except:
            print 'Unable to parse'

    if sumMonths >= 12:
        sumYear += sumMonths / 12
        sumMonths %= 12
    totalExperience = str(sumYear) + (' years ' if sumYear > 1 else ' year ') + str(sumMonths) + (
        ' months ' if sumMonths > 1 else ' month')

    return [location, totalExperience, currentCompany, currentPosition]


def main():
    email = raw_input('Enter email')
    password = raw_input('Enter password')
    col_no = input('Enter the column of public url')
    with open('input.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        mydriver = webdriver.Firefox()
        mydriver.get('https://www.linkedin.com/nhome')
        mydriver.find_elements_by_xpath("//input[@name='session_key']")[0].send_keys(email)
        mydriver.find_elements_by_xpath("//input[@name='session_password']")[0].send_keys(password)
        mydriver.find_elements_by_xpath("//input[@name='signin']")[0].click()
        time.sleep(4)

        rowCount = 0
        for row in reader:

            rowCount += 1
            try:
                if row[col_no] != '' and row[col_no].find('linkedin') > 0:
                    mydriver.get(row[2])
                    result = list(map(lambda x: x.encode('utf-8').strip(), getAllAttributes(mydriver)))
                    #Custom code
                    row[5:7] = result
            finally:
                with open('output.csv', 'ab') as csvfile2:
                    csv.writer(csvfile2).writerow(row)
            print rowCount, row


main()





