## Import Image for fomatting purposes
from PIL import Image
from env import azure_key,face_api_domain
###  here we setup everything regarding the chrome driver and the bot navigator
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
###
### 
import time
import bs4
## we use this module to download the images
import urllib.request
import requests
###
import face_recognition
import numpy
import cv2
eye_frames=[]

## headers for the azure face api
headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': azure_key,
}


### Microsoft face detector
FaceApiDetect = face_api_domain

def check_Loaded(search,waiting):
    element=driver.find_elements_by_css_selector(search)
    i=0
    while True:
        element=driver.find_elements_by_css_selector(search)
        i=i+1

        if len(element)>0 or i>waiting:
            print("logged in!")
            break

def get_current_picture():
    
    ## we get the html first
    html=driver.page_source
    soup=bs4.BeautifulSoup(html,'html.parser')
    #we select the div where the image is as a backgroudn
    pictures=soup.select(".Expand.CenterAlign > .StretchedBox")
    #print(len(pictures))
    ## we loop over all of the divs
    picture_urls=[]
    for picture in pictures:
        try:
 ## if the picture has an style attriubute and a background image property, we grab the image
            if picture["style"]: 
                properties=picture["style"].split(";")
                for prop in properties:
                    if "background-image" in prop:
                        url=prop[23:len(prop)-2]
                        picture_urls.append(url)
                       
        except:
            continue
    print(picture_urls)
    ## make sure we get the actual picture of the user we are swiping
    current_pic=picture_urls[1]
    urllib.request.urlretrieve(current_pic,f"./temp_pics/current_pic.jpg")
    picture_urls=[]
    
def get_current_picture_file():
    return  face_recognition.load_image_file("./temp_pics/current_pic.jpg")

def get_faces(image):
        return  face_recognition.face_locations(image)
def get_average_color(frame):

    average_color=[0,0,0]
    total=0
    for elem in frame:

        for color_point in elem:
                r,g,b=color_point
                if r+g+b>100 and r+g+b<400:
    
                    average_color[0]+=r
                    average_color[1]+=g
                    average_color[2]+=b
                    total+=1
    for index,elem in enumerate(average_color):
        if total==0:break
        average_color[index]=elem/total

    r,g,b=average_color
    print(b*2+g-r)   
    return average_color
def get_average_both_eyes(eyes):
    final_average_color=[0,0,0]
    for r,g,b in eyes:
            final_average_color[0]+=r
            final_average_color[1]+=g
            final_average_color[2]+=b
    for index,elem in enumerate(final_average_color):
        final_average_color[index]=elem/len(eyes)
    return final_average_color
def analyze_eyes_color(img):
    landmarks=face_recognition.face_landmarks(img)
    for feature in landmarks:
        right_eye=get_eye(feature["right_eye"],img)
        left_eye=get_eye(feature["left_eye"],img)
        r_color=get_average_color(right_eye)
        l_color=get_average_color(left_eye)
        color=(get_average_both_eyes([r_color,l_color]))
        
        return color

        # eyes_avg_color.append(r_color)
        # eyes_avg_color.append(l_color)
def get_eye(eye,single_img):
    highestX=0
    lowestX=float('inf')
    highestY=0
    lowestY=float("inf")
    for index,elem in enumerate(eye):
            x,y=eye[index]
            if x>highestX: highestX=x
            if x<lowestX: lowestX=x
            if y>highestY: highestY=y
            if y<lowestY: lowestY=y
           
    w=highestX-lowestX
    h=highestY-lowestY
    eye=single_img[int(lowestY+h/5):lowestY+h,int(lowestX+w/4):int(highestX-w/4)]
    bgr_frame=eye[:,:,::-1]
    eye_frames.append(bgr_frame)
    return eye



def get_nose_frame(nose,single_img):
    start=nose[0]
    end=nose[3]
    h=end[1]-start[1]
    nose_frame=single_img[start[1]:start[1]+h,start[0]-4:start[0]+4]
    #print(nose_frame)
    cv2.rectangle(single_img,start,end,(0,255,0),5)
    return nose_frame

user_color=input("what hair color do you want?")
print(user_color)
is_smile=input("do you want a smile?")
print(is_smile)
driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://tinder.com/")
check_Loaded(".react-swipeable-view-container",20000) ##check that we can swipe! :D
time.sleep(4)


while True:
    try:
        time.sleep(2)
        buttons=driver.find_elements_by_css_selector(".button")

        get_current_picture()
        current_picture_file=get_current_picture_file()
        faces_list=get_faces(current_picture_file)
        if len(faces_list)==0:
                print("face not found")
                buttons[1].click()
        elif len(faces_list)>1: 
            print("too many faces")
            buttons[1].click()

        else:

            im = Image.open("./temp_pics/current_pic.jpg").convert("RGB")
            im.save("./temp_pics/current_pic.jpg","jpeg")
            data = open("./temp_pics/current_pic.jpg","rb")
            response = requests.post(FaceApiDetect, headers=headers,data=data)
            face_info=response.json()
            #print(str(face_info))
            face_props=face_info[0]["faceAttributes"]
            current_smile=face_props["smile"]
            hair_color=face_props["hair"]["hairColor"]
            sorted_hair=sorted(hair_color, key=lambda x: x["confidence"],reverse=True)
            likely_color=sorted_hair[0]["color"]
            print(face_props)
            if likely_color==user_color: 
                    if is_smile=="yes":
                        if  current_smile>0.8:
                             buttons[3].click()
                        else:
                            buttons[1].click()


                    else:
                        buttons[3].click()
            else:
                print("wanted color")
                buttons[1].click()


          
            # r,g,b=analyze_eyes_color(current_picture_file)
            # print(r,g,b)
            # color_index=-r+g+b*2
            
            ##if color_index>170:
            # print("blue eyes")
            # buttons[3].click()
            # else:
            #     print("no blue eyes")
            #     buttons[1].click()
    except Exception as e: 
        print(e)
        break

for index, elem in enumerate(eye_frames):
    cv2.imshow(f"{index}",elem)



cv2.waitKey(0)
cv2.destroyAllWindows()






    # right_arrow=driver.find_elements_by_css_selector(".tappable-view")[1]
    # size=right_arrow.size
    # action = webdriver.common.action_chains.ActionChains(driver)
    # action.move_to_element_with_offset(right_arrow, int(size["width"]-size["width"]*0.1), int(size["height"]/2))
    # action.click()
    # action.perform()
    # if get_picture(f"pic_{index}"):
    #     right_arrow=driver.find_elements_by_css_selector(".tappable-view")[1]
    #     size=right_arrow.size
    #     action = webdriver.common.action_chains.ActionChains(driver)
    #     action.move_to_element_with_offset(right_arrow, int(size["width"]-size["width"]*0.1), int(size["height"]/2))
    #     action.click()
    #     action.perform()
    # else:
    #     buttons=driver.find_elements_by_css_selector(".button")
    #     buttons[1].click()

   

    # try:
    #     right_arrow[1].click_At
    # except:

    #     buttons[1].click()

