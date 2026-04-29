import os
import random


class Camino:
    def __init__(self,type):
        self.type=type
    def info(self):
        return f"идет по {self.type}"

class Animal:
    def __init__ (self,name,attak,healf,speed):
        self.name = name
        self.attak = attak
        self.healf = healf
        self.speed = speed
        
class Monsters (Animal):
    def info(self):
        return f"{self.name}\nатака: {self.attak}\nздоровье: {self.healf}\nскорость: {self.speed}"
    
class Human:
    def __init__ (self,name,attak,healf,speed):
        self.name = name
        self.attak = attak
        self.healf = healf
        self.speed = speed
    def info(self):
        return f"{self.name}\nатака: {self.attak}\nздоровье: {self.healf}\nскорость: {self.speed}"
        
class Money:
    def __init__ (self,name):
        self.name = name
    def info(self):
        return f"{self.name} только для людей"


woin=Human("Воин" ,14, 100,1)
wolf=Monsters("Волк" ,8, 40,0.8)
ork=Monsters("Орк" ,10, 100,0.5)
swin=Monsters("Свин" ,13, 150,0.4)
goblin=Monsters("Гоблин" ,16, 200,0.3)
king_ork=Monsters("Король Орк" ,12, 150,0.6)
king_swin=Monsters("Король Свин" ,15, 200,0.5)
king_goblin=Monsters("Король Гоблин" ,18, 250,0.4)
money = Money("монета")
camino=Camino("дороге")




array=[]
u=3

while True:
    x=random.randint (0,100)
    y=random.randint (0,100)
    print(x ,y)
    
    arr=random.choices([camino,wolf,ork,swin,goblin,king_ork,king_swin,king_goblin] ,weights=[99,0.85,0.1,0.04,0.009,0.0009,0.00009,0.00001] )[0]
    woin_lines=woin.info().split("\n")
    arr_lines=arr.info().split("\n")    
    for w, m in zip(woin_lines,arr_lines):
        print(f"            {w:<20} | {m}")
        
    #print(money.info())
    
    if input("хотите продолжить :") == "":
        os.system('clear')
        u = 1
        array.append(u)
        os.system('clear')
        continue
    else:
        u=0
        
        os.system('clear')
        array.append(u)
        print
        for i  in enumerate( array , 1):
            pass        
        print(array)
        print(i)
            
        if input("хотите продолжить :") == "":
            os.system('clear')
            continue
        else:
            break
