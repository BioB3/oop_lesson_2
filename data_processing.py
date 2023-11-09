import csv, os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

cities = []
with open(os.path.join(__location__, 'Cities.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        cities.append(dict(r))

countries = []
with open(os.path.join(__location__, 'Countries.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        countries.append(dict(r))

players = []
with open(os.path.join(__location__, 'Players.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        players.append(dict(r))

teams = []
with open(os.path.join(__location__, 'Teams.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        teams.append(dict(r))

titanic = []
with open(os.path.join(__location__, 'Titanic.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        titanic.append(dict(r))

class DB:
    def __init__(self):
        self.database = []

    def insert(self, table):
        self.database.append(table)

    def search(self, table_name):
        for table in self.database:
            if table.table_name == table_name:
                return table
        return None

import copy
class Table:
    def __init__(self, table_name, table):
        self.table_name = table_name
        self.table = table
    
    def join(self, other_table, common_key):
        joined_table = Table(self.table_name + '_joins_' + other_table.table_name, [])
        for item1 in self.table:
            for item2 in other_table.table:
                if item1[common_key] == item2[common_key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    joined_table.table.append(dict1)
        return joined_table
    
    def filter(self, condition):
        filtered_table = Table(self.table_name + '_filtered', [])
        for item1 in self.table:
            if condition(item1):
                filtered_table.table.append(item1)
        return filtered_table
    
    def aggregate(self, function, aggregation_key):
        temps = []
        for item1 in self.table:
            temps.append(float(item1[aggregation_key]))
        return function(temps)
    
    def select(self, attributes_list):
        temps = []
        for item1 in self.table:
            dict_temp = {}
            for key in item1:
                if key in attributes_list:
                    dict_temp[key] = item1[key]
            temps.append(dict_temp)
        return temps

    def __str__(self):
        return self.table_name + ':' + str(self.table)

table1 = Table('cities', cities)
table2 = Table('countries', countries)
table3 = Table('players', players)
table4 = Table('teams', teams)
table5 = Table('titanic', titanic)
my_DB = DB()
my_DB.insert(table1)
my_DB.insert(table2)
my_DB.insert(table3)
my_DB.insert(table4)
my_DB.insert(table5)
my_table1 = my_DB.search('cities')

print("Test filter: only filtering out cities in Italy")
my_table1_filtered = my_table1.filter(lambda x: x['country'] == 'Italy')
print(my_table1_filtered)
print()

print("Test select: only displaying two fields, city and latitude, for cities in Italy")
my_table1_selected = my_table1_filtered.select(['city', 'latitude'])
print(my_table1_selected)
print()

print("Calculting the average temperature without using aggregate for cities in Italy")
temps = []
for item in my_table1_filtered.table:
    temps.append(float(item['temperature']))
print(sum(temps)/len(temps))
print()

print("Calculting the average temperature using aggregate for cities in Italy")
print(my_table1_filtered.aggregate(lambda x: sum(x)/len(x), 'temperature'))
print()

print("Test join: finding cities in non-EU countries whose temperatures are below 5.0")
my_table2 = my_DB.search('countries')
my_table3 = my_table1.join(my_table2, 'country')
my_table3_filtered = my_table3.filter(lambda x: x['EU'] == 'no').filter(lambda x: float(x['temperature']) < 5.0)
print(my_table3_filtered.table)
print()
print("Selecting just three fields, city, country, and temperature")
print(my_table3_filtered.select(['city', 'country', 'temperature']))
print()

print("Print the min and max temperatures for cities in EU that do not have coastlines")
my_table3_filtered = my_table3.filter(lambda x: x['EU'] == 'yes').filter(lambda x: x['coastline'] == 'no')
print("Min temp:", my_table3_filtered.aggregate(lambda x: min(x), 'temperature'))
print("Max temp:", my_table3_filtered.aggregate(lambda x: max(x), 'temperature'))
print()

print("Print the min and max latitude for cities in every country")
for item in my_table2.table:
    my_table1_filtered = my_table1.filter(lambda x: x['country'] == item['country'])
    if len(my_table1_filtered.table) >= 1:
        print(item['country'], my_table1_filtered.aggregate(lambda x: min(x), 'latitude'), my_table1_filtered.aggregate(lambda x: max(x), 'latitude'))
print()

my_table4 = my_DB.search('teams')
my_table5 = my_DB.search('players')
my_table6 = my_table4.join(my_table5, 'team')
my_table6_filtered = my_table6.filter(lambda x: "ia" in x['team']).filter(lambda x: int(x['minutes']) < 200).filter(lambda x: int(x['passes']) > 100)
print('The player on a team with “ia” in the team name played less than 200 minutes and made more than 100 passses.')
print(f"Surname: {my_table6_filtered.table[0]['surname']}, Team: {my_table6_filtered.table[0]['team']}, Position: {my_table6_filtered.table[0]['position']}")
print()

top_ten_teams = my_table6.filter(lambda x: int(x['ranking']) <= 10)
below_top_ten_teams = my_table6.filter(lambda x: int(x['ranking']) > 10)
print("The average number of games played for teams ranking below 10.")
print(below_top_ten_teams.aggregate(lambda x: sum(x)/len(x), 'games'))
print("The average number of games played for teams ranking above or equal to 10.")
print(top_ten_teams.aggregate(lambda x: sum(x)/len(x), 'games'))
print()

forward_players = my_table6.filter(lambda x: x['position'] == 'forward')
midfielder_players = my_table6.filter(lambda x : x['position'] == 'midfielder')
print('The average number of passes made by forwards.')
print(forward_players.aggregate(lambda x: sum(x)/len(x), 'passes'))
print('The average number of passes made by midfielders.')
print(midfielder_players.aggregate(lambda x: sum(x)/len(x), 'passes'))
print()

my_table7 = my_DB.search('titanic')
first_class_passengers = my_table7.filter(lambda x: int(x['class']) == 1)
third_class_passengers = my_table7.filter(lambda x: int(x['class']) == 3)
print('The average fare paid paid by passengers in the first class.')
print(first_class_passengers.aggregate(lambda x: sum(x)/len(x), 'fare'))
print('The average fare paid paid by passengers in the third class.')
print(third_class_passengers.aggregate(lambda x: sum(x)/len(x), 'fare'))
print()

male_passengers = my_table7.filter(lambda x: x['gender'] == 'M')
male_passengers_survived = male_passengers.filter(lambda x: x['survived'] == 'yes')
female_passengers = my_table7.filter(lambda x: x['gender'] == 'F')
female_passengers_survived = female_passengers.filter(lambda x: x['survived'] == 'yes')
print('The survival rate of male passengers')
print(f'{(len(male_passengers_survived.table) / len(male_passengers.table)) * 100} %')
print('The survival rate of female passengers')
print(f'{(len(female_passengers_survived.table) / len(female_passengers.table)) * 100} %')
print()

embarked_table = male_passengers.filter(lambda x: x['embarked'] == 'Southampton')
print('The total number of male passengers embarked at Southampton')
print(embarked_table.aggregate(lambda x: len(x), 'class'))
print()