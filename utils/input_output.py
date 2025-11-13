import pandas as pd

class InputOutput:

    def save_to_csv_file(self, data, filename):
        with open(filename, 'w') as file:
            result = ""
            for i in range(len(data)):
                for j in range(len(data[i])):
                    result += str(data[i][j])
                    
                    if j < len(data[i]) - 1:
                        result += "," 
            
                result += "\n"
            file.write(result)
    
    def load_from_file(self, filename):
        data = pd.read_csv(filename, header=None)
        return data
    