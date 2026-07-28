class Titan:
    def __init__(self, name:str, height:int, weilder:str, abilities:dict[str,int],survived:bool = False,hardened :bool =False):
 
        self.name = name
        self.height =height
        self.weilder = weilder
        self.abilities = abilities
        self.survived = survived
        self.hardened = hardened



class AttackTitan(Titan):
   def __init__(self, name:str, height:int, weilder:str, abilities:dict[str:str],survived):
       super().__init__(name, height, weilder, abilities,survived)
class FemaleTitan(Titan):
    def __init__(self, name, height, weilder, abilities, survived = True):
        super().__init__(name, height, weilder, abilities, survived)
class BeastTitan(Titan):
    def __init__(self, name, height, weilder, abilities, survived = False):
        super().__init__(name, height, weilder, abilities, survived)
class ArmoredTitan(Titan):
    def __init__(self, name, height, weilder, abilities, survived = True):
        super().__init__(name, height, weilder, abilities, survived)
class battle(Titan):
    def __init__(self,hp:int,offence:int,defence:int,speed:int,name, height, weilder, abilities,survived,hardened :bool =False):
        super().__init__(name, height, weilder, abilities,survived,hardened)
        self.hp =hp
        self.offence = offence
        self.defence = defence
        self.speed = speed
    def attack(self,abilities_name:str)->int:
        damage = self.abilities.get(abilities_name,0)
        if self.hardened:
            damage*1.5
        print(f"Poow {abilities_name}")
        return damage
    def defend(self):
        armour = self.defence
        if self.hardened :
            armour *= 2
            
        return armour
    



        


        