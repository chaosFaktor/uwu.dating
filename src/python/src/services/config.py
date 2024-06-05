import json


file_mapper = json.load(open("settings/settings_mapper.json", "r"))
class ConfigLoader:
    def __init__(self, enable_sections=[]):
        
        self.loaded_sections = []
        self.config = {}
        for section in enable_sections:
            self.config[section] = json.load(open(file_mapper[section],"r"))
            self.loaded_sections.append(section)
            


    def load(self, section):
        if (not (section in file_mapper)):
            self.config[section]  = json.load(open(file_mapper[section], "r"))
            self.loaded_sections.append(section)

    def get(self, section):
        return self.config[section]
    def get_all(self):
        return self.config
