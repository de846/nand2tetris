class HackSymbolTable:
    def __init__(self):
        self.table = {
            "R0": "0",
            "R1": "1",
            "R2": "2",
            "R3": "3",
            "R4": "4",
            "R5": "5",
            "R6": "6",
            "R7": "7",
            "R8": "8",
            "R9": "9",
            "R10": "10",
            "R11": "11",
            "R12": "12",
            "R13": "13",
            "R14": "14",
            "R15": "15",
            "SCREEN": "16384",
            "KBD": "24576",
            "SP": "0",
            "LCL": "1",
            "ARG": "2",
            "THIS": "3",
            "THAT": "4",
        }
        self.cursor = 16

    def get(self, symbol):
        return self.table[symbol]

    def add(self, symbol, value=None):
        if value:
            self.table[symbol] = value
            return value
        else:
            self.table[symbol] = self.cursor
            self.cursor += 1
            return self.cursor - 1

    def is_in_table(self, symbol):
        return symbol in self.table

    def dump(self):
        print(self.table.items())
