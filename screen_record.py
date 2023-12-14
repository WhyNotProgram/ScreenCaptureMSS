import time

from mss import mss
import cv2 as cv
import numpy as np

with mss() as sct:
    # region ------------- MSS Setup ------------- #
    monitor_number = 2
    mon = sct.monitors[monitor_number]

    monitor = {'top': mon['top'] + 140, 'left': mon['left'] + 5, 'width': 900, 'height': 600, 'mon': monitor_number}
    # endregion ------------------------

    # region ------------- FPS Setup ------------- #
    prev_time = 0
    fps_display_delay = 0
    fps_delayed = 0
    fps_list = [0.0] * 10
    # endregion ------------------------

    while True:
        capture_screenshot = sct.grab(monitor)

        # noinspection PyTypeChecker
        img = np.asarray(capture_screenshot)

        # region ------------- FPS Manager ------------- #

        # Calculate the FPS
        current_time = time.perf_counter()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        # Add current FPS to list and remove last element
        fps_list.append(fps)
        fps_list.pop(0)

        # Get the average using the last 10 frames
        average_fps = sum(fps_list) / len(fps_list)
        fps_display_delay += 1

        if fps_display_delay >= 3:
            fps_delayed = average_fps  # update delayed fps
            fps_display_delay = 0  # reset counter

        # Drag the FPS on image
        cv.putText(img, f'FPS: {fps_delayed: .0f}', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # endregion ------------------------

        # region ------------- Display Image ------------- #
        cv.imshow('Screen Capture', img)

        # Exit
        if cv.waitKey(1) & 0xFF == ord('q'):
            cv.destroyAllWindows()
            break
        # endregion ------------------------
