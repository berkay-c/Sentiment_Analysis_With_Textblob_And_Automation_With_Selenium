from selenium import webdriver
import time
from urllib.parse import urlparse
import pandas as pd
from MainApp import ProgressBarThread
from webdriver_manager.firefox import GeckoDriverManager



def getRestaurantName():
    Name = input("Please Enter Restaurant Name = ")
    return Name


def getRestourantLinkAndRating(restourantname):
    # The link obtained at the end of the city and district selection
    driver.get("https://www.yemeksepeti.com/aydin/efeler-cumhuriyet-mah")
    searchBox = driver.find_element_by_css_selector(".search-box")
    searchBox.send_keys(restourantname)  
    time.sleep(3)
    searchButton = driver.find_element_by_css_selector("span.ys-icons")
    searchButton.click()
    time.sleep(3)
    # Get Rating
    rating = driver.find_element_by_css_selector(".point").text
    time.sleep(4)
    # Get Restourant Link
    restourantLink = driver.find_element_by_xpath(
        "//div[@class='restaurant-display-name']/a").get_attribute("href")
    return restourantLink, rating


def clickCommentSectionAndGetAllCommentsAndReturnCommentDataFrame(getrestourantLink):
    pb_thread = ProgressBarThread('Automation is working')
    pb_thread.start()

    driver.get(getrestourantLink)
    time.sleep(3)
    # Click Comment Section
    sectionComment = driver.find_element_by_css_selector(
        ".page-tabs > li:nth-child(4) > a:nth-child(1)")
    sectionComment.click()
    time.sleep(3)
    # Get All Comments
    commentlist_page_pagination_get_href = driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div[2]/div[2]/div[4]/nav/ul/li[1]/a").get_attribute("href")
    learn_max_page_number_link = commentlist_page_pagination_get_href+"99"
    driver.get(learn_max_page_number_link)
    time.sleep(3)
    max_commentlist_page_pagination_url = driver.current_url
    # Split 'max_commentlist_page_pagination_url'  with UrlParser and get Comment List Max Page
    parts = urlparse(max_commentlist_page_pagination_url)
    split_url = parts.query.strip("=").split("=")
    max_page_numbers = split_url[2]  # print(max_page_numbers)
    # We assign the necessary url to the variable to navigate the Comment Pages that we will use later.
    size = len(max_page_numbers)
    navigate_The_Comment_Page_url = max_commentlist_page_pagination_url[:len(
        max_commentlist_page_pagination_url)-size]
    listOfComments = []
    for pageNumber in range(1, int(max_page_numbers)+1):
        driver.get(navigate_The_Comment_Page_url+str(pageNumber))
        time.sleep(3)
        # The following code is receiving comments.
        getComments = driver.find_elements_by_xpath(
            "//div[@class='comment row']/p")
        for com in getComments:
            # print(com.text)
            listOfComments.append(com.text)

    pb_thread.stop()
    
    print("{} COMMENTS COLLECTED.".format(len(listOfComments)))
    dataFrameOfComments = pd.DataFrame(data=listOfComments, columns=["Comments"], dtype='string')
    # print(dataFrameOfComments)
    driver.quit()
    return dataFrameOfComments


if __name__ == '__main__':
    R_Name = getRestaurantName()
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver.set_window_position(50, 100)
    driver.set_window_size(1000, 1100)
    restourantLink, restourantRating = getRestourantLinkAndRating(R_Name)
    CommentsDataFrame = clickCommentSectionAndGetAllCommentsAndReturnCommentDataFrame(restourantLink)
    CommentsDataFrame.to_csv("DataForSentimentAnalysis.csv", index=False)
