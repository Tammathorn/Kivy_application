from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import random

class MemoryGame(GridLayout):
    def __init__(self, **kwargs):
        super(MemoryGame, self).__init__(**kwargs)
        self.cols = 4
        self.cards = list(range(1, 9)) * 2
        random.shuffle(self.cards)
        self.selected_cards = []
        self.create_board()

    def create_board(self):
        for card_value in self.cards:
            card_button = Button(text=' ', on_press=self.card_click)
            card_button.card_value = card_value
            self.add_widget(card_button)

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
        else:
            self.hide_unmatched_cards()

    def show_match_popup(self):
        content = Button(text='Match!', size_hint=(None, None), size=(100, 50))
        popup = Popup(title='Match Found', content=content, auto_dismiss=True)
        content.bind(on_press=popup.dismiss)
        popup.open()

    def hide_unmatched_cards(self):
        for card in self.selected_cards:
            card.text = ' '

class MemoryGameApp(App):
    def build(self):
        return MemoryGame()

if __name__ == '__main__':
    MemoryGameApp().run()
