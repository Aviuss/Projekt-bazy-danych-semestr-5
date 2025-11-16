import pandas as pd
import os


class InputOutput:
    @staticmethod
    def save_to_csv_file(data: pd.DataFrame, filename: str = "load_vectors.csv",
                         dir_name: str = "input_files", ) -> None:
        if dir_name not in os.listdir("../"):
            os.mkdir("..//" + dir_name)

        data.to_csv(f"..//{dir_name}//{filename}", index=False, header=False, mode="w")
        return

    @staticmethod
    def read_input_file(filename: str) -> pd.DataFrame:
        data = pd.read_csv(filename, header=None)
        return data
