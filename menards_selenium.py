from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import menards_sql as msq

## constants used to remove unecessary characters from html content
SKU = 5
MODEL = 7
itemPrice = 0
noDollar = 1

Erics_driver_location = r'C:/Users/Eric/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Python 3.6/chromedriver.exe'

Menards_shop_all_depts_url = 'https://www.menards.com/main/shop-all-departments/c-19384.htm'
Menards_home_page_url = 'https://www.menards.com/main/home.html'


# must appear exactly how it is spelled out in this list
Departments_to_look_at = [
    '',

]


'''
def connect_chrome_driver(url, driver_location):
    driver = webdriver.Chrome(executable_path=)
    driver.get(item_url)
'''

def navigate_Menards_depts():
    '''
    traverses all 
    '''

    # connect to web driver
    driver = webdriver.Chrome(executable_path=Erics_driver_location)
    driver.get(Menards_home_page_url)

    try:
        #obtain list of departments
        depts_list_at_page_bottom = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "footerQuicklinks")))
        depts_links = depts_list_at_page_bottom.find_element_by_class_name("leftFloat").find_elements_by_tag_name("li")
        
        for dept in depts_links:
            dept_name = dept.text

            # don't click any links after Project Center
            if dept_name == "Project Center":
                return

            print("Navigating to {} dept. webpage".format(dept_name))
            dept.click()
            
    except Exception as e:
        print("error: ", e)
    finally:
        driver.close()


def scour_items_page(driver):
    '''
    Searches and collects data about items, must be a page that has the grid view of Menards items.
    '''
    menards_db = msq.connect_to_sql()

    try:
        scour_more_pages = True
        
        while scour_more_pages:
            print("\nScouring: {}\n".format(driver.current_url))
            grid_area = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "grid")))
            items = grid_area.find_elements_by_class_name("ps-item")

            # obtain info on items in grid
            for i in items:
                try:
                    item_desc = i.find_element_by_class_name("ps-item-title").text

                    #determine whether item is designated by SKU or Model
                    identifier = i.find_element_by_class_name("ps-item-sku")
                    if identifier.text.startswith("SKU"):
                        item_ID = identifier.text[SKU:]
                    else:
                        item_ID = identifier.text[MODEL:]
                        
                    
                    item_price = i.find_element_by_class_name("priceInfo").text.split()[itemPrice][noDollar:]
                    if not item_price.isdigit(): #assign -1 if the price is one that requires user to add it to their cart
                        item_price = -1.0

                    print("{} is ${} (ID: {})".format(item_desc, item_price, item_ID))
                    
                    ##insert into DB
                    msq.insert_item_desc(conn=menards_db, ID=item_ID, desc=item_desc)
                    msq.insert_item_price(conn=menards_db, ID=item_ID, price=item_price)

                except NoSuchElementException:
                    pass

            # more pages to scour as indicated by active right arrow in pagination
            try:
                driver.find_element_by_css_selector(".fa.fa-chevron-right.disabledPaginationArrow")
                scour_more_pages = False
            except NoSuchElementException:   
                driver.find_element_by_class_name("fa-chevron-right").click()

    except Exception as e:
        print("error: ", e)
        driver.close()


def quick_test():
    item_url = "https://www.menards.com/main/tools-hardware/power-tools-accessories/power-tool-combo-kits/c-9066.htm"
    driver = webdriver.Chrome(executable_path=Erics_driver_location)
    driver.get(item_url)
    scour_items_page(driver)
    
    print("Finished")
    driver.close()

if __name__ == '__main__':

    '''
    url = "https://www.menards.com"
    item_url = "https://www.menards.com/main/tools-hardware/power-tools-accessories/power-tool-accessories/drill-bits-accessories/c-10079.htm?Spec_ProductType_facet=Twist+Bits"
    driver = webdriver.Chrome(executable_path=Erics_driver_location)
    
    test_urls = [
        'https://www.menards.com/main/tools-hardware/power-tools-accessories/power-tool-accessories/drill-bits-accessories/c-10079.htm?Spec_ProductType_facet=Twist+Bits',
        'https://www.menards.com/main/electrical/light-bulbs/fluorescent-tubes/c-7478.htm'
    ]

    for u in test_urls:
        driver.get(u)
        scour_items_page(driver)
    '''
    
    
    quick_test()
    
    
    print("Finished")
    




