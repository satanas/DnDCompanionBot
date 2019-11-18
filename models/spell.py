import utils

class Spell:
    def __init__(self, json_data):
        definition = json_data['definition']
        modifier = [x for x in definition['modifiers'] if x['type'] == 'damage'][0]

        self.name = utils.to_snake_case(definition['name'])
        self.school = definition['school']
        self.requires_attack_roll = definition['requiresAttackRoll']
        self.type = modifier['type']
        self.sub_type = modifier['subType']
        self.damages = {
            1: modifier['die']['diceString']
        }
        if 'higherLevelDefinitions' in modifier['atHigherLevels']:
            for d in modifier['atHigherLevels']['higherLevelDefinitions']:
                self.damages[d['level']] = d['dice']['diceString']

        #self.range = int(definition['range'])

    def get_damage(self, character_level):
        for level in self.damages:
            if character_level <= level:
                return self.damages[level]
