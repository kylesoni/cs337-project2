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
                if new_step.settings["Oven"] != "":
                    self.current_temp = self.steps[i].settings["Oven"]

    def progress_step(self):
        if self.current_step + 1 < len(self.steps):
            self.current_step += 1
            return self.steps[self.current_step]
        else:
            return "You have reached the end of the recipe!"

    def test_ingredients(self):
        for i in range(len(self.ingredients)):
            print("Amount: " + self.ingredients[i].amount)
            print("Unit: " + self.ingredients[i].unit)
            print("Ing: " + self.ingredients[i].ingredient)
            print("Prep: " + self.ingredients[i].prep)
            print("Description: " + self.ingredients[i].desc)
            print("")

    def test_ingredient_groups(self):
        keys = list(self.ingredient_groups.keys())
        for i in range(len(keys)):
            print(keys[i])
            print(self.ingredient_groups[keys[i]])
            print("")

    def test_steps(self):
        for i in range(len(self.steps)):
            print("Step: " + self.steps[i].text)
            print("Ingredients: " + str(self.steps[i].ingredients))
            print("Tools: " + str(self.steps[i].tools))
            print("Methods: " + str(self.steps[i].methods))
            print("Time: " + self.steps[i].time["Hard"] + " or " + self.steps[i].time["Soft"])
            print("Settings: " + self.steps[i].settings["Stove"] + " or " + self.steps[i].settings["Oven"])
            print("")