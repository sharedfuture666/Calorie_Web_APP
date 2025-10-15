import loc_and_temp
# The class of User

class User:
    def __init__(self, username:str, age:int, gender:str, height:float, weight:float, city:str):
        self.username = username
        self.age = age
        self.gender = gender
        self.height = height
        self.weight = weight
        self.city = city
        self.BMR = self.calculate_BMR()
        self.temperature = loc_and_temp.get_temp(self.city)

    def calculate_BMR(self):
        '''
        Calculate the BMR
        Male: BMR = (10 * weight) + (6.25 * height) - (5 * age) +5
        Female: BMR = (10 * weight) + (6.25 * height) - (5 * age) - 161

        '''
        if self.gender == 'Male':
            BMR = (10 * self.weight) + (6.25 * self.height) - (5 * self.age) + 5
        else:
            BMR = (10 * self.weight) + (6.25 * self.height) - (5 * self.age) - 161
        return BMR
     
    
    def calculate_calories(self):

        if self.temperature > 20:
            calories = self.BMR * 1.2
        else:
            calories = self.BMR * 1.4

        return calories


