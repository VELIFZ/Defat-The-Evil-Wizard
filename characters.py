
import time
import random

class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.defense = 0
        self.max_health = health # to store original health for maximum limit
        self.avoid_active = False  # not evading
    
    # opponent can avoid the attacks, if not opponent defense point will be added - give message with reaming opponent hp    
    def attack(self, opponent):
        if isinstance(self.attack_power, tuple):
            self.attack_power = random.randint(self.attack_power[0], self.attack_power[1])
        
        if opponent.avoid_active:
            print(f'{opponent.name} evades the attack!')
            opponent.avoid_active = False
        else:
            # calculate the damage and make sure it's not negative
            opponent.damage =max((self.attack_power - opponent.defense), 0) 
            opponent.health -= opponent.damage
            # Attack messages
            print(f'\n{self.name} attacks {opponent.name} with {self.attack_power}. {opponent.name} has {opponent.health}/{opponent.max_health} HP remaining.\n')
        
        # if opponent lose      
        if (opponent.health <= 0):
            print(f'{opponent.name} got defeated by {self.name}!')
            
    def heal(self):
        heal_amount = int(self.max_health * 0.1)
        self.health = min((self.health + heal_amount), self.max_health)
        print(f"{self.name}'s health increased by {heal_amount} and now has {self.health}/{self.max_health} HP.")
        
    def display_stats(self):
        print(f"{self.name}'s Stats - Health: {self.health}/{self.max_health}")

# berserk can increase the damage givin 
# MARK: Warrior               
class Warrior(Character):
    def __init__(self, name):
        self.name = name
        self.defense = 10
        super().__init__(name, health=140, attack_power=25)   

    # Berserk
    def ability_1(self, opponent):
        if (self.health >= self.max_health // 2):
            double_damage = self.attack_power * 2
            print(f'{self.name} went berserk! Dealing with {double_damage} double damage.')
            opponent.health -= double_damage
            opponent.health = max(opponent.health, 0)
            print(f'{opponent.name} has {opponent.health}/{opponent.max_health} HP remaining.\n')
        else:
            print(f'{self.name} is too weak to go berserk on {opponent.name}.')
            self.attack(opponent)
            
    # dodge        
    def ability_2(self):
        self.avoid_active = True
        #self.defense = 30 
        print(f"{self.name} prepares to dodge the next attack!") 
    
# MARK: Mage              
class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=20)
        
    # spell    
    def ability_1(self, opponent):
        absorbed_power = opponent.attack_power * 0.5
        new_attack_power = absorbed_power + 5
        opponent.health -= new_attack_power
        opponent.health = max(opponent.health, 0)
        print(f'{self.name} uses spell to absorbed power from {opponent.name}\'s attack and reflected back.')
        print(f'Damage givin {new_attack_power}. {opponent.name} has {opponent.health} HP.')
    
    # barrier
    def ability_2(self):
        self.avoid_active = True 
        print(f"{self.name} activates a magical barrier!")  
    
# MARK: Archer          
class Archer(Character):
    def __init__(self, name):
        self.name = name
        self.last_avoid_attack_time = 0 # in seconds
        super().__init__(name, health=120, attack_power=(15,25))
        
    # quick shot    
    def ability_1(self, opponent):
        damage_arrow_1 = random.randint(self.attack_power[0], self.attack_power[1])
        damage_arrow_2 = random.randint(self.attack_power[0], self.attack_power[1])
        double_arrow = (damage_arrow_1 + damage_arrow_2)
        opponent.health -= double_arrow
        opponent.health = max(opponent.health, 0)
        print(f'{self.name} used double arrow attack with {double_arrow} attack power in total.')
    
    # evade
    def ability_2(self):
        current_time = time.time()
        # Check if 60 seconds have passed since the last evade if not:
        if (current_time - self.last_avoid_attack_time >= 60):
            self.avoid_active = True
            self.last_avoid_attack_time = current_time
            print(f"{self.name} evade attack! Need a min to evade another attack!")
        else:
            remaining_time = 60 - (current_time - self.last_avoid_attack_time)
            print(f'{self.name} cannot evade yet! Please wait {int(remaining_time)} seconds.') 
        
