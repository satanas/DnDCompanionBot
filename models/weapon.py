class Weapon:
    def __init__(self, json_data):
        definition = json_data['definition']
        self.name = definition['name']
        self.type = definition['filterType']
        self.damage = definition['damage']['diceString']
        self.damage_type = definition['damageType']
        self.equipped = True if json_data['equipped'] == "true" else False
        self.range = int(definition['range'])
        self.long_range = int(definition['longRange'])
        self.properties = [p['name'] for p in definition['properties']]

    def has_thrown(self):
        return True if "Thrown" in self.properties else False

    def has_finesse(self):
        return True if "Finesse" in self.properties else False
