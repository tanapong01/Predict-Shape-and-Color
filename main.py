import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO('train4/last.pt')
path_video = "obj/test/RPReplay_Final1707572773.mp4" #เปลี่ยน path ของ vdo
cap = cv2.VideoCapture(path_video)


def ChooseByCase():
    shapeList = []
    colorList = []
    resultList = []

    while True:
        # เลือกว่าจะ predect แบบไหน [shape : รูปทรง] [color : สี ] [overall : เลือกทั้งคู่]
        textInput   = input('DO you want predict by shape ,color or overall? : ')
        if textInput not in ['shape','color','overall']:
            print('Invalid input. (!predict)')
            continue
        #เงื่อนไขถ้าเลือก predict ตามรูปทรง
        if textInput.lower() == 'shape':
            while True:
                shapeInput = input('Shape (cube/cylinder/prism) : ')
                if shapeInput not in ['cube','cylinder','prism']:
                    print('Invalid input. (!shape)')
                    continue

                if shapeInput.lower() == 'cube':
                    resultList.extend([0, 1, 2])

                    return resultList

                elif shapeInput.lower() == 'cylinder':
                    resultList.extend([3, 4, 5])

                    return resultList
                    
                elif shapeInput.lower() == 'prism':
                    resultList.extend([6, 7, 8])

                    return resultList
                break 
        
        #เงื่อนไขถ้าเลือก predict ตามรูปทรง
        elif textInput.lower() == 'color':
            while True:
                colorInput = input('Color (blue/red/yellow) : ')
                if colorInput not in ['bule','red','yellow']:
                    print('invalid input. (!color)')
                    continue

                if colorInput.lower() == 'blue':
                    resultList.extend([0, 3, 6])
                    
                    return resultList

                elif colorInput.lower() == 'red':
                    resultList.extend([1, 4, 7])

                    return resultList
                    
                elif colorInput.lower() == 'yellow':
                    resultList.extend([2, 5, 8])

                    return resultList
                break
                    
        #เงื่อนไขถ้าเลือก predict ทั้งรูปทรงเเละสี
        elif textInput.lower() == 'overall':
            #เลือกรูปทรง
            while True:
                shapeInput = input('Shape (cube/cylinder/prism) : ')
                shapeList.append(shapeInput)

                if shapeInput not in ['cube','cylinder','prism']:
                    print('Invalid input. (!shape)')
                    continue
                while True:
                    more_shapes = input('Do you want to choose more shapes? y/n : ')
                    if more_shapes not in ['y','n']:
                        print('Please select y/n')
                        continue
                    break

                if more_shapes.lower() != 'y':
                    break
                

            # เลือกสี
            while True:
                colorInput = input('Color (blue/red/yellow): ')
                colorList.append(colorInput)

                if colorInput not in ['blue','red','yellow']:
                    print('invalid input. (!color)')
                    continue
                while True:
                    more_color = input('Do you want to choose more color? y/n: ')
                    if more_color not in ['y','n']:
                        print('Please select y/n')
                        continue
                    break

                if more_color.lower() != 'y':
                    break
                
            #เงื่อนไข รูปทรง เเละ สี
            for shape in shapeList:
                for color in colorList:
                    if shape == 'cube' and color == 'blue':
                        resultList.append(0)
                    if shape == 'cube' and color == 'red':
                        resultList.append(1)
                    if shape == 'cube' and color == 'yellow':
                        resultList.append(2)
                    if shape == 'cylinder' and color == 'blue':
                        resultList.append(3) 
                    if shape == 'cylinder' and color == 'red':
                        resultList.append(4) 
                    if shape == 'cylinder' and color == 'yellow':
                        resultList.append(5) 
                    if shape == 'prism' and color == 'blue':
                        resultList.append(6) 
                    if shape == 'prism' and color == 'red':
                        resultList.append(7) 
                    if shape == 'prism' and color == 'yellow':
                        resultList.append(8) 

        print(resultList)
        print(shapeList)
        print(colorList)
        break

    return resultList

def ObjectDection(cap,shape):
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        count += 1
        if count % 3 != 0:
            continue
        frame = cv2.resize(frame, (640, 640))

        class_list = model.predict(frame, True, classes=shape)
        # ตีกรอบ
        for r in class_list:
            darw = r.plot(img=frame)
            print(r.names)
            for i, xywh in enumerate(r.boxes.xywh):
                x = int(xywh[0])
                y = int(xywh[1])
                w = int(xywh[2])
                h = int(xywh[3])

        cv2.imshow('Object Detection', darw)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break


#shape = ChooseYourShape()
shape = ChooseByCase()
ObjectDection(cap, shape)
cap.release()
cv2.destroyAllWindows()
