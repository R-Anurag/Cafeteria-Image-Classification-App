from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
import matplotlib.pyplot as plt
from kivy.utils import platform
from kivy.uix.button import Button
from camera4kivy import Preview
from applayout.swipescreen import SwipeScreen
from applayout.toast import Toast
from kivy.uix.screenmanager import Screen
import numpy as np


PS2 = """
<ScreenShot3>:
    PhotoLayout3:
"""


class ScreenShot3(Screen):

    def __init__(self, **args):
        Builder.load_string(PS2)
        super().__init__(**args)

    def on_enter(self):
        pass

    def on_pre_leave(self):
        pass


PL2 = """
#: import utils kivy.utils
<PhotoLayout3>:
    Background2:
        id: backgroundOfApp
        size_hint: (1,1)
    RelativeLayout:
        id: relLayout  
    RelativeLayout:
        id: relLayout2
    Label:
        id: headingLabel
        text:"[font=fonts/PlayfairDisplay-SemiBold][b]Machine Learning Model Predictions[/b][/font]"
        color: utils.get_color_from_hex('#fdf4dc')
        font_size: 24
        pos_hint: {"center_x": .5, "center_y":.95}
        markup : True
    Label:
        id: mostLikelyPred
        text:""
        color: utils.get_color_from_hex('#fdf4dc')
        font_size: 20
        markup : True
    Label:
        id: top5Pred
        text:""
        color: utils.get_color_from_hex('#fdf4dc')
        font_size: 20
        markup : True
    RoundedButton:
        id: getNutritionInfoButton
        icon: 'icons/nutrition.png'
        markup: True
        text: '[font=fonts/NunitoSans_7pt_Condensed-Bold]Get Nutrition Information[/font]'
        font_size: 20
        color: utils.get_color_from_hex('#fdf4dc')
        size_hint: (0.85, .04)
        pos_hint: {'center_x':.5, 'center_y':.1}
        on_press: app.nutritionixApiFunction()
        on_release: app.sm.current = '2'
        opacity: 0
        disabled: True
    RoundedButton:
        id: takeAnotherScan
        icon: 'icons/scan.png'
        markup: True
        text: '[font=fonts/NunitoSans_7pt_Condensed-Bold]Take Another Scan[/font]'
        font_size: 20
        color: utils.get_color_from_hex('#fdf4dc')
        size_hint: (0.85, .04)
        pos_hint: {'center_x':.5, 'center_y':.05}
        on_press: pass
        on_release: app.sm.current = '1'
        opacity: 0
        disabled: True

<Background2@Label>:
    canvas:
        Color: 
            rgba: utils.get_color_from_hex('#7469B6')
        Rectangle:
            pos: self.pos
            size: self.size

<RoundedButton@Button>:
    background_color: 0,0,0,0  # the last zero is the critical on, make invisible
    canvas.before:
        Color:
            rgba: utils.get_color_from_hex('#AD88C6') if self.state=='normal' else utils.get_color_from_hex('#E1AFD1')  # visual feedback of press
        RoundedRectangle:
            id: roundButton
            pos: self.pos
            size: self.size
            radius: [12,]
            canvas:
        Rectangle:
            source:self.icon
            pos: self.center[0]+(len(self.text)/2)*3.5, self.center[1]-(root.height/3)
            size: 30,30
"""

class RoundedButton(Button):
    icon = StringProperty("")
    text = StringProperty('')

class PhotoLayout3(FloatLayout):

    def __init__(self, **args):
        Builder.load_string(PL2)
        super().__init__(**args)

    def on_size(self, layout, size):
        if Window.width > Window.height:
            self.orientation = 'horizontical'
            self.ids.relLayout.size_hint = (0.4, 0.65)
            self.ids.relLayout.pos_hint = {"center_x": .23, "center_y": .37}
            self.ids.relLayout2.size_hint = (0.4, 0.65)
            self.ids.relLayout2.pos_hint = {"center_x": .66, "center_y": .34}
            self.ids.top5Pred.pos_hint = {"center_x": .65, "center_y": .76}
            self.ids.top5Pred.font_size = 18
            self.ids.mostLikelyPred.pos_hint = {
                "center_x": .24, "center_y": .78}
            self.ids.mostLikelyPred.font_size = 18
            self.ids.headingLabel.font_size = 22
            self.ids.takeAnotherScan.text = "^" 
            self.ids.takeAnotherScan.size_hint = (0.1, 0.2) 
            self.ids.takeAnotherScan.pos_hint = {"center_x":0.92, "center_y":0.2}
            self.ids.getNutritionInfoButton.text = "^" 
            self.ids.getNutritionInfoButton.size_hint = (0.1, 0.2)
            self.ids.getNutritionInfoButton.pos_hint = {"center_x":0.92, "center_y":0.5}
        else:
            self.orientation = 'vertical'
            self.ids.relLayout.size_hint = (0.9, 0.3)
            self.ids.relLayout.pos_hint = {"center_x": .5, "center_y": .69}
            self.ids.relLayout2.size_hint = (0.9, 0.3)
            self.ids.relLayout2.pos_hint = {"center_x": .5, "center_y": .28}
            self.ids.top5Pred.pos_hint = {"center_x": .5, "center_y": .49}
            self.ids.top5Pred.font_size = 20
            self.ids.mostLikelyPred.pos_hint = {
                "center_x": .5, "center_y": .88}
            self.ids.mostLikelyPred.font_size = 20
            self.ids.headingLabel.font_size = 24
            self.ids.takeAnotherScan.text = '[font=fonts/NunitoSans_7pt_Condensed-Bold]Take Another Scan[/font]'
            self.ids.takeAnotherScan.size_hint = (0.85, 0.04) 
            self.ids.takeAnotherScan.pos_hint = {"center_x":0.5, "center_y":0.05}
            self.ids.getNutritionInfoButton.text = '[font=fonts/NunitoSans_7pt_Condensed-Bold]Get Nutrition Information[/font]'
            self.ids.getNutritionInfoButton.size_hint = (0.85, .04)
            self.ids.getNutritionInfoButton.pos_hint = {"center_x":0.5, "center_y":0.1}
