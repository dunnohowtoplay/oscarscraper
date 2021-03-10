import time
from selenium.webdriver.common.keys import Keys
from oscar_settings import (
    get_web_driver_options,
    get_chrome_web_driver,
    set_ignore_certificate_error,
    set_browser_as_incognito,
    set_automation_as_head_less,
    FIRST_YEAR,
    LATEST_YEAR,
    BASE_URL,
    DIRECTORY
)
from selenium.common.exceptions import NoSuchElementException
import json


class GeneratResult:
    """
    generate OscarAPI result
    """
    def __init__(self, year, data):
        self.data = data
        self.year = year
        print("Creating report...")
        with open(f'{DIRECTORY}/{year}.json', 'w') as f:
            json.dump(data, f)
        print("Done...")

class OscarAPI:
    """
    Scrap data from oscar.org
    """
    def __init__(self, year, base_url):
        self.year = year
        self.base_url = base_url
        options = get_web_driver_options()
        set_automation_as_head_less(options)
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        self.driver = get_chrome_web_driver(options)
    
    def run(self):
        link = self.base_url+str(self.year) #(https://www.oscars.org/oscars/ceremonies/year)
        print(f"Url: {link}")
        print(f"Getting info about {self.year}'s oscar nominations...")
        nominations = self.get_nomination_info(link)
        self.driver.quit()
        return nominations
    
    def get_nomination_info(self, link):
        self.driver.get(link)
        time.sleep(2)
        title = self.get_title()
        date = self.get_date()
        place = self.get_place()
        nominations = self.get_nominations()
        if title and date and place and nominations:
            awards_info = {
                'link' : link,
                'title' : title,
                'date': date,
                'place': place,
                'nominations': nominations,
            }
            return awards_info
        return None
    
    def get_title(self):
        try:
            return self.driver.find_element_by_xpath('//*[@class="views-field views-field-title"]/span').text
        except Exception as e:
            print(e)
            print(f"Can't get date in - {self.driver.current_url}")
            return None

    def get_date(self):
        try:
            return self.driver.find_element_by_xpath('//*[@class="views-field views-field-field-date"]/div/span').text
        except Exception as e:
            print(e)
            print(f"Can't get date in - {self.driver.current_url}")
            return None

    def get_place(self):
        try:
            return self.driver.find_element_by_xpath('//*[@class="views-field views-field-field-location-name"]/div').text
        except Exception as e:
            print(e)
            print(f"Can't get place in - {self.driver.current_url}")
            return None

    def get_nominations(self):
        nominations = []
        '''
        There are 3 view-content class in the page, index[1] which is the second view-content class
        contains the nominations data
        '''
        nominee_div_content = self.driver.find_elements_by_xpath('//div[@class="view-content"]')[1]
        """
        In nominee_div_content each category is in view-grouping class, below iteration is to iterate to each
        category there are available on current year oscar nominations
        """
        for nomination in nominee_div_content.find_elements_by_class_name('view-grouping'):
            category_name = self.get_category_name(nomination)
            grouping_content_class = nomination.find_element_by_class_name('view-grouping-content')
            winner = self.get_winner(grouping_content_class)
            nominees = self.get_nominees(grouping_content_class)
            data = {
                'category' : category_name,
                'winner' : winner,
                'nominees' : nominees,
            }

            nominations.append(data)

        return nominations

    def get_category_name(self, div):
        try:
            return div.find_element_by_xpath('.//div/h2').text
        except Exception as e:
            print(e)
            return None

    def get_winner(self,div):
        entity = self.get_winner_entity(div)
        sub_entity = self.get_winner_sub_entity(div)
        winner = {
            'entity' : entity,
            'sub_entity' : sub_entity,
        }

        return winner

    def get_winner_entity(self, div):
        """
        each winner_entity always place in the first views-field-field-actor-name class and the text is in h4 tag
        """
        try:
            return div.find_elements_by_xpath(".//div[contains(@class, 'views-field-field-actor-name')]/h4")[0].text
        except Exception as e:
            print(e)
            return None
    
    def get_winner_sub_entity(self, div):
        """
        each winner_sub_entity always place in the first views-field-title class and the text is in span tag
        """
        try:
            return div.find_elements_by_xpath(".//div[contains(@class, 'views-field-title')]/span")[0].text
        except Exception as e:
            print(e)
            return None

    def get_nominees(self, div):
        nominees = []
        for index, nominee in enumerate(div.find_elements_by_xpath(".//div[contains(@class, 'views-field-field-actor-name')]")): 
            """
            we skip index 0, because that's the winner of current category, the nominees goes from index 1 till last
            """
            if index == 0:
                pass
            else:
                data = {
                    'entity' : nominee.find_element_by_xpath('.//h4').text,
                    'sub_entity' : div.find_elements_by_xpath(".//div[contains(@class, 'views-field-title')]")[index].text,
                }
                nominees.append(data)
        return nominees



if __name__ == '__main__':
    print("Starting Script...")
    for year in range(int(FIRST_YEAR),int(LATEST_YEAR)+1):
        oscar = OscarAPI(year, BASE_URL)
        data = oscar.run()
        GeneratResult(year, data)