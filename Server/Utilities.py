class Utilities:

    @staticmethod
    def getValueFromConfigurationFile(key):
        value = None

        with open(".\\configuration.ini") as file:
            for line in file:
                if line.startswith(key):
                    value = line[len(key) + 1:]

                    break
        
        return value