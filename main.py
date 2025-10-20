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
from kivy.core.window import Window

# Глобальные настройки
Window.clearcolor = (236/255, 242/255, 245/255, 1)
Window.title = "Ru_Wordly_24/7"

Config = configparser.ConfigParser()
Config.read("my.ini")


def get_all_words():
    '''Читает файлы со списками слов.
       Возврашайт картеж содержащий 2 спмска слов.'''
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


class MyApp(App):
    def __init__(self):
        super().__init__()
        self.button_backgound_color = (0/255, 87/255, 111/255, 1)
        #self.button_backgound_color = (1, 1, 1, 1)
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
        self.buttons = {}
        self.field = Label(text=make_matrix_text(self.matrix, self.color_matrix), 
                           color='#000000', 
                           font_size = '50sp', 
                           font_name='mono', 
                           markup = True)
        self.start_new_game()

    def start_new_game(self):
        self.matrix = [["_", "_", "_", "_", "_"], ["_", "_", "_", "_", "_"], ["_", "_", "_", "_", "_"], ["_", "_", "_", "_", "_"], ["_", "_", "_", "_", "_"], ["_", "_", "_", "_", "_"]]
        self.color_matrix = [["n", "n", "n", "n", "n"], ["n", "n", "n", "n", "n"], ["n", "n", "n", "n", "n"], ["n", "n", "n", "n", "n"], ["n", "n", "n", "n", "n"], ["n", "n", "n", "n", "n"]]
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
        self.buttons[instanse.text] = instanse
        if self.position[1] < 5:
            self.matrix[self.position[0]][self.position[1]] = instanse.text
            self.position[1] = self.position[1] + 1
        self.update_field()

    def color_button(self, button, color):
        '''Красит кнопки на клавиатуре'''
        color_now = self.buttons[button].background_color
        # Проверка нужна чтоб не перекрасить зелёную кнопку в желтую))
        if color_now == [0.0, 0.7176470588235294, 0.1607843137254902, 1.0]:
            return
        if color == 'b':
            self.buttons[button].background_color = '000000'
        elif color == 'y':
            self.buttons[button].background_color = 'fbbd05'
        elif color == 'g':
            self.buttons[button].background_color = '00b729'
        else:
            pass

    def clear_all_buttons(self):
        '''Убирает цвет со всех кнопок'''
        l = ["й", "ц", "у", "к", "е", "н", "г", "ш", "щ", "з", "х", "ъ", "ф", "ы", "в", "а", "п", "р", "о", "л", "д", "ж", "э", "я", "ч", "с", "м", "и", "т", "ь", "б", "ю"]
        for i in l:
            try:
                self.buttons[i].background_color = self.button_backgound_color
            except:
                pass

    def backspace(self, instanse):
        '''Обрабатывает нажатие backspace'''
        if self.position[1] > 0:
            self.position[1] = self.position[1] - 1
            self.matrix[self.position[0]][self.position[1]] = '_'
        self.update_field()

    def on_active(self, instance, value):
        if value:
            Config.set('settings', 'easy_level', '1')
            with open('my.ini', 'w') as configfile:
                Config.write(configfile)
            self.start_new_game()
        else:
            Config.set('settings', 'easy_level', '0')
            with open('my.ini', 'w') as configfile:
                Config.write(configfile)
            self.start_new_game()
    
    def set_left_enter(self, instance, value):
        if value:
            Config.set('settings', 'left_enter', '1')
            with open('my.ini', 'w') as configfile:
                Config.write(configfile)
            self.start_new_game()
        else:
            Config.set('settings', 'left_enter', '0')
            with open('my.ini', 'w') as configfile:
                Config.write(configfile)
            self.start_new_game()

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
'''
        self.scroll_notify(about_text)
    
    def scroll_notify(self, message):
        '''Выводит текст в окне с полосой прокрутки.'''
        content = BoxLayout(orientation='vertical', size=(.5, .5))
        scroll = ScrollView()
        scroll.add_widget(Label(text=message, 
                                color='#FFFFFF', 
                                padding = 30,
                                size=(Window.width * .8, Window.height * .8), 
                                text_size=(Window.width * .8, Window.height * .8), 
                                size_hint_y=None,
                                valign='middle'))
        content.add_widget(scroll)
        a = Button(text='Ok', font_size = '15dp', size_hint=[1, .1], padding = 30, background_color=self.button_backgound_color, background_normal='')
        content.add_widget(a)
        popup_a = Popup(title='', 
                      content=content, 
                      auto_dismiss=False, 
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
                                 font_size = '25sp', 
                                 size=(Window.width * .8, Window.height * .8), 
                                 text_size=(Window.width * .8, Window.height * .8), 
                                 halign='center', 
                                 valign='middle'))
        b = Button(text='Ok', 
                   font_size = '15dp',
                   background_color=self.button_backgound_color,
                   background_normal='',
                   pos_hint={"center_x": 0.5, "center_y":0.5})
        b_box = BoxLayout(orientation='vertical', size_hint=[1, .16], padding = 5)
        b_box.add_widget(b)
        content.add_widget(b_box)
        popup = Popup(title='', 
                      content=content, 
                      auto_dismiss=False, 
                      separator_height=0, 
                      size=(Window.width * .8, Window.height * .8), 
                      size_hint=(None, None),
                      background_color=(0/255, 127/255, 159/255, 1),
                      background='#FFFFFF')
        b.bind(on_press=popup.dismiss)
        popup.open()

    def menu(self, *args):
        content = BoxLayout(orientation='vertical', size=(.5, .5))
        b = BoxLayout(orientation='horizontal', size_hint=[1, .1], padding = 5)
        exit = Button(text='Закрыть меню', 
                   font_size = '15dp',
                   background_color=self.button_backgound_color,
                   background_normal='',
                   pos_hint={"center_x": 0.5, "center_y":0.5})
        b.add_widget(exit)
        a_box = BoxLayout(orientation='horizontal', size_hint=[1, .1], padding = 5)
        a_box.add_widget(Button(text='Правила', 
                                  font_size = '15dp',
                                  on_press=self.rules,
                                  background_color=self.button_backgound_color,
                                  background_normal='',
                                  pos_hint={"center_x": 0.5, "center_y":0.5}))
        b_box = BoxLayout(orientation='horizontal', size_hint=[1, .1], padding = 5)
        b_box.add_widget(Button(text='Об игре', 
                                  font_size = '15dp',
                                  on_press=self.about,
                                  background_color=self.button_backgound_color,
                                  background_normal='',
                                  pos_hint={"center_x": 0.5, "center_y":0.5}))
        с_box = BoxLayout(orientation='horizontal', size_hint=[1, .1], padding = 5)
        с_box.add_widget(Label(text='Лёгкий режим', size_hint=[.7, 1]))
        sw1 = Switch(active=self.easy)
        sw1.bind(active=self.on_active)
        с_box.add_widget(sw1)
        e_box = BoxLayout(orientation='horizontal', size_hint=[1, .1], padding = 5)
        e_box.add_widget(Label(text='Кнопка ввода слева', size_hint=[.7, 1]))
        sw2 = Switch(active=self.left_enter)
        sw2.bind(active=self.set_left_enter)
        e_box.add_widget(sw2)
        content.add_widget(с_box)
        content.add_widget(Label(text='В лёгком режиме юудут загадываться более распространенные слова', 
                                 color='#FFFFFF',
                                 size_hint=[1, .05],
                                 text_size=(Window.width * .7, Window.height * .07), 
                                 halign='center', 
                                 valign='middle'))
        content.add_widget(e_box)
        content.add_widget(Label(text='Кнопки ввод и стереть поменяются местами.\nПотребуется перезапустить приложение.', 
                                 color='#FFFFFF',
                                 size_hint=[1, .05],
                                 text_size=(Window.width * .7, Window.height * .07), 
                                 halign='center', 
                                 valign='middle'))
        content.add_widget(a_box)
        content.add_widget(b_box)
        content.add_widget(b)
        popup = Popup(title='', 
                      content=content, 
                      auto_dismiss=False, 
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

    def build(self):
        '''Основной метод для построения программы'''
        interface = BoxLayout(orientation='vertical')

        top_line = BoxLayout(orientation='horizontal', size_hint=[1, .1])
        rules_button = Button(text='Правила',
                              color = '#000000',
                              size_hint=[.3, 1], 
                              on_press=self.rules, 
                              background_color=(236/255, 242/255, 245/255, 1),
                              background_normal='')
        top_line.add_widget(rules_button)
        top_line.add_widget(Label(text='Ru Wordly', 
                                 color='#000000',
                                 font_name='mono',
                                 halign='center', 
                                 valign='middle'))
        menu_button = Button(text='Меню',
                              color = '#000000',
                              size_hint=[.3, 1], 
                              on_press=self.menu, 
                              background_color=(236/255, 242/255, 245/255, 1),
                              background_normal='')
        top_line.add_widget(menu_button)

        l = [["й", "ц", "у", "к", "е", "н", "г", "ш", "щ", "з", "х", "ъ"], ["ф", "ы", "в", "а", "п", "р", "о", "л", "д", "ж", "э"], ["я", "ч", "с", "м", "и", "т", "ь", "б", "ю"]]
        keyboard = BoxLayout(orientation='vertical', size_hint=[1, .4])
        row1 = BoxLayout(orientation='horizontal', 
                         pos_hint={"center_x": 0.5, "center_y":0.5}, 
                         size_hint=(0.95, 1), 
                         padding=5)
        row2 = BoxLayout(orientation='horizontal', 
                         pos_hint={"center_x": 0.5, "center_y":0.5}, 
                         size_hint=(0.95, 1), 
                         padding=5)
        row3 = BoxLayout(orientation='horizontal', 
                         pos_hint={"center_x": 0.5, "center_y":0.5}, 
                         size_hint=(0.95, 1), 
                         padding=5)


        for i in l[0]:
            tmp = BoxLayout(orientation='horizontal', padding=1)
            tmp.add_widget(Button(text=i, 
                                  size_hint=[0.95, 1], 
                                  on_press=self.litera, 
                                  font_size = '30sp', 
                                  background_color=self.button_backgound_color, 
                                  background_normal=''))
            row1.add_widget(tmp)

        for i in l[1]:
            tmp = BoxLayout(orientation='horizontal', padding=1)
            tmp.add_widget(Button(text=i, 
                                  size_hint=[0.95, 1], 
                                  on_press=self.litera, 
                                  font_size = '30sp', 
                                  background_color=self.button_backgound_color, 
                                  background_normal=''))
            row2.add_widget(tmp)

        tmp_b = BoxLayout(orientation='horizontal', 
                          size_hint=[1.2, 1], 
                          padding=1)
        tmp_b.add_widget(Button(text="<-", 
                                on_press=self.backspace, 
                                font_size = '35sp', 
                                background_color=self.button_backgound_color, 
                                background_normal=''))
        tmp_e = BoxLayout(orientation='horizontal', 
                          size_hint=[1.6, 1], 
                          padding=1)
        tmp_e.add_widget(Button(text="Ввод", 
                                on_press=self.enter, 
                                font_size = '20sp', 
                                background_color=self.button_backgound_color, 
                                background_normal=''))
        
        if self.left_enter:
            tmp_b, tmp_e = tmp_e, tmp_b


        row3.add_widget(tmp_b)

        for i in l[2]:
            tmp = BoxLayout(orientation='horizontal', padding=1)
            tmp.add_widget(Button(text=i, 
                                  size_hint=[0.95, 1], 
                                  on_press=self.litera, 
                                  font_size = '30sp', 
                                  background_color=self.button_backgound_color, 
                                  background_normal=''))
            row3.add_widget(tmp)

        row3.add_widget(tmp_e)

        keyboard.add_widget(row1)
        keyboard.add_widget(row2)
        keyboard.add_widget(row3)

        interface.add_widget(top_line)
        interface.add_widget(self.field)
        interface.add_widget(keyboard)

        return interface


if __name__ == "__main__":
    MyApp().run()
