from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from fake_useragent import UserAgent
import time

class CraiglistGigScraper(object):
    '''Scrape Craiglist Gig webpages'''
    def __init__(self):
        self.alter_link = None
        self.delay = 3
        self.ua = UserAgent()
        self.random = self.ua.random
        options = webdriver.FirefoxOptions()
        options.set_preference("general.useragent.override", self.random)
        self.headless = self.options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=options)
    
    def load_craigslist_url(self, url):
        '''Load a Craiglist link'''
        try:
            self.driver.get(url)
            wait = WebDriverWait(self.driver, self.delay)
            time.sleep(self.delay)
            # print('Page is ready')
        
        except TimeoutException:
            print('Loading took too much time')

    def extract_gig_information(self, url):
        '''Extract content from a Craiglist Gig page'''
        try:
            # Initiate driver
            self.load_craigslist_url(url)

            # Extract content
            compensation = self.driver.find_element(By.XPATH, '/html/body/section/section/section/div[1]/p/span').text
            title = self.driver.find_element(By.ID, 'titletextonly').text
            _type = self.driver.find_element(By.XPATH, '/html/body/section/header[1]/nav/ul/li[4]/p/a').text
            click_time = self.driver.find_element(By.XPATH, '/html/body/section/section/section/div[2]/p[2]/time').click()
            timestamp = self.driver.find_element(By.XPATH, '/html/body/section/section/section/div[2]/p[2]/time').get_attribute('datetime')
            # location = self.driver.find_element(By.XPATH, '/html/body/section/header[1]/nav/ul/li[2]/p/a').text
            time.sleep(self.delay)

            # self.quit()
            return [title, timestamp, compensation, _type]
        
        except Exception as error:
            print(error)
    
    def extract_gig_links(self):
        '''Extract all Craiglist Gig post links'''
        try:            
            # Filters
            paid = self.driver.find_element(By.XPATH, '/html/body/section/form/div[2]/div[2]/ul/li[2]').click()
            duplicate = self.driver.find_element(By.XPATH, '/html/body/section/form/div[2]/div[2]/div[2]/ul[1]/li[4]/label/input').click()

            # Post
            links = []
            while True:        
                try:
                    posts = self.driver.find_elements(By.XPATH, '//a[@class="result-title hdrlnk"]')

                    for post in posts:
                        links.append(post.get_attribute('href'))

                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/section/form/div[5]/div[3]/span[2]/a[3]'))).click()
                    time.sleep(self.delay)
                    
                except Exception as error:
                    break

            print('Dirty links total: ', len(links))
            print('Cleaned links total: ', len(list(set(links))))
            
            # self.quit()
            print('Post links acquired!')
            return links

        except Exception as error:
            print(error)
        
    def quit(self):
        '''Terminate driver'''
        self.driver.close()

if __name__ == '__main__':
    print('CraiglistGigScraper class ran')