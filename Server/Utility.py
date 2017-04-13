class Utility:

    @staticmethod
    def __getValueFromFile(directory, key):
        value = None

        with open(directory) as file:
            for line in file:
                if line.startswith(key):
                    value = line[len(key) + 1:]

                    break
        
        return str.strip(value)
    
    @staticmethod
    def getValueFromConfigurationFile(key):
        return Utility.__getValueFromFile(".\\configuration.ini", key)