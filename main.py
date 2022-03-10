from logging import currentframe
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.opera.webdriver import OperaDriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True

browser = webdriver.Firefox(options=options)
print("start...")
def loginSite():

    browser.get("YOUR_OPENCART_DOMAIN/admin/index.php?route=sale/order")

    time.sleep(2)

    username = browser.find_element_by_xpath("//*[@id='input-username']")
    password = browser.find_element_by_xpath("//*[@id='input-password']")

    username.send_keys(OPENCART_USERNAME)
    password.send_keys(OPENCART_PASSWORD)



    time.sleep(2)

    loginButton = browser.find_element_by_xpath("//*[@id='content']/div/div/div/div/div[2]/form/div[3]/button")
    loginButton.click()

    return browser.current_url.split("token=")[1]

getUrlToken = loginSite()

time.sleep(2)


def getLast10OrderIDs():
    orders = []
    orderRow = 1
    while orderRow < 10:
        elements = browser.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/form/div/table/tbody/tr[' + str(orderRow) + ']/td[2]')
        for element in elements:
            orders.append(element.text)
        orderRow += 1
    return orders


def getReadShipRecords(orderid):
    orderid = str(orderid)
    file = open("FOLDER_NAME/orderIDs.txt", "r", encoding = "UTF-8")
    contents = file.read()
    d = contents.splitlines()
    file.close()
   
    if orderid in d:
        return 1
    else:
        return 0

def getOrderInfo(orderID):

    browser.get("YOUR_OPENCART_DOMAIN/admin/index.php?route=sale/order/info&token=" + getUrlToken + "&order_id=" + orderID)

    time.sleep(2)

    getCallNumber = browser.find_element_by_xpath('//*[@id="content"]/div[2]/div[3]/div[2]/div/table/tbody/tr[4]/td[2]').text

    customerCallNumber = str(getCallNumber[-10:])

    customerInfo = browser.find_element_by_xpath("/html/body/div/div/div[2]/div[4]/div[2]/table[1]/tbody/tr/td[2]").text.splitlines()

    
    customerInfo.append(customerCallNumber)

    return customerInfo

orderIDs = getLast10OrderIDs()

time.sleep(5)

def yk_login():

    browser.get("https://selfservis.yurticikargo.com/")

    time.sleep(2)

    yk_username = browser.find_element_by_xpath('//*[@id="ctl00_main_txtUserName"]')
    yk_password = browser.find_element_by_xpath('//*[@id="ctl00_main_txtPassword"]')

    yk_username.send_keys(YURTICI_USERNAME)
    yk_password.send_keys(YURTICI_PASSWORD)

    yk_loginButton = browser.find_element_by_xpath('//*[@id="aspnetForm"]/div[5]/div[1]/div[2]/table/tbody/tr[4]/td[2]/span[1]')
    yk_loginButton.click()

    time.sleep(1)

    yk_newKargo = browser.find_element_by_xpath('//*[@id="tabs-0"]/div/div[1]/a[1]/img')
    yk_newKargo.click()

def yk_addRecordCargo(customerFullname, customerAddress, customerDistrict, customerCity, customerCallNumber):
    

    yk_customerFullname = browser.find_element_by_xpath('//*[@id="ctl00_ctl00_main_Content_txtReceiverName"]')
    yk_customerFullname.send_keys(customerFullname)
    yk_customerFullname.send_keys(Keys.TAB)

    time.sleep(1)

    yk_selectCityDD = browser.find_element_by_xpath('//*[@id="ctl00_ctl00_main_Content_tab1Container"]/div[3]/div/table/tbody/tr[3]/td[2]/div/div/div/div')
    yk_selectCityDD.click()

    time.sleep(1)

    yk_selectCity = Select(browser.find_element_by_xpath('//*[@id="ctl00_ctl00_main_Content_cbReceiverCity"]'))
    yk_selectCity.select_by_visible_text(customerCity)

    yk_selectDistrict = browser.find_element_by_xpath('//*[@id="ctl00_ctl00_main_Content_txtTownOrArea"]')
    yk_selectDistrict.send_keys(customerDistrict)
    time.sleep(2)
    yk_selectDistrict.send_keys(Keys.DOWN)
    yk_selectDistrict.send_keys(Keys.RETURN)

    time.sleep(1)

    yk_customerAddress = browser.find_element_by_xpath('//*[@id="ctl00_ctl00_main_Content_txtReceiverAddress"]')
    yk_customerAddress.send_keys(customerAddress)

    yk_customerCallNumber = browser.find_element_by_xpath('//*[@id="ctl00_ctl00_main_Content_txtReceiverGsm"]')
    yk_customerCallNumber.send_keys(customerCallNumber)

    time.sleep(1)

    yk_selectCargoTypeDD = browser.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[8]/div[3]/div[1]/div/div[7]/div/table/tbody/tr[1]/td[2]/div/div/div/div')
    yk_selectCargoTypeDD.click()
    yk_selectCargoType = Select(browser.find_element_by_xpath('//*[@id="ctl00_ctl00_main_Content_cbCargoType"]'))
    yk_selectCargoType.select_by_visible_text("1 - Mi")

    time.sleep(1)

    yk_cargoInfo = browser.find_element_by_xpath('//*[@id="ctl00_ctl00_main_Content_txtDescription"]')
    yk_cargoInfo.send_keys("SOKET")

    yk_selectADRESALIM = browser.find_element_by_xpath('//*[@id="ctl00_ctl00_main_Content_chkServiceList_0"]')
    yk_selectADRESALIM.click()


    yk_selectSIGORTA = browser.find_element_by_xpath('//*[@id="ctl00_ctl00_main_Content_chkServiceList_3"]')
    yk_selectSIGORTA.click()
    
    time.sleep(1)
    
    submit_button = browser.find_element_by_xpath('//*[@id="ctl00_ctl00_main_Content_tab1Container"]/div[10]/div/span[3]')
    submit_button.click()

orders = {}

for id in orderIDs:
    if getReadShipRecords(id) < 1:
        ship = getOrderInfo(id)
        print("kargolanıyor...")
        orders[id]=[{"name" : ship[0], "adres" : ship[1], "ilce" : ship[2], "il" : ship[3], "tel" : ship[5]}]

yk_login()

f=open("FOLDER_NAME/orderIDs.txt", "a+", encoding="UTF-8")
for i in orders:
    yk_addRecordCargo(orders[i][0]["name"], orders[i][0]["adres"], orders[i][0]["ilce"], orders[i][0]["il"], orders[i][0]["tel"])
    popup_close = browser.find_element_by_xpath('//*[@id="ctl00_ctl00_Body"]/div[5]/div[1]/a')
    print(orders[i][0]["name"] + " kargolandı.")
    time.sleep(2)
    popup_close.click()
    time.sleep(2)
    f.write(str(i) + '\n')

f.close()

browser.close()


time.sleep(5)
