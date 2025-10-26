# Импорт всех классов
import random
import configparser

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.switch import Switch
from kivy import platform
from kivy.base import EventLoop
from kivy.core.window import Window

# Глобальные настройки
Window.clearcolor = (236/255, 242/255, 245/255, 1)
Window.title = "Ru_Wordly_24/7"

Config = configparser.ConfigParser()
Config.read("my.ini")

if platform == 'android':
    from jnius import autoclass

    Intent = autoclass("android.content.Intent")
    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    System = autoclass("java.lang.System")

def get_all_words():
    '''Читает файлы со списками слов.
       Возврашайт картеж содержащий 3 спмска слов.'''
    row_words = open('russian_used.txt', 'r') # Часто используемые слова

    words = []
    for word in row_words:
        words.append(word[:5])
    
    ez_words = open('russian_easy.txt', 'r') # Очень часто используемые слова

    easy_words = []
    for ez_word in ez_words:
        easy_words.append(ez_word[:5])

    e_words = open('russian_exist.txt', 'r') # Все существительные из 5 букв

    ex_words = []
    for word in e_words:
        ex_words.append(word[:5])

    result = {"words": words, "ex_words": ex_words, "easy_words": easy_words}
    return result

def make_matrix_text(matrix, color_matrix):
    '''Возврашает строку с отформатированным текстом
       Использоватьполученный текст в label нужно с параметром markup = True'''
    m = []
    for i in range(len(matrix)):
        n = []
        for y in range(len(matrix[i])):
            if color_matrix[i][y] == 'b':
                n.append('[color=000000]' + matrix[i][y] + '[/color]')
            elif color_matrix[i][y] == 'y':
                n.append('[color=fbbd05]' + matrix[i][y] + '[/color]')
            elif color_matrix[i][y] == 'g':
                n.append('[color=00b729]' + matrix[i][y] + '[/color]')
            else:
                n.append(matrix[i][y])
        m.append(' '.join(n))
    return '\n'.join(m)

def make_clear_matrix():
    m =[]
    for x in range(6):
        n = []
        for y in range(5):
            n.append('_')
        m.append(n)
    return m


