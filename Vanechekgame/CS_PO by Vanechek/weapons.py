class Weapon:
    def __init__(self, price, type, scoped, isauto, damage, firerate, mag, speed_decrease):
        self.price = price
        self.type = type
        self.scoped = scoped
        self.isauto = isauto
        self.damage = damage
        self.firerate = firerate
        self.mag = mag
        self.speed_decrease = speed_decrease
        self.accuracy = int(100/(damage*firerate))


Glock17 = Weapon(200, "Пистолет", False, False, 19, 2, 17, 10)
mp5 = Weapon(1250, "Пистолет пулемёт", False, True, 21, 6, 25, 22)
akm = Weapon(3300, 'Штурмовая винтовка', False, True, 45, 4, 30, 30)

