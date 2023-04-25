import datetime
import numpy as np
#import music_part
#import video_part
import os
import pygame
import cv2

import time

def get_playlist(path):
    # given a path in a string format it gets back the playlist as a list
    # tracks = listdir('C:/Users/ANDREA/Desktop/PYTHON/Faust/Playlist')
    tracks = os.listdir(path)
    playlist = []

    for track in tracks:
        playlist.append(track)

    return playlist

file_name = '../video/BeachHouse7.mp4'
#video_part.play_video(file_name)
os.system("cls")
#os.chdir("../Faust/Playlist")
path = '../Faust/Playlist'
playlist = get_playlist(path)


report = open("Faust Project.txt","w")
tracklist_title =("Curb your enthusiasm. It is just a dream.")
report.writelines(tracklist_title)
report.write("\n")
startTime = datetime.datetime.now()
report.write("The tracklist has started at ")
report.write(str(startTime))
report.write("\n")
report.write("The tracklist is: ")
report.write("\n")
report.write(str(playlist))
report.close()
##### main part
os.chdir("../Faust/Playlist")
pygame.mixer.init()
pygame.display.init()
pygame.display.set_caption('Faust Project...')
pygame.font.init()

#idx = 0 #index
song = playlist.pop()
print("Loading song: {}".format(song))
pygame.mixer.music.load ( song )  # Get the first track from the playlist
song = playlist.pop()
print("Queuing song: {}".format(song))
pygame.mixer.music.queue ( song ) # Queue the 2nd song
pygame.mixer.music.set_endevent ( pygame.USEREVENT )    # Setup the end track event
print("Playing first track: {}",format(song))
pygame.mixer.music.play()           # Play the music


window_name = "FaustProject"
interframe_wait_ms = 33 #note: the value was set at 30, but it was going too fast

cap = cv2.VideoCapture(file_name)
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

running = True
idx = 0 #idx to handle the last song loop

while running:

    ret, frame = cap.read()
    if not ret:
        print("Reached end of video, exiting.")
        running = False
        break

    cv2.imshow(window_name, frame)
    if cv2.waitKey(interframe_wait_ms) & 0x7F == ord('q'):
        print("Exit requested.")
        #running = False
        break

    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:    # A track has ended
            print("Track has ended")
            if len(playlist) > 0:       # If there are more tracks in the queue... (A non-empty list is True)
                print("Songs left in playlist@ {}".format(len(playlist)))
                pygame.mixer.music.load ( song )
                pygame.mixer.music.play()
                print("Queuing next song: {}".format(str(song)))
                song = playlist.pop()
                pygame.mixer.music.queue ( song ) # Queue the next one in the list
            elif idx == 0: #N.B.: ToDO: awful way to handle the repetition of the last song
                #print("Songs left in playlist@ {}".format(len(playlist)))
                pygame.mixer.music.load ( song )
                pygame.mixer.music.play()
                print("Playlist is empty")
                idx = +1
            else:
                running = False
                os.system("shutdown.exe /h") #Raspbian: from subprocess import call, call("sudo nohup shutdown -h now", shell=True)


cap.release()
cv2.destroyAllWindows()

quit()




#####
endTime = datetime.datetime.now()
report = open("Faust Project.txt","w")
report.write("The tracklist has ended at ")
report.write(str(endTime))
report.write("\n")
report.write("The time spent running Faust is: {0}".format(str(endTime - startTime)))
report.close()
