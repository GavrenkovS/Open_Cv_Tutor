import cv2
import video
import numpy as np
import time

start_time = time.process_time()
if __name__ == '__main__':
    # создаем окно с именем result
    cv2.namedWindow("result")

    # создаем объект cap для захвата кадров с камеры
    cap = video.create_capture(0)
    kernel = np.array([[-0.1, -0.1, -0.1], [-0.1, 3, -0.1], [-0.1, -0.1, -0.1]])
    # kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

    while True:
        # захватываем текущий кадр и кладем его в переменную img
        flag, img = cap.read()
        low_blue = np.array((13, 100, 220), np.uint8)
        high_blue = np.array((25, 210, 255), np.uint8)
        try:
            img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask_blue = cv2.inRange(img_hsv, low_blue, high_blue)
            # img = cv2.GaussianBlur(img, (101, 101), 10)#1 + 2n =
            # dst = cv2.filter2D(img, -1, kernel)
            # kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            # dst = cv2.filter2D(img, -1, kernel)
            result = cv2.bitwise_and(img_hsv, img_hsv, mask=mask_blue)
            result = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)

            moments = cv2.moments(mask_blue, 1)
            dM01 = moments["m01"]
            dM10 = moments["m10"]
            dArea = moments["m00"]

            if dArea > 400:
                x = int(dM10 / dArea)
                y = int(dM01 / dArea)
                cv2.circle(img, (x, y), 10, (255, 0, 0), -1)
                print(x, y)
                if (time.process_time() - start_time) > 3:
                    print(time.process_time() - start_time)
                else:
                    print(f"start_time else2 {time.process_time() - start_time}")
            else:
                start_time = time.process_time()
                #print (f"start_time else1 {start_time}")
            dst = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            # cv2.imshow('result', mask_blue)
            # cv2.imshow('result', result)
            cv2.imshow('result', img)
            # отображаем кадр в окне с именем result

        except:
            cap.release()
            raise

        ch = cv2.waitKey(5)
        if ch == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
