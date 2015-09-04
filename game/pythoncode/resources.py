# coding=utf-8


class Resources:
    __food_index = 0
    __fuel_index = 1
    __drugs_index = 2
    __arms_index = 3
    __tools_index = 4
    __material_index = 5

    def __init__(self, food = 0, fuel = 0, drugs = 0, arms = 0, tools = 0, material = 0):
        self.__quantities = [food, fuel, drugs, arms, tools, material]
        
# Копипаст то дальше какой лютый. А хочется иметь простой доступ как отдельному ресуру, так и массиву в целом
# чтобы складывать, вычитать и т.п. В Сях я бы макрос сделал, а как быть в питоне не понятно.

    @property
    def food(self):
        return self.__quantities[Resources.__food_index]

    @food.setter
    def food(self, value):
        self.__quantities[Resources.__food_index] = value
        
    @property
    def fuel(self):
        return self.__quantities[Resources.__fuel_index]

    @fuel.setter
    def fuel(self, value):
        self.__quantities[Resources.__fuel_index] = value
        
    @property
    def drugs(self):
        return self.__quantities[Resources.__drugs_index]

    @drugs.setter
    def drugs(self, value):
        self.__quantities[Resources.__drugs_index] = value
        
    @property
    def arms(self):
        return self.__quantities[Resources.__arms_index]

    @arms.setter
    def arms(self, value):
        self.__quantities[Resources.__arms_index] = value
        
    @property
    def tools(self):
        return self.__quantities[Resources.__tools_index]

    @tools.setter
    def tools(self, value):
        self.__quantities[Resources.__tools_index] = value
        
    @property
    def material(self):
        return self.__quantities[Resources.__material_index]

    @material.setter
    def material(self, value):
        self.__quantities[Resources.__material_index] = value
            
    def __set_all(self, value):
        for i in xrange(0, len(self.__quantities)):
            self.__quantities[i] = value
    
    def reset_all_to_zero(self):
        self.__set_all(0)