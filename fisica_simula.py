#Esse nao ta funcionando

import pygame
import sys


# Inicializar o Pygame
pygame.init()

# Configurações da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Simulação Física em Python")

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)

# Parâmetros do objeto
posicao = [largura // 2, 50]
velocidade = [0, 0]
aceleracao = [0, 0.1]

# Loop principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Atualizar posição e velocidade do objeto
    velocidade[0] += aceleracao[0]
    velocidade[1] += aceleracao[1]
    posicao[0] += velocidade[0]
    posicao[1] += velocidade[1]

    # Limpar a tela
    tela.fill(branco)

    # Desenhar o objeto
    pygame.draw.circle(tela, preto, (int(posicao[0]), int(posicao[1])), 20)

    # Atualizar a tela
    pygame.display.flip()

    # Limitar a taxa de atualização
    pygame.time.Clock().tick(60)

import cv2
import numpy as np
from pygame.locals import *

# Inicializa o Pygame
pygame.init()

# Configurações da janela do Pygame
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Interagindo com objetos virtuais')

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Variáveis da bola
ball_radius = 20
ball_pos = [width // 2, height // 2]
ball_speed = [0, 0]

# Inicializa a câmera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Inverte a imagem horizontalmente

    # Desenha a bola na posição atual
    pygame.draw.circle(screen, RED, ball_pos, ball_radius)

    # Mostra a tela do Pygame
    pygame.display.flip()
    screen.fill(WHITE)

    # Captura a posição da mão usando a câmera
    # A lógica para rastrear a mão e controlar a bola deve ser adicionada aqui
    # Isso envolve a detecção da mão na imagem capturada pela câmera

    # Eventos do Pygame
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            cap.release()
            cv2.destroyAllWindows()
            exit()

    # Atualiza a posição da bola com base na posição da mão
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Limita a bola dentro dos limites da tela
    if ball_pos[0] > width - ball_radius or ball_pos[0] < ball_radius:
        ball_speed[0] = -ball_speed[0]
    if ball_pos[1] > height - ball_radius or ball_pos[1] < ball_radius:
        ball_speed[1] = -ball_speed[1]

import cv2
import mediapipe as mp


pygame.init()

largura_tela, altura_tela = 800, 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Simulação Física em Python")

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
LIMITE_CEU_COR = (0, 0, 255)
posicao = [largura_tela // 2, 50]
velocidade = [0, 0]
aceleracao = [0, 0.2]
resistencia_ar = 0.02
amortecimento = 0.9

CHAO_ALTURA = 20
CHAO_COR = (0, 255, 0)
RAIO_OBJETO = 20

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

estado_mao_aberta = False

def track_hand_state():
    global clicando_no_objeto, estado_mao_aberta

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    _, frame = cap.read()
    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        x, y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * largura_tela), int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * altura_tela)

        estado_mao_aberta = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y

        if estado_mao_aberta:
            posicao[0], posicao[1] = x, y
            velocidade[0] = 0  # Defina a velocidade horizontal para zero (a bola não se move horizontalmente)
        else:
            # Se a mão estiver fechada, a bola deve cair
            update_position()

    draw_on_screen()

def update_position():
    global posicao, velocidade
    velocidade[0] += aceleracao[0]
    velocidade[1] += aceleracao[1]
    velocidade[0] *= (1 - resistencia_ar)
    velocidade[1] *= (1 - resistencia_ar)
    posicao[0] += int(velocidade[0])
    posicao[1] += int(velocidade[1])
    check_collisions()

def check_collisions():
    global posicao, velocidade
    if posicao[1] >= altura_tela - CHAO_ALTURA - RAIO_OBJETO:
        posicao[1] = altura_tela - CHAO_ALTURA - RAIO_OBJETO
        velocidade[1] = -velocidade[1] * amortecimento
    if posicao[1] < RAIO_OBJETO:
        posicao[1] = RAIO_OBJETO
        velocidade[1] = -velocidade[1] * amortecimento
    if posicao[0] >= largura_tela - RAIO_OBJETO:
        posicao[0] = largura_tela - RAIO_OBJETO
        velocidade[0] = -velocidade[0] * amortecimento
    if posicao[0] < RAIO_OBJETO:
        posicao[0] = RAIO_OBJETO
        velocidade[0] = -velocidade[0] * amortecimento

def draw_on_screen():
    tela.fill(BRANCO)
    pygame.draw.circle(tela, PRETO, (int(posicao[0]), int(posicao[1])), RAIO_OBJETO)
    pygame.draw.rect(tela, CHAO_COR, (0, altura_tela - CHAO_ALTURA, largura_tela, CHAO_ALTURA))
    pygame.draw.rect(tela, LIMITE_CEU_COR, (0, 0, largura_tela, 1))
    pygame.display.flip()

clicando_no_objeto = False
while True:
    track_hand_state()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
