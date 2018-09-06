import sounddevice as sd
import re

class AudioDevice:
    ROBOT_LIBRARY_SCOPE = 'AUDIO DEVICE'

    def __init__(self):
        self.device_list = []

    def get_audio_device(self):
        return sd.query_devices(sd.default.device)

    def get_number_channels_record(self):
        return sd.query_devices(sd.default.device)['max_input_channels']

    def get_number_channels_play(self):
        return sd.query_devices(sd.default.device)['max_output_channels']

if __name__ == "__main__":
    ad = AudioDevice()
    print(ad.get_number_channels_record())
