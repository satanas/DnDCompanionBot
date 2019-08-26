class Armor:
    def __init__(self, json_data):
        definition = json_data['definition']
        self.type = definition['type']
        self.name = definition['name']
        self.armor_class = int(definition['armorClass'])
        self.equipped = True if json_data['equipped'] == "true" else False
