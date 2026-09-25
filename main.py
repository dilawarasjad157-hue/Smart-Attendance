from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from datetime import datetime

class CardBoxLayout(BoxLayout):
    def __init__(self, bg_color=(0.12, 0.15, 0.23, 1), **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class AttendanceScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        header = Label(
            text="[b][color=00f0ff]SMART ATTENDANCE SYSTEM[/color][/b]",
            markup=True, font_size='22sp', size_hint_y=0.1
        )
        main_layout.add_widget(header)

        scan_card = CardBoxLayout(orientation='vertical', padding=20, spacing=10, size_hint_y=0.45)
        self.status_label = Label(
            text="[color=888888]Place Finger on Scanner[/color]",
            markup=True, font_size='16sp'
        )
        scan_btn = Button(
            text="[b]SCAN FINGERPRINT[/b]",
            markup=True, background_normal='', background_color=(0, 0.6, 1, 1),
            font_size='18sp', size_hint_y=0.4
        )
        scan_btn.bind(on_press=self.simulate_scan)
        
        scan_card.add_widget(self.status_label)
        scan_card.add_widget(scan_btn)
        main_layout.add_widget(scan_card)

        nav_layout = BoxLayout(size_hint_y=0.15, spacing=10)
        reg_btn = Button(text="Register Student", background_normal='', background_color=(0.15, 0.2, 0.3, 1))
        reg_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'register'))
        
        nav_layout.add_widget(reg_btn)
        main_layout.add_widget(nav_layout)
        self.add_widget(main_layout)

    def simulate_scan(self, instance):
        self.status_label.text = "[color=ffcc00]Scanning Fingerprint...[/color]"
        Clock.schedule_once(self.mark_done, 1.5)

    def mark_done(self, dt):
        now = datetime.now().strftime("%I:%M %p")
        self.status_label.text = f"[color=00ff77][b]MATCH FOUND![/b]\nMohamed Dilawar (Roll #101)\nMarked at {now}[/color]"

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = CardBoxLayout(orientation='vertical', padding=20, spacing=15)
        
        title = Label(
            text="[b][color=00f0ff]ADD NEW STUDENT[/color][/b]",
            markup=True, font_size='20sp', size_hint_y=0.15
        )
        self.name_input = TextInput(hint_text="Student Full Name", multiline=False, size_hint_y=0.15)
        self.roll_input = TextInput(hint_text="Roll Number", multiline=False, size_hint_y=0.15)
        
        save_btn = Button(
            text="[b]SAVE STUDENT[/b]", markup=True,
            background_normal='', background_color=(0, 0.8, 0.4, 1), size_hint_y=0.2
        )
        save_btn.bind(on_press=self.back_home)
        
        layout.add_widget(title)
        layout.add_widget(self.name_input)
        layout.add_widget(self.roll_input)
        layout.add_widget(save_btn)
        self.add_widget(layout)

    def back_home(self, instance):
        self.manager.current = 'attendance'

class AttendanceApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(AttendanceScreen(name='attendance'))
        sm.add_widget(RegisterScreen(name='register'))
        return sm

if __name__ == '__main__':
    AttendanceApp().run()
      
