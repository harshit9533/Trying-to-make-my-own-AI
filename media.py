import ctypes
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


# -------------------------
# Windows Media Key Codes
# -------------------------

VK_MEDIA_PLAY_PAUSE = 0xB3
VK_MEDIA_NEXT_TRACK = 0xB1
VK_MEDIA_PREV_TRACK = 0xB0

KEYEVENTF_KEYUP = 0x0002


# -------------------------
# Media Keys
# -------------------------

def press_media_key(vk):

    ctypes.windll.user32.keybd_event(vk, 0, 0, 0)
    ctypes.windll.user32.keybd_event(
        vk,
        0,
        KEYEVENTF_KEYUP,
        0
    )


def play_pause():
    press_media_key(VK_MEDIA_PLAY_PAUSE)


def next_track():
    press_media_key(VK_MEDIA_NEXT_TRACK)


def previous_track():
    press_media_key(VK_MEDIA_PREV_TRACK)


# -------------------------
# Volume Interface
# -------------------------

def get_volume():

    device = AudioUtilities.GetSpeakers()

    return device.EndpointVolume


def mute():

    get_volume().SetMute(1, None)


def unmute():

    get_volume().SetMute(0, None)


def is_muted():

    return bool(get_volume().GetMute())