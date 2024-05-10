'''
Not used whatsoever currently, may be used in the future
Used to get a frame from a twitch stream
'''

from twitchrealtimehandler import TwitchImageGrabber

def get_status(url):
    '''
    Supposed to get the status of a match from a stream
    in reality, it just gets a frame from the stream
    '''
    image_grabber = TwitchImageGrabber(
        twitch_url=url,
        quality="1080p60",
        blocking=True,
        rate=10  # frame per rate (fps)
        )

    frame = image_grabber.grab()

    frame.show()

    image_grabber.terminate()  # stop the transcoding
