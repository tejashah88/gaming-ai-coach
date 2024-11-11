import dxcam

from services.monitor_cam import MonitorCam

print(dxcam.device_info())
print(dxcam.output_info())

if __name__ == '__main__':
    cam = MonitorCam()
    cam.preview_screenshot()