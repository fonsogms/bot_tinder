
import cv2
import numpy
import face_recognition
import os
from PIL import Image
origin_folder="../pictures/working/other"
folder_paths = os.listdir(os.path.relpath(origin_folder))
images=[]
index=0
number_faces=0
eye_index=0
eyes_avg_color=[]
eye_frames=[]
noses=[]
##we append all of the rgb images into the images list
def get_images(files,origin):

    for pic in files:
        # using cv2 read for debuggin reasons
        img = cv2.imread(origin+"/"+pic)
        # using face_recognition for detection reasons
        image = face_recognition.load_image_file(origin+"/"+pic)
        # getting at the same time the landmarks
        land=face_recognition.face_landmarks(image)
        images.append((img,image,land))
def get_average_color(frame):
    average_color=[0,0,0]
    total=0
    for elem in frame:
        for color_point in elem:
            r,g,b=color_point
            average_color[0]+=r
            average_color[1]+=g
            average_color[2]+=b
            total+=1
            # else:
            #     print("color no aceptado",r,g,b)
    for index,elem in enumerate(average_color):
        if total==0:
            print(average_color)
            break
        average_color[index]=elem/total

    r,g,b=average_color
   # print(r,g,b)   
    return average_color
def get_average(colors):
    final_average_color=[0,0,0]
    for r,g,b in colors:
        final_average_color[0]+=r
        final_average_color[1]+=g
        final_average_color[2]+=b
    for index,elem in enumerate(final_average_color):
        final_average_color[index]=elem/len(colors)
    return final_average_color
def get_faces(image):
        return  face_recognition.face_locations(image)
def get_eye(eye,single_img):
    highestX=0
    lowestX=float('inf')
    global eye_index
    eye_index+=1
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
    #cv2.rectangle(single_img,(int(lowestX+w/4),int(lowestY+h/5)),(int(highestX-w/4),lowestY+h),(255,255,0),2)
    eye=single_img[int(lowestY+h/5):lowestY+h,int(lowestX+w/4):int(highestX-w/4)]    
    bgr_frame=eye[:,:,::-1]

    ##r,g,b=get_average_color(eye)
   ## if (b*2+g-r)>200:cv2.imshow("eye"+str(eye_index),bgr_frame)
   ## cv2.imshow("eye"+str(eye_index),bgr_frame)

    return eye

def get_nose_frame(nose,single_img):
    start=nose[0]
    end=nose[3]
    h=end[1]-start[1]
    nose_frame=single_img[start[1]:start[1]+h,start[0]-4:start[0]+4]
    #print(nose_frame)
    cv2.imshow(f"{index} cheese",nose_frame)
    cv2.rectangle(single_img,start,end,(0,255,0),5)
    return nose_frame
def paint_face(faces,single_img,landmarks):
    for top,right,bottom,left in faces:
        x=left
        y=top
        w=right-left
        h=bottom-top
        face = single_img[y:y+h, x:x+w]
        #print(sum(get_average_color(face)))
        cv2.rectangle(single_img,(x,y),(x+w,y+h),(255,255,0),2)
    
    for feature in landmarks:
        # right_eye=get_eye(feature["right_eye"],single_img)
        # left_eye=get_eye(feature["left_eye"],single_img)
        # r_color=get_average_color(right_eye)
        # l_color=get_average_color(left_eye)
        # eyes_avg_color.append(r_color)
        # eyes_avg_color.append(l_color)
        nose=feature["nose_bridge"]
        nose_frame=get_nose_frame(nose,single_img)
        nose_color=get_average_color(nose_frame)
        noses.append(nose_color)
        print(nose_color)

       # print(feature)

# making sure we have all of the images ready for bulk recognition
get_images(folder_paths,origin_folder)
for cvImg,face_image,land in images:
        index=index+1
        faces=get_faces(face_image)
        paint_face(faces,cvImg,land)
        if len(faces)>0:number_faces+=1
        #cv2.imshow(f'{index}',cvImg)

print(len(images),number_faces)
#print(eyes_avg_color)
# r,g,b=get_average(eyes_avg_color)
# print(r,g,b)
# blue_index=-r+g+b*2
# print(blue_index)
avg_nose=get_average(noses)
print(avg_nose)
cv2.waitKey(0)
cv2.destroyAllWindows()



