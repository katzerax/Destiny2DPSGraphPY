import os
import configparser

class Settings:
    def __init__(self):
        self.config = configparser.ConfigParser()
        ini_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.ini')
        with open(ini_path, 'r', encoding='utf-8') as f:
            self.config.read_file(f)
        self.interface_mode = self.config.get('Interface', 'Mode')
        self.cmd_prints = self.config.getboolean('Interface', 'CMDPrints')
        self.multi_weapon = self.config.getboolean('Interface', 'Multiweapon')
        self.calc_when_damage_dealt = self.config.get('Calculations', 'WhenDamageDealt')

    def set_interface_mode(self, mode):
        self.interface_mode = mode

    def set_cmd_prints(self, value):
        self.cmd_prints = value

    def set_multi_weapon(self, value):
        self.multi_weapon = value

    def set_calc_when_damage_dealt(self, value):
        self.calc_when_damage_dealt = value

    def save_settings(self):
        self.config.set('Interface', 'Mode', self.interface_mode)
        self.config.set('Interface', 'CMDPrints', str(self.cmd_prints))
        self.config.set('Interface', 'Multiweapon', str(self.multi_weapon))
        self.config.set('Calculations', 'WhenDamageDealt', self.calc_when_damage_dealt)

        with open('settings.ini', 'w') as configfile:
            self.config.write(configfile)

settings = Settings()

print(f"Interface Mode: {settings.interface_mode}")
print(f"CMD Prints: {settings.cmd_prints}")
print(f"Multiweapon: {settings.multi_weapon}")
print(f"When Damage Dealt: {settings.calc_when_damage_dealt}")

settings.set_interface_mode('Dark')
settings.set_cmd_prints(True)
settings.set_multi_weapon(False)
settings.set_calc_when_damage_dealt('WhenAttacking')

print(f"Interface Mode: {settings.interface_mode}")
print(f"CMD Prints: {settings.cmd_prints}")
print(f"Multiweapon: {settings.multi_weapon}")
print(f"When Damage Dealt: {settings.calc_when_damage_dealt}")

settings.save_settings()
