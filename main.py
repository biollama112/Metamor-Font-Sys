#!/usr/bin/python3
import os
import shutil
import time
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.pagelayout import PageLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivymd.uix.button import MDFlatButton
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.clock import Clock
from gtts import gTTS
from io import BytesIO
from plyer import tts
from os import path
from os import listdir
from jnius import cast
from jnius import autoclass
from webview import WebView
from textwrap import fill
from PIL import Image, ImageDraw, ImageFont
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from os.path import join, exists
from os import mkdir

tools_path = os.path.dirname(__file__)
icons_path = os.path.join(tools_path, 'OpenDyslexic-Regular.ttf', 'SylexiadSansSpacedMed.ttf', 'Cadman_Roman.otf', 'Helvetica.ttf')
imgocr = ObjectProperty(None)

from android.permissions import request_permissions, Permission
request_permissions([Permission.INTERNET, Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

####### WINDOW MANAGER #######

class WindowManager(ScreenManager):
    pass

####### MAIN MENU #######

class MainMenu(Screen):
    pass

####### MENU #######

class Menu(Screen):
    pass

####### UPLOAD #######

class Upload(Screen):

    
    saved_path = ""
    def selected(self,filename):
        try:
            self.ids.my_upload.source = filename[0]
            
        except:
            pass

        global saved_path
        saved_path = str(filename[0])
        print("The path is: " , saved_path)
        file = open("saved_path.txt", "w")
        file.write(saved_path)
        file.close()
            
    def uploadfile(self):
        
        filepath = open("saved_path.txt", "r")
        fullpath = filepath.read()
        target_path = 'test_img.jpg'
        shutil.copyfile(fullpath, target_path)
        link = 'http://192.168.1.209/ocr/test.php'
        files = {'file': open(target_path, 'rb')}

        r = requests.post(link, files=files)
        print(r.status_code)
        filepath.close()
        
    def view_google(self):
        #WebView("http://192.168.1.209/ocr/python.py")
        Clock.schedule_once(self.changeScreen, 8)

    def changeScreen(self,dt):
        self.manager.current = 'fontocr'

####### TEXT INPUT #######

class TextIn(Screen):
    text_input_str = StringProperty('')
    objectt = ObjectProperty()

    def submit_text(self):

        self.text_input_str = self.objectt.text
        print("Input Text: {}".format(self.text_input_str))
        self.save()
        
    def save(self):

        dcimpath = "/storage/emulated/0/Download/ocr/recognized_texts.txt"
        fobj = open("input.txt", "w")
        input_path = os.path.realpath(fobj.name)
        fobj.write(str(self.text_input_str))
        fobj.close()
        shutil.copy(input_path,dcimpath)
            
####### FONT TEXT INPUT #######

class FontTI(Screen):

        LabelBase.register(name='OpenDyslexic',
                        fn_regular='OpenDyslexic-Regular.ttf')

        LabelBase.register(name='Sylexiad',
                        fn_regular='SylexiadSansSpacedMed.ttf')

        LabelBase.register(name='Cadman',
                        fn_regular='Cadman_Roman.otf')

        LabelBase.register(name='Helvetica',
                        fn_regular='Helvetica.ttf')
    
        def OpenDyslexic(self):

            targetpath = "/storage/emulated/0/Download/ocr/fontar.txt"
            chosen_arfont = 'opendyslexic'
            chosen_font = 'OpenDyslexic-Regular.ttf'
            fontar = open('ar.txt', 'w')
            fontar.write(chosen_arfont)
            fontar_path = os.path.realpath(fontar.name)
            fontar.close()
            shutil.copyfile(fontar_path, targetpath)
            font = open('font.txt', 'w')
            font.write(chosen_font)
            font.close()

        def Sylexiad(self):

            targetpath = "/storage/emulated/0/Download/ocr/fontar.txt"
            chosen_arfont = 'sylexiad'
            chosen_font = 'SylexiadSansSpacedMed.ttf'
            fontar = open('fontar.txt', 'w')
            fontar.write(chosen_arfont)
            fontar_path = os.path.realpath(fontar.name)
            fontar.close()
            shutil.copyfile(fontar_path, targetpath)
            font = open('font.txt', 'w')
            font.write(chosen_font)
            font.close()

        def Cadman(self):

            targetpath = "/storage/emulated/0/Download/ocr/fontar.txt"
            chosen_arfont = 'cadman'
            chosen_font = 'Cadman_Roman.otf'
            fontar = open('fontar.txt', 'w')
            fontar.write(chosen_arfont)
            fontar_path = os.path.realpath(fontar.name)
            fontar.close()
            shutil.copyfile(fontar_path, targetpath)
            font = open('font.txt', 'w')
            font.write(chosen_font)
            font.close()

        def Helvetica(self):

            targetpath = "/storage/emulated/0/Download/ocr/fontar.txt"
            chosen_arfont = 'helvetica'
            chosen_font = 'Helvetica.ttf'
            fontar = open('fontar.txt', 'w')
            fontar.write(chosen_arfont)
            fontar_path = os.path.realpath(fontar.name)
            fontar.close()
            shutil.copyfile(fontar_path, targetpath)
            font = open('font.txt', 'w')
            font.write(chosen_font)
            font.close()

class Output(Screen):
    pass

####### FONT OCR #######

class FontOCR(Screen):
    
        URL = "http://192.168.1.209/ocr/recognized_texts.txt"

        response = requests.get(URL, allow_redirects=True)
        print(response.headers.get('content-type'))
        open("recognized_texts.txt", "wb").write(response.content)

        LabelBase.register(name='OpenDyslexic',
                        fn_regular='OpenDyslexic-Regular.ttf')

        LabelBase.register(name='Sylexiad',
                        fn_regular='SylexiadSansSpacedMed.ttf')

        LabelBase.register(name='Cadman',
                        fn_regular='Cadman_Roman.otf')

        LabelBase.register(name='Helvetica',
                        fn_regular='Helvetica.ttf')

        def OpenDyslexic(self):

            targetpath = "/storage/emulated/0/Download/ocr/fontar.txt"
            chosen_arfont = 'opendyslexic'
            chosen_font = 'OpenDyslexic-Regular.ttf'
            fontar = open('fontar.txt', 'w')
            fontar.write(chosen_arfont)
            fontar_path = os.path.realpath(fontar.name)
            fontar.close()
            shutil.copyfile(fontar_path, targetpath)
            font = open('font.txt', 'w')
            font.write(chosen_font)
            font.close()

        def Sylexiad(self):

            targetpath = "/storage/emulated/0/Download/ocr/fontar.txt"
            chosen_arfont = 'sylexiad'
            chosen_font = 'SylexiadSansSpacedMed.ttf'
            fontar = open('fontar.txt', 'w')
            fontar.write(chosen_arfont)
            fontar_path = os.path.realpath(fontar.name)
            fontar.close()
            shutil.copyfile(fontar_path, targetpath)
            font = open('font.txt', 'w')
            font.write(chosen_font)
            font.close()

        def Cadman(self):

            targetpath = "/storage/emulated/0/Download/ocr/fontar.txt"
            chosen_arfont = 'cadman'
            chosen_font = 'Cadman_Roman.otf'
            fontar = open('fontar.txt', 'w')
            fontar.write(chosen_arfont)
            fontar_path = os.path.realpath(fontar.name)
            fontar.close()
            shutil.copyfile(fontar_path, targetpath)
            font = open('font.txt', 'w')
            font.write(chosen_font)
            font.close()

        def Helvetica(self):

            targetpath = "/storage/emulated/0/Download/ocr/fontar.txt"
            chosen_arfont = 'helvetica'
            chosen_font = 'Helvetica.ttf'
            fontar = open('fontar.txt', 'w')
            fontar.write(chosen_arfont)
            fontar_path = os.path.realpath(fontar.name)
            fontar.close()
            shutil.copyfile(fontar_path, targetpath)
            font = open('font.txt', 'w')
            font.write(chosen_font)
            font.close()

####### PHOTO + TTS OUTPUT OCR #######

class OutputOCR(Screen):

    image_source = StringProperty()

    def on_pre_enter(self, *args):

        num_lines = sum(1 for line in open('recognized_texts.txt'))
        font_size = 26
        if num_lines > 10:
            for lines in range(0,num_lines):
                font_size -= 2.3
                num_lines -= 2.5
                print(num_lines)
                print(font_size)
                if num_lines <= 4:
                    break

        dcimpath = "/storage/emulated/0/Download/ocr/recognized_texts.txt"
        recognized_text = open('recognized_texts.txt', 'r')
        recognized_path = os.path.realpath(recognized_text.name)
        shutil.copyfile(recognized_path, dcimpath)
        print(f"the path is : {recognized_path}")
        recog_text = recognized_text.read()
        font_open = open('font.txt', 'r')
        chosen_font = font_open.read()
        font = ImageFont.truetype(chosen_font,int(font_size))
        img=Image.new("RGBA", (500,250),(255,255,255))
        draw = ImageDraw.Draw(img)
        draw.text((0,0),recog_text,(0,0,0),font=font)
        draw = ImageDraw.Draw(img)
        img.save("output_test.png")
        path = "output_test.png"
        isFile = os.path.isfile(path)
        print(isFile)
        self.image_source = str("output_test.png")
        #self.imgocr.source = "output_test.png"
        #self.photo = ("output_test.png")
        #outputpic = self.ids["imgocr"]
        #outputpic.source = "output_test.png"
        recognized_text.close()
        font_open.close()

    def createimg(self):
        pass

    def createttsocr(self):

        fh = open("recognized_texts.txt", "r")
        myText = fh.read().replace("\ ", " ")
        language = 'tl'
        mp3_fp = BytesIO()
        output = gTTS(text=myText, lang=language, tld="com")
        output.write_to_fp(mp3_fp)
        fh.close()

        tts.speak(myText)

####### PHOTO + TTS OUTPUT TEXT INPUT #######

class OutputTI(Screen):

    image_source = StringProperty()

    def on_pre_enter(self, *args):

        num_lines = sum(1 for line in open('recognized_texts.txt'))
        font_size = 26
        if num_lines > 10:
            for lines in range(0,num_lines):
                font_size -= 1.5
                num_lines -= 2.5
                print(num_lines)
                print(font_size)
                if num_lines <= 4:
                    break

        recognized_text = open('input.txt', 'r')
        recog_text = recognized_text.read()
        font_open = open('font.txt', 'r')
        chosen_font = font_open.read()
        font = ImageFont.truetype(chosen_font, int(font_size))
        img=Image.new("RGBA", (500,250),(255,255,255))
        draw = ImageDraw.Draw(img)
        draw.text((0,0),recog_text,(0,0,0),font=font)
        draw = ImageDraw.Draw(img)
        img.save("output_test.png")
        path = "output_test.png"
        isFile = os.path.isfile(path)
        print(isFile)
        self.image_source = str("output_test.png")
        #self.imgocr.source = "output_test.png"
        #self.photo = ("output_test.png")
        #outputpic = self.ids["imgocr"]
        #outputpic.source = "output_test.png"
        recognized_text.close()
        font_open.close()
    
    def createimg(self):
        pass

    def createttsit(self):
        fh = open("input.txt", "r")
        myText = fh.read().replace("\ ", " ")

        language = 'tl'
        mp3_fp = BytesIO()
        output = gTTS(text=myText, lang=language, tld="com")
        output.write_to_fp(mp3_fp)

        tts.speak(myText)

class OpenAR(Screen):
    
   def getapp(self):

        package = 'com.DefaultCompany.Myproject3'

        Intent: type[autoclass] = autoclass('android.content.Intent')
        PythonActivity: type[autoclass] = autoclass(
            'org.kivy.android.PythonActivity'
        )
        activity: type[PythonActivity] = PythonActivity.mActivity

        pm: type[activity] = activity.getPackageManager()
        app_intent: type[pm] = pm.getLaunchIntentForPackage(package)
        app_intent.setAction(Intent.ACTION_VIEW)
        app_intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)

        activity.startActivity(app_intent)

class UI(MDApp):
    
    def file_filter(self, folder, file):
        return not os.path.isdir(file)

UI().run()