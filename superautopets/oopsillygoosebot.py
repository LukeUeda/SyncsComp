from submissionhelper.botbattle import BotBattle
from submissionhelper.info.gameinfo import GameInfo
from submissionhelper.info.pettype import PetType
from submissionhelper.info.foodtype import FoodType

bot_battle = BotBattle()

PET_BLACKLIST = []
FOOD_BLACKLIST = []

POSITION_1_PRIORITY = [
    PetType.ELEPHANT,
    PetType.CAMEL,
    PetType.PEACOCK,
    PetType.BISON,
    PetType.MOSQUITO,
    PetType.FLAMINGO,
    PetType.HEDGEHOG,
    PetType.CRICKET
]

POSITION_2_PRIORITY = [
    PetType.PEACOCK,
    PetType.CAMEL,
    PetType.GIRAFFE,
    PetType.DODO,
    PetType.CRICKET
]

POSITION_3_PRIORITY = [
    PetType.KANGAROO,
    PetType.GIRAFFE,
    PetType.HIPPO,
]

POSITION_4_PRIORITY = [
    PetType.SKUNK,
    PetType.PENGUIN,
    PetType.BUNNY,
    PetType.BLOWFISH,
]

POSITION_5_PRIORITY = [
    PetType.DOG,
    PetType.BLOWFISH,
    PetType.HORSE,
    PetType.PENGUIN,
    PetType.BUNNY
]

PRIORITIES = [POSITION_1_PRIORITY, POSITION_2_PRIORITY, POSITION_3_PRIORITY, POSITION_4_PRIORITY, POSITION_5_PRIORITY]

def sillyOuput(game_info):
    print(f"\nRound #{game_info.round_num}\n")
    player = game_info.player_info
    nextOpponent = game_info.next_opponent_info

    printable = "Player Info:\n"

    printable += f"Health: {player.health}"

    for i, pet in enumerate(player.pets):
        printable += f"\nPet {i}: "
        if pet != None:
            printable += printPet(pet)


    printable += "\n\n"

    printable += "Next Opponent Info:"

    for i, pet in enumerate(nextOpponent.pets):
        printable += f"\nPet {i}: "
        if pet != None:
            printable += printPet(pet)

    printable += "\n\n"

    printable += "Additional Comments:\n"

    print(printable, flush=True)

def printPet(pet):
    printable = str(pet.type)[8:]
    printable += f", H/A: {pet.health}/{pet.attack}"
    printable += f", Level: {pet.level}"
    printable += f", Food: {str(pet.carried_food)[9:]}"
    return printable

