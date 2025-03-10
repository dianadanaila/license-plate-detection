import cv2
import tkinter as tk
import easyocr
import numpy as np
import matplotlib.pyplot as plt

reader = easyocr.Reader(['en'], gpu=False)

detected_plates = set()
saved_plate_path = "salvat.jpeg"  

# Initialize Tkinter window
tab = tk.Tk()
tab.title("License Plate Detection")
tab.geometry("500x400")
tab.resizable(width=False, height=False)
tab.configure(background='#f0f0f0')

#Instructions
instructions_label = tk.Label(tab, text="Click 'Poza' to detect a license plate.\nClick 'Date' to read detected data.", bg='#f0f0f0', font=("Arial", 12))
instructions_label.pack(pady=20)

def screen():
    global saved_plate_path  

    haarcascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")
    cap = cv2.VideoCapture(0) 
    cap.set(3, 640)
    cap.set(4, 480)

    minArea = 500
    detected_text = None  # Store detected plate number

    while True:
        success, img = cap.read()
        if not success or img is None:  
            print("Error: Failed to capture image.")
            continue  

        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        plates = haarcascade.detectMultiScale(imgGray, 1.1, 4)

        for (x, y, w, h) in plates:
            area = w * h
            if area > minArea:
                # Extract the plate region
                plate_img = img[y:y + h, x:x + w]
                plate_gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)

                # OCR text detection
                text = reader.readtext(plate_gray)

                for _, detected_text, _ in text:
                    if detected_text not in detected_plates:  # Avoid duplicates
                        detected_plates.add(detected_text)
                        print(f"Detected Plate: {detected_text}")  
                        saved_plate_path = "salvat.jpeg"
                        cv2.imwrite(saved_plate_path, plate_img)  # Save only plate region
                        break  # Stop after first detected plate
                
                
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(img, "Plate Detected", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)

        cv2.imshow("Real-Time Plate Detection", img)

        if cv2.waitKey(1) & 0xFF == ord('s'): 
            break

    cap.release()
    cv2.destroyAllWindows()

def citit():
    img = cv2.imread(saved_plate_path)
    if img is None:
        print("Error: Image 'salvat.jpeg' not found.")
        return

    text = reader.readtext(img)

    detected_texts_set = set()  

    for bbox, detected_text, _ in text:
        detected_texts_set.add(detected_text)  # Add detected text to the set

        
        (x1, y1) = bbox[0]  # Top-left corner
        (x2, y2) = bbox[2]  # Bottom-right corner

        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(img, detected_text, (int(x1), int(y1) - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

 
    if detected_texts_set:
        print("Plate ")
        print(" ".join(detected_texts_set))

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis('off')  
    plt.show()



# Buttons
button_frame = tk.Frame(tab, bg='#f0f0f0')
button_frame.pack(pady=30)

a = tk.Button(button_frame, text='Poza', command=screen, bg='blue', fg='white', font=("Arial", 14), width=15)
a.pack(side=tk.LEFT, padx=20)

b = tk.Button(button_frame, text='Date', command=citit, bg='green', fg='white', font=("Arial", 14), width=15)
b.pack(side=tk.RIGHT, padx=20)



tab.mainloop()
