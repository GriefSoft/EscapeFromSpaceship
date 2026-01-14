import pygame
import sys
import sqlite3
import pgzrun as pg

"""Задачи:
    
            Перенос текста +- сколько то пикселей
    2) Перелопатить код
    3) Добавить циферблат для ввода пароля и открытие двери
"""


class Cat:
    def __init__(self, sprite_sheet_path, frame_count=7, scale=0.3, x = 640, y = 448):
        # Загружаем спрайт-лист
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        # Размер одного кадра
        self.frame_width = self.sprite_sheet.get_width() // frame_count
        self.frame_height = self.sprite_sheet.get_height()

        # Масштабируем размер кадра
        self.scaled_width = int(self.frame_width * scale)
        self.scaled_height = int(self.frame_height * scale)
        # Создаем список кадров для анимации влево
        self.frames_left = []
        for i in range(frame_count):
            frame = self.sprite_sheet.subsurface(
                pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height))

            # Масштабируем кадр
            scaled_frame = pygame.transform.scale(frame, (self.scaled_width, self.scaled_height))
            self.frames_left.append(scaled_frame)

            # Создаем кадры для движения вправо
            self.frames_right = [pygame.transform.flip(frame, True, False) for frame in self.frames_left]

            # Текущие кадры для отображения
            self.current_frames = self.frames_left

            # Начальная позиция кота
            #self.x = 1280 // 2 - self.scaled_width // 2
            #self.y = 896 // 2 - self.scaled_height // 2
            self.x = x
            self.y = y

            # Настройки анимации
            self.frame_count = frame_count
            self.current_frame = 0
            self.animation_speed = 0.2
            self.animation_counter = 0
            self.speed = 5

            # Направление движения
            self.direction = "left"
            self.is_moving = False

            # Границы движения
            self.boundary_left = 0
            self.boundary_right = 1280 - self.scaled_width
            self.boundary_top = 0
            self.boundary_bottom = 896 - self.scaled_height

            # Rect для коллизий
            self.rect = pygame.Rect(self.x, self.y, self.scaled_width, self.scaled_height)


    def update(self, keys):
        # Обработка движения
        dx, dy = 0, 0
        self.is_moving = False
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.speed
            self.direction = "left"
            self.current_frames = self.frames_left
            self.is_moving = True

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.speed
            self.direction = "right"
            self.current_frames = self.frames_right
            self.is_moving = True

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.speed
            self.direction = "up"
            self.is_moving = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.speed
            self.direction = "down"
            self.is_moving = True

        # Обновляем позицию
        new_x = self.x + dx
        new_y = self.y + dy

        # Проверяем границы
        if self.boundary_left <= new_x <= self.boundary_right:
            self.x = new_x
        else:
            if new_x < self.boundary_left:
                self.x = self.boundary_left
            elif new_x > self.boundary_right:
                self.x = self.boundary_right

        if self.boundary_top <= new_y <= self.boundary_bottom:
            self.y = new_y
        else:
            if new_y < self.boundary_top:
                self.y = self.boundary_top
            elif new_y > self.boundary_bottom:
                self.y = self.boundary_bottom

        # Обновляем анимацию, если кот движется
        if self.is_moving:
            self.animation_counter += self.animation_speed
            if self.animation_counter >= 1:
                self.current_frame = (self.current_frame + 1) % self.frame_count
                self.animation_counter = 0

                # Обновляем Rect для коллизий
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        # Отображаем текущий кадр
        current_image = self.current_frames[self.current_frame]
        screen.blit(current_image, (self.x, self.y))


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

def DrawDBText(font, color, result, roll = 0):
    for i, line in enumerate(result):
        s = ""
        for x, text in enumerate(line):
            #s += text + "  "
            i -= roll
            if i <= 20 and i >= 0:
                DrawText(font, color, str(text), i, x)

pygame.init()

clock = pygame.time.Clock()
Max_FPS = 60

# Всевозможные обьекты игры
screen = pygame.display.set_mode((1280, 896))

pygame.display.set_caption("Escape From Spaceship")

font = pygame.font.SysFont("couriernew", 24)

overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
overlay.fill((0, 0, 0, 200))


