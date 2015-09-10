# coding=utf-8


class Resources:

    def __init__(self, food = 0, fuel = 0, drugs = 0, arms = 0, tools = 0, material = 0):
        self.food = food
        self.fuel = fuel
        self.drugs = drugs
        self.arms = arms
        self.tools = tools
        self.material = material

    def _set_all(self, value):
        self.food = value
        self.fuel = value
        self.drugs = value
        self.arms = value
        self.tools = value
        self.material = value

    def reset_all_to_zero(self):
        self._set_all(0)

    def subtract(self, sub_resources):
        self.food -= sub_resources.food
        self.fuel -= sub_resources.fuel
        self.drugs -= sub_resources.drugs
        self.arms -= sub_resources.arms
        self.tools -= sub_resources.tools
        self.material -= sub_resources.material
    
    def summary_except_food(self):
        return self.fuel + self.drugs + self.arms + self.tools + self.material
    
    def summary(self):
        return self.food + self.fuel + self.drugs + self.arms + self.tools + self.material
    
    def get_can_buy_number(self):
        # По тому целое ли число определяется можно ли проводить сделку. Поэтому преобразуем во float по необходимости
        sum = self.summary()
        if sum % 2 == 0:
            return sum / 2
        return float(sum) / 2
        
    def to_list(self):
        return [self.food, self.fuel, self.drugs, self.arms, self.tools, self.material]
        
    def from_list(self, list):
        self.food = list[0]
        self.fuel = list[1]
        self.drugs = list[2]
        self.arms = list[3]
        self.tools = list[4]
        self.material = list[5]