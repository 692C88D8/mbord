# coding=utf-8


class Resources:
    __food_index = 0
    __fuel_index = 1
    __drugs_index = 2
    __arms_index = 3
    __tools_index = 4
    __material_index = 5

    def __init__(self, food = 0, fuel = 0, drugs = 0, arms = 0, tools = 0, material = 0):
        self.quantities = [food, fuel, drugs, arms, tools, material]

# Копипаст то дальше какой лютый. А хочется иметь простой доступ как отдельному ресуру, так и массиву в целом
# чтобы складывать, вычитать и т.п. В Сях я бы макрос сделал, а как быть в питоне не понятно.

    def get_food(self):
        return self.quantities[Resources.__food_index]

    def set_food(self, value):
        self.quantities[Resources.__food_index] = value

    def add_food(self, value):
        self.quantities[Resources.__food_index] += value

    def get_fuel(self):
        return self.quantities[Resources.__fuel_index]

    def set_fuel(self, value):
        self.quantities[Resources.__fuel_index] = value

    def add_fuel(self, value):
        self.quantities[Resources.__fuel_index] += value

    def get_drugs(self):
        return self.quantities[Resources.__drugs_index]

    def set_drugs(self, value):
        self.quantities[Resources.__drugs_index] = value

    def add_drugs(self, value):
        self.quantities[Resources.__drugs_index] += value

    def get_arms(self):
        return self.quantities[Resources.__arms_index]

    def set_arms(self, value):
        self.quantities[Resources.__arms_index] = value
        
    def get_tools(self):
        return self.quantities[Resources.__tools_index]

    def set_tools(self, value):
        self.quantities[Resources.__tools_index] = value
        
    def get_material(self):
        return self.quantities[Resources.__material_index]

    def set_material(self, value):
        self.quantities[Resources.__material_index] = value
            
    def _set_all(self, value):
        for i in xrange(0, len(self.quantities)):
            self.quantities[i] = value

    def reset_all_to_zero(self):
        self._set_all(0)

