#

import time
import sys
import vlc
import pafy
import random
import os
import traceback as tb
from datetime import datetime, timedelta
import collections


__root = os.path.realpath("..")
__raw_stream_list = os.path.join(__root, "Streams.txt")
__formatted_stream_list = os.path.join(__root, "Formatted_Streams.txt")
__next_stream = os.path.join(__root, "UpNext.txt")
__current_stream = os.path.join(__root, "Current.txt")
__test_stream = "https://www.youtube.com/watch?v=4MeEoa0Ep0I"
__stream_time = 1800
__skip_file = "skip"
__file_separator = "::::"


class StreamEntry:
    def __init__(self, entry_text):
        if str.split(entry_text, "::::").__len__() <= 1:
            self.url = str.split(entry_text, "\n")[0]
            self.description = ""
        elif str.split(entry_text, "::::").__len__() <= 2:
            self.url = str.split(entry_text, "::::")[0]
            self.description = str.split(str.split(entry_text, "::::")[1], "\n")[0]


def setup_stream_list(stream_list_location=__raw_stream_list, formatted_list_location=__formatted_stream_list):
    f = open(stream_list_location, 'r', encoding='utf-8')
    all_lines = []
    for line in f:
        all_lines.append(line)
    f.close()
    formatted_lines = []
    for i, line in enumerate(all_lines):
        try:
            url = str.split(line, "\n")[0]
            if i == 0:
                formatted_lines.append(url + "::::" + pafy.new(url).title)
            else:
                formatted_lines.append("\n" + url + "::::" + pafy.new(url).title)
        except Exception:
            print(str(url))
    f = open(formatted_list_location, 'w', encoding='utf-8')
    for line in formatted_lines:
        f.write(str(line))


# Updates the nextStream.txt file from streamList.txt file
# returns True if update was successful
# returns False if update failed
def update_next_stream(next_txt=__next_stream, stream_txt=__formatted_stream_list, current_txt=__current_stream,
                       allow_repeats=False):
    try:
        f = open(str(next_txt), 'r', encoding='utf-8')
        new_current = f.read().split(__file_separator)[0]
        f.close()
    except():
        f = open(str(stream_txt), 'r', encoding='utf-8')
        new_current = f.read().split('\n')[0].split(__file_separator)[0]
        f.close()

    f = open(str(current_txt), 'w', encoding='utf-8')
    f.write(str(new_current))
    f.close()

    f = open(str(stream_txt), 'r', encoding="utf-8")
    streams = f.read().split('\n')
    new_next = streams[random.randint(0, streams.__len__() - 1)]
    if not allow_repeats:
        while new_current == new_next:
            new_next = streams[random.randint(0, streams.__len__() - 1)]
    f.close()
    f = open(str(next_txt), 'w', encoding='utf-8')
    f.write(str(new_next))
    f.close()
    return True, new_current, new_next


def play_stream(url_entry, timer):
    url = StreamEntry(url_entry.split(__file_separator)[0])
    best = pafy.new(url.url).getbest()
    media = vlc.MediaPlayer(best.url)
    media.set_fullscreen(True)
    try:
        start_time = datetime.now()
        media.play()
        timeout_timer = datetime.now()
        media_time = media.get_time()
        while datetime.now() - start_time < timedelta(seconds=timer):
            if os.path.isfile(__skip_file):
                os.remove(__skip_file)
            if datetime.now() - timeout_timer > timedelta(seconds=5):
                if media_time == media.get_time():
                    media.stop()
                    timeout_timer = datetime.now()
                    while datetime.now() - timeout_timer < timedelta(seconds=1):
                        time.sleep(0)
                    media.play()
                    timeout_timer = datetime.now()
                    while datetime.now() - timeout_timer < timedelta(seconds=1):
                        time.sleep(0)
                else:
                    media_time = media.get_time()
                timeout_timer = datetime.now()
        setup_stream_list()
        media.stop()
    except Exception as e:
        if os.path.isfile("error.txt"):
            f = open("error.txt", 'a', encoding='utf-8')
        else:
            f = open("error.txt", 'w', encoding='utf-8')
        f.write("Error at " + datetime.now().strftime("%Y %m %d, %H:%M:%S") + "\n" +
                "Stream Name: " + str(url) + str(best.title) + "\n" +
                str(sys.exc_info()[0]) + "\n" +
                str(sys.exc_info()[1]) + "\n" +
                str(tb.format_tb(sys.exc_info()[2])[0]) + "\n" +
                str(e))
        f.close()
        media.stop()
        print("ERROR")
        exit
    return


def main():
    setup_stream_list()
    fault, current, next = update_next_stream()
    while True:
        play_stream(current, __stream_time)
        fault, current, next = update_next_stream()


if __name__ == '__main__':
    main()
