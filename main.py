import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'  # Força renderização compatível
os.environ['KIVY_WINDOW'] = 'sdl2'           # Usa janela SDL2 (mais estável)

from kivy.config import Config
Config.set('graphics', 'multisamples', '0')  # Desativa anti-aliasing (importante para Android)
Config.write()

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.properties import ListProperty
import random

class Bolinha(Button):
    pass

class SomaBolinhasGame(FloatLayout):
    bolinhas_ativas = ListProperty([])
    soma_correta = 0
    fase = 1  # Nova variável para controlar a fase (nível)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mostrar_menu()

    def mostrar_menu(self):
        self.clear_widgets()
        self.fase = 1  # Reseta a fase ao voltar ao menu
        menu_label = Label(
            text="SOMA BOLINHAS",
            font_size='40sp',
            size_hint=(None, None),
            size=(300, 60),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        botao_comecar = Button(
            text="Começar",
            font_size='20sp',
            size_hint=(0.3, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.4}
        )
        botao_comecar.bind(on_press=lambda x: self.iniciar_fase())

        self.add_widget(menu_label)
        self.add_widget(botao_comecar)

    def iniciar_fase(self):
        self.clear_widgets()
        self.bolinhas_ativas = []
        self.soma_correta = 0

        self.prep_label = Label(
            text=f"Fase {self.fase} - Prepare-se!",
            font_size='30sp',
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.prep_label)

        Clock.schedule_once(self.mostrar_bolinhas, 1)

    def gerar_posicao_sem_sobreposicao(self, existentes):
        max_tentativas = 50
        for _ in range(max_tentativas):
            x = random.uniform(0.0, 0.85)
            y = random.uniform(0.3, 0.75)
            colisao = False
            for pos in existentes:
                if abs(x - pos[0]) < 0.15 and abs(y - pos[1]) < 0.15:
                    colisao = True
                    break
            if not colisao:
                return x, y
        return 0.5, 0.5

    def cor_aleatoria(self):
        return (
            random.uniform(0.2, 1),
            random.uniform(0.2, 1),
            random.uniform(0.2, 1),
            1
        )

    def mostrar_bolinhas(self, dt):
        self.remove_widget(self.prep_label)

        posicoes_usadas = []
        num_bolinhas = 3 + self.fase  # Começa com 4 bolinhas na fase 1
        for _ in range(num_bolinhas):
            numero = random.randint(1, 9)
            self.soma_correta += numero

            x, y = self.gerar_posicao_sem_sobreposicao(posicoes_usadas)
            posicoes_usadas.append((x, y))

            bolinha = Bolinha(
                text=str(numero),
                size_hint=(0.15, 0.15),
                pos_hint={'x': x, 'y': y},
                background_normal='',
                background_color=self.cor_aleatoria()
            )

            self.bolinhas_ativas.append(bolinha)
            self.add_widget(bolinha)

        Clock.schedule_once(self.mostrar_opcoes, 5)

    def mostrar_opcoes(self, dt):
        for bolinha in self.bolinhas_ativas:
            self.remove_widget(bolinha)

        opcoes = [self.soma_correta]
        while len(opcoes) < 5:
            valor = random.randint(self.soma_correta - 5, self.soma_correta + 5)
            if valor > 0 and valor not in opcoes:
                opcoes.append(valor)

        random.shuffle(opcoes)

        for i, opcao in enumerate(opcoes):
            resposta = Button(
                text=str(opcao),
                size_hint=(0.15, 0.15),
                pos_hint={'x': 0.05 + i * 0.19, 'y': 0.05},
                background_normal='',
                background_color=(1, 0.6, 0.3, 1)
            )
            resposta.bind(on_press=self.verificar_resposta)
            self.add_widget(resposta)

    def verificar_resposta(self, instance):
        escolhido = int(instance.text)
        if escolhido == self.soma_correta:
            instance.background_color = (0, 1, 0, 1)
            msg = Label(
                text="Você acertou!",
                font_size='30sp',
                size_hint=(None, None),
                size=(300, 50),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            self.add_widget(msg)
            self.fase += 1  # Avança para próxima fase
            Clock.schedule_once(lambda dt: self.iniciar_fase(), 2)
        else:
            instance.background_color = (1, 0, 0, 1)
            msg = Label(
                text="Você errou!",
                font_size='30sp',
                size_hint=(None, None),
                size=(300, 50),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            self.add_widget(msg)
            Clock.schedule_once(lambda dt: self.mostrar_menu(), 2)

class SomaBolinhasApp(App):
    def build(self):
        return SomaBolinhasGame()

if __name__ == '__main__':
    SomaBolinhasApp().run()
