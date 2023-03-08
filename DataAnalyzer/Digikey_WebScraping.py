import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class Digikey_WebScraping():
    def __init__(self, PartNumber = ""):
        self.initial()
        self.TargetPN = PartNumber
#       self.Scraping()
#       self.terminate()

    def terminate(self):
        self.chrome.close()
        self.chrome.quit()

    def initial(self):
#       self.chrome = webdriver.Chrome(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-extensions")
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("detach",True)
        self.chrome = webdriver.Chrome(ChromeDriverManager().install(), options=options)


    def Scraping(self):
#       Mouser_URL = 'https://www.mouser.ca/Search/Refine?Keyword='
        Digikey_URL = "https://www.digikey.ca/en/products?KeyWords="
        Search_URL = Digikey_URL + self.TargetPN

        self.chrome.get(Search_URL)

        try:
            SearchCount = int(self.chrome.find_element_by_xpath('/html/body/div[2]/main/section/div[1]/section/div[1]/div[2]/span/span').text)
            if SearchCount > 1:
                ### Search it until single product
                #First_PartNumber = self.chrome.find_element_by_class_name("tr-mfgPartNumber")
                First_PartNumber = self.chrome.find_element_by_xpath('/html/body/div[2]/main/section/div[2]/div[2]/div/div[1]/table/tbody/tr[1]/td[2]/div/div[3]/a[1]')
                #aTag = First_PartNumber.find_element_by_tag_name("a")
                url = First_PartNumber.get_attribute("href")
                self.chrome.get(url)
        except:
            pass

        ParameterRow = self.chrome.find_elements_by_tag_name("tr")
        self.PartInfo = {}
        for param in ParameterRow:
#            idx_space = param.text.find(' ')
            idx_newline = param.text.find('\n')
#            idx = min([idx_space,idx_newline])
            idx = idx_newline
            Param_Later = param.text[idx + 1:]
            if len(Param_Later) > 0:
                if Param_Later[:2] == '/ ':
                    Param_Later = Param_Later[2:]
                if Param_Later[0] == ' ':
                    Param_Later = Param_Later[1:]
                if Param_Later[:2] == '- ':
                    Param_Later = Param_Later[2:]

            if Param_Later.find('\n') == -1:
                self.PartInfo[param.text[:idx]] = Param_Later[:]
            else:
                self.PartInfo[param.text[:idx]] = Param_Later[:Param_Later.find('\n')]

        #### Getting DigiKey Qty ###
        try:
            Qty_text = self.chrome.find_element_by_xpath('/html/body/div[2]/main/div/div[1]/div[2]/div[1]/div/div[1]/div/div/span').text
            return Qty_text
        except:
            return ""



if __name__ == "__main__":
    starttime = time.time()
    PartNumber = "MAX13450EAUD+"
    DigikeyResult = Digikey_WebScraping(PartNumber=PartNumber)
    DigikeyResult.Scraping()

    for key, value in DigikeyResult.PartInfo.items():
        print("{} : {}".format(key, value))

    DigikeyResult.terminate()
    elapsedtime = time.time() - starttime

    print("Operation Completed in {:.3}s".format(elapsedtime))