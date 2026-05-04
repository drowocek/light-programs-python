import os
import random

# ============================================================
#  КЛАССЫ
# ============================================================

class Camino:
    def __init__(self, name):
        self.name = name
    def info(self):
        return f"прошел 5 км,\nпо {self.name}\n"

class Tiempo(Camino):
    def __init__(self, name, attak_debuff=0, speed_debuff=0):
        self.name = name
        self.attak_debuff = attak_debuff
        self.speed_debuff = speed_debuff
    def info(self):
        efecto = ""
        if self.attak_debuff: efecto += f" | атака -{self.attak_debuff}"
        if self.speed_debuff: efecto += f" | скорость -{self.speed_debuff}"
        return f"Погода: {self.name}{efecto}"

class Gumanoid:
    def __init__(self, name, attak, healf, speed):
        self.name  = name
        self.attak = attak
        self.healf = healf
        self.speed = speed

class Monsters(Gumanoid):
    def info(self):
        return f"{self.name}\nатака: {self.attak}\nздоровье: {self.healf}\nскорость: {self.speed}"
    def atak(self, other, debuff=0):
        dmg = max(1, self.attak - debuff)
        other.healf -= dmg
        return f"{self.name} атакует {other.name}! здоровье {other.name}: {other.healf}"

# ============================================================
#  ПРЕДМЕТЫ
# ============================================================

RARITY = {
    "обычный":    {"color": "",     "bonus": 1.0},
    "редкий":     {"color": "🔵",   "bonus": 1.3},
    "магический": {"color": "🟣",   "bonus": 1.6},
    "легендарный":{"color": "🟡",   "bonus": 2.0},
}

class Weapon:
    def __init__(self, name, attak_bonus, speed_bonus, rarity, price, emoji="⚔️"):
        self.name        = name
        self.attak_bonus = attak_bonus
        self.speed_bonus = speed_bonus
        self.rarity      = rarity
        self.price       = price
        self.emoji       = emoji
        mult = RARITY[rarity]["bonus"]
        self.attak_bonus = int(attak_bonus * mult)
        self.speed_bonus = int(speed_bonus * mult)
    def info(self):
        icon = RARITY[self.rarity]["color"]
        return (f"{self.emoji} {icon}{self.name} [{self.rarity}]\n"
                f"   атака +{self.attak_bonus} | скорость +{self.speed_bonus} | цена: {self.price}g")

class Armor:
    def __init__(self, name, defense, healf_bonus, rarity, price, slot, emoji="🛡️"):
        self.name       = name
        self.defense    = defense
        self.healf_bonus= healf_bonus
        self.rarity     = rarity
        self.price      = price
        self.slot       = slot   # helmet / chest / boots
        self.emoji      = emoji
        mult = RARITY[rarity]["bonus"]
        self.defense     = int(defense     * mult)
        self.healf_bonus = int(healf_bonus * mult)
    def info(self):
        icon = RARITY[self.rarity]["color"]
        return (f"{self.emoji} {icon}{self.name} [{self.rarity}] [{self.slot}]\n"
                f"   защита +{self.defense} | здоровье +{self.healf_bonus} | цена: {self.price}g")

class Consumable:
    def __init__(self, name, heal, price, emoji="🧪"):
        self.name  = name
        self.heal  = heal
        self.price = price
        self.emoji = emoji
    def info(self):
        return f"{self.emoji} {self.name} | восстанавливает {self.heal} hp | цена: {self.price}g"

class Bomb:
    def __init__(self, name, damage, price, emoji="💣"):
        self.name   = name
        self.damage = damage
        self.price  = price
        self.emoji  = emoji
    def info(self):
        return f"{self.emoji} {self.name} | урон {self.damage} | цена: {self.price}g"

# ============================================================
#  HUMAN
# ============================================================

