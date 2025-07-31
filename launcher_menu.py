import json
import os
import sys
from pygame import *

def show_settings_menu():
   init()
   window = display.set_mode((600, 400))
   display.set_caption("Налаштування")
   font.init()
   font_ = font.Font(None, 32)

   def list_images(prefix):
       return [f for f in os.listdir("images") if f.startswith(prefix) and f.endswith((".png", ".jpg"))]

   backgrounds = list_images("background")
   balls = list_images("ball")
   paddles = list_images("paddle")

   selected = {
        "background": 0,
        "ball": 0,
        "paddle":0
   }

   def draw_text(text, x, y):
       text_surf = font_.render(text, True, (214, 203, 199))
       window.blit(text_surf, (x, y))

   def draw_skin_info():
       draw_text(f"Фон: {backgrounds[selected['background']]}", 50, 50)
       draw_text(f"М'яч: {balls[selected['ball']]}", 50, 120)
       draw_text(f"Платформа: {paddles[selected['paddle']]}", 50, 190)
       draw_text("←/→ - зміна фону", 50, 80)
       draw_text("A/D - зміниа м'яча", 50, 150)
       draw_text("Z/C - зміниа платформи", 50, 220)
       draw_text("Enter - зберегти", 50, 290)
       draw_text(" Esc - назад", 50, 360)

   running = True
   while running:
       window.fill((59, 51, 50))
       draw_skin_info()
       display.update()

       for e in event.get():
           if e.type == QUIT:
               running = False
           if e.type == KEYDOWN:
               if e.key == K_LEFT:
                   selected["background"] = (selected["background"] - 1) % len(backgrounds)
               if e.key == K_RIGHT:
                   selected["background"] = (selected["background"] + 1) % len(backgrounds)
               if e.key == K_a:
                   selected["ball"] = (selected["ball"] - 1) % len(balls)
               if e.key == K_d:
                   selected["ball"] = (selected["ball"] + 1) % len(balls)
               if e.key == K_z:
                   selected["paddle"] = (selected["paddle"] - 1) % len(paddles)
               if e.key == K_c:
                   selected["paddle"]= (selected["paddle"] + 1) % len(paddles)
               if e.key == K_RETURN:
                    with open("settings.json", "r") as f:
                        data = json.load(f)
                    data["ball"] = balls[selected["ball"]]
                    data["background"] = backgrounds[selected["background"]]
                    with open("settings.json", "w") as f:
                        json.dump(data, f)

def run_menu():
    window_size = 600, 400
    window = display.set_mode(window_size)
    display.set_caption("Пін-понг лаунчер")
    font.init()
    main_font = font.Font(None, 36)

    # --- JSON збереження ---
    filename = "settings.json"
    sound_on = True

    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
            sound_on = data.get("sound", True)
    else:
        with open(filename, 'w') as f:
            json.dump({'sound': True}, f)

    class Button:
        def __init__(self, x, y, width, height, color, text, text_color=(0, 0, 0)):
            self.rect = Rect(x, y, width, height)
            self.color = color
            self.text = text
            self.text_color = text_color
            self.font = font.Font(None, 28)

        def draw(self):
            draw.rect(window, self.color, self.rect)
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            window.blit(text_surf, text_rect)

        def is_clicked(self, event):
            return event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

    # --- Кнопки ---
    play_button = Button(200, 80, 200, 50, (214, 203, 199), "Грати")
    sound_button = Button(200, 160, 200, 50, (214, 203, 199), "Sound: On")
    settings_button = Button(200, 240, 200, 50, (214, 203, 199), "Налаштування")
    exit_button = Button(200, 480, 200, 50, (214, 203, 199), "Вийти")

    def update_sound_button():
        text = f"Sound: {'On' if sound_on else 'Off'}"
        sound_button.text = text

    running = True
    while running:
        window.fill((59, 51, 50))

        play_button.draw()
        sound_button.draw()
        settings_button.draw()
        exit_button.draw()

        display.update()

        for e in event.get():
            if e.type == QUIT:
                sys.exit()
            if play_button.is_clicked(e):
                with open(filename, 'w') as f:
                    json.dump({'sound': sound_on}, f)
                running = False
            if sound_button.is_clicked(e):
                sound_on = not sound_on
                update_sound_button()
            if settings_button.is_clicked(e):
                show_settings_menu()
            if exit_button.is_clicked(e):
                sys.exit()

run_menu()