class SillyBot():
    def __init__(self):
        self.current_round = 0
        self.game_info = bot_battle.get_game_info()

    def getGameInfo(self):
        self.game_info = bot_battle.get_game_info()

    def displayPlayerInfo(self):
        sillyOuput(self.game_info)

    def updateRound(self):
        new_round = self.current_round != self.game_info.round_num
        if new_round:
            self.current_round = self.game_info.round_num
            return True
        return False
    
    
    def hasEmptySpots(self):
        for pet in self.game_info.player_info.pets:
            if pet == None:
                return True
            
        return False


    def fillFirstEmptySpotWithRandom(self):
        # Fills first empty spot from the left. If no empty spots are found or the shop is empty, 
        # function returns false. Otherwise the first empty spot found will be filled with the 
        # first pet in the shop and return true.
        for shop_pet in self.game_info.player_info.shop_pets:
            for i, pet in enumerate(self.game_info.player_info.pets):
                if pet == None and shop_pet.cost <= self.game_info.player_info.coins and shop_pet.type not in PET_BLACKLIST:
                    print("Buying", shop_pet.id, " at position", i)
                    bot_battle.buy_pet(shop_pet, i)
                    self.getGameInfo()
                    return True
                
        return False
    
    def fillLastEmptySpotWithRandom(self):
        # Fills first empty spot from the left. If no empty spots are found or the shop is empty, 
        # function returns false. Otherwise the first empty spot found will be filled with the 
        # first pet in the shop and return true.
        for shop_pet in self.game_info.player_info.shop_pets:
            for i, pet in reversed(list(enumerate(self.game_info.player_info.pets))): # Iterate through pets backwards while maintaining original indecies.
                if pet == None and shop_pet.cost <= self.game_info.player_info.coins and shop_pet.type not in PET_BLACKLIST:
                    print("Buying", shop_pet.id, " at position", i)
                    bot_battle.buy_pet(shop_pet, i)
                    self.getGameInfo()
                    return True
                
        return False
    
    def fillFirstEmptySpotWithSelected(self, shop_pet):
        # Purchases the selected shop pet and places it in the first emtpy spot from the left. If no empty spots are found 
        # or the shop is empty, function returns false. Otherwise the first empty spot found will be filled and return true.
        for i, pet in enumerate(self.game_info.player_info.pets):
            if pet == None and shop_pet.cost <= self.game_info.player_info.coins and shop_pet.type not in PET_BLACKLIST:
                print("Buying", shop_pet.id, " at position", i)
                bot_battle.buy_pet(shop_pet, i)
                self.getGameInfo()
                return True
                
        return False
    
    def fillLastEmptySpotWithSelected(self, shop_pet):
        # Purchases the selected shop pet and places it in the first emtpy spot from the left. If no empty spots are found 
        # or the shop is empty, function returns false. Otherwise the first empty spot found will be filled and return true.
        for i, pet in reversed(list(enumerate(self.game_info.player_info.pets))):
            if pet == None and shop_pet.cost <= self.game_info.player_info.coins and shop_pet.type not in PET_BLACKLIST:
                print("Buying", shop_pet.id, " at position", i)
                bot_battle.buy_pet(shop_pet, i)
                self.getGameInfo()
                return True
                
        return False
    
    def fillSelectedSpotWithRandom(self, index):
        # Buys random pet at a selected spot. If the spot is taken or there aren't enough coins, return fales.
        # Otherwise purchase the first shop pet and return true.
        for shop_pet in self.game_info.player_info.shop_pets:
            if self.game_info.player_info.pets[index] == None and shop_pet.cost <= self.game_info.player_info.coins and shop_pet.type not in PET_BLACKLIST:
                print("Buying", shop_pet.id, " at position", i)
                bot_battle.buy_pet(shop_pet, index)
                self.getGameInfo()
                return True
                
        return False

    def getFirstPetWithoutHeldFood(self):
        # Returns the current first pet without a held food effect.
        for pet in self.game_info.player_info.pets:
            if pet != None:
                if pet.carried_food == None:
                    return pet
        return None

    def buyPet(self, shop_pet, index):
        # Buys selected pet at a selected spot. If there aren't enough coins, return false.
        # Otherwise if the spot is empty purchase the selected shop pet and return true.
        # If the spot is occupied, sell the pet and purchase.
        if shop_pet.cost <= self.game_info.player_info.coins:
            if self.game_info.player_info.shop_pets[index] == None:
                bot_battle.buy_pet(shop_pet, index)
                self.getGameInfo()
                return True
            else:
                if self.game_info.remaining_moves < 2:
                    bot_battle.end_turn()
                    self.getGameInfo()
                    return False

                bot_battle.sell_pet(self.game_info.player_info.shop_pets[index])
                self.getGameInfo()

                bot_battle.buy_pet(shop_pet, index)
                self.getGameInfo()
                return True
        return False

    def buyFood(self, shop_food, target = None):
        # Buys food... yeah.
        if self.coinCountCheck(shop_food.cost):
            if shop_food.type in [FoodType.CANNED_FOOD, FoodType.SALAD_BOWL]:
                bot_battle.buy_food(shop_food)
                self.getGameInfo()
                return True
            else:
                bot_battle.buy_food(shop_food, target)
                self.getGameInfo()
                return True
        return False

    
    def getPetMaxStatSum(self):
        # Gets the owned pet with the maximum stat sum.
        max_pet = None
        max_pet_index = -1
        max_pet_sum = 0
        for i, pet in enumerate(self.game_info.player_info.pets):
            if pet != None:
                if(max_pet == None or pet.health + pet.attack > max_pet_sum):
                    max_pet_sum = pet.health + pet.attack
                    max_pet = pet
                    max_pet_index = i
        
        return max_pet_index, max_pet, max_pet_sum
    
    def getPetMinStatSum(self):
        # Gets the owned pet with the minimum stat sum.
        min_pet = None
        min_pet_index = -1
        min_pet_sum = 0
        for i, pet in enumerate(self.game_info.player_info.pets):
            if pet != None:
                if(min_pet == None or pet.health + pet.attack < min_pet_sum):
                    min_pet_sum = pet.health + pet.attack
                    min_pet = pet
                    min_pet_index = i
        
        return min_pet_index, min_pet, min_pet_sum
    
    def getShopPetMaxStatSum(self):
        # Gets the shop pet with the maximum stat sum.
        max_pet = None
        max_pet_index = -1
        max_pet_sum = 0
        for i, shop_pet in enumerate(self.game_info.player_info.shop_pets):
            if shop_pet != None:
                if(max_pet == None or shop_pet.health + shop_pet.attack > max_pet_sum):
                    max_pet_sum = shop_pet.health + shop_pet.attack
                    max_pet = shop_pet
                    max_pet_index = i
            
        return max_pet_index, max_pet, max_pet_sum
    
    def getShopPetMinStatSum(self):
        # Gets the shop pet with the minimum stat sum.
        min_pet = None
        min_pet_index = -1
        min_pet_sum = 0
        for i, shop_pet in enumerate(self.game_info.player_info.shop_pets):
            if shop_pet != None:
                if(min_pet == None or shop_pet.health + shop_pet.attack < min_pet_sum):
                    min_pet_sum = shop_pet.health + shop_pet.attack
                    min_pet = shop_pet
                    min_pet_index = i
        
        return min_pet_index, min_pet, min_pet_sum


    def getFoodConsumed(self):
        # Returns a list of foods that are currently in the shop and have permenant effects
        foods = []
        for shop_food_index, shop_food in enumerate(self.game_info.player_info.shop_foods):
            if(shop_food.type in [FoodType.APPLE, FoodType.PEAR, FoodType.CANNED_FOOD] and shop_food.type not in FOOD_BLACKLIST):
                foods.append([shop_food_index, shop_food])
        return foods
    
    def getFoodHeld(self):
        # Returns a list of foods that are currently in the shop and have held effects
        foods = []
        for shop_food_index, shop_food in enumerate(self.game_info.player_info.shop_foods):
            if(shop_food.type in [FoodType.HONEY, FoodType.MEAT_BONE, FoodType.GARLIC] and shop_food.type not in FOOD_BLACKLIST):
                foods.append([shop_food_index, shop_food])
        return foods
    
    def getFoodTemporary(self):
        # Returns a list of foods that are currently in the shop and have temporary effects
        foods = []
        for shop_food_index, shop_food in enumerate(self.game_info.player_info.shop_foods):
            if(shop_food.type in [FoodType.CUPCAKE, FoodType.SALAD_BOWL] and shop_food.type not in FOOD_BLACKLIST):
                foods.append([shop_food_index, shop_food])
        return foods
    
    def coinCountCheck(self, amount):
        # Checks if bot has at least the parsed amount
        if(self.game_info.player_info.coins < amount):
            return False
        return True
    
    def reroll(self):
        # Rerolls the shop
        if(self.game_info.player_info.coins != 0):
            bot_battle.reroll_shop()
            self.getGameInfo()
            return True
        return False
    
    def freezePet(self, shop_pet):
        # Freezes shop pets after making sure they aren't already frozen
        if not shop_pet.is_frozen :
            bot_battle.freeze_pet(shop_pet)
            self.getGameInfo()
            return True
        return False
    
    def freezeFood(self, shop_food):
        # Im sure u get the idea.
        if not shop_food.is_frozen :
            bot_battle.freeze_food(shop_food)
            self.getGameInfo()
            return True
        return False
    
    def endTurn(self):
        bot_battle.end_turn()
        self.getGameInfo()

    def chooseIdealUnitForPosition(self, position_index):
        prioritized_pet = None
        current_max_p_val = -1
        priorities = PRIORITIES[position_index]

        for i in range(0, 5):
            pet = self.game_info.player_info.pets[i]
            if pet != None:
                priority_val = priorities.index(pet.type) if pet.type in priorities else 100
                if current_max_p_val == -1 or priority_val < current_max_p_val:
                    current_max_p_val = priority_val
                    prioritized_pet = pet

        return prioritized_pet, current_max_p_val