class Human(Gumanoid):
    def __init__(self, name, attak, healf, speed):
        super().__init__(name, attak, healf, speed)
        self.gold      = 0
        self.kills     = 0
        self.steps     = 0
        self.inventory = []          # расходники / бомбы
        self.weapon    = None        # активное оружие (одно или список для пистолет+кинжал)
        self.armor     = {"helmet": None, "chest": None, "boots": None}
        self.base_attak = attak
        self.base_speed = speed
        self.base_healf = healf

    def equip_weapon(self, w):
        # снять старое
        if isinstance(self.weapon, list):
            for old in self.weapon:
                self.attak -= old.attak_bonus
                self.speed -= old.speed_bonus
        elif self.weapon:
            self.attak -= self.weapon.attak_bonus
            self.speed -= self.weapon.speed_bonus
        self.weapon = w
        if isinstance(w, list):
            for nw in w:
                self.attak += nw.attak_bonus
                self.speed += nw.speed_bonus
        else:
            self.attak += w.attak_bonus
            self.speed += w.speed_bonus
        print(f"✅ Экипировано оружие!")

    def equip_armor(self, a):
        old = self.armor[a.slot]
        if old:
            self.healf -= old.healf_bonus
            # снять старую защиту (учитываем в atak)
        self.armor[a.slot] = a
        self.healf += a.healf_bonus
        print(f"✅ Экипирована броня: {a.name}")

    def total_defense(self):
        d = 0
        for a in self.armor.values():
            if a: d += a.defense
        return d
        
    def show_equip(self):
        print("\n⚔️  ЭКИПИРОВКА:")
        # Оружие
        if isinstance(self.weapon, list):
            for w in self.weapon:
                print(f"  {w.info()}")
        elif self.weapon:
            print(f"  {self.weapon.info()}")
        else:
            print("  Оружие: нет")
        # Броня
        slots = {"helmet": "Шлем", "chest": "Нагрудник", "boots": "Сапоги"}
        for slot, label in slots.items():
            a = self.armor[slot]
            if a:
                print(f"  {a.info()}")
            else:
                print(f"  {label}: нет")
        print(f"  Защита итого: {self.total_defense()}")

    def info(self):
        wpn = "нет"
        if isinstance(self.weapon, list):
            wpn = " + ".join(w.name for w in self.weapon)
        elif self.weapon:
            wpn = self.weapon.name
        return (f"{self.name}\nатака: {self.attak}\nздоровье: {self.healf:.0f}\n"
                f"скорость: {self.speed}\nзолото: {self.gold}\nоружие: {wpn}")

    def atak(self, other, debuff=0):
        dmg = max(1, self.attak - debuff)
        other.healf -= dmg
        return f"{self.name} атакует {other.name}! здоровье {other.name}: {other.healf:.0f}"

    def heal(self, amount):
        self.healf += amount
        if self.healf > 150:
            self.healf = 150
        return f"{self.name} восстановил здоровье. Здоровье: {self.healf:.0f}"

    def show_inventory(self):
        if not self.inventory:
            print("  Инвентарь пуст.")
            return
        for i, item in enumerate(self.inventory, 1):
            print(f"  {i}. {item.info()}")

    def use_item(self, idx, target=None):
        if idx < 1 or idx > len(self.inventory):
            print("Неверный номер.")
            return
        item = self.inventory[idx - 1]
        if isinstance(item, Consumable):
            self.heal(item.heal)
            print(f"🧪 Использован {item.name}. +{item.heal} hp. Здоровье: {self.healf:.0f}")
            self.inventory.pop(idx - 1)
        elif isinstance(item, Bomb):
            if target:
                target.healf -= item.damage
                print(f"💣 Брошена {item.name}! Урон {item.damage}. Здоровье {target.name}: {target.healf:.0f}")
                self.inventory.pop(idx - 1)
            else:
                print("Некого взрывать!")
        else:
            print("Этот предмет нельзя использовать так.")

# ============================================================
#  СОКРОВИЩА / МАГАЗИН
# ============================================================

class Treasure:
    def __init__(self, name, gold, item=None):
        self.name = name
        self.gold = gold
        self.item = item   # может содержать предмет
    def info(self):
        txt = f"Найдено: {self.name}! (+{self.gold}g)"
        if self.item:
            txt += f"\n  + предмет: {self.item.name}"
        return txt

class Mud:
    def info(self):
        return "Грязь на дороге! Скорость снижена."

