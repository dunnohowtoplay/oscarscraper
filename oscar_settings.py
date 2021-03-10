from selenium import webdriver

DIRECTORY = 'result'
FIRST_YEAR = '1929'
LATEST_YEAR = '2020'
BASE_URL = 'https://www.oscars.org/oscars/ceremonies/'


def get_chrome_web_driver(options):
    return webdriver.Chrome(chrome_options=options)


def get_web_driver_options():
    return webdriver.ChromeOptions()


def set_ignore_certificate_error(options):
    options.add_argument('--ignore-certificate-errors')


def set_browser_as_incognito(options):
    options.add_argument('--incognito')


def set_automation_as_head_less(options):
    options.add_argument('--headless')