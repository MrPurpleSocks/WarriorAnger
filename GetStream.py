from twitchrealtimehandler import (TwitchAudioGrabber,
                                   TwitchImageGrabber)
from PIL import Image

def getStatus(url):
    image_grabber = TwitchImageGrabber(
        twitch_url=url,
        quality="1080p60",  # quality of the stream could be ["160p", "360p", "480p", "720p", "720p60", "1080p", "1080p60"]
        blocking=True,
        rate=10  # frame per rate (fps)
        )

    frame = image_grabber.grab()

    frame.show()

    image_grabber.terminate()  # stop the transcoding
