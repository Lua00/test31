import cv2
import numpy as np

# IP kamera bağlantı adresi
IP_CAMERA_URL = 'http://192.168.1.109:8080/video'

# Renk aralıkları (HSV formatında)
# Kırmızı için iki aralık gerekir (HSV renk çemberi nedeniyle)
LOWER_RED1 = np.array([0, 100, 100])
UPPER_RED1 = np.array([10, 255, 255])
LOWER_RED2 = np.array([160, 100, 100])
UPPER_RED2 = np.array([179, 255, 255])

# Mavi için aralık
LOWER_BLUE = np.array([100, 150, 50])
UPPER_BLUE = np.array([140, 255, 255])

def detect_and_draw(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Kırmızı maskesi (iki aralık birleştiriliyor)
    mask_red1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)
    mask_red2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    
    # Mavi maskesi
    mask_blue = cv2.inRange(hsv, LOWER_BLUE, UPPER_BLUE)

    # Gürültü azaltma
    kernel = np.ones((5, 5), np.uint8)
    mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
    mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_OPEN, kernel)

    # Kırmızı nesneleri bul
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours_red:
        area = cv2.contourArea(cnt)
        if area > 500:  # Gürültüleri ele
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, 'DUSMAN', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Mavi nesneleri bul
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours_blue:
        area = cv2.contourArea(cnt)
        if area > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, 'DOST', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    return frame

def main():
    cap = cv2.VideoCapture(IP_CAMERA_URL)
    if not cap.isOpened():
        print('Kamera bağlantısı başarısız!')
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            print('Görüntü alınamadı!')
            break
        frame = detect_and_draw(frame)
        cv2.imshow('IP Kamera Hedef Takip', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()