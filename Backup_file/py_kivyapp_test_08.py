from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader
from kivy.uix.filechooser import FileChooserIconView

import random

class MemoryGame(GridLayout):
    def __init__(self, **kwargs):
        super(MemoryGame, self).__init__(**kwargs)
        self.cols = 5  # Add column for switch
        self.images = ['image1.png', 'image2.png', 'image3.png', 'image4.png', 'image5.png', 'image6.png', 'image7.png', 'image8.png']
        self.cards = self.images * 2
        random.shuffle(self.cards)
        self.selected_cards = []
        self.sound_enabled = False  # Start with sound off
        self.sound = None
        self.create_board()
        self.add_sound_switch()
        self.add_change_sound_button()

    def create_board(self):
        for card_image in self.cards:
            card_button = Button(background_normal='path/to/your/images/back_image.png', on_press=self.card_click)
            card_button.card_image = card_image
            self.add_widget(card_button)

    def add_sound_switch(self):
        sound_switch = Switch(active=self.sound_enabled)
        sound_switch.bind(active=self.toggle_sound)
        self.add_widget(sound_switch)

    def show_file_chooser(self, instance):
        file_chooser = FileChooserIconView()
        file_chooser.bind(on_submit=self.change_sound)
        popup = Popup(title="Choose Sound File", content=file_chooser, size_hint=(0.9, 0.9))
        popup.open()

    def card_click(self, button):
        if button.background_normal != 'path/to/your/images/back_image.png':
            return  # Card already revealed

        button.background_normal = button.card_image
        self.selected_cards.append(button)

        if len(self.selected_cards) == 2:
            self.check_match()
            self.selected_cards = []

    def check_match(self):
        if self.selected_cards[0].card_image == self.selected_cards[1].card_image:
            self.show_match_popup()
        else:
            self.hide_unmatched_cards()

    def show_match_popup(self):
        if self.sound_enabled and self.sound:
            if not self.sound.state == 'play':
                self.sound.play()

        content = Button(text='Match!', size_hint=(None, None), size=(100, 50))
        popup = Popup(title='Match Found', content=content, auto_dismiss=True)
        content.bind(on_press=popup.dismiss)
        popup.open()

    def hide_unmatched_cards(self):
        for card in self.selected_cards:
            card.background_normal = 'path/to/your/images/back_image.png'

    def toggle_sound(self, instance, value):
        self.sound_enabled = value
        if value and self.sound:
            self.sound.play()
        elif not value and self.sound:
            self.sound.stop()

class MemoryGameApp(App):
    def build(self):
        return MemoryGame()

if __name__ == '__main__':
    MemoryGameApp().run()
