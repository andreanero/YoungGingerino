import datetime
import os
import pygame
import cv2
import logging
import subprocess

from pathlib import Path
from sys import platform

# module logger
logger = logging.getLogger(__name__)


def get_playlist(path):
    # given a path in a string format it gets back the playlist as a list
    # tracks = listdir('C:/Users/ANDREA/Desktop/PYTHON/Faust/Playlist')
    tracks = os.listdir(path)
    playlist = []

    for track in tracks:
        playlist.append(track)

    return playlist


def shutdown_func():
    # given the OS it shuts down the machine.
    match platform:
        case 'linux':
            subprocess.Popen(['shutdown', '-h', 'now'])
        case 'win32':
            os.system("shutdown /s /t 1")
        case 'darwin':
            # fuck Mac OS X
            os.system("shutdown -h now")
        case _:
            logger.error('OS not handled. Check it {}.'.format(platform))


def runner_main(video_path: Path, playlist_path: Path, shutdown: bool, playlist_name: str, interframe_wait_ms=30):
    playlist = get_playlist(playlist_path)

    report = open('{}.txt'.format(playlist_name), 'w')
    tracklist_title = 'Curb your enthusiasm. It is just a dream.'
    report.writelines(tracklist_title)
    report.write('\n')
    startTime = datetime.datetime.now()
    report.write('The tracklist has started at {} \n'.format(startTime))
    report.write('The tracklist is: {} \n'.format(playlist))
    report.close()

    ##### main part
    pygame.mixer.init()
    pygame.display.init()
    pygame.display.set_caption('{}...'.format(playlist_name))
    pygame.font.init()

    song = playlist.pop()
    logger.info('Loading song: {}'.format(song))
    song_path = Path.joinpath(playlist_path, song)
    pygame.mixer.music.load(song_path)  # Get the first track from the playlist
    song = playlist.pop()

    song_path = Path.joinpath(playlist_path, song)
    logger.info('Queuing song: {}'.format(song))
    pygame.mixer.music.queue(song_path)  # Queue the 2nd song
    pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Setup the end track event

    logger.info('Playing first track: {}'.format(song))
    pygame.mixer.music.play()  # Play the music

    window_name = playlist_name

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        logger.error('Error: Could not open video.')

    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    running = True
    idx = 0  # idx to handle the last song loop

    while running:

        ret, frame = cap.read()
        if not ret:
            logger.warning('Reached end of video, exiting.')
            break

        cv2.imshow(window_name, frame)

        if cv2.waitKey(interframe_wait_ms) & 0x7F == ord('q'):
            logger.info('Exit requested.')
            quit()

        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:  # A track has ended
                logger.info('Track has ended.')
                song_path = Path.joinpath(playlist_path, song)
                n_songs_left = len(playlist)
                if n_songs_left > 0:  # If there are more tracks in the queue... (A non-empty list has length)
                    logger.info('Songs left in playlist: {}'.format(n_songs_left))

                    pygame.mixer.music.load(song_path)
                    pygame.mixer.music.play()
                    logger.info('Queuing next song: {}'.format(song))
                    song = playlist.pop()
                    try:
                        pygame.mixer.music.queue(song_path)  # Queue the next one in the list
                    except:
                        logger.info('Playlist is empty.')
                        running = False
                        break
                else:
                    running = False



    cap.release()
    cv2.destroyAllWindows()

    #####
    endTime = datetime.datetime.now()
    report = open('{}.txt'.format(playlist_name), 'w')
    report.write('The tracklist has ended at {} \n'.format(endTime))
    report.write('The time spent running {} is: {}'.format(playlist_name, endTime - startTime))
    report.close()

    if shutdown:
        shutdown_func()


if __name__ == '__main__':
    video_path = Path('visual\\BeachHouse7.mp4')
    playlist_path = Path('playlist\\')
    os.system('cls')
    runner_main(video_path, playlist_path, False, 'YoungGingerino')
