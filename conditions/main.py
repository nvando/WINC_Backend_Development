# Do not modify these lines
__winc_id__ = "25596924dffe436da9034d43d0af6791"
__human_name__ = "conditions"

# Add your code after this line

# weather, time_of_day, milking_status, location, season, tank, grass


def farm_action(weather, time_of_day, milking_status, location, season, tank, grass):
    if location == "pasture":
        if weather == "rainy" or time_of_day == "night":
            return "take cows to cowshed"
        elif milking_status:
            return "take cows to cowshed\nmilk cows\ntake cows back to pasture"
        elif tank == True and (weather != "sunny" and weather != "windy"):
            return "take cows to cowshed\nfertilize pasture\ntake cows back to pasture"
        elif grass == True and season == "spring" and weather == "sunny":
            return "take cows to cowshed/nmow grass\ntake cows back to pasture"
        else:
            return "wait"
    if location == "cowshed":
        if milking_status:
            return "milk cows"
        elif tank == True and (weather != "sunny" and weather != "windy"):
            return "fertilize pasture"
        elif grass == True and season == "spring" and weather == "sunny":
            return "mow grass"
        else:
            return "wait"
    else:
        return "wait"


print(farm_action("clear", "day", False, "pasture", "spring", True, True))
