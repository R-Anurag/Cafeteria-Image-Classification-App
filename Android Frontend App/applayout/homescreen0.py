from kivy.uix.floatlayout import FloatLayout
from applayout.swipescreen import SwipeScreen
from kivy.lang import Builder
from kivy.core.window import Window


PS2 = """
<HomeScreen0>:
    PhotoLayout2:
"""

class HomeScreen0(SwipeScreen):
    def __init__(self, **args):
        Builder.load_string(PS2)
        super().__init__(**args)

    def on_enter(self):
        pass

    def on_pre_leave(self):
        pass

    def capture_path(self, file_path):
        pass

PL2 = """
<PhotoLayout2>:
    Background2:
        id: backgroundOfApp
        size_hint: (1,1)
    Image:
        source: 'images/appname1.png'
        anim_delay: 0.08
        size_hint_x: 0.85
        pos_hint: {"center_x": 0.5, "center_y":0.8}
    Image:
        id: tagline
        source: 'images/apptagline.png'
        anim_delay: 0.08
        size_hint_x: 0.84
        pos_hint: {"center_x": 0.5, "center_y":0.72}
    Image:
        id: pikachuImage
        source: 'images/pikachu-unscreen.zip'
        anim_delay: 0.08
        size_hint_x: 0.7
        pos_hint: {"center_x": 0.6, "center_y":0.5}
    Label:
        id: swipeRightLabel1
        text:"[font=fonts/NunitoSans_7pt_Condensed-Bold]Swipe right to click a picture[/font]"
        color: utils.get_color_from_hex('#C7C8CC')
        font_size: '22px'
        pos_hint: {"center_x": .5, "center_y":.25}
        markup : True
    Label:
        id: swipeRightLabel2
        text:"[font=fonts/NunitoSans_7pt_Condensed-Bold]of your meal >>[/font]"
        color: utils.get_color_from_hex('#C7C8CC')
        font_size: '22px'
        pos_hint: {"center_x": .5, "center_y":.22}
        markup : True

<Background2@Label>:
#: import utils kivy.utils
    canvas:
        Color: 
            rgba: utils.get_color_from_hex('#7469B6')
        Rectangle:
            pos: self.pos
            size: self.size
"""


class PhotoLayout2(FloatLayout):

    def __init__(self, **args):
        Builder.load_string(PL2)
        super().__init__(**args)

    def on_size(self, layout, size):
        if Window.width < Window.height:
            self.orientation = 'vertical'
            self.ids.tagline.pos_hint ={"center_x": 0.5, "center_y":0.72}
            self.ids.pikachuImage.size_hint_x = 0.7
            self.ids.swipeRightLabel1.pos_hint = {"center_x": .5, "center_y":.25}
            self.ids.swipeRightLabel2.pos_hint = {"center_x": .5, "center_y":.22}
        else:
            self.orientation = 'horizontal'
            self.ids.tagline.pos_hint ={"center_x": 0.5, "center_y":0.62}
            self.ids.pikachuImage.size_hint_x = 0.3
            self.ids.swipeRightLabel1.pos_hint = {"center_x": .5, "center_y":.1}
            self.ids.swipeRightLabel2.pos_hint = {"center_x": .5, "center_y":.05}
