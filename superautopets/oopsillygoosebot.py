from submissionhelper.botbattle import BotBattle
from submissionhelper.info.gameinfo import GameInfo
from submissionhelper.info.pettype import PetType
from submissionhelper.info.foodtype import FoodType
from submissionhelper.info.shoppetinfo import ShopPetInfo
from submissionhelper.info.playerpetinfo import PlayerPetInfo

bot_battle = BotBattle()

PET_BLACKLIST = []
FOOD_BLACKLIST = []

SUMMONER_BONUS = 5

HORSE_EMPTY_BONUS = 10
FISH_LEVEL_UP_BONUS = 5

REROLL_THRESHOLD = 5
FREEZE_THRESHOLD = 7

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
        self.opponent_tally = {}
        self.shop_ignore_list = []

    def getGameInfo(self):
        self.game_info = bot_battle.get_game_info()

    def displayPlayerInfo(self):
        sillyOuput(self.game_info)

    def addOpponentTally(self):
        for pet in self.game_info.next_opponent_info.pets:
            if pet != None:
                if pet.type in self.opponent_tally:
                    self.opponent_tally[pet.type] += 1
                else:
                    self.opponent_tally[pet.type] = 1
    
    def displayOpponentTally(self):
        for entry in self.opponent_tally.items():
            print("   ",entry[0], ": ", entry[1], flush=True)

    def updateRound(self):
        new_round = self.current_round != self.game_info.round_num
        if new_round:
            self.current_round = self.game_info.round_num
            self.shop_ignore_list = []
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
                    self.buyPet(shop_pet, i)
                    return True
                
        return False
    
    def fillLastEmptySpotWithRandom(self):
        # Fills first empty spot from the left. If no empty spots are found or the shop is empty, 
        # function returns false. Otherwise the first empty spot found will be filled with the 
        # first pet in the shop and return true.
        for shop_pet in self.game_info.player_info.shop_pets:
            for i, pet in reversed(list(enumerate(self.game_info.player_info.pets))): # Iterate through pets backwards while maintaining original indecies.
                if pet == None and shop_pet.cost <= self.game_info.player_info.coins and shop_pet.type not in PET_BLACKLIST:
                    self.buyPet(shop_pet, i)
                    return True
                
        return False
    
    def fillFirstEmptySpotWithSelected(self, shop_pet):
        # Purchases the selected shop pet and places it in the first emtpy spot from the left. If no empty spots are found 
        # or the shop is empty, function returns false. Otherwise the first empty spot found will be filled and return true.
        for i, pet in enumerate(self.game_info.player_info.pets):
            if pet == None and shop_pet.cost <= self.game_info.player_info.coins and shop_pet.type not in PET_BLACKLIST:
                self.buyPet(shop_pet, i)
                return True
                
        return False
    
    def fillLastEmptySpotWithSelected(self, shop_pet):
        # Purchases the selected shop pet and places it in the first emtpy spot from the left. If no empty spots are found 
        # or the shop is empty, function returns false. Otherwise the first empty spot found will be filled and return true.
        for i, pet in reversed(list(enumerate(self.game_info.player_info.pets))):
            if pet == None and shop_pet.cost <= self.game_info.player_info.coins and shop_pet.type not in PET_BLACKLIST:
                self.buyPet(shop_pet, i)
                return True
                
        return False
    
    def fillSelectedSpotWithRandom(self, index):
        # Buys random pet at a selected spot. If the spot is taken or there aren't enough coins, return fales.
        # Otherwise purchase the first shop pet and return true.
        for shop_pet in self.game_info.player_info.shop_pets:
            if self.game_info.player_info.pets[index] == None and shop_pet.cost <= self.game_info.player_info.coins and shop_pet.type not in PET_BLACKLIST:
                self.buyPet(shop_pet, index)
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
            if self.game_info.player_info.pets[index] == None:
                print("Buying ", shop_pet.type, " at position", index, flush=True)
                bot_battle.buy_pet(shop_pet, index)
                self.getGameInfo()
                return True
            else:
                if self.game_info.remaining_moves < 2:
                    bot_battle.end_turn()
                    self.getGameInfo()
                    return False
                
                print("Replacing ", self.game_info.player_info.pets[index].type, " with ",shop_pet.type, " at position", index, flush=True)
                bot_battle.sell_pet(self.game_info.player_info.pets[index])
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
    
    def freeze(self, shop_item):
        # Freezes shop pets after making sure they aren't already frozen
        if not shop_item.is_frozen :
            if type(shop_item) == ShopPetInfo:
                bot_battle.freeze_pet(shop_item)
            else:
                bot_battle.freeze_food(shop_item)
            self.getGameInfo()
            return True
        return False
    
    def unfreeze(self, shop_item):
        # Freezes shop pets after making sure they aren't already frozen
        if shop_item.is_frozen :
            if type(shop_item) == ShopPetInfo:
                bot_battle.unfreeze_pet(shop_item)
            else:
                bot_battle.unfreeze_food(shop_item)
            self.getGameInfo()
            return True
        return False
    
    def endTurn(self):
        bot_battle.end_turn()
        self.getGameInfo()

    def ownsPet(self, pet_type):
        for pet in self.game_info.player_info.pets:
            if pet != None:
                if pet.type == pet_type:
                    return True
        return False
    
    def shopHasPet(self, pet_type):
        for shop_pet in self.game_info.player_info.shop_pets:
            if shop_pet.type == pet_type:
                return True
        return False
    
    def emptySpaceCount(self):
        count = 0
        for pet in self.game_info.player_info.pets:
            if pet == None:
                count += 1
        return count

    def findBestTierOneShopPet(self, ignore_frozen = True):
        best_pet_score = 0
        best_pet = None
        for shop_pet in self.game_info.player_info.shop_pets:
            current_pet_score = self.getTierOneShopPetScore(shop_pet)
            if current_pet_score >= best_pet_score and shop_pet.type not in self.shop_ignore_list:
                if not ignore_frozen or (ignore_frozen and not shop_pet.is_frozen):
                    best_pet_score = current_pet_score
                    best_pet = shop_pet

        return best_pet, best_pet_score
    
    def findBestTierTwoShopPet(self, ignore_frozen = True):
        best_pet_score = 0
        best_pet = None
        for shop_pet in self.game_info.player_info.shop_pets:
            current_pet_score = self.getTierTwoShopPetScore(shop_pet)
            if current_pet_score >= best_pet_score and shop_pet.type not in self.shop_ignore_list:
                if not ignore_frozen or (ignore_frozen and not shop_pet.is_frozen):
                    best_pet_score = current_pet_score
                    best_pet = shop_pet

        return best_pet, best_pet_score
    
    def findWorstTierOneOwnedPet(self):
        worst_pet_score = 300
        worst_pet = None
        for pet in self.game_info.player_info.pets:
            if pet != None:
                current_pet_score = self.getTierOneShopPetScore(pet)
                if current_pet_score > worst_pet_score:
                    worst_pet_score = current_pet_score
                    worst_pet = pet

        return worst_pet, worst_pet_score
    
    def findWorstTierTwoOwnedPet(self):
        worst_pet_score = 300
        worst_pet = None
        for pet in self.game_info.player_info.pets:
            if pet != None:
                current_pet_score = self.getTierTwoShopPetScore(pet)
                if current_pet_score > worst_pet_score:
                    worst_pet_score = current_pet_score
                    worst_pet = pet

        return worst_pet, worst_pet_score

    def findBestTierOneOwnedPet(self):
        best_pet_score = 0
        best_pet = None
        for pet in self.game_info.player_info.pets:
            if pet != None:
                current_pet_score = self.getTierOneShopPetScore(pet)
                if current_pet_score >= best_pet_score:
                    best_pet_score = current_pet_score
                    best_pet = pet

        return best_pet, best_pet_score

    def getTierOneShopPetScore(self, pet):
        score = pet.health + pet.attack
        # CONSIDERING HORSE
        if pet.type == PetType.HORSE:
            if self.ownsPet(PetType.CRICKET) or self.shopHasPet(PetType.CRICKET):
                score += SUMMONER_BONUS
            
            if self.emptySpaceCount() >= 3 and self.game_info.player_info.coins >= 6:
                score += HORSE_EMPTY_BONUS

        # CONSIDERING CRICKET
        if pet.type == PetType.CRICKET:
            if self.ownsPet(PetType.HORSE) or self.shopHasPet(PetType.HORSE):
                score += SUMMONER_BONUS
        
        # CONSIDERING FISH
        if pet.type == PetType.FISH:
            if self.ownsPet(PetType.FISH) or self.shopHasPet(PetType.FISH):
                score += FISH_LEVEL_UP_BONUS
        
        return score
    
    def getTierTwoShopPetScore(self, pet):
        score = 0
        # CONSIDERING PEACOCK
        if pet.type == PetType.PEACOCK:
            score += 10
            if self.ownsPet(pet):
                score -= 3

        # CONSIDERING KANGAROO
        if pet.type == PetType.KANGAROO:
            score += 10

        if pet.type == PetType.SPIDER:
            score += 5
            if self.ownsPet(PetType.HORSE) or self.shopHasPet(PetType.HORSE):
                score += SUMMONER_BONUS

        # CONSIDERING HEDGEHOG
        if pet.type == PetType.HEDGEHOG:
            total_health = 0
            for pet in self.game_info.player_info.pets:
                if pet != None:
                    total_health += pet.health
            if total_health/5 > 2:
                score += 5

        return score

    def buyInBestEmptyTierOnePosition(self, shop_pet):
        # Buys the given shop pet at the best position for that type
        if shop_pet.type == PetType.HORSE:
            self.fillLastEmptySpotWithSelected(shop_pet)
        else:
            self.fillFirstEmptySpotWithSelected(shop_pet)

    def getOwnedCombinations(self):
        pairs = []
        for i, pet_i in enumerate(self.game_info.player_info.pets):
            for j, pet_j in enumerate(self.game_info.player_info.pets):
                if j > i and pet_i.type == pet_j.type and pet_i.level != 3 and pet_j.level != 3:
                    pairs.append([pet_i, pet_j])
        return pairs

    def getPet(self, pet_type):
        max_sub_level = 0
        max_level_pet = None
        for i, pet in enumerate(self.game_info.player_info.pets):
            if pet.type == pet_type and pet.sub_level >= max_sub_level:
                max_level_pet = pet
        
        return max_level_pet, i

    def levelUpPet(self, target_pet, secondary_pet):
        if target_pet.level != 3 and target_pet.type == secondary_pet.type:
            if type(secondary_pet) == PlayerPetInfo:
                if secondary_pet.level != 3:
                    bot_battle.level_pet_from_pets(secondary_pet, target_pet)
                    self.getGameInfo()
                    return True
            else:
                bot_battle.level_pet_from_shop(secondary_pet, target_pet)
                self.getGameInfo()
                return True
        return False


    def petsPurchaseable(self):
        # Returns number of pets that could be bought with funds
        return self.game_info.player_info.coins//3
    
    def petsPurchasableAfterReroll(self):
        # Returns the number of pets that could possibly bought with the remaining
        # funds if a reroll occurs
        return (self.game_info.player_info.coins - 1)//3
    
    def petsPurchasableChangesOnReroll(self):
        # Returns true if the number of pets that can be purchased reduces on reroll
        # Otherwise returns false
        return self.petsPurchasableAfterReroll() != self.petsPurchaseable()
    
    def unfreezeAll(self):
        for i in range(0, len(self.game_info.player_info.shop_pets)):
            self.unfreeze(self.game_info.player_info.shop_pets[i])
        
        for i in range(0, len(self.game_info.player_info.shop_foods)):
            self.unfreeze(self.game_info.player_info.shop_foods[i])

    def findBestShopPet(self, ignoreFrozen = True):
        if self.game_info.round_num < 3:
            return self.findBestTierOneShopPet(ignore_frozen=ignoreFrozen)
        elif self.game_info.round_num < 5:
            return self.findBestTierTwoShopPet(ignore_frozen=ignoreFrozen)
        else:
            return 0
        
    def findBestShopFood(self, ignoreFrozen = True):
        if self.game_info.round_num < 3:
            return self.findBestTierOneShopFood(ignore_frozen=ignoreFrozen)
        else:
            return None, 0, None

    def getShopFoodScore(self, food):
        if self.game_info.round_num < 3:
            return self.getTierOneShopFoodScore(food)
        else:
            return 0

    def getShopPetScore(self, pet):
        if self.game_info.round_num < 3:
            return self.getTierOneShopPetScore(pet)
        elif self.game_info.round_num < 5:
            return self.getTierTwoShopPetScore(pet)

    def findWorstOwnedPet(self):
        if self.game_info.round_num < 3:
            return self.findWorstTierOneOwnedPet()
        elif self.game_info.round_num < 5:
            return self.findWorstTierTwoOwnedPet()

    def getTierOneShopFoodScore(self, shop_food):
        score = 9 - shop_food.cost
        target = None

        if shop_food.type == FoodType.PEAR:
            score += 2

        if shop_food.type in [FoodType.HONEY, FoodType.MEAT_BONE, FoodType.GARLIC]:
            score += 1

        target = self.findBestTierOneOwnedPet()[0]

        return score, target

    def findBestTierOneShopFood(self, ignore_frozen = True):
        best_shop_food = None
        best_shop_food_score = 0
        best_shop_food_target = None
        for shop_food in self.game_info.player_info.shop_foods:
            current_score, current_target = self. getTierOneShopFoodScore(shop_food)
            if current_score > best_shop_food_score:
                if not ignore_frozen or (ignore_frozen and not shop_food.is_frozen):
                    best_shop_food = shop_food
                    best_shop_food_score = current_score
                    best_shop_food_target = current_target
        
        return best_shop_food, best_shop_food_score, best_shop_food_target

    def performBestOption(self):
        # This is our tier one strategy. A move or series of moves will be performed which represents
        # our best possible option in the current situation.

        # If the turn has started, unfreeze all to refresh
        if self.game_info.remaining_moves == 30:
            self.unfreezeAll()

        # best shop pet and its score
        b_shop_pet, b_shop_pet_score = self.findBestShopPet()
        b_shop_food, b_shop_food_score, b_shop_food_target = self.findBestShopFood()

        print("\n\nCurrent Shop: ", flush=True)
        for shop_pet in self.game_info.player_info.shop_pets:
            print("  -", shop_pet.type, " has a score of ", self.getShopPetScore(shop_pet), flush=True)
        
        for shop_food in self.game_info.player_info.shop_foods:
            print("  -", shop_food.type, " has a score of ", self.getShopFoodScore(shop_food), flush=True)

        if(b_shop_pet != None):
            print("My best shop pet is ", b_shop_pet.type, flush=True)

        # When there are empty spaces
        if self.emptySpaceCount() > 0:
            if self.petsPurchaseable() != 0:
                # If a pet can be purchased...
                can_be_rerolled = self.petsPurchasableAfterReroll() >= self.emptySpaceCount() or not self.petsPurchasableChangesOnReroll()
                if b_shop_pet_score < REROLL_THRESHOLD and can_be_rerolled:
                    # ... but there are no good pets, reroll if there will be enough funds to buy
                    # a sufficient number of pets
                    self.reroll()
                else:
                    # ... and there is a good one, buy it
                    print("Since I still have empty spaces and the best pet is ", b_shop_pet.type, ", I'll buy it", flush=True)
                    self.buyInBestEmptyTierOnePosition(b_shop_pet)
            else:
                # If a pet cannot be purchased, freeze pets that exceed the freeze threshold
                print("I can't afford any pets, so I'll freeze the best ones and reroll if possible", flush=True)
                for shop_pet in self.game_info.player_info.shop_pets:
                    if self.getShopPetScore(shop_pet) > FREEZE_THRESHOLD:
                        self.freeze(shop_pet)

                # Reroll if possible (Method will check)
                self.reroll()
        else:
            # When there are no empty spaces, see if the best pet exceeds the reroll threshold
            if b_shop_pet_score > REROLL_THRESHOLD:
                if self.ownsPet(b_shop_pet.type):
                    # Otherwise if the shop pet can level up an owned pet, do it!!!
                    target_pet, i = self.getPet(b_shop_pet.type)
                    if target_pet.level != 3 and self.coinCountCheck(b_shop_pet.cost):
                        print("Imma combine", target_pet.type, " with the shop pet I have", flush=True)
                        self.levelUpPet(target_pet, b_shop_pet)

                    elif b_shop_pet_score > FREEZE_THRESHOLD and target_pet.level != 3: # If the pet is worth freezing and it can still be used to 
                        self.freeze(shop_pet)
                        self.shop_ignore_list.append(b_shop_pet.type)

                elif self.getOwnedCombinations() != []:
                    # If two owned pets can be combined, combine them and buy the shop pet if funds are available
                    if self.coinCountCheck(b_shop_pet.cost):
                        pet_i, pet_j = self.getOwnedCombinations()[0]
                        print("Imma combine two", pet_i.type, "'s I have so I have room to buy the", b_shop_pet.type, flush=True)
                        self.levelUpPet(pet_i, pet_j)
                        b_shop_pet, b_shop_pet_score = self.findBestShopPet()
                        self.fillFirstEmptySpotWithSelected(b_shop_pet)
                    
                    elif b_shop_pet_score > FREEZE_THRESHOLD:
                        self.freeze(shop_pet)
                        self.shop_ignore_list.append(b_shop_pet.type)

                elif self.findWorstOwnedPet()[1] < b_shop_pet_score:
                    # Finally, if there is a pet with a worst score than the shop and the pet can be afforded, buy it
                    if self.coinCountCheck(b_shop_pet.cost):
                        print(self.findWorstOwnedPet()[0].type, " is worse than", pet_i.type, " so Imma replace it", flush=True)
                        self.buyPet(b_shop_pet, self.game_info.player_info.pets.index(self.findWorstOwnedPet()[0]))
                    elif b_shop_pet_score > FREEZE_THRESHOLD:
                        self.freeze(shop_pet)
                else:
                    print("The pet is good, but it doesn't beat my other pets")
                    self.shop_ignore_list.append(b_shop_pet.type)
            elif b_shop_food_score > REROLL_THRESHOLD:
                if self.coinCountCheck(b_shop_food.cost):
                    b_shop_food, b_shop_food_score, b_shop_food_target = self.findBestShopFood()
                    self.buyFood(b_shop_food, b_shop_food_target)
                elif b_shop_food_score > FREEZE_THRESHOLD:
                    self.freeze(b_shop_food)
            else:
                print("No good options, just gonna reroll", flush=True)
                self.reroll()
                self.shop_ignore_list = []


