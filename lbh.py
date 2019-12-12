#

import streamlink
import datetime
import multiprocessing
import time
import sys
import vlc

__streamlist = "N:\temp\LBH\Streams.txt"
__nextStream = "N:\temp\LBH\UpNext.txt"
__testStream = "https://www.youtube.com/embed/n0E_aZ5C0x8?autoplay=1"

def exit(msg):
    print(msg, file=sys.stderr)
    sys.exit()


def openStream(streamURL):
    # Create the Streamlink session
    sl = streamlink()

    # Enable logging
    sl.set_loglevel("info")
    sl.set_logoutput(sys.stdout)


    # Attempt to fetch streams
    try:
        streams = streamlink.streams(streamURL)
    except NoPluginError:
        exit("Streamlink is unable to handle the URL '{0}'".format(streamURL))
    except PluginError as err:
        exit("Plugin error: {0}".format(err))

    if not streams:
        exit("No streams found on URL '{0}'".format(streamURL))

    # We found the stream
    stream = streams[quality]

    # Create the player and start playback
    player = streamlinkPlayer()

    # Blocks until playback is done
    player.play(stream)
    return


# Updates the nextStream.txt file from streamList.txt file
# returns True if update was successful
# returns False if update failed
def updateNextStream(nextStreamTxt, streamListTxt, allowRepeats=False):
    return True


# reads the next stream from the nextStreamTxt file
def getNextStream(nextStreamTxt):
    return "the string of the next stream"


def main():
    streamProcess = multiprocessing.Process(target=openStream(getNextStream(), args=getNextStream(__nextStream)))
    fault = updateNextStream(__nextStream,__streamlist)
    while not fault:
        streamProcess.start()
        fault = updateNextStream(__nextStream, __streamlist)
        streamStopTime = datetime.datetime.now() + datetime.timedelta.min(30)
        while datetime.datetime.now() < streamStopTime:
            # Read keys, do stuff, wait
            time.sleep(1)
        streamProcess.terminate()
    if fault:
        print("An error occurred")
        return


if __name__ == '__main__':
    main()
