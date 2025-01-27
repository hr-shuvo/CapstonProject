import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# store unique length of row // it will help to know if there are any missing data 
unique_lengths = set()
book_details = []

def get_book_details(book):
    global unique_lengths

    details = book.text.split('\n')
    # title = book.find_element(By.CLASS_NAME, 'bookTitle').text
    unique_lengths.add(len(details))

    if len(details) == 12:
        details.insert(3, '')

    content = {}

    content['Rank']  = details[0]
    content['Title'] = details[1]
    content['Author']= details[2]
    content['Rating']= details[4]
    
    

    return content




def main():
    url = 'https://www.goodreads.com/list/show/1.Best_Books_Ever'

    driver = webdriver.Chrome()
    driver.get(url=url)

    columns = ['Rank', 'Title', 'Author', 'Rating']

    data_table = driver.find_element(By.ID, 'all_votes')

    table_body = data_table.find_element(By.XPATH, './table/tbody')

    rows = table_body.find_elements(By.XPATH, './tr')


    for idx, row in enumerate(rows):
        book_details.append(get_book_details(row))

    # print('different types of length (tr): ', unique_lengths)


    df = pd.DataFrame(data=book_details, columns=columns)
    print(df.head())
    df.to_csv('data.csv', index=False)

    



    time.sleep(10)
    driver.close()



if __name__ == '__main__':
    main()