running = True

loc = 1

while running:

    pcTxtur = None
    pcTxtur_dest = None
    location = None
    button = None
    button_dest = None
    button_rect = None
    cat = None
    doorTriggerRect = None
    pc_rect = None


    swithLoc = False

    if loc == 1:
        '''текстуры'''
        pcTxtur = pygame.image.load("Texture\\PC_Sprite.png")
        pcTxtur = pygame.transform.scale_by(pcTxtur, 0.3)
        pcTxtur_dest = (505, 240)

        location = pygame.image.load("Texture\\loction_lab1.png")
        location = pygame.transform.scale(location, (1280, 896))

        button = pygame.image.load("Texture\\Button_Sprite.png")
        button = pygame.transform.scale_by(button, 0.1)
        button_dest = (1211, 25)
        button_rect = button.get_rect(topleft=button_dest)

        cat = Cat("Texture\\Cat_Sheet.png", frame_count=7, scale=0.3)

        doorTriggerRect = pygame.Rect(1123, 537, 100, 100) #(964, 528)
        # Создаем Rect для монитора
        pc_rect = pcTxtur.get_rect(topleft=pcTxtur_dest)

    elif loc == 2:
        location = pygame.image.load("Texture\\loction_lab2.png")
        location = pygame.transform.scale(location, (1280, 896))
        cat = Cat("Texture\\Cat_Sheet.png", frame_count=7, scale=0.3, x=52, y=851)
        doorTriggerRect = pygame.Rect(2939, 2457, 40, 100)

    ########
    # Флаг для отслеживания состояния монитора
    monitor_opened = False
    # Масштабированная версия для полного экрана
    pc_fullscreen = None



    """SELECT 
    	f.title, g.title 
    FROM films f 
    JOIN genres g ON f.genre = g.id 
    WHERE g.title IS \"комедия\" AND f.duration >= 60"""

    """SELECT title FROM films
            WHERE title LIKE '%?'"""

    # переменные
    SQL_query = f"""SELECT 
    	f.title, g.title 
    FROM films f 
    JOIN genres g ON f.genre = g.id 
    WHERE g.title IS \"комедия\" AND f.duration >= 60"""

    SQL_result = []
    roll = 0

    while running and not swithLoc:

        '''Отрисовка всего'''
        screen.blit(location, (0, 0))

        cat.draw(screen)

        '''Отрисовка открытого и закрытого ПК'''
        if pcTxtur is not None:
            if not monitor_opened:
                # Отрисовываем обычный монитор
                screen.blit(pcTxtur, pcTxtur_dest)
            else:
                screen.blit(overlay, (0, 0))
                # Отрисовываем монитор на весь экран
                screen.blit(pc_fullscreen, (0, 0))
                screen.blit(button, button_dest)
                # отрисовка текста
                if len(SQL_result) == 0:  # Не робит!
                    DrawText(font, (157, 164, 171), SQL_query)
                else:
                    DrawDBText(font, (157, 164, 171), SQL_result, roll)



        pygame.display.update()

        '''логика игры'''

        #(1236, 620)

        if doorTriggerRect.collidepoint(cat.x, cat.y):
            swithLoc = True
            loc = 2
            print("Yes")


        keys = pygame.key.get_pressed()

        if not monitor_opened:
            cat.update(keys)
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                #swithLoc = True
                #loc = 2
                # кнопка
                if button_rect.collidepoint(event.pos):
                    SQL_result = ExecuteSQL(SQL_query)

                # Комп
                if pc_rect.collidepoint(event.pos):  # Открываем комп
                    monitor_opened = not monitor_opened

                    if monitor_opened:
                        screen_width, screen_height = screen.get_size()  # окно игры

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
                    roll -= 1
                    print("Колесо вверх")
                elif event.button == 5:  # Колесо вниз
                    roll += 1
                    print("Колесо вниз")

            elif event.type == pygame.KEYDOWN:  # ввод текста
                if monitor_opened:
                    SQL_query = InputText(SQL_query, event)

                    if event.key == pygame.K_ESCAPE:
                        monitor_opened = False
                # eles:
                # управление котом

            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

        clock.tick(Max_FPS)


