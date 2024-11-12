import time

import dxcam
import cv2

from modules.image_proc.monitor_cam import MonitorCam

print(dxcam.device_info())
print(dxcam.output_info())

if __name__ == '__main__':
    cam = MonitorCam()
    target_fps = 60
    dtime = 1 / target_fps

    with cam.screencap_session(target_fps=target_fps, video_mode=True):
        writer = cv2.VideoWriter(
            'video.mp4', cv2.VideoWriter.fourcc(*'mp4v'), target_fps, (2560, 1600)
        )

        try:
            for i in range(target_fps):
                last_frame_time = time.time()

                frame = cam.get_screencap_frame()
                writer.write(frame)

                elapsed_frame_time = time.time() - last_frame_time
                print(elapsed_frame_time - dtime)
                if elapsed_frame_time < dtime:
                    time.sleep(dtime - elapsed_frame_time)
        except KeyboardInterrupt:
            print('Exiting due to user request...')
            writer.release()
