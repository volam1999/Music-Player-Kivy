import os
import eyed3
from kivy.core.audio import SoundLoader

music_dir = os.path.dirname(os.path.realpath(__file__))+ "\musics\\"
list_music = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]

audiofile = eyed3.load(music_dir + list_music[2])

sound = SoundLoader.load(music_dir + list_music[2])
print(sound.length/60)