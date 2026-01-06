import pygame
import sys
import sqlite3
import pgzrun as pg

"""Задачи:
    1) Исправить проблемы с табуляцией и переносом строк
    2) Перелопатить код
    3) Добавить циферблат для ввода пароля и открытие двери
"""


def handle_text_input_simple(current_text, event):
    """Минимальная версия для ввода текста"""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            return current_text[:-1]

        elif event.unicode and event.unicode.isprintable():
            current_text += event.unicode
            return current_text

    #return current_text


def ExecuteSQL(SQL_query):
    print("1111111111111111111111111111111")
    con = sqlite3.connect("films_db_.sqlite")
    cr = con.cursor()

    res = cr.execute(SQL_query).fetchall()

    for elm in res:
        print(elm)



    con.close()






pygame.init()

clock = pygame.time.Clock()
Max_FPS = 60


# Всевозможные обьекты игры
screen = pygame.display.set_mode((1280, 896))
pygame.display.set_caption("Escape From Spaceship")

consoleFont = pygame.font.SysFont("couriernew", 24)

########

pcTxtur = pygame.image.load("Texture\\Screen.png")
pcTxtur = pygame.transform.scale_by(pcTxtur, 0.5)
pcTxtur_dest = (50, 260)
# Создаем Rect для кнопки монитора
pc_rect = pcTxtur.get_rect(topleft=pcTxtur_dest)
# Флаг для отслеживания состояния монитора
monitor_opened = False
# Масштабированная версия для полного экрана
pc_fullscreen = None


location = pygame.image.load("Texture\\Location1.jpg")
button = pygame.image.load("Texture\\b-icon.jpg")
button = pygame.transform.scale_by(button, 0.1)
button_dest = (750, 450)
button_rect = button.get_rect(topleft=button_dest)


SQL_query = "12345\t6789"


running = True
while running:


    consoleText = consoleFont.render(SQL_query, False, (157, 164, 171))

    screen.blit(location, (0,0))
    if not monitor_opened:
        # Отрисовываем обычный монитор
        screen.blit(pcTxtur, pcTxtur_dest)
    else:
        # Отрисовываем монитор на весь экран
        screen.blit(pc_fullscreen, (0, 0))
        screen.blit(button, button_dest)
        # отрисовка текста
        screen.blit(consoleText, (420, 220))









    pygame.display.update()

    for event in pygame.event.get():



        if event.type == pygame.MOUSEBUTTONDOWN:

            if button_rect.collidepoint(event.pos):
                ExecuteSQL(SQL_query)


            if pc_rect.collidepoint(event.pos):     # Открываем комп
                monitor_opened = not monitor_opened

                if monitor_opened:
                    screen_width, screen_height = screen.get_size()
                    pc_fullscreen = pygame.transform.scale(pcTxtur, (screen_width, screen_height))

            print(f"Нажата кнопка: {event.button}")  # 1-левая, 3-правая, 2-средняя
            print(f"Позиция: {event.pos}")  # (x, y)

            # Проверка конкретных кнопок:
            if event.button == 1:  # Левая кнопка
                print("ЛКМ нажата")

            elif event.button == 3:  # Правая кнопка
                print("ПКМ нажата")
            elif event.button == 4:  # Колесо вверх
                print("Колесо вверх")
            elif event.button == 5:  # Колесо вниз
                print("Колесо вниз")

        elif event.type == pygame.KEYDOWN:
            SQL_query = handle_text_input_simple(SQL_query, event)

            if event.key == pygame.K_ESCAPE and monitor_opened:
                monitor_opened = False


        if event.type == pygame.QUIT:
            pygame.quit()
            running = False




        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                screen.fill((228,228,228))
    clock.tick(Max_FPS)




#def PC_Enabled():