sg_bot = SillyBot()

while True:
    # If it is a new round, diplsay player info
    if sg_bot.updateRound: 
        sg_bot.displayPlayerInfo()
        sg_bot.addOpponentTally()
        print("Opponent Tally:")
        sg_bot.displayOpponentTally()
    
    # Keep taking turns while there are still coins
    while sg_bot.coinCountCheck(1):
        if sg_bot.game_info.round_num < 5:
            sg_bot.performBestOption()
        else:
            # Consider the best shop pet and the worst owned pet
            worst_pet_index, worst_pet, worst_pet_stat_sum = sg_bot.getPetMinStatSum()
            best_shop_pet, best_shop_pet_stat_sum = sg_bot.getPetMinStatSum()[1:]

            # While a better pet is in the shop, buy it if possible or freeze it.
            while best_shop_pet_stat_sum > worst_pet_stat_sum:
                if sg_bot.coinCountCheck(best_shop_pet.cost - worst_pet.level):
                    sg_bot.buyPet(best_shop_pet, worst_pet_index)
                else:
                    sg_bot.freeze(best_shop_pet)

                # Get new best shop pet and worst owned pet
                worst_pet, worst_pet_stat_sum = sg_bot.getPetMinStatSum()[1:]
                best_shop_pet, best_shop_pet_stat_sum = sg_bot.getPetMinStatSum()[1:]

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
                        sg_bot.freeze(food_item[1])
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
    sg_bot.endTurn()