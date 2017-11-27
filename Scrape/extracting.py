from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas

class App:
    def __init__(self,path='F:\Imaging'):
        self.path=path
        self.driver = webdriver.Chrome('F:\chromedriver')
        self.driver.get('https://www.amazon.in/s/ref=sr_pg_1?rh=i%3Aaps%2Ck%3Anovels&keywords=novels&ie=UTF8&qid=1510727563')
        sleep(1)
        self.scroll_down()
        self.driver.close()

    def scroll_down(self):
        title=[]
        sleep(3)
        self.driver.execute_script("window.scrollTo(0,5450);")
        soup=BeautifulSoup(self.driver.page_source,"html.parser")
        titles=soup.find_all("h2",{"class":"a-size-medium s-inline s-access-title a-text-normal"})
        authors=soup.find_all("div",{"class":"a-row a-spacing-small"})
        for value in range(len(titles)):
            d={}
            d["Title"]=titles[value].text
            temp = authors[value].text
            temp = temp.split("by")
            #print(temp[1])
            d["Author"]=temp[1]
            title.append(d)
        print(title)
        sleep(3)
        load_more = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='pagnRA']/a[@title='Next Page']")))
        self.driver.execute_script("arguments[0].click();", load_more)
        sleep(3)
        for value in range(2,20):
            print(self.driver.current_url)
            sleep(5)
            self.driver.execute_script("window.scrollTo(0,5500);")
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            titles = soup.find_all("h2", {"class": "a-size-medium s-inline s-access-title a-text-normal"})
            authors = soup.find_all("div", {"class": "a-row a-spacing-small"})
            #print(authors)
            for value in range(len(titles)):
                d = {}
                d["Title"] = titles[value].text
                temp = authors[value].text
                temp1 = temp.split("by")
                #print(temp[1])
                if temp1[0]!=temp:
                    d["Author"] = temp1[1]
                else:
                    d["Author"] = "None"
                title.append(d)
            sleep(1)
            load_more = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='pagnRA']/a[@title='Next Page']")))
            self.driver.execute_script("arguments[0].click();", load_more)
            #load_more.click()
            sleep(3)
        print(title)
        df=pandas.DataFrame(title)
        df.to_csv("Novels_list1.csv",index=False)
        sleep(3)


if __name__=='__main__':
    app=App()