# MARK: Paladin                   
class Paladin(Character):
    def __init__(self, name):
        super().__init__(name, health=130, attack_power = (15, 25))
        
    # holy_strike
    def ability_1(self, opponent):
        max_damage = max(random.randint(*self.attack_power), random.randint(*self.attack_power))
        opponent.health -= max_damage
        opponent.health = max(opponent.health, 0)
        self.health = min((self.health + 5), self.max_health)
        print(f'{self.name} use Holy Strike! Got healed by 5 HP and gave {max_damage} damage to {opponent.name}, {opponent.health} HP.')
        
    # Shield
    def ability_2(self):
        self.avoid_active = True
        print(f'{self.name} uses Holy Shield to protect from attacks!')  
    
# MARK: Wizard        
class EvilWizard(Character):
    def __init__(self, name):
        super().__init__(name, health=150, attack_power=30)
    
    def regenerate(self): 
        if (self.health < self.max_health):
            self.health += 5  # Lower regeneration amount
            print(f"{self.name} regenerates 5 health! Current health: {self.health}")
        
    def minion(self):
        pass
 
# MARK: Create Character Helper    
def create_character():    
    print('''
        ****** Hero ******
        1. Warrior! Special Abilities: 1. Berserk, 2. Dodge
        2. Mage! Special Abilities: 1. Absorb Spell, 2. Barrier
        3. Archer! Special Abilities: 1. Double Arrow, 2. Evade Attack
        4. Paladin! Special Abilities: 1. Bonus Damage, 2. Divine Shield
        \n
    ''')
    
    char_choice = input('Enter the number of your class choice: \n').strip()
    name = input("Enter your character's name: \n").strip().title()
    
    if char_choice == '1':
        return Warrior(name)
    elif char_choice == '2':
        return Mage(name)
    elif char_choice == '3':
        return Archer(name)    
    elif char_choice == '4':
        return Paladin(name)
    else:
        print("Invalid choice. Please choose a number from 1 to 4.")
        return create_character() 
    
# MARK: Battle Helper     
def battle(player, wizard):
    healed = False
    while (player.health > 0) and (wizard.health > 0):
        player.display_stats()
        wizard.display_stats()
        
        # player's turn
        print("\n--- Your Turn ---")
        print("1. Attack")
        print("2. Use Special Ability")
        print("3. Heal")
        print("4. View Stats")
        print("5. Exit")
        
        choice = input("Choose an action: \n").strip()
        
        if (choice == '1'):
            player.attack(wizard)
            healed = False
        elif (choice == '2'):
            ability_choice = input('Which Ability? 1 or 2: \n').strip()
            healed = False
            if ability_choice == '1':
                player.ability_1(wizard)
            elif ability_choice == '2':
                player.ability_2()
        elif (choice == '3'):
            if healed:
                print(f"{player.name}, you cannot heal again until you fight with {wizard.name} again\n.")
            else:
                player.heal() 
                healed = True  # Set the heal to True 
                print(f"{wizard.name} cannot attack while {player.name} is healing.\n") 
        elif choice == '4':
            player.display_stats()
            wizard.display_stats()
        elif choice == '5':
            print('Exiting the game:') 
            player.display_stats()
            wizard.display_stats()
            break
        else:
            print("Invalid choice, try again.\n")
            continue
        
        # Wizard's turn
        if (wizard.health > 0) and (choice != '3'):
            wizard.regenerate()  
            wizard.attack(player)
                
        if player.health <= 0:
            break

# MARK: main()
# # Main function to handle the flow of the game
def main():
    # Character creation phase
    player = create_character()

    # Evil Wizard is created
    wizard = EvilWizard("The Dark Wizard")

    # Start the battle
    battle(player, wizard)

if __name__ == "__main__":
    main()