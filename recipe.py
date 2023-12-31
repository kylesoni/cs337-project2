from ingredient import Ingredient
from step import Step
import re

class Recipe:

    def __init__(self, scraped_ingredients, scraped_steps):
        
        self.ingredients = []
        self.steps = []
        self.tools = []
        self.methods = []
        self.ingredient_groups = {"generic" : []}
        self.current_temp = ""

        self.current_step = -1

        current_category = "generic"
        for i in range(len(scraped_ingredients)):
            if ":" in scraped_ingredients[i]:
                current_category = re.sub(":", "", scraped_ingredients[i]).lower()
            else:
                ing = Ingredient(scraped_ingredients[i])
                self.ingredients.append(ing)
                if current_category in self.ingredient_groups:
                    self.ingredient_groups[current_category].append(ing)
                else:
                    self.ingredient_groups[current_category] = [ing]

        current_category = "generic"
        for i in range(len(scraped_steps)):
            for key in list(self.ingredient_groups.keys()):
                key_words = key.split()
                for word in key_words:
                    if word in scraped_steps[i].lower():
                        current_category = key
            if current_category in self.ingredient_groups:
                new_step = Step(scraped_steps[i], self.ingredient_groups[current_category])
                self.steps.append(new_step)
                if new_step.settings["Oven"].replace(" ", "") != "":
                    self.current_temp = self.steps[i].settings["Oven"]
                    new_step.current_temp = self.steps[i].settings["Oven"]
                else:
                    new_step.current_temp = self.current_temp

    def progress_step(self):
        if self.current_step + 1 < len(self.steps):
            self.current_step += 1
            return self.steps[self.current_step]
        else:
            return "You have reached the end of the recipe!"
        
    def regress_step(self):
        if self.current_step - 1 >= 0:
            self.current_step -= 1
            return self.steps[self.current_step]
        else:
            return "You are on the first step of the recipe!"

    def test_ingredients(self):
        for i in range(len(self.ingredients)):
            print("Amount: " + self.ingredients[i].amount)
            print("Amount Clarification: " + self.ingredients[i].amount_clar)
            print("Unit: " + self.ingredients[i].unit)
            print("Ing: " + self.ingredients[i].ingredient)
            print("Prep: " + self.ingredients[i].prep)
            print("Description: " + self.ingredients[i].desc)
            print("Tools: " + str(self.ingredients[i].tools))
            print("")

    def test_ingredient_groups(self):
        keys = list(self.ingredient_groups.keys())
        for i in range(len(keys)):
            print(keys[i])
            print(self.ingredient_groups[keys[i]])
            print("")

    def test_steps(self):
        for i in range(len(self.steps)):
            act_ing = []
            for j in range(len(self.steps[i].ingredients)):
                act_ing.append(self.steps[i].ingredients[j].ingredient)
            print("Step: " + self.steps[i].text)
            print("Ingredients: " + str(act_ing))
            print("Tools: " + str(self.steps[i].tools))
            print("Methods: " + str(self.steps[i].methods))
            print("Time: " + str(self.steps[i].time))
            print("Settings: " + str(self.steps[i].settings))
            print("")