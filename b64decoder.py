import threading
import pyperclip
import binascii
import base64


class ENMBase64:
    def __init__(self, monitor_interval: float = 0.5):
        self.monitor_interval = monitor_interval
        self.latest_resource = ''
        self.timer = None
        self.start_timer()

    def is_base64(self):
        try:
            if isinstance(self.latest_resource, str):
                resource_bytes = bytes(self.latest_resource, 'ascii')
            elif isinstance(self.latest_resource, bytes):
                resource_bytes = self.latest_resource
            else:
                raise ValueError("Argument must be string or bytes")
            return base64.b64encode(base64.b64decode(resource_bytes)) == resource_bytes
        except binascii.Error:
            return False
        except UnicodeDecodeError:
            return False

    def decode_base64(self):
        resource_state = self.is_base64()
        convert_resource = ''
        if resource_state:
            convert_resource = base64.b64decode(self.latest_resource).decode('ascii')
        return resource_state, convert_resource

    def clip_monitoring(self):
        print('check')
        clip_resource = pyperclip.paste()
        if clip_resource != self.latest_resource:
            self.latest_resource = clip_resource
            self.decode_base64()
        self.start_timer()

    def start_timer(self):
        self.timer = threading.Timer(self.monitor_interval, self.clip_monitoring)
        self.timer.start()

    def stop_monitoring(self):
        if self.timer is None:
            return False
        self.timer.cancle()