# ============================================================
#  КАТАЛОГ ПРЕДМЕТОВ
# ============================================================

# ОРУЖИЕ — 5 видов × 4 редкости
def make_weapons():
    items = []
    for rarity, price_mult in [("обычный",1),("редкий",2),("магический",3),("легендарный",5)]:
        items += [
            Weapon(f"Меч",           attak_bonus=6, speed_bonus=0, rarity=rarity, price=30*price_mult, emoji="🗡️"),
            Weapon(f"Пистолет",      attak_bonus=8, speed_bonus=1, rarity=rarity, price=40*price_mult, emoji="🔫"),
            Weapon(f"Кинжал",        attak_bonus=4, speed_bonus=3, rarity=rarity, price=25*price_mult, emoji="🔪"),
            Weapon(f"Лук",           attak_bonus=5, speed_bonus=2, rarity=rarity, price=28*price_mult, emoji="🏹"),
            Weapon(f"Боевой топор",  attak_bonus=9, speed_bonus=-1,rarity=rarity, price=45*price_mult, emoji="🪓"),
        ]
    return items

# БРОНЯ — шлем / нагрудник / сапоги × 4 редкости
def make_armors():
    items = []
    for rarity, pm in [("обычный",1),("редкий",2),("магический",3),("легендарный",5)]:
        items += [
            Armor("Шлем",        defense=2, healf_bonus=5,  rarity=rarity, price=20*pm, slot="helmet",  emoji="⛑️"),
            Armor("Нагрудник",   defense=4, healf_bonus=10, rarity=rarity, price=35*pm, slot="chest",   emoji="🦺"),
            Armor("Сапоги",      defense=1, healf_bonus=3,  rarity=rarity, price=15*pm, slot="boots",   emoji="👢"),
        ]
    return items

# РАСХОДНИКИ
potions = [
    Consumable("Малое зелье",   heal=20, price=15),
    Consumable("Среднее зелье", heal=40, price=30),
    Consumable("Большое зелье", heal=70, price=55),
]
bombs = [
    Bomb("Дымовая бомба",  damage=15, price=20),
    Bomb("Огненная бомба", damage=35, price=40),
    Bomb("Магическая бомба",damage=60,price=70),
]

all_weapons = make_weapons()
all_armors  = make_armors()
all_shop_items = all_weapons + all_armors + potions + bombs

# Пистолет + Кинжал вместе (очень редко в сокровищнице)
def pistol_dagger_combo(rarity="редкий"):
    return [
        Weapon("Пистолет", attak_bonus=8, speed_bonus=1, rarity=rarity, price=0, emoji="🔫"),
        Weapon("Кинжал",   attak_bonus=4, speed_bonus=3, rarity=rarity, price=0, emoji="🔪"),
    ]

# Сокровищницы с предметами
def make_treasures():
    return [
        Treasure("Старый кошелёк", 10),
        Treasure("Серебряная монета", 25),
        Treasure("Золотой слиток", 50),
        Treasure("Сундук с золотом", 100),
        Treasure("Тайник путника", 20, item=random.choice(potions)),
        Treasure("Оружейный ящик", 10, item=random.choice(all_weapons[:5])),
        Treasure("Броня павшего", 15, item=random.choice(all_armors[:3])),
        Treasure("Бомбы!", 5, item=random.choice(bombs)),
        Treasure("Легендарный сундук", 200, item=random.choice(all_weapons[-5:])),
    ]

# ============================================================
#  МАГАЗИН
# ============================================================

