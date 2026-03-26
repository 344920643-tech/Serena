import cv2
import numpy as np
import os

BACKGROUND_PATH = "background.jpg"
OVERLAYS = {0: "overlay_liao.png", 1: "overlay_jin.png", 2: "overlay_ming.png",
            3: "overlay_qing.png", 4: "overlay_modern.png"}
DETAILS = {"dougong": "detail_dougong.png", "beam": "detail_beam.png",
          "mural": "detail_mural.png", "roof": "detail_roof.png"}

PERIODS = ["辽代", "金代", "明代", "清代", "现代"]
DETAIL_MODES = ["无", "斗拱细节", "梁柱榫卯", "壁画复原", "屋架剖切"]

def main():
    bg = cv2.imread(BACKGROUND_PATH)
    if bg is None:
        print("❌ 找不到 background.jpg，请放一张寺庙照片进去")
        return

    overlays = {}
    for i, path in OVERLAYS.items():
        if os.path.exists(path):
            overlays[i] = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    detail_imgs = {}
    for key, path in DETAILS.items():
        if os.path.exists(path):
            detail_imgs[key] = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    cv2.namedWindow("华严寺 AR 复原设备模拟器", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("华严寺 AR 复原设备模拟器", 1280, 720)

    cv2.createTrackbar("历史时期", "华严寺 AR 复原设备模拟器", 0, 4, lambda x: None)
    cv2.createTrackbar("细节模式", "华严寺 AR 复原设备模拟器", 0, 4, lambda x: None)
    print("✅ 启动成功！拖动下面两个滑块试试看～ 按 Q 退出")

    while True:
        frame = bg.copy()
        period = cv2.getTrackbarPos("历史时期", "华严寺 AR 复原设备模拟器")
        detail = cv2.getTrackbarPos("细节模式", "华严寺 AR 复原设备模拟器")

        # 时间轴
        cv2.rectangle(frame, (80, 30), (1200, 160), (0, 255, 255), -1)
        cv2.addWeighted(frame, 0.35, frame, 0.65, 0, frame)  # 半透明
        cv2.line(frame, (150, 95), (1130, 95), (255, 255, 255), 8)
        for i in range(5):
            x = 150 + i * 245
            color = (0, 255, 0) if i == period else (255, 255, 255)
            cv2.circle(frame, (x, 95), 18, color, -1)
            cv2.putText(frame, PERIODS[i], (x-35, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 3)

        # 主AR叠加
        if period in overlays and overlays[period] is not None:
            ov = cv2.resize(overlays[period], (frame.shape[1], frame.shape[0]))
            if ov.shape[2] == 4:
                alpha = ov[:, :, 3] / 255.0
                alpha = cv2.merge([alpha, alpha, alpha])
                fg = cv2.multiply(ov[:, :, :3].astype(float), alpha)
                bg_part = cv2.multiply(frame.astype(float), 1 - alpha)
                frame = cv2.add(fg.astype(np.uint8), bg_part.astype(np.uint8))

        # 细节AR
        if detail > 0:
            keys = list(DETAILS.keys())
            key = keys[detail-1] if detail-1 < len(keys) else None
            if key and key in detail_imgs:
                dt = cv2.resize(detail_imgs[key], (frame.shape[1], frame.shape[0]))
                if dt.shape[2] == 4:
                    alpha = dt[:, :, 3] / 255.0
                    alpha = cv2.merge([alpha, alpha, alpha])
                    fg = cv2.multiply(dt[:, :, :3].astype(float), alpha)
                    bg_part = cv2.multiply(frame.astype(float), 1 - alpha)
                    frame = cv2.add(fg.astype(np.uint8), bg_part.astype(np.uint8))

        cv2.putText(frame, f"AR 实时复原：{PERIODS[period]}时期", (100, 220), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 255, 255), 4)
        if detail > 0:
            cv2.putText(frame, f"当前细节：{DETAIL_MODES[detail]}", (100, 280), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3)

        cv2.imshow("华严寺 AR 复原设备模拟器", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
