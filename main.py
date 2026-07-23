import os
import requests
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

RAW_KEY = "AQ.Ab8RN6LbdlGqc9MzzTZNi5_FyK7Sr_JwDA1xpz9z1Hv3wEBU_g"

class KarenApp(App):
    def build(self):
        self.title = "KAREN AI"
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.scroll = ScrollView(size_hint=(1, 0.85))
        self.chat_history = Label(
            text="🤖 [KAREN]: Systems online! Tu batao, aaj kya program hai?\n",
            font_size='16sp',
            size_hint_y=None,
            color=(0.2, 0.8, 1, 1),
            halign='left',
            valign='top'
        )
        self.chat_history.bind(texture_size=self.chat_history.setter('size'))
        self.scroll.add_widget(self.chat_history)
        main_layout.add_widget(self.scroll)
        
        input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=5)
        self.user_input = TextInput(hint_text="Talk to Karen...", multiline=False, size_hint=(0.75, 1))
        send_btn = Button(text="Send 🚀", size_hint=(0.25, 1))
        send_btn.bind(on_press=self.send_to_karen)
        
        input_layout.add_widget(self.user_input)
        input_layout.add_widget(send_btn)
        main_layout.add_widget(input_layout)
        return main_layout

    def send_to_karen(self, instance):
        user_text = self.user_input.text.strip()
        if not user_text: return
        self.chat_history.text += f"\n👤 [YOU]: {user_text}\n"
        self.user_input.text = ""
        
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={RAW_KEY.strip()}"
            payload = {
                "contents": [{"parts": [{"text": user_text}]}],
                "systemInstruction": {
                    "parts": [{"text": "You are KAREN, a sharp, witty AI assistant. Speak in casual informal Hinglish (tu/tum/batao)."}]
                }
            }
            res = requests.post(url, json=payload, timeout=15)
            data = res.json()
            
            if "candidates" in data and len(data["candidates"]) > 0:
                reply = data["candidates"][0]["content"]["parts"][0]["text"]
                self.chat_history.text += f"🤖 [KAREN]: {reply}\n"
            else:
                self.chat_history.text += f"⚠️ API Response Error: {data}\n"
        except Exception as e:
            self.chat_history.text += f"⚠️ Error: {str(e)}\n"

if __name__ == '__main__':
    KarenApp().run()
