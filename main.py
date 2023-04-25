import datetime
import os
import pygame
import cv2
import logging

from pathlib import Path

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


def main():
    video_path = Path('visual\\BeachHouse7.mp4')
    os.system('cls')
    playlist_path = Path('playlist\\')
    playlist = get_playlist(playlist_path)

    report = open('Faust Project.txt', 'w')
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
    pygame.display.set_caption('Faust Project...')
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

    window_name = 'FaustProject'
    interframe_wait_ms = 30  # note: the value was set at 30, but it was going too fast

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
            logger.error('Reached end of video, exiting.')

        cv2.imshow(window_name, frame)

        if cv2.waitKey(interframe_wait_ms) & 0x7F == ord('q'):
            logger.error('Exit requested.')

        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:  # A track has ended
                logger.info('Track has ended')
                song_path = Path.joinpath(playlist_path, song)
                if len(playlist) > 0:  # If there are more tracks in the queue... (A non-empty list has length)
                    logger.info('Songs left in playlist {}'.format(len(playlist)))

                    pygame.mixer.music.load(song_path)
                    pygame.mixer.music.play()
                    logger.info('Queuing next song: {}'.format(str(song)))
                    song = playlist.pop()
                    pygame.mixer.music.queue(song)  # Queue the next one in the list
                elif idx == 0:  # ToDO: awful way to handle the repetition of the last song
                    pygame.mixer.music.load(song_path)
                    pygame.mixer.music.play()
                    logger.info('Playlist is empty.')
                    idx = +1
                else:
                    running = False
                    os.system(
                        'shutdown.exe /h')  # Raspbian: from subprocess import call, call('sudo nohup shutdown -h now', shell=True)

    cap.release()
    cv2.destroyAllWindows()

    quit()

    #####
    endTime = datetime.datetime.now()
    report = open('Faust Project.txt', 'w')
    report.write('The tracklist has ended at ')
    report.write(str(endTime))
    report.write('\n')
    report.write('The time spent running Faust is: {0}'.format(str(endTime - startTime)))
    report.close()


if __name__ == '__main__':
    main()
