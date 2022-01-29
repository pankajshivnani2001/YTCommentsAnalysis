from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import csv
import io
import pandas as pd
import os

# TODO: Return a file name constructed using the video title
# TODO: Alter the  sleep() time 
# TODO: Make changes in the while True loop.

def scrape_youtube_comments(
        url):  # takes the youtube video URL as parameter and returns the csv file name with the comments

    option = webdriver.ChromeOptions()
    option.add_argument("--headless")  # to make sure that the GUI is not visible to the user
    option.add_argument("--disable-dev-shm-usage")
    option.add_argument("--no-sandbox")
    # change executable path according to the web driver location on your system
    option.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=option)

    driver.get(url)
    driver.maximize_window()
    #sleep(5)
    sleep(1)

    try:
        video_title = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
        comment_section = driver.find_element_by_xpath('//*[@id="comments"]')

    except NoSuchElementException:  # in case the layout or element ids of youtube changes
        print("NoSuchElementException")
        return ""

    # execute JavaScript to scroll to the comments section
    driver.execute_script("arguments[0].scrollIntoView();", comment_section)
    #sleep(5)
    sleep(1)

    # execute JavaScript to scroll to the bottom of the document
    prev_h = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        # execute JavaScript to scroll down and wait for new comments to load .
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        #sleep(5)
        sleep(1)

        # calculate new height
        curr_h = driver.execute_script("return document.documentElement.scrollHeight")
        comments = driver.find_elements_by_xpath('//*[@id="content-text"]')
        if curr_h == prev_h or len(comments) > 400:  # no new comments
            break
        prev_h = curr_h

    try:
        # Extract the elements storing the usernames, comments and number of likes.
        usernames = driver.find_elements_by_xpath('//*[@id="author-text"]')
        comments = driver.find_elements_by_xpath('//*[@id="content-text"]')
        num_of_likes = driver.find_elements_by_xpath('//*[@id="vote-count-middle"]')

    except NoSuchElementException:  # in case the layout or element ids of youtube changes
        print("NoSuchElementException")
        return ""

    df = pd.DataFrame(columns=["Username", "Comment", "Likes"])
    username_lst = []
    comment_lst = []
    likes_lst = []

    for username, comment, likes in zip(usernames, comments, num_of_likes):
        username_lst.append(username.text)
        comment_lst.append(comment.text)
        likes_lst.append(likes.text)

    driver.close()

    d = {"Username": username_lst, "Comment": comment_lst, "Likes": likes_lst}
    #df = pd.DataFrame(d)

    #return df
    return d
