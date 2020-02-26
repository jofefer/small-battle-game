from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random






#create black magic
fire = Spell("Fire", 10, 100,"black")
thunder = Spell("Thunder",10,100,"black")
blizzard = Spell("Blizzard",10,100,"black")
meteor = Spell("Meteor",20,200,"black")
quake = Spell("Quake",13,140,"black")

#create white magic
cure = Spell("Cure",12, 120,"white")
cura = Spell("Cura",18,200,"white")


# Create som Items
potion = Item("Potion","potion","Heals 50 HP",50)
hipotion = Item("Hi-Potion","potion","Heals 100 HP",100)
superpotion = Item("Super Potion","potion","Heals 500 HP",500)
elixer = Item("Elixer","elixer","Fully restore HP/MP  of one party member", 99999)
hielixer = Item("MegaElixer","elixer","Fully restore party's HP/MP",9999)

grenade = Item("Grenade","attack","Deals 500 damage",500)

player_spells = [fire,thunder,blizzard,meteor,cure,cura]
player_items = [{"item":potion,"quantity":15},{"item":hipotion,"quantity":5},
                {"item":superpotion,"quantity":5},{"item":elixer,"quantity":5},
                {"item":hielixer, "quantity":2},{"item":grenade,"quantity":5}]

#instance people
player1 = Person("Casado",460,63,200,34,player_spells,player_items)
player2 = Person("Abascal",460,63,400,34,player_spells,player_items)
player3 = Person("Rivera",460,63,100,34,player_spells,player_items)

enemy = Person("P.Sanchez",18000,65,450,25,[],[])
enemy2 = Person("P.Iglesias",100,65,405,25,[],[])
enemy3 = Person("Echenique",100,65,450,25,[],[])

players = [player1, player2, player3]
enemies = [enemy, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!"+ bcolors.ENDC)

while running:
    print("============================")
    print("NAME\t\t\t\tHP\t\t\t\t\t\t\t\t\t\t\t\t\t MP")
    for player in players:

        player.get_stats()
    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:


        player.choose_action()
        choice = input("Choose action: ")
        index = int(choice)-1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("You attaked "+enemies[enemy].name+" for",dmg, " points of damage. ")
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose magic: "))-1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()


            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL+ "\n Not enough MP\n"+bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE+"\n"+ spell.name+ " heal for "+str(magic_dmg)," HP",bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE+"\n"+spell.name, " deals",str(magic_dmg), " points of damage to "+enemies[enemy].name+ bcolors.ENDC)

        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose item: ")) -1

            if item_choice == -1:
                continue

            if player.items[item_choice]["quantity"]==0 :
                print(bcolors.FAIL+"\n"+"None left..."+bcolors.ENDC)
                continue

            item = player.items[item_choice]["item"]
            player.items[item_choice]["quantity"] -= 1



            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), " MP" + bcolors.ENDC)
            elif item.type == "elixer":
                player.hp = player.maxhp
                player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP",bcolors.ENDC)
            elif item.type == "attack":
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), " points of damage", bcolors.ENDC)



    enemy_choice = 1
    target = random.randrange(0,len(players))


    enemy_dmg = enemies[0].generate_damage()
    players[target].take_damage(enemy_dmg)
    print("Enemy attacks "+players[target].name+" for: ",enemy_dmg )

    print("--------------------------------")
    print("Enemy HP:", bcolors.FAIL + str(enemies[enemy].get_hp())+"/"+ str(enemies[enemy].get_max_hp())+bcolors.ENDC +"\n")

    defeated_enemies = 0
    defeated_players = 0


    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies +=1

    for player in players   :
        if player.get_hp() == 0:
            defeated_players +=1

    if defeated_enemies == len(enemies):
        print(bcolors.OKGREEN + "You win!"+bcolors.ENDC)
        running = False
    elif defeated_players == len(players):
        print(bcolors.FAIL + "Your enemy has defeated you!"+bcolors.ENDC)
        running = False

