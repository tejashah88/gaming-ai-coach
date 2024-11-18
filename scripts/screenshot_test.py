import dxcam

from modules.image_proc.monitor_cam import MonitorCam


if __name__ == '__main__':
    print(dxcam.device_info())
    print(dxcam.output_info())

    cam = MonitorCam()
    cam.preview_screenshot()
