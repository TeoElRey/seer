import cv2
import pandas as pd
from datetime import datetime
import numpy as np

df = pd.DataFrame(columns=["Start", "End"])
first_frame = None
status_list = [None, None]
times = []
video = cv2.VideoCapture(1)

while True:
  check, frame = video.read()
  status = 0
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  gray = cv2.GaussianBlur(src=gray, ksize=(21,21), sigmaX=0)
  
  if first_frame is None:
    first_frame = gray
    continue
  
  delta_frame = cv2.absdiff(first_frame, gray)
  delta_frame = cv2.dilate(delta_frame, np.ones((5,5)), iterations=1)
  thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
  
  cnts,_ = cv2.findContours(thresh_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  
  for contour in cnts:
    if cv2.contourArea(contour) < 100:
      continue
    status = 1
    # (x, y, w, h) = cv2.boundingRect(contour)
    # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.drawContours(image=frame, contours=contour, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
  status_list.append(status)
  
  status_list = status_list[-2:]
  
  if status_list[-1] == 1 and status_list[-2] == 0:
    times.append(datetime.now())
    
  if status_list[-1] == 0 and status_list[-2] == 1:
    times.append(datetime.now())
    
  cv2.imshow("Capturing", gray)
  cv2.imshow("delta frame", delta_frame)
  cv2.imshow("Threshold frame", thresh_frame)
  cv2.imshow("Color frame", frame)
  alpha = 0.1
  first_frame = cv2.addWeighted(first_frame, 1 - alpha, gray, alpha, 0)
  key = cv2.waitKey(1)
  
  if(key == ord('q')):
    if status == 1:
      times.append(datetime.now())
    break
  
# print(status_list)
# print(times)

for i in range (0, len(times), 2):
  df = pd.concat([df, pd.DataFrame.from_dict({"Start": [times[i]], "End": [times[i+1]]})], ignore_index=True)
  
df.to_csv("Times.csv")
video.release()
cv2.destroyAllWindows

