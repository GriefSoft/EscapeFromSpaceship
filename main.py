import pygame
import sys
import sqlite3
import pgzrun as pg

"""Задачи:
    
            Перенос текста +- сколько то пикселей
    2) Перелопатить код
    3) Добавить циферблат для ввода пароля и открытие двери
"""


def InputText(current_text, event):
    """Минимальная версия для ввода текста"""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            return current_text[:-1]
        elif event.key == pygame.K_RETURN:
            current_text += '\n'
        elif event.unicode and event.unicode.isprintable():
            current_text += event.unicode
            return current_text
    return current_text


def ExecuteSQL(SQL_query):
    res = []
    con = sqlite3.connect("films_db_.sqlite")
    cr = con.cursor()


    try:
        res = cr.execute(SQL_query).fetchall()
        if len(res) != 0:
            for elm in res:
                print("Elm tupe: ", type(elm), "\t", elm)
            con.close()
            print("Res type:", type(res))
            return res
        con.commit()

    except sqlite3.OperationalError as err:
        res.append(f"Syntaxis err: {err}")
        print(res)
        return res

    except sqlite3.Error as err:
        print("unknown sqlite Err: ", err)

    finally:
        con.close()

def DrawText(font, color, text: str, j = 0, x = 0):
    lines = text.split('\n')
    if x == 0:
        x_dest = 33
    else:
        x_dest = 700*x
    for i, line in enumerate(lines):
        consoleText = font.render(line, False, color)
        screen.blit(consoleText, (x_dest, 33 + (j+i)*font.get_height()))

def DrawTextList(font, color, textList):
    for i, line in enumerate(textList):
        DrawText(font, color, line, i)

def DrawDBText(font, color, result):
    for i, line in enumerate(result):
        s = ""
        for x, text in enumerate(line):
            #s += text + "  "
            DrawText(font, color, text, i, x)

pygame.init()

clock = pygame.time.Clock()
Max_FPS = 60


# Всевозможные обьекты игры
screen = pygame.display.set_mode((1280, 896))

pygame.display.set_caption("Escape From Spaceship")

font = pygame.font.SysFont("couriernew", 24)


########
'''текстуры'''
pcTxtur = pygame.image.load("Texture\\PC_Sprite.png")
pcTxtur = pygame.transform.scale_by(pcTxtur, 0.3)
pcTxtur_dest = (505, 240)

# Создаем Rect для монитора
pc_rect = pcTxtur.get_rect(topleft=pcTxtur_dest)
# Флаг для отслеживания состояния монитора
monitor_opened = False
# Масштабированная версия для полного экрана
pc_fullscreen = None


location = pygame.image.load("Texture\\loction_lab1.png")
location = pygame.transform.scale(location, (1280, 896))


button = pygame.image.load("Texture\\Button_Sprite.png")
button = pygame.transform.scale_by(button, 0.1)
button_dest = (1211, 25)
button_rect = button.get_rect(topleft=button_dest)

overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
overlay.fill((0,0,0,200))


"""SELECT 
	f.title, g.title 
FROM films f 
JOIN genres g ON f.genre = g.id 
WHERE g.title IS \"комедия\" AND f.duration >= 60"""


"""SELECT title FROM films
        WHERE title LIKE '%?'"""

#переменные
SQL_query = f"""SELECT 
	f.title, g.title 
FROM films f 
JOIN genres g ON f.genre = g.id 
WHERE g.title IS \"комедия\" AND f.duration >= 60"""

SQL_result = []


running = True
while running:


    '''Отрисовка всего'''
    '''Отрисовка открытого и закрытого ПК'''
    screen.blit(location, (0,0))
    if not monitor_opened:
        # Отрисовываем обычный монитор
        screen.blit(pcTxtur, pcTxtur_dest)
    else:
        screen.blit(overlay, (0, 0))
        # Отрисовываем монитор на весь экран
        screen.blit(pc_fullscreen, (0, 0))
        screen.blit(button, button_dest)
        # отрисовка текста
        if len(SQL_result) == 0: #Не робит!
            DrawText(font, (157, 164, 171), SQL_query)
        else:
            DrawDBText(font, (157, 164, 171), SQL_result)



    pygame.display.update()




    '''логика игры'''
    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:

            #кнопка
            if button_rect.collidepoint(event.pos):
                SQL_result = ExecuteSQL(SQL_query)

            #Комп
            if pc_rect.collidepoint(event.pos):     # Открываем комп
                monitor_opened = not monitor_opened

                if monitor_opened:
                    screen_width, screen_height = screen.get_size() #окно игры

                    print(f"screen_width{screen_width}, screen_height{screen_height}")
                    pc_fullscreen = pygame.transform.scale_by(pcTxtur, 9)

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

        elif event.type == pygame.KEYDOWN:      #ввод текста
            if monitor_opened:
                SQL_query = InputText(SQL_query, event)

                if event.key == pygame.K_ESCAPE:
                    monitor_opened = False
            #eles:
                #управление котом

        if event.type == pygame.QUIT:
            pygame.quit()
            running = False


    clock.tick(Max_FPS)
