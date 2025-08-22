from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import platform
from android_permissions import AndroidPermissions
from kivy.uix.screenmanager import CardTransition, FallOutTransition, RiseInTransition
from camera4kivy import CameraProviderInfo
from applayout.homescreen0 import HomeScreen0
from applayout.photoscreen1 import PhotoScreen1
from applayout.photoscreen2 import PhotoScreen2
from applayout.screenshot3 import ScreenShot3
from applayout.toast import Toast
import matplotlib.pyplot as plt
import matplotlib.image as img
import requests
import json
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from backend_kivyagg import FigureCanvasKivyAgg
from kivy.clock import Clock
import json
import numpy as np
import kivy.utils as utils
import threading



if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    from sharedstorage import SharedStorage
    from chooser import Chooser
    from android import mActivity
    View = autoclass('android.view.View')

    @run_on_ui_thread
    def hide_landscape_status_bar(instance, width, height):
        # width,height gives false layout events, on pinch/spread
        # so use Window.width and Window.height
        if Window.width > Window.height:
            # Hide status bar
            option = View.SYSTEM_UI_FLAG_FULLSCREEN
        else:
            # Show status bar
            option = View.SYSTEM_UI_FLAG_VISIBLE
        mActivity.getWindow().getDecorView().setSystemUiVisibility(option)
elif platform != 'ios':
    # Dispose of that nasty red dot, required for gestures4kivy.
    from kivy.config import Config
    Config.set('input', 'mouse', 'mouse, disable_multitouch')

import matplotlib.axes as axes
import matplotlib.patches as mpatches


class StaticColorAxisBBox(mpatches.FancyBboxPatch):
    def set_edgecolor(self, color):
        if hasattr(self, "_original_edgecolor"):
            return
        self._original_edgecolor = color
        self._set_edgecolor(color)

    def set_linewidth(self, w):
        super().set_linewidth(10)


class FancyAxes(axes.Axes):
    name = "fancy_box_axes"
    _edgecolor: str

    def __init__(self, *args, **kwargs):
        self._edgecolor = kwargs.pop("edgecolor", None)
        self._linewidth = kwargs.pop("linewidth", None)
        super().__init__(*args, **kwargs)

    def _gen_axes_patch(self):
        return StaticColorAxisBBox(
            (0, 0),
            1.0,
            1.0,
            boxstyle="round, rounding_size=0.06, pad=0",
            edgecolor=self._edgecolor
        )


