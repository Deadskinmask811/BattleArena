import random
import sys
class Entity:
    """
    Class of all Entities in the game, used for player and for enemy NPCs.
    """
    def __init__(self, name, health, dodge, block, hit, crit, Weapon):
        self.name = name
        self.health = health
        self.dodge = dodge
        self.block = block
        self.hit = hit
        self.crit = crit
        self.weapon = Weapon
        
    alive = True
    #TODO skill scaling your stats will be implemented after combat and rolls are already working properly.
    skill = 0

    def attack(self):
        #do you hit?
        if self.check_hit():
            #do you crit?
            if self.check_crit():
                #do crit
                damage = random.randrange(self.weapon.min_dmg, self.weapon.max_dmg)
                crit = round(damage + (damage * .2))
                return crit

            return random.randrange(self.weapon.min_dmg, self.weapon.max_dmg) 

        else:
            return 0 

    def check_hit(self):
        roll = random.random()
        print("DEBUG: hit roll = {}".format(roll))
        if roll <= self.hit:
            return True
        else:
            return False
    
    def check_crit(self):
        roll = random.random()
        if roll <= self.crit:
            return True
        else:
            return False

    def vital_check(self):
        if self.health <= 0:
            self.alive = False
            return False
        else:
            return True

    def update_health(self, value):
        self.health =+ value

    def receive_damage(self, value):
        self.health -= value

class Weapon:
    """
    Class to create weapons used by all entities in the game
    """
    def __init__(self, name, min_dmg, max_dmg):
        self.name = name
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg

class Battle:
    """
    Class to run the battles between 2 entities, handles attacking and status checks for when someone dies.
    """
    def __init__(self, entity1, entity2):
        """
        While creating the class there is a roll that determines who attacks first between the 2 entities.
        """
        roll = self.roll_priority()
        if(roll <= .5):
            self.attacker1 = entity1
            self.attacker2 = entity2
        else:
            self.attacker1 = entity2
            self.attacker2 = entity1

    def print_priority_attacker(self):
        return self.attacker1.name
            
    def roll_priority(self):
        return random.random()

    def do_battle(self):
        while self.attacker1.alive and self.attacker2.alive:
            # attacker 1 is attacking
            attacker1_attack = self.attacker1.attack()
            if attacker1_attack == 0:
                print("{} misses!".format(self.attacker1.name))
            else:
                self.attacker2.receive_damage(attacker1_attack)
                print("{} deals {} damage to {}".format(self.attacker1.name, attacker1_attack, self.attacker2.name))
                #print("DEBUG: {} has {} health remaining".format(self.attacker2.name, self.attacker2.health))
                # if vita_check() returns False break out of combat
                if not self.attacker2.vital_check():
                    print("{} has defeated {}".format(self.attacker1.name, self.attacker2.name))
                    break
            
            # attacker 2 is attacking
            attacker2_attack = self.attacker2.attack()
            if attacker2_attack == 0:
                print("{} misses!".format(self.attacker2.name))
            else:
                self.attacker1.receive_damage(attacker2_attack)
                print("{} receives {} damage from {}".format(self.attacker1.name, attacker2_attack, self.attacker2.name))
                #print("DEBUG: {} have {} health left".format(self.attacker1.name, self.attacker1.health))
                # if vital_check() returns False break out of combat
                if not self.attacker1.vital_check():
                    print("{} has been defeated".format(self.attacker1.name))
                    break


def create_player():
    name = input("what is your name?\n>>")
    # entity returns an entity object
    player_character = Entity(name, 100, .5, .5, .75, .15, Weapon("sword of ultimate doom", 2, 6))
    return player_character


# start game here, all code for the game goes into game()

class Game:

    def setup(self):
        player = create_player()
        return player

    def show_lobby(self, player):
        print("\nStats - Name: {}, Health: {}, Weapon: {}".format(player.name, player.health, player.weapon.name))

        print("1. Fight")
        print("4. Exit Game")

    def random_enemy(self):
        '''
        returns an Entity enemy object that is selected randomly from a list of Entity objects
        '''
        enemies_list = [
                        #TODO dodge and block are currently unused.
                        # name, health, dodge, block, hit, crit, Weapon
                        Entity("Bear", 35, .5, 0, .75, .15, Weapon("Claws", 1, 3)),
                        Entity("Klaud", 25, .10, .5, .65, .20, Weapon("Dual Scimitars", 2, 4)),
                        Entity("Donald Trump", 30, .2, 0, .75, .15, Weapon("YUGE MOUTH", 1, 5))

                       ]
        random_num = random.randrange(0, len(enemies_list))
        return enemies_list[random_num]
    
    
def main():
    game = Game()
    player = game.setup()
    print("Welcome, {}!!!".format(player.name))
    while player.alive:

        game.show_lobby(player)
        
        selection = input("What do you wish to do? ")
        if selection == "1":
            # TODO this gets replaced by a class that takes care of doing the battling, taking the player class
            # and getting an enemy, either by random creation or predetermined order?
            '''
            print("DEBUG: DOING TEST BATTLE")
            npc = Entity("bear", 100, .5, .5, .75, .15, Weapon("Claws", 1, 3))

            fight = Battle(player, npc)
            fight.do_battle()
            '''
            fight = Battle(player, game.random_enemy())
            fight.do_battle()
        elif selection == "4":
            sys.exit()


    

if __name__ == "__main__":
    main()
