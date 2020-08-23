from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, username, password, classes, url):
        self.USERNAME = username
        self.PASSWORD = password
        self.url = url
        self.source = ""
        self.temp_grades = []
        self.output = []
        if isinstance(classes, list):
            self.classes = list(map(str.strip, classes))
        else:
            raise TypeError("Classes parameter must be of type: List")

    def get_source(self):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(self.url)
        user = driver.find_element_by_id("fieldAccount")
        passw = driver.find_element_by_id("fieldPassword")
        user.send_keys(self.USERNAME)
        passw.send_keys(self.PASSWORD)
        submit = driver.find_element_by_id("btn-enter-sign-in")
        submit.click()
        self.source = driver.page_source
        driver.close()
        return self.source

    def get_grades(self):
        print("Getting grades.")
        self.get_source()
        parsed_html = BeautifulSoup(self.source, features="lxml")
        pre_tags = parsed_html.body.find_all('tr', attrs={'class': 'center'})
        tags = []
        for tag in pre_tags:
            if "th2" not in tag.attrs['class']:
                name = list(tag.contents[14].descendants)[0].strip()
                if name.lower() in list(map(str.lower, self.classes)):
                    tags.append(tag)
        self.temp_grades = [round(int(t.contents[16].text[1:])) if t.contents[16].text[1:] != " i ]" else -1 for t in
                            tags]
        self.output = list(zip(self.classes, self.temp_grades))
        return self.output
