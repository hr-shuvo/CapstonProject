import pandas as pd
import numpy as np

from selenium import webdriver
import time



def main():
    url = 'https://www.goodreads.com/list/show/1.Best_Books_Ever'

    driver = webdriver.Chrome()
    driver.get(url=url)



    time.sleep(10)
    driver.close()



if __name__ == '__main__':
    main()