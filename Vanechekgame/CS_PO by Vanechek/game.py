import pygame
import random as rd
import time as t

#vanechek rights reserved
# made with          aboba
FPS = 60

reload = False
pos = 'left'
Zposes = ['left', 'right', 'up', 'down']
shootpos = pos
shooted = False
ab = 0
dcount = 0
YELLOW = (225, 225, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
pygame.init()
screen = pygame.display.set_mode((1900, 1050))
clock = pygame.time.Clock()
Zpos = rd.choice(Zposes)
vic = 300
wave = 1
rltrn = 0
wave_done = 0

surf = pygame.Surface((400, 10))
sr = surf.get_rect()
surf.fill(YELLOW)
surf.set_alpha(0)


def txt1_():
    global reload
    global fullammo
    global ammo
    fnt = pygame.font.Font(None, 50)
    if reload:
        txz = 'Перезарядка...'
        txt1 = fnt.render(str(txz), True, RED)
    if fullammo < 0 and ammo < 0:
        txz = 'Патроны закончились'
        txt1 = fnt.render(str(txz), True, RED)
    else:
        txz = ' ' + str(ammo) + ' патронов, всего ' + str(fullammo)
        txt1 = fnt.render(str(txz), True, RED)
    screen.blit(txt1, [50, 950])


def txtL_():
    fnt = pygame.font.Font(None, 150)
    txz = 'ВЫ УМЕРЛИ'
    txt1 = fnt.render(str(txz), True, RED)
    screen.blit(txt1, [900, 450])


def txtHP_():
    fnt = pygame.font.Font(None, 50)
    txz = 'Здровье персонажа:' + str(int(player.health))
    txt5 = fnt.render(str(txz), True, RED)
    screen.blit(txt5, [1300, 950])


def txtCW_():
    fnt = pygame.font.Font(None, 50)
    txz = 'Текущее оружие:' + current_weapon.name
    txt5 = fnt.render(str(txz), True, RED)
    screen.blit(txt5, [800, 950])


def txt2_():
    global vic
    global wave
    fnt = pygame.font.Font(None, 50)
    txz = ' ' + str(vic) + ' Здрорвья у базы, волна ' + str(wave)
    txt2 = fnt.render(str(txz), True, BLACK)
    screen.blit(txt2, [1300, 50])


def wait(sec):
    t.sleep(sec)


def rint(a, b):
    rd.randint(a, b)
    return a, b


img1 = pygame.image.load('playerMAIN_rightS.png')
imgB = pygame.image.load('Bullet1.png')


class Weapon:
    def __init__(self, image, price, type, scoped, isauto, damage, firerate, mag, speed_decrease, name):
        self.image = image
        self.price = price
        self.type = type
        self.scoped = scoped
        self.isauto = isauto
        self.damage = damage
        self.firerate = firerate
        self.mag = mag
        self.speed_decrease = speed_decrease
        self.name = name
        self.accuracy = float(damage * firerate / 90)


class showW(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = current_weapon.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = imgB
        self.rect = sr
        self.rect.x = player.rect.x + 55
        self.rect.y = player.rect.y + 150
        self.speed = current_weapon.firerate
        self.isflying = False

    def update(self):
        global pos
        if pos == 'down':
            shootpos = 'down'
            self.isflying = True


class Maps(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Zombie(pygame.sprite.Sprite):
    def __init__(self, image, x, y, turn):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.turn = turn
        self.health = rd.randint(50, 150)
        self.attack = rd.randint(10, 50)
        self.drop = rd.randint(0, 3)
        self.dead = False

    def R_move(self):
        global vic
        global wave_done
        global wave
        global dcount

        if self.health <= 0:
            self.dead = True
        if self.dead:
            if self.turn == 230:
                dcount += 1
            self.image = pygame.image.load('Zombie_Dead.png')
            self.turn += 1
            if self.turn == 250:
                self.dead = False
                self.turn = 0
                self.rect.x = 0
                self.health = rd.randint(50, 150)
        if vic >= 1 and wave_done != 1:
            if not self.dead:
                if self.rect.x < 1900:
                    self.rect.x += rd.randint(1, 5)
                    self.image = pygame.image.load('Zombie_Right.png')
                if self.rect.x >= 1830:
                    vic -= self.attack
                    self.dead = True

        else:
            pass


class Drop(pygame.sprite.Sprite):
    def __init__(self, x, y, turn):
        super().__init__()
        self.image = pygame.image.load('ammo1.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.turn = turn
        self.collision = False
        self.isdropped = False

    def dropper(self):
        global fullammo
        print(self.turn)
        self.turn += 1
        if self.turn == 1:
            fullammo += int(current_weapon.mag / 2)
            pygame.mixer.music.load('dropS.mp3')
            pygame.mixer.music.play()
            self.rect.x = -100
            self.rect.y = -100


class Playerr(pygame.sprite.Sprite):

    def __init__(self, x, y, image, speed, health):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.health = health

    def update(self):
        global reload
        global pos
        global shootpos
        global ammo
        global rltrn
        global fullammo
        global shooted

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            pos = 'left'
            shootpos = 'left'
            if current_weapon.type == 'Пистолет':
                self.image = pygame.image.load('playerSEC_leftS.png')
            else:
                self.image = pygame.image.load('playerMAIN_leftS.png')
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            pos = 'right'
            shootpos = 'right'
            if current_weapon.type == 'Пистолет':
                self.image = pygame.image.load('playerSEC_rightS.png')
            else:
                self.image = pygame.image.load('playerMAIN_rightS.png')
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            pos = 'up'
            shootpos = 'up'
            if current_weapon.type == 'Пистолет':
                self.image = pygame.image.load('playerSEC_upS.png')
            else:
                self.image = pygame.image.load('playerMAIN_upS.png')
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            pos = 'down'
            shootpos = 'down'
            if current_weapon.type == 'Пистолет':
                self.image = pygame.image.load('playerSEC_downS.png')
            else:
                self.image = pygame.image.load('playerMAIN_downS.png')
            self.rect.y += self.speed

        if keys[pygame.K_q] and pos == 'right':
            self.rect.y -= self.speed

        if keys[pygame.K_e] and pos == 'right':
            self.rect.y += self.speed

        if keys[pygame.K_q] and pos == 'left':
            self.rect.y -= self.speed

        if keys[pygame.K_e] and pos == 'left':
            self.rect.y += self.speed

        if keys[pygame.K_q] and pos == 'up':
            self.rect.x -= self.speed

        if keys[pygame.K_e] and pos == 'up':
            self.rect.x += self.speed

        if keys[pygame.K_q] and pos == 'down':
            self.rect.x -= self.speed

        if keys[pygame.K_e] and pos == 'down':
            self.rect.x += self.speed

        if keys[pygame.K_LSHIFT]:
            if not reload:
                if ammo <= 0:
                    print('empty')
                else:
                    if shooted == True:
                        pass
                    else:
                        if current_weapon.type == 'Штурмовая винтовка':
                            pygame.mixer.music.load('gunshot1.mp3')
                            pygame.mixer.music.play()
                        if current_weapon.type == 'Снайперская винтовка':
                            pygame.mixer.music.load('sniper.mp3')
                            pygame.mixer.music.play()
                        if current_weapon.type == 'Пистолет':
                            pygame.mixer.music.load('pistol.mp3')
                            pygame.mixer.music.play()
                        if current_weapon.type == 'Пистолет пулемёт':
                            pygame.mixer.music.load('smg.mp3')
                            pygame.mixer.music.play()
                        print(ammo)
                        ammo -= 1
                        bullet.isflying = True
                        shooted = True

        if keys[pygame.K_r]:
            if fullammo > 0:
                if rltrn <= 100:
                    reload = True
                    pygame.mixer.music.load('reloadd.mp3')
                    pygame.mixer.music.play()
                    if ammo == current_weapon.mag:
                        print('reload')
                        fh = current_weapon.mag - ammo
                        ammo = current_weapon.mag + 1
                        fullammo -= fh
                        print(ammo)
                    elif 0 < ammo < current_weapon.mag:
                        print('reload')
                        fh = current_weapon.mag - ammo
                        ammo = current_weapon.mag + 1
                        fullammo -= fh
                        print(ammo)
                    elif ammo <= 0:
                        print('reload')
                        fh = current_weapon.mag - ammo
                        ammo = current_weapon.mag
                        fullammo -= fh
                        print(ammo)
                    elif ammo > current_weapon.mag:
                        print('can`t reload')
                if rltrn > 100:
                    rltrn = 0
                    reload = False
            else:
                print('Нет патрон')


player = Playerr(700, 350, img1, 20, 100)

Glock17 = Weapon(pygame.image.load('Pistol_deco.png'), 200, "Пистолет", False, False, 7, 2, 17, 10, 'Глок 17')
Glock18C = Weapon(pygame.image.load('Pistol_deco.png'), 700, 'Пистолет', False, True, 7, 8, 17, 10, 'Глок 18')
Beretta = Weapon(pygame.image.load('Pistol_deco.png'), 500, 'Пистолет', False, False, 8, 2, 12, 12, 'Беретта')

mp5 = Weapon(pygame.image.load('SMG_deco.png'), 1250, "Пистолет пулемёт", False, True, 21, 9, 25, 22, 'Мп-5')
mp9_sil = Weapon(pygame.image.load('SMG_deco.png'), 1300, 'Пистолет пулемёт', False, True, 15, 10, 20, 15,
                 'Мп-9 с глушителем')
p90 = Weapon(pygame.image.load('SMG_deco.png'), 1750, 'Пистолет пулемёт', False, True, 23, 13, 50, 20, 'П-90')

FN_FNC = Weapon(pygame.image.load('AR_decor.png'), 3000, 'Штурмовая винтовка', False, True, 31, 8, 30, 27, 'ФН Фал')
akm = Weapon(pygame.image.load('AR_decor.png'), 3300, 'Штурмовая винтовка', False, True, 45, 7, 30, 30, 'АК-47')
m4 = Weapon(pygame.image.load('AR_decor.png'), 3500, 'Штурмовая винтовка', False, True, 30, 9, 30, 28, 'М4')
# m4_Acog = Weapon(pygame.image.load('AR_decor.png'), 3650, 'Штурмовая винтовка', True, True, 30, 9, 30, 29, '')
m4_silencer = Weapon(pygame.image.load('AR_decor.png'), 3450, 'Штурмовая винтовка', False, True, 24, 11, 30, 29,
                     'М4 с глушителем')
ak74 = Weapon(pygame.image.load('AR_decor.png'), 3250, 'Штурмовая винтовка', False, True, 34, 8, 30, 28, 'Ак-74')
Famas = Weapon(pygame.image.load('AR_decor.png'), 3750, 'Штурмовая винтовка', False, True, 28, 10, 25, 25, 'Фамас')

SVD = Weapon(pygame.image.load('Sniper_deco.png'), 4250, 'Снайперская винтовка', True, True, 67, 5, 10, 39, 'СВД')
# Auto_XT = Weapon(pygame.image.load('Sniper_deco.png'), 7000, 'Секрет', True, True, 105, 60, 20000, 50)
AWM = Weapon(pygame.image.load('Sniper_deco.png'), 4800, "Снайперская винтовка", True, False, 130, 0.5, 5, 50, 'АВП')
weapons = [Glock17, Glock18C, Beretta, mp5, mp9_sil, p90, FN_FNC, akm, m4, m4_silencer, ak74, Famas, SVD, AWM]

current_weapon = akm
ammo = current_weapon.mag
fullammo = current_weapon.mag * 4
bullet = Bullet(pygame.draw.rect(screen, YELLOW, (player.rect.y, player.rect.y, 1, 1)), 0, 0)
start_x = 0
start_y = rd.randint(100, 500)
start_x1 = 0
start_y1 = rd.randint(100, 500)
start_y2 = rd.randint(100, 500)
start_y3 = rd.randint(100, 500)
zombies = pygame.sprite.Group()

wp = showW(550, 850)
dic = {}
for i in range(wave):
    dic["zombie" + str(i)] = Zombie(pygame.image.load('Zombie_Up.png'), start_x, rd.randint(100, 500), 0)

map1 = Maps(pygame.image.load('map_ZombieStrelyalka1.png'), 0, 0)


def zombies_iteration():
    for z in range(len(dic)):
        dic["zombie" + str(z)].R_move()


mode = 'game'
jx = 0
xm = 0
fx = 0
drop_all = 0
drop_possible = wave
runnin = True
while runnin:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runnin = not runnin
    # 0_o
    if mode == 'game':
        if wave % 2 == 0:
            fx += 1
            if fx == 2:
                print(current_weapon.name)
                current_weapon = rd.choice(weapons)
                wp.image = current_weapon.image
                ammo = current_weapon.mag
                print(current_weapon.name)
        else:
            fx = 0
        screen.fill(BLACK)
        drop_possible = wave
        screen.blit(map1.image, (map1.rect.x, map1.rect.y))
        if player.health <= 0:
            print('Поражение')
            mode = 'lost'

        if wave_done == 1:
            xm = 0
            print(wave)
            print(wave_done)
            print(dcount)
            wave += 1
            dic = {}
            for i in range(wave):
                dic["zombie" + str(i)] = Zombie(pygame.image.load('Zombie_Up.png'), start_x, rd.randint(100, 500), 0)
            wave_done = 0
        txt1_()
        screen.blit(wp.image, (wp.rect.x, wp.rect.y))
        txt2_()
        txtHP_()
        txtCW_()
        screen.blit(player.image, (player.rect.x, player.rect.y))
        if dcount == wave * 2:
            wave_done = 1
            dcount = 0
        for i in range(len(dic)):
            xm += 1
            if xm == 1:
                pygame.mixer.music.load('spawn.mp3')
                pygame.mixer.music.play()
            fd = dic["zombie" + str(i)]
            screen.blit(fd.image, (fd.rect.x, fd.rect.y))

        screen.blit(surf, (bullet.rect.x, bullet.rect.y))

        player.update()
        # стрельба
        if reload and rltrn <= 100:
            rltrn += 1
        else:
            reload = False
            rltrn = 0
        if bullet.isflying == True:
            if 1000 > bullet.rect.y > -1000 and 2000 > bullet.rect.x > -2000:
                screen.blit(bullet.image, (bullet.rect.x, bullet.rect.y))
                if shootpos == 'down':
                    bullet.rect.y += current_weapon.firerate * rd.randint(28, 32)
                elif shootpos == 'up':
                    bullet.rect.y -= current_weapon.firerate * rd.randint(28, 32)
                elif shootpos == 'right':
                    bullet.rect.x += current_weapon.firerate * rd.randint(58, 62)
                elif shootpos == 'left':
                    bullet.rect.x -= current_weapon.firerate * rd.randint(58, 62)
            else:
                bullet.isflying = False
                # print('end')
        else:
            if shootpos == 'down':
                bullet.rect.y = player.rect.y + 180
                bullet.rect.x = player.rect.x + 50
            elif shootpos == 'up':
                bullet.rect.y = player.rect.y + 10
                bullet.rect.x = player.rect.x + 42
            elif shootpos == 'right':
                bullet.rect.y = player.rect.y + 80
                bullet.rect.x = player.rect.x + 180
            elif shootpos == 'left':
                bullet.rect.y = player.rect.y + 55
                bullet.rect.x = player.rect.x
            shooted = False
        # Зомбари
        zombies_iteration()
        for i in range(len(dic)):
            xa = dic["zombie" + str(i)]
            if pygame.sprite.collide_rect(bullet, xa):
                xa.health -= current_weapon.damage
            if xa.dead:
                if xa.drop == 0:
                    drop = Drop(xa.rect.x, xa.rect.y, 0)
                    drop.isdropped = True
                    if drop.isdropped:
                        screen.blit(drop.image, (xa.rect.x + 70, xa.rect.y + 40))
                    if pygame.sprite.collide_rect(player, drop):
                        drop_all += 1
                        if drop.turn < 3:
                            drop.dropper()
                            drop.isdropped = False
                            drop.turn += 1
                            drop_possible += 1
                            del drop
                        else:
                            pass
                    else:
                        drop_all = 0
            else:
                drop_possible = 0

        for i in range(len(dic)):
            xb = dic["zombie" + str(i)]
            if pygame.sprite.collide_rect(player, xb):
                if not xb.dead:
                    player.health -= xb.attack / 10
                    jx += 1
                    if jx == 3:
                        pygame.mixer.music.load('blizh.mp3')
                        pygame.mixer.music.play()
            else:
                jx = 0

            # print(str(zombie.rect.x) + 's' + str(zombie.rect.y))
        pygame.display.flip()
        clock.tick(FPS)
    elif mode == 'lost':
        jx += 1
        screen.blit(map1.image, (map1.rect.x, map1.rect.y))
        txtL_()
        if jx == 3:
            pygame.mixer.music.load('spawn.mp3')
            pygame.mixer.music.play()
        if jx == 75:
            pygame.mixer.music.load('dead.mp3')
            pygame.mixer.music.play()
        pygame.display.flip()
        clock.tick(FPS)

print('End')
