from curses import tigetflag
from fileinput import filename
from lib2to3.pgen2 import driver
import os
from numpy import inner, outer
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from  webdriver_manager.chrome import ChromeDriverManager
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup as bs
import user_email
import ossaudiodev
import pandas as pd
import time
import datetime
import smtplib
import imghdr
from email.message import EmailMessage
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

class Flights_Scraper:

    def __init__(self, url: str = 'https://www.edreams.co.uk/'):

        self.driver = Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()
        self.driver.get(url)

    def accept_cookies(self, xpath: str = '(//*[contains(text(), "Agree & Close")])[1]'):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.driver.find_element(By.XPATH, xpath).click()
    
        except TimeoutException:
            print('No cookies found')

    def flight_button(self, xpath: str =  "//a[@href='https://www.edreams.co.uk/flights/']"):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(By.XPATH, xpath))
        self.driver.find_element(By.XPATH, xpath).click()

    return_ticket = "//label[@for='tripTypeSwitcher_roundTrip']"
    one_way_ticket = "//label[@for='tripTypeSwitcher_oneWayTrip']"
    def ticket_chooser(self, ticket):
    
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, ticket)))
            return self.driver.find_element(By.XPATH, ticket).click()
        except Exception as e:
            pass

    def dep_country_chooser(self,dep_country, xpath: str = "//input[@placeholder='Where from?']", xpath2: str = "//div[@class='odf-box odf-box-layer odf-popup odf-popup-flex odf-space-outer-top-xs opened css-5ofyg9']//ul//li[1]"):

        flyfrom = self.driver.find_element(By.XPATH, xpath)
        time.sleep(1.5)
        flyfrom.clear()
        time.sleep(2)
        flyfrom.send_keys(' ' + dep_country)
        time.sleep(1.5)
        first_item = self.driver.find_element(By.XPATH, xpath2)
        time.sleep(2)
        first_item.click()

    def arrival_country_chooser(self, arrival_country, xpath: str = '//input[@placeholder="Where to?"]', xpath1: str = "//div[@class='odf-box odf-box-layer odf-popup odf-popup-flex odf-space-outer-top-xs opened css-5ofyg9']//ul//li[1]"):
        fly_to = self.driver.find_element(By.XPATH, xpath)
        time.sleep(1.5)
        fly_to.clear()
        time.sleep(2)
        fly_to.send_keys('  ' + arrival_country)
        time.sleep(1.5)
        first_item = self.driver.find_element(By. XPATH, xpath1)
        time.sleep(2)
        first_item.click()

    # def departure_box(self, xapth: str = '//input[@placeholder="Departure"]'):
    #     time.sleep(1.5)
    #     dep_date_button = self.driver.find_element(By.XPATH, xapth)
    #     dep_date_button.click()
    #     dep_date_button.click()
    #     time.sleep(2)

    def month_year_chooser(self, month_year):
        while True:
            calendar_title = self.driver.find_element(By. XPATH, '//div[@class="odf-calendar-title"]').text
            next_button = self.driver.find_element(By.XPATH, '//span[@glyph="arrow-right"]')
            if calendar_title == month_year:
                break        
            else:
                next_button.click()
                       
    def day_chooser(self, day):
        alldays = self.driver.find_elements(By.XPATH, "//div[@class='odf-calendar-month']//div[@class='odf-calendar-day']|//div[@class='odf-calendar-day odf-calendar-day-weekend']")

        for date in alldays:
            if date.text == day:
                date.click()
                break
    
    def done(self):
        done_button = self.driver.find_element(By.XPATH, "//button[@class='odf-btn odf-btn-primary']")
        done_button.click()

    # def return_box(self):
    #     time.sleep(1.5)
    #     return_box = self.driver.find_element(By.XPATH, '//input[@placeholder="Return"]')
    #     return_box.click()
    #     time.sleep(2)

    def return_month_year_chooser(self, month_year):
        while True:
            calendar_title = self.driver.find_element(By. XPATH, '//div[@class="odf-calendar-title"]').text
            next_button = self.driver.find_element(By.XPATH, '//span[@glyph="arrow-right"]')
            if calendar_title == month_year:
                break        
            else:
                next_button.click()
                time.sleep(1.5)
                       
    def return_day_chooser(self, day):
        alldays = self.driver.find_elements(By.XPATH, "//div[@class='odf-calendar-month']//div[@class='odf-calendar-day']|//div[@class='odf-calendar-day odf-calendar-day-weekend']")

        for date in alldays:
            if date.text == day:
                date.click()
                break
        
        # done_button = self.driver.find_element(By.XPATH, "//button[@class='odf-btn odf-btn-primary']")
        # done_button.click()

    def search_flights(self, search_xpath: str = "//button[@test-id='search-flights-btn']"):
        time.sleep(1.5)
        search_flights_button = self.driver.find_element(By.XPATH, search_xpath)
        search_flights_button.click()
        time.sleep(2)
    
    fastest = '//div[contains (text(), "Fastest")]'
    cheapest = '//div[contains (text(), "Cheapest")]'
    def select_flight(self, choice):      
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, choice)))
            return self.driver.find_element(By.XPATH, choice).click()
        except Exception as e:
            pass

    # def first_option(self, xpath: str = '//div[@class="css-1jnhkd7-Box e1tveian0"]/div[1]//button'):
    #     WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
    #     self.driver.find_element(By.XPATH, xpath).click()

    def get_dep_data(self):
        global a
        time.sleep(10)
        flight_dict = {
            'dep_times': [],
            'arr_times': [],
            'airlines': [],
            'duration': [],
            'stops': [],
            'total_price': []
        }

        dep_times = self.driver.find_element(By.XPATH, '//div[@class="css-1jnhkd7-Box e1tveian0"]/div[1]//div[@class="css-v7vujh-Box-BaseFlex evtgkbl0"]//div[@class="css-v0s8x5-BaseText-Body emkoh790"]')
        flight_dict['dep_times'].append(dep_times.text)

        arr_times = self.driver.find_element(By.XPATH, '//div[@class="css-1jnhkd7-Box e1tveian0"]/div[1]//div[@class="css-1bmhsyh-Box-BaseFlex evtgkbl0"]//div[@class="css-v0s8x5-BaseText-Body emkoh790"]')
        flight_dict['arr_times'].append(arr_times.text)
        
        airlines = self.driver.find_element(By.XPATH, '//div[@class="css-1jnhkd7-Box e1tveian0"]/div[1]//div[@class="css-1um4vyc-BaseText-Body emkoh790"]')
        flight_dict['airlines'].append(airlines.text)
        
        duration = self.driver.find_element(By.XPATH, '//div[@class="css-1jnhkd7-Box e1tveian0"]/div[1]//span[@class="css-rhtc89-BaseText-Text e1gw91g00"]')
        flight_dict['duration'].append(duration.text)
        
        stops = self.driver.find_element(By.XPATH, '//div[@class="css-1jnhkd7-Box e1tveian0"]/div[1]//span[@class="css-p611qh-BaseText-Text e1gw91g00"]')
        flight_dict['stops'].append(stops.text)

        prices = self.driver.find_element(By.XPATH, '//div[@class="css-1jnhkd7-Box e1tveian0"]/div[1]//div[@class="of_autos-itinerary-prime-price css-1x3sxzl-Box e1tveian0"]//span[@class="css-1iu0vlo-StyledContainer e1mg04uk3"]').get_attribute('aria-label')
        flight_dict['total_price'].append(prices)
        df = pd.DataFrame(flight_dict)
        os.makedirs('data', exist_ok=True) 
        a = df.to_csv('data/dep_flight.csv', index=False, encoding='utf-8')

    def dep_send_email(self):
        EMAIL_ADDRESS = user_email.username
        EMAIL_PASSWORD = user_email.password

        contacts = []

        emailfrom = EMAIL_ADDRESS
        emailto = ', '.join(contacts)
        fileToSend = "data/dep_flight.csv"
        username = EMAIL_ADDRESS
        password = EMAIL_PASSWORD

        msg = MIMEMultipart()
        msg["From"] = emailfrom
        msg["To"] = emailto
        msg["Subject"] = "Check out your Cheapest/Fastest flight!"
        msg.preamble = "File attached!"

        ctype, encoding = mimetypes.guess_type(fileToSend)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)

        if maintype == "text":
            fp = open(fileToSend)
            # Note: we should handle calculating the charset
            attachment = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "image":
            fp = open(fileToSend, "rb")
            attachment = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "audio":
            fp = open(fileToSend, "rb")
            attachment = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(fileToSend, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
        msg.attach(attachment)

        server = smtplib.SMTP("smtp.gmail.com:587")
        server.starttls()
        server.login(username,password)
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()

    def get_return_data(self):
        global b
        time.sleep(10)
        flight_dict = {
            'dep_times': [],
            'arr_times': [],
            'airlines': [],
            # 'prices': [],
            'duration': [],
            'stops': []
        }

        dep_times = self.driver.find_element(By.XPATH, '(//div[@class="css-1jnhkd7-Box e1tveian0"]/div[1]//div[@class="css-v7vujh-Box-BaseFlex evtgkbl0"]//div[@class="css-v0s8x5-BaseText-Body emkoh790"])[2]')
        flight_dict['dep_times'].append(dep_times.text)

        arr_times = self.driver.find_element(By.XPATH, '(//div[@class="css-1jnhkd7-Box e1tveian0"]/div[1]//div[@class="css-1bmhsyh-Box-BaseFlex evtgkbl0"]//div[@class="css-v0s8x5-BaseText-Body emkoh790"])[2]')
        flight_dict['arr_times'].append(arr_times.text)
        
        airlines = self.driver.find_element(By.XPATH, '(//div[@class="css-1jnhkd7-Box e1tveian0"]/div[1]//div[@class="css-1um4vyc-BaseText-Body emkoh790"])[2]')
        flight_dict['airlines'].append(airlines.text)
        
        # prices = self.driver.find_element(By.XPATH, '//div[@class="css-1jnhkd7-Box e1tveian0"]/div[1]//div[@class="of_autos-itinerary-prime-price css-1x3sxzl-Box e1tveian0"]//span[@class="css-1iu0vlo-StyledContainer e1mg04uk3"]').get_attribute('aria-label')
        # flight_dict['prices'].append(prices)
        
        duration = self.driver.find_element(By.XPATH, '(//div[@class="css-1jnhkd7-Box e1tveian0"]/div[1]//span[@class="css-rhtc89-BaseText-Text e1gw91g00"])[2]')
        flight_dict['duration'].append(duration.text)
        
        stops = self.driver.find_element(By.XPATH, '(//div[@class="css-1jnhkd7-Box e1tveian0"]/div[1]//span[@class="css-p611qh-BaseText-Text e1gw91g00"])[2]')
        flight_dict['stops'].append(stops.text)
        df = pd.DataFrame(flight_dict)
        os.makedirs('data', exist_ok=True) 
        b = df.to_csv('data/return_flight.csv', index=False, encoding='utf-8')

    def merge_df(self):
        a = pd.read_csv('data/dep_flight.csv')
        b = pd.read_csv('data/return_flight.csv')
        merged = pd.merge(a, b, how='outer')
        merged.to_csv('data/flights.csv', index=False, encoding='utf-8')

    def flight_send_email(self):
        EMAIL_ADDRESS = user_email.username
        EMAIL_PASSWORD = user_email.password

        contacts = ['rexhino.rexhepi@outlook.it', 'ermelinda.aliaj@outlook.com']

        emailfrom = EMAIL_ADDRESS
        emailto = ', '.join(contacts)
        fileToSend = "data/flights.csv"
        username = EMAIL_ADDRESS
        password = EMAIL_PASSWORD

        msg = MIMEMultipart()
        msg["From"] = emailfrom
        msg["To"] = emailto
        msg["Subject"] = "Check out your Cheapest/Fastest flight!"
        msg.preamble = "File attached!"

        ctype, encoding = mimetypes.guess_type(fileToSend)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)

        if maintype == "text":
            fp = open(fileToSend)
            # Note: we should handle calculating the charset
            attachment = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "image":
            fp = open(fileToSend, "rb")
            attachment = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "audio":
            fp = open(fileToSend, "rb")
            attachment = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(fileToSend, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
        msg.attach(attachment)

        server = smtplib.SMTP("smtp.gmail.com:587")
        server.starttls()
        server.login(username,password)
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()
       
if __name__ == '__main__':
    bot = Flights_Scraper()
    bot.accept_cookies()
    ticket = (bot.return_ticket)
    bot.ticket_chooser(ticket)
    bot.dep_country_chooser('London')
    bot.arrival_country_chooser('Miami')
    # bot.departure_box()
    bot.month_year_chooser("May '22")
    bot.day_chooser('3')
    if ticket == bot.return_ticket:
        # bot.return_box()
        bot.return_month_year_chooser("May '22")
        bot.return_day_chooser('17')
    bot.done()
    bot.search_flights()
    bot.select_flight(bot.fastest)
    # bot.first_option()
    bot.get_dep_data()
    if ticket == bot.one_way_ticket:
        bot.dep_send_email()
    if ticket == bot.return_ticket:
        bot.get_return_data()
        bot.merge_df()
        bot.flight_send_email()