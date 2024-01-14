from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.image import Image

import random

class MemoryGame(GridLayout):
    def __init__(self, **kwargs):
        super(MemoryGame, self).__init__(**kwargs)
        self.cols = 4  # Increase columns to accommodate new widgets
        self.cards = list(range(1, 9)) * 2
        
        self.selected_cards = []
        self.sound_enabled = False
        self.sound = SoundLoader.load('D:\\Downloads Files\\NewJeans - OMG [320] Kbps-(PagalWorld.Gay).mp3')  # Replace with your sound file path
        self.create_board()
        self.add_sound_switch()
        self.match_found = False  # Flag to track if a match has been found
        self.score = 0  # Initialize score
        self.add_widget(Label(text="Score: 0", font_size=20))  # Score Label
        self.add_widget(Button(text="Restart", on_press=self.restart_game, font_size=20))  # Restart Button

    def random_shuffle(self):
        random.shuffle(self.cards)

    def create_board(self):
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
            return  # Card already revealed

        button.text = str(button.card_value)
        self.selected_cards.append(button)

        if len(self.selected_cards) == 2:
            self.check_match()
            self.selected_cards = []

    def check_match(self):
        if self.selected_cards[0].card_value == self.selected_cards[1].card_value:
            self.show_match_popup()
            self.match_found = True  # Set flag to indicate a match has been found
            self.update_score(10)  # Increase score by 10 for each match
        else:
            self.hide_unmatched_cards()
            self.update_score(-1)  # Decrease score by 1 for each mismatch

    def show_match_popup(self):
        if self.sound_enabled and self.sound:
            if not self.sound.state == 'play':
                self.sound.play()

        content = Button(text='Match!', size_hint=(None, None), size=(100, 50))
        popup = Popup(title='Match Found', content=content, auto_dismiss=True)
        content.bind(on_press=popup.dismiss)
        popup.open()
        self.selected_cards = []  # Clear selected cards after popup is closed
        img = Image(source='your_image_path.png')  # แทนที่ 'your_image_path.png' ด้วยที่เก็บภาพของคุณ
        popup.content.add_widget(img)
        img.bind(on_press=self.image_click)

        # Restart the game if a match was found
        if self.match_found:
            self.match_found = False  # Reset the flag
            self.restart_game()
    def image_click(self, instance):
            print("Image Clicked!")

    def show_card(self, instance):
        value = instance.card_value
        instance.background_normal = ''
        instance.background_color = (0, 0, 0, 0)
        img = AsyncImage(source=f'D:\\Downloads Files\\image_folder\\{value}.png')  # Change from Image to AsyncImage
        instance.add_widget(img)
        self.check_match()

    def restart_game(self, instance=None):
        self.cards = list(range(1, 9)) * 2
        random.shuffle(self.cards)
        for child in self.children[2:]:  # Exclude the sound switch, score label, and restart button
            child.text = ' '  # Clear card text
        self.score = 0  # Reset the score
        self.update_score(0)  # Update the score label

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
        return MemoryGame()

if __name__ == '__main__':
    MemoryGameApp().run()