def show_shop(woin):
    shop = random.sample(all_shop_items, 8)  # 8 случайных товаров
    print("\n" + "="*45)
    print("        🏪  МАГАЗИН")
    print(f"  Золото: {woin.gold}g")
    print("="*45)
    for i, item in enumerate(shop, 1):
        print(f"  {i}. {item.info()}")
    print("  0. Выйти")
    print("="*45)

    while True:
        if input("Посмотреть экипировку? [д/н]: ").strip().lower() == "д":
            woin.show_equip()
        choice = input("Купить (номер) или 0 выйти: ").strip()
        if choice == "0":
            break
        if not choice.isdigit():
            continue
        idx = int(choice) - 1
        if idx < 0 or idx >= len(shop):
            continue
        item = shop[idx]
        if woin.gold < item.price:
            print(f"❌ Недостаточно золота! Нужно {item.price}g, у вас {woin.gold}g")
            continue
        woin.gold -= item.price
        if isinstance(item, Weapon):
            woin.equip_weapon(item)
        elif isinstance(item, Armor):
            woin.equip_armor(item)
        else:
            woin.inventory.append(item)
            print(f"✅ Куплено: {item.name}")
        print(f"  Осталось золота: {woin.gold}g")

# ============================================================
#  ОБЪЕКТЫ МИРА
# ============================================================

nieve  = Tiempo("снег",          speed_debuff=2)
rain   = Tiempo("дождь",         attak_debuff=1)
fuerte = Tiempo("сильный дождь", attak_debuff=2, speed_debuff=1)
sol    = Tiempo("солнце")

woin = Human("Воин", 14, 100, 10)

wolf      = Monsters("Волк",           8,  40,  8)
ork       = Monsters("Орк",           10, 100,  5)
swin      = Monsters("Свин",          13, 150,  4)
goblin    = Monsters("Гоблин",        16, 200,  3)
king_ork  = Monsters("Король Орк",    12, 150,  6)
king_swin = Monsters("Король Свин",   15, 200,  5)
king_gob  = Monsters("Король Гоблин", 18, 250,  4)

bosque = Camino("лесной тропинка")
stone  = Camino("пещера")
monte  = Camino("гора")
sahara = Camino("пустыня")

locaciones = [bosque, stone, monte, sahara]
pogoda     = [sol, rain, nieve, fuerte]

current_loc    = bosque
current_pogoda = sol
step_counter   = 0

# ============================================================
#  ГЛАВНЫЙ ЦИКЛ
# ============================================================

print("=" * 45)
print("         ⚔️  ПРИКЛЮЧЕНИЕ НАЧИНАЕТСЯ  ⚔️")
print("=" * 45)