class MyApp(App):
    def __init__(self):
        super().__init__()
        self.button_backgound_color = (0/255, 87/255, 111/255, 1)
        self.literas = {}
        self.matrix = []
        self.color_matrix = []
        self.position = [0, 0]
        if Config.get('settings', 'easy_level') == '1':
            self.easy = True
        else:
            self.easy = False
        if Config.get('settings', 'left_enter') == '1':
            self.left_enter = True
        else:
            self.left_enter = False
        self.words = ""
        self.ex_words = ""
        self.word = ""
        self.easy_words = ""
        self.field = Label(text=make_matrix_text(self.matrix, self.color_matrix), 
                           color='#000000', 
                           font_size = Window.width / 7, 
                           font_name='mono', 
                           markup = True)
        self.start_new_game()

    def start_new_game(self):
        self.matrix = make_clear_matrix()
        self.color_matrix = make_clear_matrix()
        self.position = [0, 0]
        all_words = get_all_words()
        self.words = all_words["words"]
        self.ex_words = all_words["ex_words"]
        self.easy_words = all_words['easy_words']
        if self.easy:
            self.word = self.easy_words[random.randint(0, len(self.easy_words) - 1)]
        else:
            self.word = self.words[random.randint(0, len(self.words) - 1)]
        self.clear_all_buttons()
        self.update_field()

    def litera(self, instanse):
        '''Обрабатывает нажатия на кнопки с буквами'''
        self.literas[instanse.text] = instanse
        if self.position[1] < 5:
            self.matrix[self.position[0]][self.position[1]] = instanse.text
            self.position[1] = self.position[1] + 1
        self.update_field()

    def color_button(self, button, color):
        '''Красит кнопки на клавиатуре'''
        color_now = self.literas[button].background_color
        # Проверка нужна чтоб не перекрасить зелёную кнопку в желтую))
        if color_now == [0.0, 0.7176470588235294, 0.1607843137254902, 1.0]:
            return
        if color == 'b':
            self.literas[button].background_color = '000000'
        elif color == 'y':
            self.literas[button].background_color = 'fbbd05'
        elif color == 'g':
            self.literas[button].background_color = '00b729'
        else:
            pass

    def clear_all_buttons(self):
        '''Возвращает дефолтный цвет всем кнопкам'''
        l = ["й", "ц", "у", "к", "е", "н", "г", 
             "ш", "щ", "з", "х", "ъ", "ф", "ы", 
             "в", "а", "п", "р", "о", "л", "д", 
             "ж", "э", "я", "ч", "с", "м", "и", 
             "т", "ь", "б", "ю"]
        for i in l:
            try:
                self.literas[i].background_color = self.button_backgound_color
            except:
                pass

    def backspace(self, instanse):
        '''Обрабатывает нажатие backspace'''
        if self.position[1] > 0:
            self.position[1] = self.position[1] - 1
            self.matrix[self.position[0]][self.position[1]] = '_'
        self.update_field()

    def set_easy_level(self, instance, value):
        '''Меняет уровень сложности'''
        if value:
            Config.set('settings', 'easy_level', '1')
            with open('my.ini', 'w') as configfile:
                Config.write(configfile)
            self.easy = True
            self.start_new_game()
        else:
            Config.set('settings', 'easy_level', '0')
            with open('my.ini', 'w') as configfile:
                Config.write(configfile)
            self.easy = False
            self.start_new_game()
    
    def set_left_enter(self, instance, value):
        '''Меняет местами кнопки ввод и стереть'''
        if value:
            Config.set('settings', 'left_enter', '1')
            with open('my.ini', 'w') as configfile:
                Config.write(configfile)
            self.left_enter = True
            self.start_new_game()
            self.restart()
        else:
            Config.set('settings', 'left_enter', '0')
            with open('my.ini', 'w') as configfile:
                Config.write(configfile)
            self.left_enter = False
            self.start_new_game()
            self.restart()
    
    def restart(self, *args):
        if platform == 'android':
            activity = PythonActivity.mActivity
            intent = Intent(activity.getApplicationContext(), PythonActivity)
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TASK)
            activity.startActivity(intent)
            System.exit(0)
        else:
            self.root.clear_widgets()
            self.stop()
            MyApp().run()

    def rules(self, *args):
        '''Всплывающее окно с правилами игры
           Выводит текст в окне с полосой прокрутки.'''
        about_text='''Угадайте загаданное слово с шести попыток.

После каждой попытки цвет букв будет меняться, чтобы показать, какие буквы есть в загаданном слове!
Если буква есть в загаданном слове, но стоит в другом месте, цвет будет желтый.
Если буква есть в загаданном слове и стоит на правильном месте, её цвет будет зелёным.

Загадываются существительные в единственном числе.

В загаданном слове могут быть одинаковые буквы.

По правилам русских кроссвордов буква Ё в словах заменена на E!
'''
        self.scroll_notify(about_text)

    def about(self, *args):
        '''Всплывающее окно с текстом "Об игре"
           Выводит текст в окне с полосой прокрутки.'''
        about_text='''
https://github.com/Ekibostos/ru_wordly_24_7

Пункт в доработке
'''
        self.scroll_notify(about_text)
    
    def scroll_notify(self, message):
        '''Выводит текст в окне с полосой прокрутки.'''
        content = BoxLayout(orientation='vertical', size=(.5, .5))
        scroll = ScrollView()
        scroll.add_widget(Label(text=message, 
                                color='#FFFFFF', 
                                padding = 30,
                                font_size = Window.width / 30,
                                size=(Window.width * .8, Window.height * .8), 
                                text_size=(Window.width * .8, Window.height * .8), 
                                size_hint_y=None,
                                valign='middle'))
        content.add_widget(scroll)
        a = Button(text='Ok', 
                   font_size = Window.width / 20, 
                   size_hint=[1, .1], 
                   padding = 30, 
                   background_color=self.button_backgound_color, 
                   background_normal='')
        content.add_widget(a)
        popup_a = Popup(title='', 
                      content=content, 
                      auto_dismiss=True, 
                      separator_height=0, 
                      size=(Window.width * .8, Window.height * .8), 
                      size_hint=(None, None),
                      background_color=(0/255, 127/255, 159/255, 1),
                      background='#FFFFFF')
        a.bind(on_press=popup_a.dismiss)
        popup_a.open()

    def notify(self, message):
        '''Выводит всплывающее окно с текстом из переменной message
           Текст не должен быть слишком большим, может не войти'''
        content = BoxLayout(orientation='vertical', size=(.5, .5))
        content.add_widget(Label(text=message, 
                                 color='#FFFFFF', 
                                 markup = True, 
                                 font_name='mono', 
                                 font_size = Window.width / 16, 
                                 size=(Window.width * .8, Window.height * .8), 
                                 text_size=(Window.width * .8, Window.height * .8), 
                                 halign='center', 
                                 valign='middle'))
        b = Button(text='Ok', 
                   font_size = Window.width / 20,
                   background_color=self.button_backgound_color,
                   background_normal='',
                   pos_hint={"center_x": 0.5, "center_y":0.5})
        b_box = BoxLayout(orientation='vertical', size_hint=[1, .16], padding = 5)
        b_box.add_widget(b)
        content.add_widget(b_box)
        popup = Popup(title='', 
                      content=content, 
                      auto_dismiss=True, 
                      separator_height=0, 
                      size=(Window.width * .8, Window.height * .8), 
                      size_hint=(None, None),
                      background_color=(0/255, 127/255, 159/255, 1),
                      background='#FFFFFF')
        b.bind(on_press=popup.dismiss)
        popup.open()

    def menu(self, *args):
        '''Сюда запихал всё что ни попадя
        Все пункты в отдельном BoxLayout, иначе разъедутся.'''
        content = BoxLayout(orientation='vertical', size=(.5, .5))

        # Тумблер переключалка уровня сложности
        с_box = BoxLayout(orientation='horizontal', size_hint=[1, .1], padding = 5)
        с_box.add_widget(Label(text='Лёгкий режим', font_size = Window.width / 28, size_hint=[.7, 1]))
        sw1 = Switch(active=self.easy)
        sw1.bind(active=self.set_easy_level)
        с_box.add_widget(sw1)
        content.add_widget(с_box)
        content.add_widget(Label(text='В лёгком режиме будут загадываться более распространенные слова', 
                                 color='#FFFFFF',
                                 size_hint=[1, .12],
                                 text_size=(Window.width * .7, Window.height * .07), 
                                 font_size = Window.width / 35,
                                 halign='center', 
                                 valign='middle'))

        # Тумблер меняющий местами кнопки ввод и стереть
        e_box = BoxLayout(orientation='horizontal', size_hint=[1, .1], padding = 5)
        e_box.add_widget(Label(text='Кнопка ввода слева', font_size = Window.width / 28, size_hint=[.7, 1]))
        sw2 = Switch(active=self.left_enter)
        sw2.bind(active=self.set_left_enter)
        e_box.add_widget(sw2)
        content.add_widget(e_box)
        content.add_widget(Label(text='Кнопки ввод и стереть поменяются местами\nПриложение перезапустится.', 
                                 color='#FFFFFF',
                                 size_hint=[1, .12],
                                 text_size=(Window.width * .7, Window.height * .07), 
                                 font_size = Window.width / 35,
                                 halign='center', 
                                 valign='middle'))

        # Кнопка вызывает окно с правилами игры
        a_box = BoxLayout(orientation='horizontal', size_hint=[1, .1], padding = 5)
        a_box.add_widget(Button(text='Правила', 
                                  font_size = Window.width / 25,
                                  on_press=self.rules,
                                  background_color=self.button_backgound_color,
                                  background_normal='',
                                  pos_hint={"center_x": 0.5, "center_y":0.5}))
        content.add_widget(a_box)
        
        # Кнопка вызывает окно с инфомацией об игре
        b_box = BoxLayout(orientation='horizontal', size_hint=[1, .1], padding = 5)
        b_box.add_widget(Button(text='Об игре', 
                                  font_size = Window.width / 25,
                                  on_press=self.about,
                                  background_color=self.button_backgound_color,
                                  background_normal='',
                                  pos_hint={"center_x": 0.5, "center_y":0.5}))
        content.add_widget(b_box)

        # Кнопка закрыть меню
        b = BoxLayout(orientation='horizontal', size_hint=[1, .1], padding = 5)
        exit = Button(text='Закрыть меню', 
                   font_size = Window.width / 25,
                   background_color=self.button_backgound_color,
                   background_normal='',
                   pos_hint={"center_x": 0.5, "center_y":0.5})
        b.add_widget(exit)
        content.add_widget(b)

        # Само всплывающее окно
        popup = Popup(title='', 
                      content=content, 
                      auto_dismiss=True, 
                      separator_height=0, 
                      size=(Window.width * .8, Window.height * .8), 
                      size_hint=(None, None),
                      background_color=(0/255, 127/255, 159/255, 1),
                      background='#FFFFFF')
        exit.bind(on_press=popup.dismiss)
        popup.open()

    def enter(self, instanse):
        '''Обрабатывает нажатие кнопки ввод
           Вся логика и проверки тут.'''
        input_word = ''.join(self.matrix[self.position[0]])
        if input_word not in self.ex_words:
            self.notify('Такого слова нет.\nПопробуйте другое!')
        elif input_word == self.word:
            # Красим всю строку с правильным словом
            self.color_matrix[self.position[0]] = ['g', 'g', 'g', 'g', 'g']
            self.update_field()
            self.notify(make_matrix_text(self.matrix, self.color_matrix) + '\n\nСлово отгадано!')
            self.start_new_game()
        else:
            for i in range(5):
                if input_word[i] == self.word[i]:
                    self.color_matrix[self.position[0]][i] = 'g'
                    self.color_button(input_word[i], 'g')
                elif input_word[i] in self.word:
                    self.color_matrix[self.position[0]][i] = 'y'
                    self.color_button(input_word[i], 'y')
                else:
                    self.color_button(input_word[i], 'b')

            if self.position[0] < 5:
                self.position[0] = self.position[0] + 1
                self.position[1] = 0
                self.update_field()
            else:
                self.notify('Попытки закончились.\nБыло загадоно слово ' + self.word)
                self.start_new_game()

    def update_field(self, *args):
        '''Перерисовывает интерфейс'''
        self.field.text = make_matrix_text(self.matrix, self.color_matrix)

    def on_key_down(self, window, key, *largs):
        '''Функция для поддердки аппаратной клавиатуры'''
        match key:
            case 113 | 1081:
                self.litera(self.literas['й'])
            case 119 | 1094:
                self.litera(self.literas['ц'])
            case 101 | 1091:
                self.litera(self.literas['у'])
            case 114 | 1082:
                self.litera(self.literas['к'])
            case 116 | 1077:
                self.litera(self.literas['е'])
            case 121 | 1085:
                self.litera(self.literas['н'])
            case 117 | 1075:
                self.litera(self.literas['г'])
            case 105 | 1096:
                self.litera(self.literas['ш'])
            case 111 | 1097:
                self.litera(self.literas['щ'])
            case 112 | 1079:
                self.litera(self.literas['з'])
            case 91 | 1093:
                self.litera(self.literas['х'])
            case 93 | 1098:
                self.litera(self.literas['ъ'])
            case 97 | 1092:
                self.litera(self.literas['ф'])
            case 115 | 1099:
                self.litera(self.literas['ы'])
            case 100 | 1074:
                self.litera(self.literas['в'])
            case 102 | 1072:
                self.litera(self.literas['а'])
            case 103 | 1087:
                self.litera(self.literas['п'])
            case 104 | 1088:
                self.litera(self.literas['р'])
            case 106 | 1086:
                self.litera(self.literas['о'])
            case 107 | 1083:
                self.litera(self.literas['л'])
            case 108 | 1076:
                self.litera(self.literas['д'])
            case 59 | 1078:
                self.litera(self.literas['ж'])
            case 39 | 1101:
                self.litera(self.literas['э'])
            case 122 | 1103:
                self.litera(self.literas['я'])
            case 120 | 1095:
                self.litera(self.literas['ч'])
            case 99 | 1089:
                self.litera(self.literas['с'])
            case 118 | 1084:
                self.litera(self.literas['м'])
            case 98 | 1080:
                self.litera(self.literas['и'])
            case 110 | 1090:
                self.litera(self.literas['т'])
            case 109 | 1100:
                self.litera(self.literas['ь'])
            case 44 | 1073:
                self.litera(self.literas['б'])
            case 46 | 1102:
                self.litera(self.literas['ю'])
            case 13:
                self.enter(0)
            case 8:
                self.backspace(0)
            case 27:
                return False

    def build(self):
        '''Основной метод для построения программы'''
        EventLoop.window.bind(on_keyboard=self.on_key_down)
        interface = BoxLayout(orientation='vertical')

        # Рисуем верхнее меню, кнопки без фона, текст везде чёрный
        top_line = BoxLayout(orientation='horizontal', size_hint=[1, .1])
        rules_button = Button(text='Правила',
                              color = '#000000',
                              font_size = Window.width / 28,
                              size_hint=[.3, 1], 
                              on_press=self.rules, 
                              background_color=(236/255, 242/255, 245/255, 1),
                              background_normal='')
        top_line.add_widget(rules_button)
        top_line.add_widget(Label(text='Ru Wordly', 
                                  font_size = Window.width / 28,
                                  color='#000000',
                                  font_name='mono',
                                  halign='center', 
                                  valign='middle'))
        menu_button = Button(text='Меню',
                              color = '#000000',
                              font_size = Window.width / 28,
                              size_hint=[.3, 1], 
                              on_press=self.menu, 
                              background_color=(236/255, 242/255, 245/255, 1),
                              background_normal='')
        top_line.add_widget(menu_button)

        # Рисуем клавиатуру тремя рядами, каждый ряд отдельный BoxLayout
        keyboard = BoxLayout(orientation='vertical', size_hint=[1, .45])
        line1 = BoxLayout(orientation='horizontal', 
                         pos_hint={"center_x": 0.5, "center_y":0.5}, 
                         size_hint=(.98, 1), 
                         padding=1)
        line2 = BoxLayout(orientation='horizontal', 
                         pos_hint={"center_x": 0.5, "center_y":0.5}, 
                         size_hint=(.98, 1), 
                         padding=1)
        line3 = BoxLayout(orientation='horizontal', 
                         pos_hint={"center_x": 0.5, "center_y":0.5}, 
                         size_hint=(.98, 1), 
                         padding=1)

        for i in ["й", "ц", "у", "к", "е", "н", "г", "ш", "щ", "з", "х", "ъ"]:
            tmp = BoxLayout(orientation='horizontal', padding=1)
            b = Button(text=i, 
                       size_hint=[1, 1], 
                       on_press=self.litera, 
                       font_size = Window.width / 16,
                       background_color=self.button_backgound_color, 
                       background_normal='')
            tmp.add_widget(b)
            self.literas[i] = b
            line1.add_widget(tmp)

        for i in ["ф", "ы", "в", "а", "п", "р", "о", "л", "д", "ж", "э"]:
            tmp = BoxLayout(orientation='horizontal', padding=1)
            b = Button(text=i, 
                       size_hint=[1, 1], 
                       on_press=self.litera, 
                       font_size = Window.width / 16,
                       background_color=self.button_backgound_color, 
                       background_normal='')
            tmp.add_widget(b)
            self.literas[i] = b
            line2.add_widget(tmp)

        tmp_b = BoxLayout(orientation='horizontal', 
                          size_hint=[1.2, 1], 
                          padding=1)
        tmp_b.add_widget(Button(text="⌫", 
                                on_press=self.backspace, 
                                font_size = Window.width / 20,
                                font_name='mono',
                                background_color=self.button_backgound_color, 
                                background_normal=''))
        tmp_e = BoxLayout(orientation='horizontal', 
                          size_hint=[1.6, 1], 
                          padding=1)
        tmp_e.add_widget(Button(text="Ввод", 
                                on_press=self.enter, 
                                font_size = Window.width / 20,
                                background_color=self.button_backgound_color, 
                                background_normal=''))
        
        if self.left_enter:
            tmp_b, tmp_e = tmp_e, tmp_b


        line3.add_widget(tmp_b)

        for i in ["я", "ч", "с", "м", "и", "т", "ь", "б", "ю"]:
            tmp = BoxLayout(orientation='horizontal', padding=1)
            b = Button(text=i, 
                       size_hint=[1, 1], 
                       on_press=self.litera, 
                       font_size = Window.width / 16,
                       background_color=self.button_backgound_color, 
                       background_normal='')
            tmp.add_widget(b)
            self.literas[i] = b
            line3.add_widget(tmp)

        line3.add_widget(tmp_e)

        keyboard.add_widget(line1)
        keyboard.add_widget(line2)
        keyboard.add_widget(line3)

        # Добавляем элементы в интерфейс
        interface.add_widget(top_line)
        interface.add_widget(self.field)
        interface.add_widget(keyboard)

        return interface


if __name__ == "__main__":
    MyApp().run()
