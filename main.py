from ultralytics import YOLO
import cv2
import numpy as np
import os

# Set debug True/False to obtain or not frames of the intermediate
# steps for debbuging purposes.
debug = True

# Modify the following parameters if needed:
input_video_name  = "input_video.mp4"
output_video_name = "output_video.mp4"
yolo_model_name   = "yolov8n.pt"
output_fps        = 30
classes           = [41]    # 41 is for 'cup'
ksize             = (25,25) # Blur filter size

# Define paths
root_path = os.path.abspath(os.path.dirname(__file__)) + "/"
input_video_path  = root_path + input_video_name
output_video_path = root_path + output_video_name

# Paths for debugging results:
original_path   = root_path + "debug_images/original/"
roi_path        = root_path + "debug_images/roi/"
blur_roi_path   = root_path + "debug_images/blur_roi/"
blur_frame_path = root_path + "debug_images/blur_frame/"

# Load YOLOv8 model
model = YOLO(yolo_model_name)

# Open the video file
input_video = cv2.VideoCapture(input_video_path)

# Set the output video
fps = output_fps #int(input_video.get(cv2.CAP_PROP_FPS))
video_w = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH))
video_h = int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
output_video = cv2.VideoWriter(output_video_path, 
                               cv2.VideoWriter_fourcc(*'mp4v'), 
                               fps, 
                               (video_w, video_h), 
                               isColor=True)

# Loop through the video frames
j = 0
while input_video.isOpened():
    j  += 1
    # Read a frame from the video
    success, frame = input_video.read()

    if success:
        # Get a copy of the original frame
        original_frame = np.copy(frame)

        # Run YOLOv8 inference on the frame
        results = model(source=frame, 
                        device='cpu',
                        classes=classes)

        if len(results) == 1:
            for result in results:
                if len(result.boxes) == 1:
                    for i in range(len(result.boxes)):
                        x1 = int(result.boxes.xyxy[i][0])
                        y1 = int(result.boxes.xyxy[i][1])
                        x2 = int(result.boxes.xyxy[i][2])
                        y2 = int(result.boxes.xyxy[i][3])
                        roi = frame[y1:y2, x1:x2]
                        blur_roi = np.copy(roi)
                        cv2.GaussianBlur(blur_roi, ksize, 0, blur_roi)
                        frame[y1:y2, x1:x2] = blur_roi
                        
                        # TODO UNtrack and retrack modifying problem with roi withoutblur
                        if debug == True:
                            original_name = original_path + "frame_"+str(j)+".jpg"
                            cv2.imwrite(original_name, original_frame)
                            roi_name = roi_path + "frame_"+str(j)+".jpg"
                            cv2.imwrite(roi_name, roi)
                            blur_roi_name = blur_roi_path + "frame_"+str(j)+".jpg"
                            cv2.imwrite(blur_roi_name, blur_roi)
                            blur_frame_name = blur_frame_path + "frame_"+str(j)+".jpg"
                            cv2.imwrite(blur_frame_name, frame)

                        # Comment/uncomment the following line to draw a
                        # rectangle in the output video around the detected 
                        # element
                        # cv2.rectangle(frame, (x1,y1), (x2, y2), (255,0,0), 2)
                else:
                    pass
        else:
            pass

        # Save the annotated frame
        output_video.write(frame)

    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object
input_video.release()