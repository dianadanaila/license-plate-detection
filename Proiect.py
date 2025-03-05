#Libraries
import cv2
import tkinter as tk
import easyocr
import matplotlib.pyplot as plt


tab = tk.Tk()

def screen():
    
    haarcascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")

    cap = cv2.VideoCapture(0)
    cap.set(3,640) #latime
    cap.set(4,480) #lungime
    count=0
    minArea= 500


    while True:
        success, img = cap.read()
        
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        plates = haarcascade.detectMultiScale(imgGray, 1.1, 4)
        for (x,y,w,h) in plates:
            area = w*h
            if area > minArea:
                cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0),2)
                cv2.putText(img, "Plate Number", (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 1,(0, 255 , 255), 2)
                imgtst=img[y:y+h,x:x+w]
                cv2.imshow("Zambiti",imgtst)
                cv2.imwrite('poza.jpg',imgtst)  
        cv2.imshow("Result", img)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite('images.jpeg', imgtst)
            cv2.rectangle(img,(0,200),(640,300),(255,0,0),cv2.FILLED)
            cv2.putText(img,"Salvat",(15,265),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),2)
            cv2.imshow("Final", img)
            cv2.waitKey(500)
            count=count+1
            break
    cap.release()
    cap.destroyAllWindows()
    
    
def citit():

    img= cv2.imread('images.jpg')

    reader= easyocr.Reader(['en'], gpu=False)

    text =reader.readtext(img)

    for t in text:

        print(t)
        bbox, text, score=t

        cv2.rectangle (img, bbox[0],bbox[2], (0,255,0),1)
        cv2.putText(img,text,bbox[0],cv2.FONT_HERSHEY_COMPLEX,1 ,(255, 0 ,0),3)

        plt.imshow(img)
        plt.show()

tab.geometry("500x500", )
tab.resizable(width=False, height=False)
tab.configure(background='black')
a=tk.Button(tab,text='Poza', command =screen,bg='blue', fg= 'red')
a.pack(padx=100, pady=20, side=tk.LEFT)
b=tk.Button(tab,text='Date', command= citit,bg='blue', fg= 'red')
b.pack(padx=100, pady=20, side=tk.RIGHT)


tab.mainloop()