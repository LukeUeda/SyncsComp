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
FISH_LEVEL_UP_BONUS = 8

REROLL_THRESHOLD = 5
FREEZE_THRESHOLD = 7

POSITION_ONE_BLACKLIST = [
    PetType.BUNNY,
    PetType.KANGAROO,
    PetType.GIRAFFE,
    PetType.CRAB,
    PetType.HORSE,
    PetType.DODO,
    PetType.DOG,
    PetType.PENGUIN
]

POSITION_TWO_BLACKLIST = [
    PetType.BUNNY,
    PetType.HORSE,
    PetType.DOG,
    PetType.PENGUIN
]

POSITION_THREE_BLACKLIST = [
    PetType.BUNNY,
    PetType.HORSE,
    PetType.DOG,
    PetType.PENGUIN
]
    
POSITION_FOUR_BLACKLIST = [

]
    
POSITION_FIVE_BLACKLIST = [
    PetType.FLAMINGO,
    PetType.CAMEL,
    PetType.ELEPHANT,
    PetType.FLAMINGO
]

POSITION_BLACKLIST = [
    POSITION_ONE_BLACKLIST,
    POSITION_TWO_BLACKLIST,
    POSITION_THREE_BLACKLIST,
    POSITION_FOUR_BLACKLIST,
    POSITION_FIVE_BLACKLIST
]

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
                for pet in self.game_info.player_info.shop_pets:
                    if pet != None:
                        if pet.type == shop_pet.type:
                            shop_pet = pet
                            break
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
    
    def findBestTierThreeShopPet(self, ignore_frozen = True):
        best_pet_score = 0
        best_pet = None
        for shop_pet in self.game_info.player_info.shop_pets:
            current_pet_score = self.getTierThreeShopPetScore(shop_pet)
            if current_pet_score >= best_pet_score and shop_pet.type not in self.shop_ignore_list:
                if not ignore_frozen or (ignore_frozen and not shop_pet.is_frozen):
                    best_pet_score = current_pet_score
                    best_pet = shop_pet

        return best_pet, best_pet_score
    
    def findBestTierFourShopPet(self, ignore_frozen = True):
        best_pet_score = 0
        best_pet = None
        for shop_pet in self.game_info.player_info.shop_pets:
            current_pet_score = self.getTierFourShopPetScore(shop_pet)
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
                if current_pet_score < worst_pet_score:
                    worst_pet_score = current_pet_score
                    worst_pet = pet

        return worst_pet, worst_pet_score
    
    def findWorstTierTwoOwnedPet(self):
        worst_pet_score = 300
        worst_pet = None
        for pet in self.game_info.player_info.pets:
            if pet != None:
                current_pet_score = self.getTierTwoShopPetScore(pet)
                if current_pet_score < worst_pet_score:
                    worst_pet_score = current_pet_score
                    worst_pet = pet

        return worst_pet, worst_pet_score
        
    def findWorstTierThreeOwnedPet(self):
        worst_pet_score = 300
        worst_pet = None
        for pet in self.game_info.player_info.pets:
            if pet != None:
                current_pet_score = self.getTierThreeShopPetScore(pet)
                if current_pet_score < worst_pet_score:
                    worst_pet_score = current_pet_score
                    worst_pet = pet

        return worst_pet, worst_pet_score
    
    def findWorstTierFourOwnedPet(self):
        worst_pet_score = 300
        worst_pet = None
        for pet in self.game_info.player_info.pets:
            if pet != None:
                current_pet_score = self.getTierFourShopPetScore(pet)
                if current_pet_score < worst_pet_score:
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

    def findBestTierTwoOwnedPet(self):
        best_pet_score = 0
        best_pet = None
        for pet in self.game_info.player_info.pets:
            if pet != None:
                current_pet_score = self.getTierTwoShopPetScore(pet)
                if current_pet_score >= best_pet_score:
                    best_pet_score = current_pet_score
                    best_pet = pet

        return best_pet, best_pet_score

    def findBestTierThreeOwnedPet(self):
        best_pet_score = 0
        best_pet = None
        for pet in self.game_info.player_info.pets:
            if pet != None:
                current_pet_score = self.getTierThreeShopPetScore(pet)
                if current_pet_score >= best_pet_score:
                    best_pet_score = current_pet_score
                    best_pet = pet

        return best_pet, best_pet_score
    
    def findBestTierFourOwnedPet(self):
        best_pet_score = 0
        best_pet = None
        for pet in self.game_info.player_info.pets:
            if pet != None:
                current_pet_score = self.getTierFourShopPetScore(pet)
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

        # TIER ONE CONSIDERATION
        if pet.type == PetType.FISH:
            if self.ownsPet(PetType.FISH):
                score += 6
                if self.getPet(PetType.FISH)[0].level >= 2:
                    score += FISH_LEVEL_UP_BONUS + self.getPet(PetType.FISH)[0].sub_level

        # CONSIDERING PEACOCK
        if pet.type == PetType.PEACOCK:
            if type(pet) == PlayerPetInfo:
                score += 10
            elif self.ownsPet(PetType.PEACOCK):
                if self.getPet(PetType.PEACOCK)[0].level == 2:
                    score = 0
            else:
                score += 10

        if pet.type == PetType.FLAMINGO:
            score += 7

        # CONSIDERING KANGAROO
        if pet.type == PetType.KANGAROO:
            if type(pet) == PlayerPetInfo:
                score += 10
            elif self.ownsPet(PetType.KANGAROO):
                if self.getPet(PetType.KANGAROO)[0].level == 2:
                    score = 0
            else:
                score += 10

        if pet.type == PetType.SPIDER:
            score += 3
            if self.ownsPet(PetType.HORSE) or self.shopHasPet(PetType.HORSE):
                score += SUMMONER_BONUS

        # CONSIDERING CRAB
        if pet.type == PetType.CRAB:
            if self.ownsPet(PetType.CRAB):
                if self.getPet(PetType.CRAB)[0].level >= 2:
                    score += 200
            score += 7
            max_health = 0
            for pet in self.game_info.player_info.pets:
                
                if pet != None:
                    if pet.health > max_health:
                        max_health = pet.health
                
                if max_health > 14:
                    score += 10
                elif max_health > 8:
                    score += 5
                

        return score

    def getTierThreeShopPetScore(self, pet):
        score = 0

        # TIER ONE CONSIDERATION
        if pet.type == PetType.FISH:
            if self.ownsPet(PetType.FISH):
                score += 6
                if self.getPet(PetType.FISH)[0].level >= 2:
                    score += FISH_LEVEL_UP_BONUS + self.getPet(PetType.FISH)[0].sub_level

        # TIER TWO CONSIDERATIONS
        if pet.type == PetType.FLAMINGO:
                score += 3

        if pet.type == PetType.SPIDER:
            score += 1
        if pet.type == PetType.KANGAROO:
            if type(pet) == PlayerPetInfo:
                score += 10
            elif self.ownsPet(PetType.KANGAROO):
                if self.getPet(PetType.KANGAROO)[0].level == 2:
                    score = 0
            else:
                score += 10


        if pet.type == PetType.PEACOCK:
            if type(pet) == PlayerPetInfo:
                score += 10
            elif self.ownsPet(PetType.PEACOCK):
                if self.getPet(PetType.PEACOCK)[0].level == 2:
                    score = 0
            else:
                score += 10

        if pet.type == PetType.CRAB:
            if self.ownsPet(PetType.CRAB):
                if self.getPet(PetType.CRAB)[0].level >= 2:
                    score += 200
            score += 7
            max_health = 0
            for p in self.game_info.player_info.pets:
                
                if p != None:
                    if p.health > max_health:
                        max_health = p.health
                
                if max_health > 20:
                    score += 10
                elif max_health > 15:
                    score += 5

        # TIER THREE CONSIDERATIONS
        if pet.type == PetType.GIRAFFE:
            score += 10

        if pet.type == PetType.BUNNY:
            score += 7
            if self.ownsPet(PetType.CRAB):
                score += 5
            if type(pet) == ShopPetInfo and self.ownsPet(pet.type):
                score -= 10

        if pet.type == PetType.CAMEL:
            score += 7
            if self.ownsPet(PetType.KANGAROO):
                score += 3

        if pet.type == PetType.ELEPHANT:
            if self.ownsPet(PetType.PEACOCK) or self.ownsPet(PetType.CAMEL):
                score += 7

        if pet.type == PetType.DODO:
            score += 7
            if self.ownsPet(PetType.CRAB):
                score += 8
        return score
    
    def getTierFourShopPetScore(self, pet):
        score = 0

        # TIER ONE CONSIDERATION
        if pet.type == PetType.FISH:
            score += 3
            if self.ownsPet(PetType.FISH):
                if self.getPet(PetType.FISH)[0].level >= 2:
                    score += FISH_LEVEL_UP_BONUS + self.getPet(PetType.FISH)[0].sub_level

        # TIER TWO CONSIDERATIONS
        if pet.type == PetType.CAMEL:
            score += 7

        if pet.type == PetType.PEACOCK:
            if type(pet) == PlayerPetInfo:
                score += 10
            elif self.ownsPet(PetType.PEACOCK):
                if self.getPet(PetType.PEACOCK)[0].level == 2:
                    score = 0
            else:
                score += 10

        if pet.type == PetType.KANGAROO:
            if type(pet) == PlayerPetInfo:
                score += 10
            elif self.ownsPet(PetType.KANGAROO):
                if self.getPet(PetType.KANGAROO)[0].level == 2:
                    score = 0
            else:
                score += 10

        if pet.type == PetType.CRAB:
            if self.ownsPet(PetType.CRAB):
                if self.getPet(PetType.CRAB)[0].level >= 2:
                    score += 200
            score += 6
            score += self.getHealthiestPet().health

        # TIER THREE CONSIDERATIONS
        if pet.type == PetType.GIRAFFE:
            score += 7

        if pet.type == PetType.BUNNY:
            score += 7
            if self.ownsPet(PetType.CRAB):
                score += 5
            if type(pet) == ShopPetInfo and self.ownsPet(pet.type):
                score -= 10

        # TIER FOUR CONSIDERATIONS

        if pet.type == PetType.BISON:
            for p in self.game_info.player_info.pets:
                
                if p != None:
                    if p.level == 3:
                        score += 15
                        

        if pet.type == PetType.PENGUIN:
            for p in self.game_info.player_info.pets:
                if p != None:
                    if p.level > 1:
                        score += 10

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
            if pet != None:
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
        elif self.game_info.round_num < 7:
            return self.findBestTierThreeShopPet(ignore_frozen=ignoreFrozen)
        else:
            return self.findBestTierFourShopPet(ignore_frozen=ignoreFrozen)
        
    def findBestShopFood(self, ignoreFrozen = True):
        best_shop_food = None
        best_shop_food_score = 0
        best_shop_food_target = None
        for shop_food in self.game_info.player_info.shop_foods:
            current_score, current_target = self. getShopFoodScore(shop_food)
            if current_score > best_shop_food_score and shop_food.type not in self.shop_ignore_list:
                if not ignoreFrozen or (ignoreFrozen and not shop_food.is_frozen):
                    best_shop_food = shop_food
                    best_shop_food_score = current_score
                    best_shop_food_target = current_target
        
        return best_shop_food, best_shop_food_score, best_shop_food_target

    def getShopPetScore(self, pet):
        if self.game_info.round_num < 3:
            return self.getTierOneShopPetScore(pet)
        elif self.game_info.round_num < 5:
            return self.getTierTwoShopPetScore(pet)
        elif self.game_info.round_num < 10:
            return self.getTierThreeShopPetScore(pet)
        else:
            return self.getTierFourShopPetScore(pet)

    def findWorstOwnedPet(self):
        if self.game_info.round_num < 3:
            return self.findWorstTierOneOwnedPet()
        elif self.game_info.round_num < 5:
            return self.findWorstTierTwoOwnedPet()
        elif self.game_info.round_num < 10:
            return self.findWorstTierThreeOwnedPet()
        else:
            return self.findWorstTierFourOwnedPet()
        
    def findBestOwnedPet(self):
        if self.game_info.round_num < 3:
            return self.findBestTierOneOwnedPet()
        elif self.game_info.round_num < 5:
            return self.findBestTierTwoOwnedPet()
        elif self.game_info.round_num < 10:
            return self.findBestTierThreeOwnedPet()
        else:
            return self.findBestTierFourOwnedPet()


    def getHealthiestPet(self):
        max_health = 0
        max_health_pet = None
        for pet in self.game_info.player_info.pets:
            if pet != None:
                if max_health_pet == None or pet.health > max_health:
                    max_health = pet.health
                    max_health_pet = pet

        return max_health_pet


    def getShopFoodScore(self, shop_food):
        score = 5
        target = self.findBestOwnedPet()[0]

        if shop_food.type == FoodType.PEAR or shop_food.type == FoodType.APPLE or shop_food.type == FoodType.SALAD_BOWL or shop_food.type == FoodType.CUPCAKE and self.game_info.round_num > 2:
            score += 2
            if self.ownsPet(PetType.PEACOCK) or self.ownsPet(PetType.CAMEL) or self.ownsPet(PetType.CRAB) or self.ownsPet(PetType.DODO):
                min_stat = 0
                min_stat_pet = None
                for pet in self.game_info.player_info.pets:
                    if pet != None:
                        if min_stat_pet == None or pet.health + pet.attack < min_stat and pet.type in [PetType.PEACOCK, PetType.CAMEL, PetType.DODO, self.game_info.player_info.pets[self.getPet(PetType.CRAB)[1] - 1].type]:
                            min_stat_pet = pet
                            min_stat = pet.health + pet.attack
                
                target = min_stat_pet
            else:
                score -= 10

        if shop_food.type in [FoodType.HONEY, FoodType.MEAT_BONE, FoodType.GARLIC]:
            score += 1

        if shop_food.type == FoodType.MEAT_BONE:
            bestpet = None
            for pet in self.game_info.player_info.pets:
                if pet.carried_food == None:
                    if pet.type == PetType.CRAB: 
                        score += 2
                        return score, pet
                    elif pet.type not in [PetType.PEACOCK, PetType.HORSE]:
                        bestpet = pet
            if bestpet != None:
                target = bestpet

        if shop_food.type == FoodType.GARLIC:
            bestpet = None
            for pet in self.game_info.player_info.pets:
                if pet.carried_food == None:
                    if pet.type == PetType.PEACOCK: 
                        score += 2
                        return score, pet
                    elif pet.health < 15 and pet.attack > 10 and bestpet == None:
                        bestpet = pet

            if bestpet != None:
                target = bestpet
            else:
                score -= 6

        return score, target

    def getIdealPetForPosition(self, pos):
        candidates = []
        for i in range(pos, 5):
            pet = self.game_info.player_info.pets[i]
            if pet != None:
                if pet.type not in POSITION_BLACKLIST[pos]:
                    candidates.append(pet)
        
        candidate_types = []
        print("POSITION ", pos, " CANDIDATES", flush=True)
        for pet in candidates:
            print("   -", pet.type, flush=True)
            candidate_types.append(pet.type)

        if pos == 0:
            if PetType.CRICKET in candidate_types and self.ownsPet(PetType.HORSE):
                return candidates[candidate_types.index(PetType.CRICKET)]
            
            if PetType.FLAMINGO in candidate_types:
                return candidates[candidate_types.index(PetType.FLAMINGO)]

            if PetType.ELEPHANT in candidate_types and self.ownsPet(PetType.PEACOCK):
                return candidates[candidate_types.index(PetType.ELEPHANT)]
            
            if PetType.PEACOCK in candidate_types:
                return candidates[candidate_types.index(PetType.PEACOCK)]
            
            if len(candidates) > 0:
                return candidates[0]
            else:
                return None
        
        elif pos == 1:
            if PetType.PEACOCK in candidate_types and self.ownsPet(PetType.ELEPHANT):
                return candidates[candidate_types.index(PetType.PEACOCK)]

            if PetType.CRAB in candidate_types and self.game_info.player_info.pets[pos - 1] == self.getHealthiestPet():
                return candidates[candidate_types.index(PetType.CRAB)]
            elif PetType.CRAB in candidate_types:
                candidates.pop(candidate_types.index(PetType.CRAB))
                candidate_types.pop(candidate_types.index(PetType.CRAB))

            if PetType.CRICKET in candidate_types and self.ownsPet(PetType.HORSE):
                return candidates[candidate_types.index(PetType.CRICKET)]
            
            if PetType.CAMEL in candidate_types and self.ownsPet(PetType.KANGAROO):
                return candidates[candidate_types.index(PetType.CAMEL)]
            
            if len(candidates) > 0:
                return candidates[0]
            else:
                return None
            
        elif pos == 2:
            if PetType.CRAB in candidate_types and self.game_info.player_info.pets[pos - 1] == self.getHealthiestPet():
                return candidates[candidate_types.index(PetType.CRAB)]
            elif PetType.CRAB in candidate_types:
                candidates.pop(candidate_types.index(PetType.CRAB))
                candidate_types.pop(candidate_types.index(PetType.CRAB))

            if PetType.CRICKET in candidate_types and self.ownsPet(PetType.HORSE):
                return candidates[candidate_types.index(PetType.CRICKET)]
            
            if PetType.CAMEL in candidate_types and self.ownsPet(PetType.KANGAROO):
                return candidates[candidate_types.index(PetType.CAMEL)]

            if PetType.KANGAROO in candidate_types and self.ownsPet(PetType.CAMEL):
                return candidates[candidate_types.index(PetType.KANGAROO)]
            
            if len(candidates) > 0:
                return candidates[0]
            else:
                return None
            
        elif pos == 3:
            if PetType.CRAB in candidate_types and self.game_info.player_info.pets[pos - 1] == self.getHealthiestPet():
                return candidates[candidate_types.index(PetType.CRAB)]
            elif PetType.CRAB in candidate_types:
                candidates.pop(candidate_types.index(PetType.CRAB))
                candidate_types.pop(candidate_types.index(PetType.CRAB))

            if PetType.CRICKET in candidate_types and self.ownsPet(PetType.HORSE):
                return candidates[candidate_types.index(PetType.CRICKET)]
            
            if PetType.CAMEL in candidate_types and self.ownsPet(PetType.KANGAROO):
                return candidates[candidate_types.index(PetType.CAMEL)]

            if PetType.KANGAROO in candidate_types and self.ownsPet(PetType.CAMEL):
                return candidates[candidate_types.index(PetType.KANGAROO)]
            
            if PetType.GIRAFFE in candidate_types:
                return candidates[candidate_types.index(PetType.GIRAFFE)]

            if len(candidates) > 0:
                return candidates[0]
            else:
                return None
            
        elif pos == 4:
            if PetType.CRAB in candidate_types and self.game_info.player_info.pets[pos - 1] == self.getHealthiestPet():
                return candidates[candidate_types.index(PetType.CRAB)]
            elif PetType.CRAB in candidate_types:
                candidates.pop(candidate_types.index(PetType.CRAB))
                candidate_types.pop(candidate_types.index(PetType.CRAB))
            
            if PetType.CRICKET in candidate_types and self.ownsPet(PetType.HORSE):
                return candidates[candidate_types.index(PetType.CRICKET)]
            
            if PetType.BUNNY in candidate_types:
                return candidates[candidate_types.index(PetType.BUNNY)]
            
            if PetType.PENGUIN in candidate_types:
                return candidates[candidate_types.index(PetType.PENGUIN)]
            
            if PetType.HORSE in candidate_types:
                return candidates[candidate_types.index(PetType.HORSE)]
            
            if len(candidates) > 0:
                return candidates[0]
            else:
                return None
        else:

            if len(candidates) > 0:
                return candidates[0]
            else:
                return None

    def repositionPets(self):
        print("REPOSITIONING:", flush=True)
        for i in range(0,5):
            ideal_pet = self.getIdealPetForPosition(i)
            if ideal_pet != None:
                ideal_pet_index = self.game_info.player_info.pets.index(ideal_pet)
                print("For index ", ideal_pet_index, ": ", ideal_pet.type, flush=True)
                if ideal_pet_index != i:
                    bot_battle.swap_pets(ideal_pet_index, i)
                    self.getGameInfo()



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

        print("Ignored: ", self.shop_ignore_list, flush=True)
        print("Worst Pet: ", self.findWorstOwnedPet()[1], flush=True)

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
                        print("I can't afford the ", target_pet.type, " but it is worth freezing", flush=True)
                        self.freeze(shop_pet)
                        self.shop_ignore_list.append(b_shop_pet.type)
                    else:
                        print("I can't afford the", b_shop_pet.type, " and its not worth freezing", flush=True)
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
                        print("I can't afford the ", b_shop_pet.type, " but it is worth freezing", flush=True)
                        self.freeze(shop_pet)
                        self.shop_ignore_list.append(b_shop_pet.type)
                    else:
                        print("I can't afford the", b_shop_pet.type, " and its not worth freezing", flush=True)
                        self.shop_ignore_list.append(b_shop_pet.type)

                elif self.findWorstOwnedPet()[1] < b_shop_pet_score:
                    # Finally, if there is a pet with a worst score than the shop and the pet can be afforded, buy it
                    if self.coinCountCheck(b_shop_pet.cost):
                        print(self.findWorstOwnedPet()[0].type, " is worse than", b_shop_pet.type, " so Imma replace it", flush=True)
                        self.buyPet(b_shop_pet, self.game_info.player_info.pets.index(self.findWorstOwnedPet()[0]))
                    else:
                        print("I can't afford the", b_shop_pet.type, " and its not worth freezing", flush=True)
                        self.shop_ignore_list.append(b_shop_pet.type)
                else:
                    print("The pet is good, but it doesn't beat my other pets")
                    self.shop_ignore_list.append(b_shop_pet.type)
            elif b_shop_food_score > REROLL_THRESHOLD and b_shop_food != None:
                if self.coinCountCheck(b_shop_food.cost):
                    self.buyFood(b_shop_food, b_shop_food_target)
                elif b_shop_food_score > FREEZE_THRESHOLD:
                    self.freeze(b_shop_food)
                    self.shop_ignore_list.append(b_shop_food.type)
                else:
                    self.shop_ignore_list.append(b_shop_food.type)
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
        sg_bot.performBestOption()
    sg_bot.repositionPets()
    sg_bot.endTurn()