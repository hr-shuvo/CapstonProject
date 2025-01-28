import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# store unique length of row // it will help to know if there are any missing data 
unique_lengths = set()
book_details = []

def get_book_details(book):
    global unique_lengths

    details = book.text.split('\n')
    image = book.find_element(By.CLASS_NAME, 'bookCover')

    # print(details, '\n')

    unique_lengths.add(len(details))

    if len(details) == 12:
        details.insert(3, '')

    content = {}

    content['Rank']  = details[0]
    content['Title'] = details[1]
    content['Author']= details[2].replace('by ', '')
    content['Rating']= details[4].split()[0]
    content['Rating Count']= details[4].split()[4].replace(',','')
    content['Score'] = details[5].split()[1].replace(',','')
    content['People Voted'] = details[5].split()[3].replace(',','')

    content['Image'] = image.get_attribute('src')

    # print(content)
    
    

    return content




def main():
    url = 'https://www.goodreads.com/list/show/1.Best_Books_Ever'
      

    columns = ['Rank', 'Title', 'Author', 'Rating', 'Rating Count', 'Score', 'People Voted', 'Image']

    for pageId in range(1, 11):
        print(f'----------  Loading data for page {pageId}  ----------')
        siteUrl = f'{url}?page={pageId}'

        driver = webdriver.Chrome()  
        driver.get(url=siteUrl)

        data_table = driver.find_element(By.ID, 'all_votes')
        table_body = data_table.find_element(By.XPATH, './table/tbody')
        rows = table_body.find_elements(By.XPATH, './tr')

        for idx, row in enumerate(rows):
            book_details.append(get_book_details(row))                    

        driver.close()


    print(f'---------> page: {pageId}, different types of length (tr): ', unique_lengths)


    df = pd.DataFrame(data=book_details, columns=columns)
    print(df.head())
    df.to_csv('data.csv', index=False)    






if __name__ == '__main__':
    main()