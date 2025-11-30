import cv2
import numpy as np

width, height = 800, 600
video = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 30, (width, height))

for _ in range(300):
    # Генерация флуид-эффекта через шум
    frame = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    video.write(frame)

video.release()