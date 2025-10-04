import pyautogui
import cv2
import numpy as np
import time

def get_rgb_input():
    print("🎨 감지할 RGB 값을 입력하세요.")
    r = int(input("R (0~255): "))
    g = int(input("G (0~255): "))
    b = int(input("B (0~255): "))
    return (r, g, b)

def main():
    print("🟢 실시간 화면 색상 감지 시작")

    target_rgb = get_rgb_input()
    tolerance = 20
    scan_interval = 0.5
    move_mouse_on_detect = True

    print(f"\n🎯 목표 색상: RGB{target_rgb}")
    print(f"🔎 감지 중... (Ctrl+C로 종료)")

    try:
        while True:
            screenshot = pyautogui.screenshot()
            screenshot = np.array(screenshot)
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

            target_bgr = target_rgb[::-1]
            lower = np.array([max(c - tolerance, 0) for c in target_bgr])
            upper = np.array([min(c + tolerance, 255) for c in target_bgr])

            mask = cv2.inRange(screenshot, lower, upper)
            coords = cv2.findNonZero(mask)

            if coords is not None:
                x, y = coords[0][0]
                print(f"\n✅ 찾음! 좌표: {x}, {y}")

                if move_mouse_on_detect:
                    pyautogui.moveTo(x, y)
                    print("🖱️ 마우스를 해당 위치로 이동했습니다.")

                break

            time.sleep(scan_interval)

    except KeyboardInterrupt:
        print("\n⛔ 사용자가 탐지 중단.")

if __name__ == "__main__":
    main()
