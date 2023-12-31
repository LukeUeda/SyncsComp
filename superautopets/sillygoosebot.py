from submissionhelper.botbattle import BotBattle
from submissionhelper.info.gameinfo import GameInfo
from submissionhelper.info.pettype import PetType
from submissionhelper.info.foodtype import FoodType

# Core class for the submission helper
# Use this to make moves and get game info
bot_battle = BotBattle()
#awedaedcadwdawdadwaddwda
# Core game loop
# Each iteration you will be expected to make one move
prev_round_num = 0


def sillyOuput(game_info):
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




while True:
    # This function will pause until the game engine
    # is ready for you to make a move. Always call it
    # before making a move. It provides the information
    # required to make a sensible move
    game_info = bot_battle.get_game_info()

    #           print(game_info.remaining_moves)
    #           print(game_info, flush = True)
    #           print("", flush = True)

    # How to detect whether it is a new round
    new_round = prev_round_num != game_info.round_num
    if new_round:
        
        print(f"\nRound #{game_info.round_num}\n")
        sillyOuput(game_info)
        prev_round_num = game_info.round_num

    # Now let's go through a very simple (and poorly written!)
    # example submission
    def make_move(game_info: 'GameInfo'):

        # Look for horse in round one
        if prev_round_num == 1 and game_info.player_info.pets[4] == None and game_info.player_info.coins >= 9:
            print("Looking for horse")
            for shop_pet in game_info.player_info.shop_pets:
                if(shop_pet.type == PetType.HORSE):
                    print("WE BOUGHT A HORSE YIPEE")
                    bot_battle.buy_pet(shop_pet, 4)
                    return
            
            if(game_info.player_info.coins == 10):
                bot_battle.reroll_shop()
                return

        # Fill empty spaces
        for shop_pet in game_info.player_info.shop_pets:
            for i, pet in enumerate(game_info.player_info.pets):
                if pet == None and shop_pet.cost <= game_info.player_info.coins and shop_pet.type != PetType.BEE:
                    print("Buying", shop_pet.id, " at position", i)
                    bot_battle.buy_pet(shop_pet, i)
                    return
                

        for shop_pet_index, shop_pet in enumerate(game_info.player_info.shop_pets):
            for pet_index, pet in enumerate(game_info.player_info.pets):
                # If a shop pet beats an owned pet...
                if pet != None:
                    if pet.health + pet.attack < shop_pet.attack + shop_pet.health and shop_pet.type != PetType.BEE:
                        if(shop_pet.cost <= game_info.player_info.coins):
                            # Replace if there are enough coins
                            if game_info.remaining_moves < 2:
                                bot_battle.end_turn()
                                return

                            bot_battle.sell_pet(pet)

                            game_info = bot_battle.get_game_info()

                            shop_pet = game_info.player_info.shop_pets[shop_pet_index]
                            bot_battle.buy_pet(shop_pet, pet_index)
                            return
                        elif(not shop_pet.is_frozen):
                            # Otherwise freeze for next turn
                            bot_battle.freeze_pet(shop_pet)
                            return
        
        for shop_food_index, shop_food in enumerate(game_info.player_info.shop_foods):
            # If a food has an ongoing effect...
            if shop_food.type in [FoodType.MEAT_BONE, FoodType.GARLIC]:
                for pet_index, pet in enumerate(game_info.player_info.pets):
                    # Ensure that it will not override a currently existing one and purchase if possible.
                    if pet != None:
                        if pet.carried_food == None: 
                            if(shop_food.cost <= game_info.player_info.coins):
                                bot_battle.buy_food(shop_food, pet)
                                return
                            elif(not shop_food.is_frozen):
                                bot_battle.freeze_food(shop_food)
                                return
            # If a food is a single use on a selected pet...
            elif shop_food.type in [FoodType.APPLE, FoodType.PEAR, FoodType.CUPCAKE]:
                # Find the pet with max stats and feed them the food if possible
                max_stat_pet = None
                for pet_index, pet in enumerate(game_info.player_info.pets):
                    if pet != None:
                        if(max_stat_pet == None or max_stat_pet.health + max_stat_pet.attack < pet.health + pet.attack):
                            max_stat_pet = pet
                if max_stat_pet != None:
                    if(shop_food.cost <= game_info.player_info.coins):
                        bot_battle.buy_food(shop_food, max_stat_pet)
                        return
                    elif(not shop_food.is_frozen):
                        bot_battle.freeze_food(shop_food)
                        return
            elif(shop_food.type != FoodType.HONEY):
                if(shop_food.cost <= game_info.player_info.coins):
                    bot_battle.buy_food(shop_food)
                    return
                elif(not shop_food.is_frozen):
                    bot_battle.freeze_food(shop_food)
                    return

        if game_info.player_info.coins == 0:
            bot_battle.end_turn()
        else:
            bot_battle.reroll_shop()

    # Last but not least, don't forget to call the function!
    make_move(game_info)