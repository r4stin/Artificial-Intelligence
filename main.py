import random
from functools import reduce
from enum import Enum
from copy import deepcopy
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn import tree


# Food class is used to store the food type, amount and expiry
class Food:
    FoodType = 0
    amount = 0
    expiry = 0

    def __init__(self, food_type, amount, expiry):
        self.food_type = food_type
        self.amount = amount
        self.expiry = expiry

    # Food types are defined as an enum from 1 to 5
    class FoodTypes(Enum):
        Dairy = 1
        Meat = 2
        Fruits = 3
        Vegetables = 4
        Grains = 5


# Generate random numbers for consumption for each food type
def random_sum(total_sum):
    nums = []
    food_type_Num = 5
    for rand_num in range(food_type_Num - 1):
        nums.append(random.randint(int(total_sum / (food_type_Num + 1)), int(total_sum / (food_type_Num - 1))))
    nums.append(total_sum - sum(nums))
    random.shuffle(nums)
    return nums


# Consume the food and return the remaining food and hunger
def consume(foods):
    hunger = 0
    n = random_sum(4000)
    foodsToConsume = deepcopy(foods)
    for i in range(len(foodsToConsume)):
        if foodsToConsume[i].amount > n[i]:  # compare the amount of food with the amount of food to consume
            foodsToConsume[i].amount -= n[i]  # if the amount of food is greater than the amount of food to consume,
                                             #subtract the amount of food to consume from the amount of food
        else:  # if the amount of food is less than the amount of food to consume,
                # subtract the amount of food from the amount of food to consume and set the amount of food to 0
            n[i] -= foodsToConsume[i].amount
            foodsToConsume[i].amount = 0
            while n[i] > 0:  # if the amount of food to consume is greater than 0, find the food with the maximum amount
                maxFood = 0
                maxFoodIndex = 0
                for j in range(len(foodsToConsume)):
                    if maxFood < foodsToConsume[j].amount: # find the food with the maximum amount
                        maxFood = foodsToConsume[j].amount
                        maxFoodIndex = j
                if foodsToConsume[maxFoodIndex].amount > n[i]:
                    foodsToConsume[maxFoodIndex].amount -= n[i]
                    n[i] = 0
                else:
                    n[i] -= foodsToConsume[maxFoodIndex].amount
                    foodsToConsume[maxFoodIndex].amount = 0
                if lambda foodsToConsume: reduce(lambda x, y: x + y.amount, foods, 0) == 0: # if the sum of the amount of food is 0, break
                    hunger += n[i]
                    break
    return foodsToConsume, hunger


# Day class is used to store the food, day, hunger, waste and yesterday
class Day:
    foods = []
    day = 0
    hunger = 0
    waste = 0
    yesterday = None

    def __init__(self, foods, day=0, hunger=0, waste=0, yesterday=None):
        self.foods = foods
        self.day = day
        self.hunger = hunger
        self.waste = waste
        self.yesterday = yesterday

    # Return the sum of the food amounts
    def getSum(self):
        return sum(food.amount for food in self.foods)


# select best states and remove the foods that are expired
def removeExtraStates(_states, n=100):
    #  remove the states that have expired food
    lastday = 0
    for i in range(len(_states)):
        if _states[i].day > lastday:
            lastday = _states[i].day
        for j in range(len(_states[i].foods)):
            if _states[i].foods[j].expiry <= _states[i].day:  # if the expiry of the food is less than the day,
                _states[i].waste += _states[i].foods[j].amount  # add the amount of food to the waste and set the amount of food to 0
                _states[i].foods[j].amount = 0

    Lastday =[]
    remaningDays = []

    for j in range(len(_states)):
        if _states[j].day == lastday:
            Lastday.append(_states[j])
        else:
            remaningDays.append(_states[j])
    sortedList = sorted(Lastday, key=lambda x: (x.foods[0].amount, x.foods[1].amount, x.foods[2].amount,
                                                x.foods[3].amount, x.foods[4].amount), reverse=False) # sort the states based on the amount of food
    result = remaningDays + sortedList[:n] # add the best states to first n states

    return result



def main():
    foods = []
    states = []
    # generate the input amounts and expiry dates for each food type

    foods.append(Food(Food.FoodTypes.Dairy, random.randint(10000, 10500), 7))
    foods.append(Food(Food.FoodTypes.Meat, random.randint(15000, 15500), 14))
    foods.append(Food(Food.FoodTypes.Fruits, random.randint(25000, 25500), 18))
    foods.append(Food(Food.FoodTypes.Vegetables, random.randint(30000, 30500), 22))
    foods.append(Food(Food.FoodTypes.Grains, random.randint(40000, 40500), 31))

    currentDay = Day(foods)
    waste = 0
    while currentDay.day < 30: # run the simulation for 30 days
        for food in range(50):
            newFood, hunger = consume(currentDay.foods.copy()) # consume the food and get the remaining food and hunger
            states.append(
                Day(newFood, currentDay.day + 1, currentDay.hunger + hunger, currentDay.waste + waste, currentDay)) # add the new state to the states list

            states = removeExtraStates(states) # select the best states and remove the foods that are expired
        currentDay = states[0]
        states.remove(states[0])

    states.append(currentDay)
    # bestState = states[0]
    # print the output for last day
    for state in range(len(states)):
        print()
        print((state + 1), ") end of Day ", states[state].day, "  -  ", states[state].getSum())
        summ = 0
        for food in range(len(states[state].foods)):
            print(" ", states[state].foods[food].food_type.name, " ", states[state].foods[food].amount)
        print("hunger: ", states[state].hunger)
        print("waste: ", states[state].waste)
        # find and print the best root of the tree from day 1 to day 30

    bestState = sorted(states, key=lambda x: (x.hunger, -x.getSum()))[0] # sort the states based on the hunger and available food

    print("------------------------------------")
    bestSituations = []
    while bestState.yesterday is not None:  # save yesterday's state to find the best root
        print()
        print("Day ", bestState.day, "  -  ", bestState.getSum())
        for food in range(len(bestState.foods)):
            print(" ", bestState.foods[food].food_type.name, " ", bestState.foods[food].amount)
        print("hunger: ", bestState.hunger)
        print("waste: ", bestState.waste)
        bestState = bestState.yesterday
        bestSituations.append(bestState)

    # List of hunger values
    hunger_values = [state.hunger for state in bestSituations]

    # List of waste values
    waste_values = [state.waste for state in bestSituations]

    # List of days
    days = [state.day for state in bestSituations]

    # Plot hunger and waste curves on the same plot
    plt.plot(days, hunger_values, color='red', label='Hunger')
    plt.xlabel('Day')
    plt.ylabel('Value')
    plt.title('Hunger over Time')
    plt.legend()
    plt.show()
    plt.plot(days, waste_values, color='blue', label='Waste')
    plt.xlabel('Day')
    plt.ylabel('Value')
    plt.title('Waste over Time')
    plt.legend()
    plt.show()

  


if __name__ == "__main__":
    main()
