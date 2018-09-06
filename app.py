from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import FadeTransition
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
import pandas as pd
import m_predictor as mp
import threading
import sys
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import pandas

Config.set("graphics", "width", "400")
Config.set("graphics", "height", "550")
Config.set("graphics", "resizable", False)

Builder.load_file("interface.kv")

errors = {"HTTP Error 404: Not Found": "Nie znaleziono gracza",
          "HTTP Error 403: Forbidden": "Dostęp zabroniony",
          'HTTP Error 429: Too Many Requests': "Za dużo zapytań",
          'HTTP Error 504: Gateway Timeout': "Jakiś error",
          'HTTP Error 400: Bad Request': 'Zle zapytanie'}

class ImageButton(ButtonBehavior, Image):
    def __init__(self, number=None,  **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.number1 = number


class Exc_thread(threading.Thread):
    def __init__(self, **kwargs):
        super(Exc_thread, self).__init__(**kwargs)
        self.r_start = self.start
        self.start = self.catch_start

    def catch_start(self):
        try:
            self.r_start()
        except Exception as error:
            pop = Error(sys.exc_info())
            pop.open()


class Error(Popup):
    def __init__(self,error, **kwargs):
        super(Error, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (200, 150)
        self.content = Label(text=error)


    def on_touch_down(self, touch):
        self.dismiss()




class Menu(Screen):
    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)

    def start(self):
        player_nick = self.ids.player_input.text
        sm.current = 'loading'
        self.Predict = mp.MainPredictor()
        Load.load(player_nick, self.Predict)



class Loading(Screen):
    def __init__(self, **kwargs):
        super(Loading, self).__init__(**kwargs)

    def load(self, nick, Obj):
        self.Obj = Obj
        self.th = threading.Thread(target=self.Obj.stats, args=(nick, ))
        self.th.start()
        Clock.schedule_interval(self.update, 2)

    def update(self, dt):
        if len(str(self.Obj.error)) == 0:
            if not self.Obj.stats_collected:
                nick1 = str(self.Obj.c_nick1)
                nick2 = str(self.Obj.c_nick2)
                self.ids.statystyki1.text = "Analizuje gracza: " + nick1
                self.ids.statystyki2.text = "Analizuje gracza: " + nick2
                self.ids.l1k.text = "Kills/min: " + str(self.Obj.public_stats1[0])
                self.ids.l1d.text = "Deaths/min: " + str(self.Obj.public_stats1[1])
                self.ids.l1a.text = "Assists/min: " + str(self.Obj.public_stats1[2])
                self.ids.l1m.text = "Minions/min: " + str(self.Obj.public_stats1[3])
                self.ids.l2k.text = "Kills/min: " + str(self.Obj.public_stats2[0])
                self.ids.l2d.text = "Deaths/min: " + str(self.Obj.public_stats2[1])
                self.ids.l2a.text = "Assists/min: " + str(self.Obj.public_stats2[2])
                self.ids.l2m.text = "Minions/min: " + str(self.Obj.public_stats2[3])
                self.wynik = self.predict()
            else:
                Clock.unschedule(self.update)
                if self.wynik:
                    Error(error="Wygra drużyna niebieska", title="Wynik").open()
                else:
                    Error(error="Wygra drużyna czerwona", title="Wynik").open()

        else:
            Clock.unschedule(self.update)
            sm.current = "menu"
            pop = Error(error=errors[self.Obj.error], title = "Error")
            pop.open()

    def predict(self):
        dane = pd.read_csv("Data/learnt_data7.data", sep=" ", header=None)
        x = dane.iloc[:, :dane.shape[1] - 1].values
        y_learn = dane.iloc[:, dane.shape[1] - 1].values
        ss = StandardScaler()
        ss.fit(x)
        x_learn_std = ss.transform(x)
        log = LogisticRegression(C=1000, random_state=0)
        log.fit(x_learn_std, y_learn)
        roznica = self.Obj.public_stats1 - self.Obj.public_stats2
        roznica = roznica.reshape(1, -1)
        wygrana = log.predict(roznica)
        szansa = log.predict_proba(roznica)
        print(szansa)
        self.ids.szansa1.text = "Szansa na wygrana " + str(round(szansa[0][1] * 100,2)) + "%"
        self.ids.szansa2.text = "Szansa na wygrana " + str(round(szansa[0][0] * 100, 2)) + "%"
        if wygrana:
            self.ids.l1k.color = (0, 1, 0, 1)
            self.ids.l1d.color = (0, 1, 0, 1)
            self.ids.l1a.color = (0, 1, 0, 1)
            self.ids.l1m.color = (0, 1, 0, 1)
            self.ids.statystyki1.color = (0, 1, 0, 1)
            self.ids.szansa1.color = (0, 1, 0, 1)
            self.ids.l2k.color = (1, 1, 1, 1)
            self.ids.l2d.color = (1, 1, 1, 1)
            self.ids.l2a.color = (1, 1, 1, 1)
            self.ids.l2m.color = (1, 1, 1, 1)
            self.ids.statystyki2.color = (1, 1, 1, 1)
            self.ids.szansa2.color = (1, 1, 1, 1)

        else:
            self.ids.l2k.color = (0, 1, 0, 1)
            self.ids.l2d.color = (0, 1, 0, 1)
            self.ids.l2a.color = (0, 1, 0, 1)
            self.ids.l2m.color = (0, 1, 0, 1)
            self.ids.statystyki2.color = (0, 1, 0, 1)
            self.ids.szansa2.color = (0, 1, 0, 1)
            self.ids.l1k.color = (1, 1, 1, 1)
            self.ids.l1d.color = (1, 1, 1, 1)
            self.ids.l1a.color = (1, 1, 1, 1)
            self.ids.l1m.color = (1, 1, 1, 1)
            self.ids.statystyki1.color = (1, 1, 1, 1)
            self.ids.szansa1.color = (1, 1, 1, 1)
        return wygrana
    def back(self):
        self.Obj.terminate = True
        Clock.unschedule(self.update)
        sm.current = "menu"
        self.ids.statystyki1.text = "Analizuje gracza: "
        self.ids.statystyki2.text = "Analizuje gracza: "
        self.ids.l1k.text = "Kills/min: 0.0"
        self.ids.l1d.text = "Deaths/min: 0.0"
        self.ids.l1a.text = "Assists/min: 0.0"
        self.ids.l1m.text = "Minions/min: 0.0"
        self.ids.l2k.text = "Kills/min: 0.0"
        self.ids.l2d.text = "Deaths/min: 0.0"
        self.ids.l2a.text = "Assists/min: 0.0"
        self.ids.l2m.text = "Minions/min: 0.0"


Load = Loading(name="loading")
sm = ScreenManager(transition=FadeTransition())
sm.add_widget(Menu(name="menu"))
sm.add_widget(Load)



class Interface(App):
    def build(self):
        return sm

if __name__ == "__main__":
    from kivy.base import runTouchApp
    runTouchApp(sm)