class MyApp(App):
    currentImagePath = StringProperty('')
    MyFigure = ObjectProperty(None)
    modelResponse = ObjectProperty('')
    screen2gif = StringProperty('')
    screen2label1 = StringProperty('')
    screen2label2 = StringProperty('')
    screen2label3 = StringProperty('')
    # This stops any threading event running
    stop = threading.Event()

    def build(self):
        self.postRequestThread = threading.Thread(target=self.getDataFromModel, args=(None,))
        self.enable_swipe = False
        self.sm = ScreenManager()
        self.screens = [
                        HomeScreen0(name='0'),
                        PhotoScreen1(name='1'),
                        PhotoScreen2(name='2'),
                        ScreenShot3(name='3')]
        for s in self.screens:
            self.sm.add_widget(s)
        if platform == 'android':
            Window.bind(on_resize=hide_landscape_status_bar)
        return self.sm

    def on_start(self):
        self.dont_gc = AndroidPermissions(self.start_app)

    def start_app(self):
        self.dont_gc = None
        self.enable_swipe = True

    def swipe_screen(self, right):
        if self.enable_swipe:
            i = int(self.sm.current)
            if right:
                self.sm.transition.direction = 'right'
                self.sm.current = str((i-1) % len(self.screens))
            else:
                self.sm.transition.direction = 'left'
                self.sm.current = str((i+1) % len(self.screens))

    def updateCurFilePath(self, image_path):
        self.currentImagePath = image_path
        self.postRequestThread.start()
        self.threadCheck = Clock.schedule_interval(self.checkThreadActive, 0.1)

    def checkThreadActive(self, *args):
        if not self.postRequestThread.is_alive():
            print("Thread ended")
            Clock.schedule_once(self.changeToAnotherScreen, 5)
            Clock.unschedule(self.threadCheck)

    def getDataFromModel(self, *args):
        # This function runs in a new thread
        try:
            response = requests.post("https://food-court-meal-classification-fefad985126d.herokuapp.com/predict",
                                                     files={'file': open(f'{self.currentImagePath}', 'rb')})
            self.modelResponse = json.loads(response.text)
            # self.responseResult = 'successful'
            response.raise_for_status()
            self.responseResult = 'applicationError' if type(self.modelResponse) != dict else 'successful'
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Specific HTTP related error
        except ConnectionError as conn_err:
            self.responseResult = 'internetError'
        except Timeout as timeout_err:
            self.responseResult = 'internetError'
        except Exception as e:
            print(e)

    def changeToAnotherScreen(self, *args):
        if self.responseResult == 'successful':
            self.sm.current = '3'
            self.addPredictionLabeledImage()
        elif self.responseResult == 'applicationError':
            # self.sm.current = '2'
            self.screen2gif = 'images/applicatioError.zip'
            self.screen2label1 = '[font=fonts/NunitoSans_7pt_Condensed-Bold]Our server is currently practicing yoga[/font]'
            self.screen2label2 = '[font=fonts/NunitoSans_7pt_Condensed-Bold]It’s in the ‘server-down’ pose[/font]'
            self.screen2label3 = '[font=fonts/NunitoSans_7pt_Condensed-Bold]We’ll be up and running soon![/font]'
        elif self.responseResult == 'internetError':
            # self.sm.current = '2'
            self.screen2gif = 'images/internetError.zip'
            self.screen2label1 = '[font=fonts/NunitoSans_7pt_Condensed-Bold]Looks like your internet is stuck[/font]'
            self.screen2label2 = '[font=fonts/NunitoSans_7pt_Condensed-Bold]in Bangalore Traffic[/font]'
            self.screen2label3 = '[font=fonts/NunitoSans_7pt_Condensed-Bold]It`s unreachable![/font]'
            
    def addPredictionLabeledImage(self, *args):
        imageWithPrediction = img.imread(
            self.currentImagePath)
        fig = plt.figure(figsize=(2, 4), facecolor='#7469B6').add_subplot(
            111, axes_class=FancyAxes, edgecolor='#AD88C6', linewidth=10)
        fig.spines[["bottom", "left", "right", "top"]].set_visible(False)
        fig.patch.set_facecolor('#7469B6')
        plt.gca().axes.get_xaxis().set_visible(False)
        plt.gca().axes.get_yaxis().set_visible(False)
        # plt.rcParams["figure.figsize"] = (20, 3)
        # plt.rcParams["figure.autolayout"] = True
        plt.imshow(imageWithPrediction,
                   interpolation=None, aspect='auto')
        plt.gca().set_position((0.05, 0.05, 0.9, 0.9))
        plt.text(20, 10, f"Detected: {self.modelResponse['top-prediction'].title()}", fontsize=12,color='white', backgroundcolor='#AD88C6')
        # plt.axis('off')

        MyFigure = FigureCanvasKivyAgg(plt.gcf())
        self.sm.get_screen(
            '3').children[0].ids.relLayout.add_widget(MyFigure)

        self.sm.get_screen(
            '3').children[0].ids.mostLikelyPred.text = f"[font=fonts/NunitoSans_7pt_Condensed-Bold]The dish is predicted to be [b]{self.modelResponse['top-prediction'].title()}[/b]    \nwith [b]{round(self.modelResponse['top-5'][self.modelResponse['top-prediction']]*100, 2)}%[/b] confidence[/font]"
        self.sm.get_screen(
            '3').children[0].ids.top5Pred.text = f"[font=fonts/NunitoSans_7pt_Condensed-Bold]The top-5 model predictions, with their   \nrespective confidence percentages, for  \nthe dish are:-[/font]"

        fig = plt.figure(facecolor='#7469B6').add_subplot(
            111, axes_class=FancyAxes, edgecolor='#fdf4dc')
        fig.spines[["bottom", "left", "right", "top"]].set_visible(False)
        self.x = np.array(list(self.modelResponse["top-5"].keys()))
        self.y = np.array(
            [round(val*100, 2) for val in list(self.modelResponse["top-5"].values())])
        self.x = np.array([x for _, x in sorted(
            zip(self.y, self.x), reverse=True)])
        self.y = np.array(sorted(self.y, reverse=True))

        self.colors = ['#cdb4db', '#95b8d1',
                       '#b8e0d2', '#f1ffc4', '#ffcaaf']
        self.colors = [utils.get_color_from_hex(x) for x in self.colors]
        self.barcollection = plt.barh(
            self.x, np.array([100, 100, 100, 100, 100]), color=self.colors)
        plt.gca().xaxis.set_ticks_position('none')
        plt.gca().yaxis.set_ticks_position('none')
        plt.gca().xaxis.set_tick_params(pad=5)
        plt.gca().yaxis.set_tick_params(pad=2)
        plt.gca().invert_yaxis()
        plt.gca().set_position((0.05, 0.05, 0.9, 0.9))
        plt.gca().axes.get_xaxis().set_visible(False)
        plt.gca().axes.get_yaxis().set_visible(False)
        plt.setp(plt.gca().get_yticklabels(), rotation=30,
                 horizontalalignment='right', fontsize='xx-small')
        # plt.axis('off')
        fig.patch.set_facecolor('#fdf4dc')
        MyFigure2 = FigureCanvasKivyAgg(plt.gcf())
        self.sm.get_screen(
            '3').children[0].ids.relLayout2.clear_widgets()
        self.sm.get_screen(
            '3').children[0].ids.relLayout2.add_widget(MyFigure2)

        self.num = 0
        self.i = 0
        self.event = Clock.schedule_interval(self.drawGraph, 0.05)

    def drawGraph(self, *args):
        self.i += 1
        self.num = self.y/(100-self.i)
        for i, b in enumerate(self.barcollection):
            b.set_width(self.num[i])
        MyFigure2 = FigureCanvasKivyAgg(plt.gcf())
        self.sm.get_screen(
            '3').children[0].ids.relLayout2.clear_widgets()
        self.sm.get_screen(
            '3').children[0].ids.relLayout2.add_widget(MyFigure2)
        if self.i == 99:
            Clock.unschedule(self.event)
            for ind, i in enumerate(plt.gca().patches):
                plt.text(i.get_x()+2, i.get_y()+0.5, f'{self.x[ind]}: ' + str(round((i.get_width()), 2))+'%',
                         fontsize=10, fontweight='bold',
                         color='grey')
            else:
                # Now show the getNutrientInfoButton
                self.sm.get_screen('3').children[0].ids.getNutritionInfoButton.opacity = 1
                self.sm.get_screen('3').children[0].ids.getNutritionInfoButton.disabled = False
                self.sm.get_screen('3').children[0].ids.takeAnotherScan.opacity = 1
                self.sm.get_screen('3').children[0].ids.takeAnotherScan.disabled = False

    def nutritionixApiFunction(self, *args):
        Toast().show('Coming Soon!')

    def imageChooser(self, *args):
        if platform == 'android':
            self.chooser = Chooser(self.chooser_callback)
            self.chooser.choose_content('image/*')
        else:
            self.currentImagePath = r'app/testimage.jpg'
            self.getDataFromModel()
            self.addPredictionLabeledImage()
            self.transition = RiseInTransition()
            self.sm.switch_to(
            self.sm.get_screen('3'), direction='right', duration=1.)

    def chooser_callback(self, shared_file_list):
       self.private_files = []
       ss = SharedStorage()
       for shared_file in shared_file_list:
           self.private_files.append(ss.copy_from_shared(shared_file))



MyApp().run()
