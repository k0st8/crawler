from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, re

driver = webdriver.Firefox(service=Service(executable_path=GeckoDriverManager().install()))
driver.get('https://example.com')
# Wait for page load
# time.sleep(5)
elm = WebDriverWait(driver, 10).until(
    lambda x: x.find_element(By.XPATH, "//div[@class='all-courses']")
)
links = driver.find_elements(By.XPATH, '//a[@class="course-preview-link"]')
c = []
# Search for the link with the desired trigger word
for link in links:
    bingo = link.get_attribute('href')
    # Change or add if there is somthing that you like this: |word
    if re.search('hack|cyber|python|bug|pentest', bingo):
        # click on the link
        driver.execute_script('''window.open("%s","_blank");''' % bingo)
        driver.switch_to.window(driver.window_handles[1])
        # Checking the Language of the course
        lang = WebDriverWait(driver, 15).until(
            lambda x: x.find_element(By.XPATH, '//html/body/div/div[2]/div/div[1]/div[5]/span/div/h5').text
        )
        # Sibling is not working !!!
        # lang = driver.find_element(By.XPATH, '//*[@class="bi-globe"]//following-sibling::h5').text
        if re.search('English', lang):
            bb = driver.find_element(By.XPATH, '//div[@class="three"]/a').get_attribute('href')
            c.append(bb)
            time.sleep(3)
        # Close tab
        driver.close()
        # Switch back to first tab
        driver.switch_to.window(driver.window_handles[0])
        # print(bingo)

# Get the COUPON from the URL on the Course Page
# Session for opening new tabs
coupons = []
for cc in c:
    res = re.search('ulp=(.*)', cc)
    if res:
        coupons.append(res[1])
# Close the used one move on to new
time.sleep(5)
driver.close()

# Create file with COUPON links
with open("udemy_" +time.strftime("%Y%m%d-%H%M%S") + ".txt", 'w') as f:
    for line in coupons:
        f.write(f"{line}\n")
