import cv2
import easyocr

picture = cv2.imread('.\cars\car3.PNG')
reader = easyocr.Reader(['en'])
#picture_crop = picture[x0:x1, y0:y1]
#resized_crop = cv2.resize(picture_crop, (picture_crop.shape[1]*10, picture_crop.shape[0]*10))
#_, black_white_numberplate = cv2.threshold(resized_crop, 120, 255, cv2.THRESH_BINARY_INV)

running = True
numberplate_characters = reader.readtext(picture)
accuracy_threshold = 0.3
filtered_words = []
for item in numberplate_characters:
    text = item[1]
    confidence = item[2]

    if confidence > accuracy_threshold:
        filtered_words.append(text)  # Add the text to the filtered list

result = " ".join(filtered_words)
print(numberplate_characters)
print(result)

"""
while running:
    cv2.imshow('image', picture)
    cv2.imshow('image2', picture_crop)
    key = cv2.waitKey(0)

    if key == 27:  #esc
        running = False

cv2.destroyAllWindows()  
"""