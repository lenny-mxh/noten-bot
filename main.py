import os
import requests
from time import sleep
from evaluate import evaluate

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class SchulnetzBot:
    url = 'https://api.telegram.org/bot1206066782:AAHKDt7cW793myZCuqL8eDswV-Ji2hZB-xc/'

    def __init__(self):
        self.options = Options()
        self.options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
        self.options.add_argument('start-maximized')
        self.options.add_argument('disable-infobars') 
        self.options.add_experimental_option("detach", True)

        # make selenium headless -> heroku
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--no-sandbox')
        
        # avoid chrome controlled by automated software (config)
        self.driver = webdriver.Chrome(
            options=self.options, 
            executable_path=os.environ.get('CHROMEDRIVER_PATH')
        )

        # open schulnetz
        self.driver.get('https://www.schul-netz.com/altekanti/')
        sleep(2)

        # log in
        self.driver.find_element_by_xpath("//input[@name=\"loginfmt\"]")\
            .send_keys(os.environ.get('USERNAME'))
        self.driver.find_element_by_xpath('//input[@type="submit"]')\
            .click()
        sleep(8)

        self.driver.find_element_by_xpath('//input[@name=\'passwd\']')\
            .send_keys(os.environ.get('PW'))
        self.driver.find_element_by_xpath('//input[@type="submit"]')\
            .click()
        sleep(5)

        # pop-up
        self.driver.find_element_by_xpath('//input[@type="button"]')\
            .click()
        
    def _refresh(self):
        time_button = self.driver.find_element_by_xpath('//*[@id="sn-timer"]')
        time_button.click()
        
    def _get_grade(self):
        titles = self.driver.find_elements_by_class_name('tabletitle')
        for title in titles:
            if title.text == 'Ihre letzten Noten':
                parent = title.find_element_by_xpath('..')
                tds = parent.find_elements_by_tag_name('td')
                
                # findet der bot eine neue note, dann try:
                try:
                    data = {'Fach': '', 'Thema': '', 'Datum': '', 'Note': ''}
                    keys = list(data.keys())
                    for i in range(4):
                        data.update({keys[i]: tds[i].text})

                # wenn keine note gefunden wird, return None
                except IndexError:
                    return None

                return data
    
    def _confirm_grade(self, fach):
        # overview page of my grades
        self.driver.find_element_by_xpath('//*[@id="menu21311"]').click()

        # compare the subject of the test with all the subjects to find the right 'bestätigen' link
        faecher = self.driver.find_elements_by_tag_name('b')
        for _fach in faecher:
            if _fach.text == fach:
                parent = _fach.find_element_by_xpath('..')
                
                # parent of parent, in order to find the link to click
                parent_of_parent = parent.find_element_by_xpath('..')

                # find the 'bestätigen' link
                links = parent_of_parent.find_elements_by_tag_name('a')
                for link in links:
                    if link.text == 'bestätigen':
                        link.click()
                        alert = self.driver.switch_to_alert()
                        alert.accept()
                        sleep(5)

        # get back to home page
        # self.driver.find_element_by_xpath('//*[@id="menu1"]')
    
    def send_message(self):
        # get the grade
        data = self._get_grade()

        if data is not None:
            fach = data['Fach']
            note = data['Note']

            # change fra to französisch
            edited_fach = evaluate(fach)
            message = f'Neue Note im Fach {edited_fach}!\nDu hast eine {note} :)'

            # telegram message
            chat_id = 1117316592
            endpoint = f'{self.url}sendMessage?chat_id={chat_id}&text={message}'
            requests.get(endpoint)

            # note bestätigen, damit nach neuen noten gesucht werden kann
            self._confirm_grade(fach)
        
        else:
            print('Keine neue Noten!')
        
        self.driver.close()
        

if __name__ == '__main__':
    bot = SchulnetzBot()
    print(bot.send_message())