sg_bot = SillyBot()

while True:
    # If it is a new round, diplsay player info
    if sg_bot.updateRound: 
        sg_bot.displayPlayerInfo()

    # While empty spots are present, attempt to fill them with best shop pet.
    # Idealy this should only run in the first couple of rounds.

    while sg_bot.hasEmptySpots(): # Break if there are no empty spots
        best_stat_shop_pet = sg_bot.getShopPetMaxStatSum()[1]
        if best_stat_shop_pet == None: break # Break if there are no shop pets

        success = sg_bot.fillFirstEmptySpotWithSelected(best_stat_shop_pet)
        if not success: break # Break if there are insufficient funds
    
    # Keep taking turns while there are still coins
    while sg_bot.coinCountCheck(1):
        # Consider the best shop pet and the worst owned pet
        worst_pet_index, worst_pet, worst_pet_stat_sum = sg_bot.getPetMinStatSum()
        best_shop_pet, best_shop_pet_stat_sum = sg_bot.getPetMinStatSum()[1:]

        # While a better pet is in the shop, buy it if possible or freeze it.
        while best_shop_pet_stat_sum > worst_pet_stat_sum:
            if sg_bot.coinCountCheck(best_shop_pet.cost - worst_pet.level):
                sg_bot.buyPet(best_shop_pet, worst_pet_index)
            else:
                sg_bot.freezePet(best_shop_pet)

            # Get new best shop pet and worst owned pet
            worst_pet, worst_pet_stat_sum = sg_bot.getPetMinStatSum()[1:]
            best_shop_pet, best_shop_pet_stat_sum = sg_bot.getPetMinStatSum()[1:]

        if sg_bot.current_round > 6:
        # Over each food class, the shop foods are applied appropriately
        # Each loop has a very similar structure:

        # food_consumed is a list of relevant food entries.
        # item_index is an index of food_consumed.

        # If food_consumed is empty, the shop contains no food
        # of the consummable type and hence the loop ends
        
        # When a food is bought, the size of food_consumed is reduced
        # leading towards the end of the loop.

        # However, if food is either frozen or not bought, the list remains
        # the same size. Hence, item_index is used to increment throught
        # the list.

        # If item_index reaches the length of food_consumed, all food items have
        # been considered, hence the loop breaks with this condition.

            food_consumed = sg_bot.getFoodConsumed()
            item_index = 0
            while food_consumed != [] and item_index != len(food_consumed):
                food_item = food_consumed[item_index]
                target_pet = sg_bot.getPetMaxStatSum()[1]
                if target_pet != None and sg_bot.coinCountCheck(food_item[1].cost):
                    sg_bot.buyFood(food_item[1], target_pet)
                else:
                    if food_item[1].type == FoodType.PEAR:
                        sg_bot.freezeFood(food_item[1])
                    item_index += 1
                food_consumed = sg_bot.getFoodConsumed()


            food_held = sg_bot.getFoodHeld()
            item_index = 0
            while food_held != [] and item_index != len(food_held):
                food_item = food_held[item_index]
                target_pet = sg_bot.getFirstPetWithoutHeldFood()
                if(target_pet != None and sg_bot.coinCountCheck(food_item[1].cost)):
                    sg_bot.buyFood(food_item[1], target_pet)
                else:
                    item_index += 1  
                food_held = sg_bot.getFoodHeld()


            food_temporary = sg_bot.getFoodTemporary()
            item_index = 0
            while food_temporary != [] and item_index != len(food_temporary):
                food_item = food_temporary[item_index]
                if sg_bot.coinCountCheck(food_item[1].cost):
                    if(food_item[1].type == FoodType.CUPCAKE):
                        target_pet = sg_bot.getPetMaxStatSum()[1]
                        if(target_pet != None):
                            sg_bot.buyFood(food_item[1], target_pet)
                        else:
                            item_index += 1 
                    else:
                        sg_bot.buyFood(food_item[1])
                else:
                    item_index += 1 
                food_temporary = sg_bot.getFoodTemporary()

        if sg_bot.coinCountCheck(1):
            sg_bot.reroll()

    for i in range(0, 5):
        p_pet, p_val = sg_bot.chooseIdealUnitForPosition(i)
        if p_pet != None:
            print(f"Ideal for position {i} is " + str(p_pet.type)[8:] + f" with a priority value of {p_val}.\n", flush=True)
        else:
            print("There are no pets hmmmmmmmmmmmmmm", flush=True)
    sg_bot.endTurn()