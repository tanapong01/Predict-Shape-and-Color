import cv2
import numpy as np
from ultralytics import YOLO
from picamera2 import Picamera2

model = YOLO('train4/last.pt')
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

def choose_by_case():
    shape_list = []
    color_list = []
    result_list = []

    while True:
        text_input = input('Do you want to predict by shape, color, or overall? : ')
        if text_input not in ['shape', 'color', 'overall']:
            print('Invalid input. Please enter shape, color, or overall.')
            continue

        if text_input.lower() == 'shape':
            shape_input = input('Shape (cube/cylinder/prism): ')
            if shape_input not in ['cube', 'cylinder', 'prism']:
                print('Invalid input. Please enter cube, cylinder, or prism.')
                continue

            if shape_input.lower() == 'cube':
                result_list.extend([0, 1, 2])
            elif shape_input.lower() == 'cylinder':
                result_list.extend([3, 4, 5])
            elif shape_input.lower() == 'prism':
                result_list.extend([6, 7, 8])

        elif text_input.lower() == 'color':
            color_input = input('Color (blue/red/yellow): ')
            if color_input not in ['blue', 'red', 'yellow']:
                print('Invalid input. Please enter blue, red, or yellow.')
                continue

            if color_input.lower() == 'blue':
                result_list.extend([0, 3, 6])
            elif color_input.lower() == 'red':
                result_list.extend([1, 4, 7])
            elif color_input.lower() == 'yellow':
                result_list.extend([2, 5, 8])

        elif text_input.lower() == 'overall':
            while True:
                shape_input = input('Shape (cube/cylinder/prism): ')
                if shape_input not in ['cube', 'cylinder', 'prism']:
                    print('Invalid input. Please enter cube, cylinder, or prism.')
                    continue

                shape_list.append(shape_input)
                more_shapes = input('Do you want to choose more shapes? y/n: ')
                if more_shapes.lower() != 'y':
                    break

            while True:
                color_input = input('Color (blue/red/yellow): ')
                if color_input not in ['blue', 'red', 'yellow']:
                    print('Invalid input. Please enter blue, red, or yellow.')
                    continue

                color_list.append(color_input)
                more_color = input('Do you want to choose more colors? y/n: ')
                if more_color.lower() != 'y':
                    break

            for shape in shape_list:
                for color in color_list:
                    if shape == 'cube' and color == 'blue':
                        result_list.append(0)
                    if shape == 'cube' and color == 'red':
                        result_list.append(1)
                    if shape == 'cube' and color == 'yellow':
                        result_list.append(2)
                    if shape == 'cylinder' and color == 'blue':
                        result_list.append(3)
                    if shape == 'cylinder' and color == 'red':
                        result_list.append(4)
                    if shape == 'cylinder' and color == 'yellow':
                        result_list.append(5)
                    if shape == 'prism' and color == 'blue':
                        result_list.append(6)
                    if shape == 'prism' and color == 'red':
                        result_list.append(7)
                    if shape == 'prism' and color == 'yellow':
                        result_list.append(8)

        print(result_list)
        print(shape_list)
        print(color_list)
        break

    return result_list

def object_detection(shape):
    count = 0
    while True:
        frame = picam2.capture_array()
        count += 1
        if count % 3 != 0:
            continue

        frame = cv2.resize(frame, (640, 640))
        class_list = model.predict(frame, True, classes=shape)

        for r in class_list:
            draw = r.plot(img=frame)
            print(r.names)
            for i, xywh in enumerate(r.boxes.xywh):
                x = int(xywh[0])
                y = int(xywh[1])
                w = int(xywh[2])
                h = int(xywh[3])

        cv2.imshow('Object Detection', draw)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

choose_by_case()
object_detection()
cv2.destroyAllWindows()
