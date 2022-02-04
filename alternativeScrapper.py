import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import streamlit as st

def scrape(url):
    data=[]

    with Chrome(executable_path=r'C:\Program Files\chromedriver.exe') as driver:
        option = webdriver.ChromeOptions()
        option.add_argument("--headless")  # to make sure that the GUI is not visible to the user
        option.add_argument("--disable-dev-shm-usage")
        option.add_argument("--no-sandbox")
        # change executable path according to the web driver location on your system
        option.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=option)
        wait = WebDriverWait(driver,15)
        driver.get(url)

        for item in range(200): 
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
            time.sleep(15)

        for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content"))):
            data.append(comment.text)
            
    return data
  
  def app():
    url = st.text_input("YouTube URL", placeholder = "Enter YouTube URL")
    data = scrape(url)
    st.write(data)
    

app()
