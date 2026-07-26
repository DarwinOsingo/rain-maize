class Character:
    def __init__(self,name:str,health:int,abilities:dict[str,int] ):
        self.abilities = abilities
        self.health = health
        self.name = name
    def potency(self,ability_name:str) -> int:
        damage = self.abilities.get(ability_name,0)
        return damage
    
    def attack(self,abilities_name: str ):
        print(f"Take thiss {abilities_name}")
        
    def take_damage(self,damage_recieved:int)->int:
        damage_recieved = self.potency(ability_name="some_ability")
        self.health -= damage_recieved



        
