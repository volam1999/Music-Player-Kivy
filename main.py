import kivy
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import Screen
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

import os
import eyed3
import time

os.environ["KIVY_AUDIO"] = "ffpyplayer"

Window.size = (320,600)

music_dir = os.path.dirname(os.path.realpath(__file__))+ "\musics\\"
list_music = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]

print(os.path.dirname(os.path.realpath(__file__)))

class MusicScreen(Screen):
    pass

class SongCover(MDBoxLayout):
    angle = NumericProperty()
    anim = Animation(angle= 360, d=7, t='linear')
    anim += Animation(angle= 0, d=0, t='linear')
    anim.repeat = True
    isResume = False
    
    def rotate(self):
        self.anim.start(self)

    def stopRotate(self):
        self.anim.stop(self)

    def play(self):
        if self.btn_play.icon == "pause-circle-outline":
            self.stop()
        elif self.isResume:
            self.resume()
        else:
            self.sound = SoundLoader.load(music_dir + list_music[2])
            audiofile = eyed3.load(music_dir + list_music[2])
            image_file = open("temp.jpg", "wb")
            image_file.write(audiofile.tag.images[0].image_data)
            image_file.close()
            self.rotate_image.source = "temp.jpg"
            self.background_image.source = "temp.jpg"
            self.artist_name.text = audiofile.tag.artist
            self.song_name.text = audiofile.tag.title
            self.rotate()
            self.sound.play()
            self.process_bar.max = self.sound.length
            self.updateProcessbarEvent = Clock.schedule_interval(self.updateProcessbar, 1)
            self.updateTimeEvent = Clock.schedule_interval(self.setTime, 1)
            self.btn_play.icon = "pause-circle-outline"
            self.isResume = False

    def resume(self):
        self.isResume = False
        self.sound.play()
        self.sound.seek(self.currtentSeekTime)
        self.updateProcessbarEvent = Clock.schedule_interval(self.updateProcessbar, 1)
        self.updateTimeEvent = Clock.schedule_interval(self.setTime, 1)
        self.rotate()

    def stop(self):
        if self.sound:
            self.currtentSeekTime = self.sound.get_pos()
            self.sound.stop()
            self.btn_play.icon = "play-outline"
            self.updateProcessbarEvent.cancel()
            self.updateTimeEvent.cancel()
            self.stopRotate()
            self.isResume = True
           

    def next(self):
        pass
        
    def updateProcessbar(self, value):
        if self.process_bar.value < self.sound.length:
            self.process_bar.value += 1
    
    def setTime(self, t):
        currtentTime = time.strftime("%M:%S", time.gmtime(self.process_bar.value))
        totalTime = time.strftime("%M:%S", time.gmtime(self.sound.length))

        self.current_time.text = currtentTime
        self.total_time.text = totalTime

    def seek(self):
        if self.sound:
            self.sound.seek(self.process_bar.value)
            print("seeking: ")

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        return MusicScreen()

MainApp().run()