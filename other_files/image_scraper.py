
## I was using this script to scrape for tinder images to gather data and have a more approximate face and color recognition
### Driver and navigation setup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://tinder.com/")
###
import time
import bs4
## we use this module to download the images
import urllib.request

##check if the whatever element we are using is loaded
def check_Loaded(search,waiting):
    element=driver.find_elements_by_css_selector(search)
    i=0
    while True:
        element=driver.find_elements_by_css_selector(search)
        i=i+1

        if len(element)>0 or i>waiting:
            print("logged in!")
            break
### function to get and download the picture
def get_picture(name):
    
    ## we get the html first
    html=driver.page_source
    soup=bs4.BeautifulSoup(html,'html.parser')
    #we select the div where the image is as a backgroudn
    pictures=soup.select(".Expand.CenterAlign > .StretchedBox")
    #print(len(pictures))
    ## we loop over all of the divs
    for picture in pictures:
        try:
 ## if the picture has an style attriubute and a background image property, we grab the image
            if picture["style"]: 
                properties=picture["style"].split(";")
                for prop in properties:
                    if "background-image" in prop:
                        url=prop[23:len(prop)-2]
                        ## we download the images in the prefered folder
                        #print(url)
                        urllib.request.urlretrieve(url,f"../pictures/{name}.jpg")

        except:
            continue

check_Loaded(".react-swipeable-view-container",20000) ##check that we can swipe! :D
time.sleep(4)

index=0
## here I download the images of each profile infinetely
while True:
    index=index+1
    get_picture(f"new_round{index}")
    elem=driver.find_elements_by_css_selector(".button")
    time.sleep(1)
    elem[1].click()


        

    


