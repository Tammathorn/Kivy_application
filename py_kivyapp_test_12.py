from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen

import random

class WelcomeScreen(GridLayout):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(text="Welcome to Memory Game!", font_size=36))
        self.add_widget(Image(source='D:\Downloads Files\Memory Game\pngtree-welcome-wide-banner-style-png-image_6684044.png',
                                size_hint=(None, None), size=(1600, 1000)))  # Replace with your image
        self.add_widget(Button(text="Start Game", on_press=self.start_game, font_size=24))

    def start_game(self, instance):
        game = MemoryGame()
        self.parent.add_widget(game)
        self.parent.remove_widget(self)

class MemoryGame(GridLayout):
    def __init__(self, **kwargs):
        super(MemoryGame, self).__init__(**kwargs)
        self.cols = 4
        self.cards = list(range(1, 9)) * 2
        self.selected_cards = []
        self.sound_enabled = False
        self.sound = SoundLoader.load('D:\\Downloads Files\\NewJeans - OMG [320] Kbps-(PagalWorld.Gay).mp3')  # Replace with your sound file path
        self.create_board()
        self.add_sound_switch()
        self.match_found = False
        self.score = 0
        self.add_widget(Label(text="Score: 0", font_size=20))
        self.add_widget(Button(text="Restart", on_press=self.restart_game, font_size=20))

    def random_shuffle(self):
        random.shuffle(self.cards)

    def create_board(self):
        self.random_shuffle()
        for card_value in self.cards:
            card_button = Button(text=' ', on_press=self.card_click)
            card_button.card_value = card_value
            self.add_widget(card_button)

    def add_sound_switch(self):
        sound_switch = Switch(active=self.sound_enabled)
        sound_switch.bind(active=self.toggle_sound)
        self.add_widget(sound_switch)

    def card_click(self, button):
        if button.text != ' ':
            return

        button.text = str(button.card_value)
        self.selected_cards.append(button)

        if len(self.selected_cards) == 2:
            self.check_match()

    def check_match(self):
        if self.selected_cards[0].card_value == self.selected_cards[1].card_value:
            self.show_match_popup()
            self.match_found = True
            self.update_score(10)
        else:
            self.hide_unmatched_cards()
            self.update_score(-1)

    def show_match_popup(self):
        if self.sound_enabled and self.sound:
            if not self.sound.state == 'play':
                self.sound.play()

        content = Image(source='D:\Downloads Files\card-game-48980_960_720.png', size_hint=(None, None), size=(100, 50))
        popup = Popup(title='Match Found', content=content, auto_dismiss=True)
        content.bind(on_press=popup.dismiss)
        popup.open()

        if self.match_found:
            self.match_found = False
            self.restart_game()

    def restart_game(self, instance=None):
        self.clear_widgets()
        self.create_board()
        self.score = 0
        self.update_score(0)

    def hide_unmatched_cards(self):
        for card in self.selected_cards:
            card.text = ' '

    def toggle_sound(self, instance, value):
        self.sound_enabled = value
        if value and self.sound:
            self.sound.play()
        elif not value and self.sound:
            self.sound.stop()

    def update_score(self, points):
        self.score += points
        self.children[0].text = f"Score: {self.score}"

class MemoryGameApp(App):
    def build(self):
        welcome_screen = WelcomeScreen()
        return welcome_screen
if __name__ == '__main__':
    MemoryGameApp().run()
