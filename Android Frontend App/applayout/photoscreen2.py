from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen


# # Setting size in Chart based on
# # given values
# sizes = [500, 100, 70]
# # Setting labels for items in Chart
# labels = ['Carbohydrates', 'Protein', 'Fat']
# # colors
# colors = ['#FA8771', '#a073de', '#CADD64']
# # explosion
# explode = (0.05, 0.05, 0.05)
# # Pie Chart
# plt.pie(sizes, colors=colors, labels=labels,
#         autopct='%1.1f%%', pctdistance=0.80, radius=0.9,
#         explode=explode, textprops={"fontsize": 10}, labeldistance=1.1)
# # draw circle
# centre_circle = plt.Circle((0, 0), 0.67, fc='#DBB5B5')
# fig = plt.gcf()
# fig.set_facecolor('#DBB5B5')
# # Adding Circle in Pie chart
# fig.gca().add_artist(centre_circle)
# # plt.title('Favourite Fruit Survey')
# # Add Legends
# plt.legend(labels, loc="upper right")


# class MyFigure(FigureCanvasKivyAgg):
#     def __init__(self, **kwargs):
#         super().__init__(plt.gcf(), **kwargs)


PS2 = """
<PhotoScreen2>:
    PhotoLayout23:
"""


class PhotoScreen2(Screen):
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
<PhotoLayout23>:
    Background2:
        id: backgroundOfApp
        size_hint: (1,1)
    Image:
        source: app.screen2gif
        anim_delay: 0.08
        size_hint_x: 0.5
        pos_hint: {"center_x": 0.5, "center_y":0.6}
    Label:
        text: app.screen2label1
        color: utils.get_color_from_hex('#C7C8CC')
        font_size: 20
        pos_hint: {"center_x": .5, "center_y":.45}
        markup : True
    Label:
        text: app.screen2label2
        color: utils.get_color_from_hex('#C7C8CC')
        font_size: 20
        pos_hint: {"center_x": .5, "center_y":.42}
        markup : True
    Label:
        text: app.screen2label3
        color: utils.get_color_from_hex('#C7C8CC')
        font_size: 20
        pos_hint: {"center_x": .5, "center_y":.39}
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


class PhotoLayout23(FloatLayout):

    def __init__(self, **args):
        Builder.load_string(PL2)
        super().__init__(**args)

    def on_size(self, layout, size):
        if Window.width < Window.height:
            self.orientation = 'vertical'
        else:
            self.orientation = 'horizontal'
