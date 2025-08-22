from kivy.core.window import Window
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import CardTransition, FallOutTransition, RiseInTransition
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.utils import platform
from camera4kivy import Preview
from applayout.swipescreen import SwipeScreen
from applayout.toast import Toast
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen


PS1 = """
<PhotoScreen1>:
    photo_preview: photo_layout.ids.preview
    PhotoLayout1:
        id:photo_layout
"""


class PhotoScreen1(Screen):
    photo_preview = ObjectProperty(None)

    def __init__(self, **args):
        Builder.load_string(PS1)
        super().__init__(**args)

    def on_enter(self):
        self.photo_preview.connect_camera(
            filepath_callback=self.capture_path)

    def on_pre_leave(self):
        self.photo_preview.disconnect_camera()

    def capture_path(self, file_path):
        App.get_running_app().updateCurFilePath(file_path)


PL1 = """
#: import utils kivy.utils
<PhotoLayout1>:
    Background1:
        id: pad_end
    Preview:
        id: preview
        letterbox_color: utils.get_color_from_hex('#7469B6')
        aspect_ratio: '16:9'
    ButtonsLayout1:
        id: buttons

<Background1@Label>:
    canvas.before:
        Color: 
            rgba: utils.get_color_from_hex('#7469B6')
        Rectangle:
            pos: self.pos
            size: self.size
"""


class PhotoLayout1(FloatLayout):

    def __init__(self, **args):
        Builder.load_string(PL1)
        super().__init__(**args)

    def on_size(self, layout, size):
        if Window.width < Window.height:
            self.orientation = 'vertical'
            self.ids.preview.size_hint = (1, 1)
            self.ids.buttons.size_hint = (1, .1)
            self.ids.pad_end.size_hint = (1, .1)
        else:
            self.orientation = 'horizontal'
            self.ids.preview.size_hint = (1, 1)
            self.ids.buttons.size_hint = (.2, 1)
            self.ids.pad_end.size_hint = (.1, 1)


BL1 = """
<ButtonsLayout1>:
    Background1:
    Button:
        id:other
        on_press: app.imageChooser()
        height: self.width
        width: self.height
        background_normal: 'icons/gallery.png'
        background_down:   'icons/camera-flip-outline.png'
    Button:
        id:flash
        on_press: root.flash()
        height: self.width
        width: self.height
        background_normal: 'icons/flash-off.png'
        background_down:   'icons/flash-off.png'
    Button:
        id:photo
        on_press: root.photo()
        height: self.width
        width: self.height
        background_normal: 'icons/camera_white.png'
        background_down:   'icons/camera_red.png'
"""


class ButtonsLayout1(RelativeLayout):

    def __init__(self, **args):
        Builder.load_string(BL1)
        super().__init__(**args)

    def on_size(self, layout, size):
        if platform in ['android', 'ios']:
            self.ids.photo.min_state_time = 0.3
        else:
            self.ids.photo.min_state_time = 1
        if Window.width < Window.height:
            self.ids.other.pos_hint = {'center_x': .2, 'center_y': .5}
            self.ids.other.size_hint = (.12, None)
            self.ids.photo.pos_hint = {'center_x': .5, 'center_y': .5}
            self.ids.photo.size_hint = (0.13, None)
            self.ids.flash.pos_hint = {'center_x': .8, 'center_y': .5}
            self.ids.flash.size_hint = (.11, None)
        else:
            self.ids.other.pos_hint = {'center_x': .5, 'center_y': .8}
            self.ids.other.size_hint = (None, .12)
            self.ids.photo.pos_hint = {'center_x': .5, 'center_y': .5}
            self.ids.photo.size_hint = (None, 0.13)
            self.ids.flash.pos_hint = {'center_x': .5, 'center_y': .2}
            self.ids.flash.size_hint = (None, .11)

    def changeToLoadingScreen(self, *args):
        app = App.get_running_app()
        app.screen2gif = 'images/pikachu-running.zip'
        app.screen2label1 = '[font=fonts/NunitoSans_7pt_Condensed-Bold]Pikachu is on a sprint to fetch the results[/font]'
        app.screen2label2 = '[font=fonts/NunitoSans_7pt_Condensed-Bold]He`ll be back in a lightning flash![/font]'
        app.sm.transition = RiseInTransition()
        app.sm.switch_to(
            app.sm.get_screen('2'), direction='right', duration=1.)

    def photo(self):
        self.parent.ids.preview.capture_photo()
        Clock.schedule_once(self.changeToLoadingScreen, 0)

    def flash(self):
        icon = self.parent.ids.preview.flash()
        if icon == 'on':
            self.ids.flash.background_normal = 'icons/flash.png'
            self.ids.flash.background_down = 'icons/flash.png'
        elif icon == 'auto':
            self.ids.flash.background_normal = 'icons/flash-auto.png'
            self.ids.flash.background_down = 'icons/flash-auto.png'
        else:
            self.ids.flash.background_normal = 'icons/flash-off.png'
            self.ids.flash.background_down = 'icons/flash-off.png'

    def select_camera(self, facing):
        self.parent.ids.preview.select_camera(facing)