while True:
    step_counter  += 1
    woin.steps    += 1

    # Смена локации каждые 5 шагов
    if step_counter % 5 == 0:
        current_loc = random.choice(locaciones)
        print(f"\n🗺️  Новая локация: {current_loc.name.upper()}")

    # Смена погоды каждые 3 шага
    if step_counter % 3 == 0:
        current_pogoda = random.choice(pogoda)

    # Магазин каждые 10 шагов
    if step_counter % 10 == 0:
        print("\n🏪 На пути встретился торговец!")
        ans = input("Зайти в магазин? [д/н]: ").strip().lower()
        if ans == "д":
            show_shop(woin)
        os.system('clear')
        
    attak_debuff = current_pogoda.attak_debuff
    speed_debuff = current_pogoda.speed_debuff

    print(f"\n{'='*45}")
    print(current_pogoda.info())
    print(f"Локация: {current_loc.name}")
    print(f"Шаг: {woin.steps} | Убийств: {woin.kills} | Золото: {woin.gold}g")
    print(f"{'='*45}")

    # Случайное событие
    arr = random.choices(
        [bosque, wolf, ork, swin, goblin, king_ork, king_swin, king_gob],
        weights=[70, 10, 8, 5, 4, 1.5, 1, 0.5]
    )[0]

    # Сокровище каждые 7 шагов
    if step_counter % 7 == 0:
        treasures = make_treasures()
        t = random.choices(
            treasures,
            weights=[30,20,15,10,10,6,5,3,1]
        )[0]
        woin.gold += t.gold
        print(f"\n💰 {t.info()}")
        if t.item:
            ans = input(f"  Взять {t.item.name}? [д/н]: ").strip().lower()
            if ans == "д":
                if isinstance(t.item, Weapon):
                    woin.equip_weapon(t.item)
                elif isinstance(t.item, Armor):
                    woin.equip_armor(t.item)
                else:
                    woin.inventory.append(t.item)
                    print(f"  Добавлено в инвентарь.")

        # Редкий шанс — пистолет + кинжал вместе
        if random.random() < 0.03:
            combo = pistol_dagger_combo()
            print(f"\n🌟 РЕДКАЯ НАХОДКА: Пистолет + Кинжал!")
            ans = input("  Экипировать комбо? [д/н]: ").strip().lower()
            if ans == "д":
                woin.equip_weapon(combo)

    # Грязь каждые 4 шага
    if step_counter % 4 == 0:
        print(f"\n🟫 {Mud().info()}")
        speed_debuff += 2

    # Вывод статов
    woin_lines = woin.info().split("\n")
    arr_lines  = arr.info().split("\n")
    for w, m in zip(woin_lines, arr_lines):
        print(f"  {w:<28} | {m}")

    # БОЙ
    if isinstance(arr, Monsters):
        print(f"\n⚔️  Появился {arr.name}!")
        print(f"  Ваша защита: {woin.total_defense()} | Инвентарь: {len(woin.inventory)} предметов")

        choice = input("Драться [д] / бежать [б] / инвентарь [и] / экипировка [э]: ").strip().lower()

        if choice == "и":
            woin.show_inventory()
            use = input("Использовать (номер) или 0: ").strip()
            if use.isdigit() and int(use) > 0:
                woin.use_item(int(use))
            choice = input("Теперь: драться [д] / бежать [б]: ").strip().lower()
            
        if choice == "э":
            woin.show_equip()
            choice = input("Драться [д] / бежать [б]: ").strip().lower()
    
        if choice == "б":
            if (woin.speed - speed_debuff) >= arr.speed:
                print(f"🏃 {woin.name} успешно сбежал!")
            else:
                print(f"❌ Не удалось сбежать!")
                dmg = max(1, arr.attak // 2 - woin.total_defense())
                woin.healf -= dmg
                print(f"  Получен урон {dmg}. Здоровье: {woin.healf:.0f}")
        else:
            start_healf  = arr.healf
            woin_counter = 0
            arr_counter  = 0

            while arr.healf > 0 and woin.healf > 0:
                woin_counter += max(1, woin.speed - speed_debuff)
                arr_counter  += arr.speed

                if woin_counter >= 10:
                    woin_counter -= 10
                    # предложить бомбу если есть
                    has_bomb = [i for i,x in enumerate(woin.inventory,1) if isinstance(x, Bomb)]
                    if has_bomb and arr.healf > 50:
                        ans = input(f"  Бросить бомбу? (номер {has_bomb}) или Enter: ").strip()
                        if ans.isdigit() and int(ans) in has_bomb:
                            woin.use_item(int(ans), target=arr)
                    print(woin.atak(arr, attak_debuff))
                    if arr.healf <= 0:
                        print(f"💀 {arr.name} погиб!")
                        woin.kills += 1
                        reward = random.randint(5, 20)
                        woin.gold += reward
                        print(f"🪙 +{reward}g. Всего: {woin.gold}g")
                        break

                if arr_counter >= 10:
                    arr_counter -= 10
                    dmg = max(1, arr.attak - woin.total_defense())
                    woin.healf -= dmg
                    print(f"{arr.name} атакует {woin.name}! здоровье {woin.name}: {woin.healf:.0f}")
                    if woin.healf <= 0:
                        print("💀 Воин погиб!")
                        break

            arr.healf = start_healf

    else:
        print(arr.info())
        print(woin.heal(5))

    # Конец игры
    if woin.healf <= 0:
        print("\n" + "="*45)
        print("        💀  ИГРА ОКОНЧЕНА  💀")
        print(f"  Шагов   : {woin.steps}")
        print(f"  Убийств : {woin.kills}")
        print(f"  Золото  : {woin.gold}g")
        print("="*45)
        break

    if input("\nПродолжить? [Enter / н]: ").strip().lower() == "н":
        print("\n" + "="*45)
        print("        🏁  ВЫ ВЫШЛИ ИЗ ИГРЫ")
        print(f"  Шагов   : {woin.steps}")
        print(f"  Убийств : {woin.kills}")
        print(f"  Золото  : {woin.gold}g")
        print("="*45)
        break

    os.system('clear')

