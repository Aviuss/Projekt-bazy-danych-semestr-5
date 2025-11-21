from typing import Dict
import pandas as pd
import matplotlib.pyplot as plt

class ChartMSE:
    def __init__(self):
        self.data = {
            "algorithm": [],
            "average": [],
            "median": [],
            "max": [],
        }
        pass

    # algorithm_score -> { MSE_average, MSE_median, MSE_max }
    def add_series(self, algorithm_name: str, algorithm_score: Dict[str, float]):
        self.data["algorithm"].append(algorithm_name)
        self.data["average"].append(algorithm_score["MSE_average"])
        self.data["median"].append(algorithm_score["MSE_median"])
        self.data["max"].append(algorithm_score["MSE_max"])
        return

    def draw(self):
        df = pd.DataFrame(self.data).set_index("algorithm")
        plot, axes = plt.subplots(1, 3, figsize=(12, 7))
        plot.canvas.manager.set_window_title("Porównanie metod alokacji shardów")

        COLORS = ["#e6194b", "#4363d8", "#3cb44b", "#ffe119",  "#f58231", "#911eb4", "#46f0f0", "#f032e6"]
        COLOR_MAP = dict(zip(df.index, COLORS))
        STATS = ["average", "median", "max"]
        LABELS = ["Średni błąd", "Mediana błędu", "Maksymalny błąd"]

        for i, ax in zip(range(len(STATS)), axes):
            c = [COLOR_MAP[el] for el in df.index]
            ax.bar(df.index, df[STATS[i]], color=c)
            ax.set_title(LABELS[i])
            ax.set_xticks(range(len(df.index)))
            ax.set_xticklabels(df.index, rotation=15)

            for p in ax.patches:
                value = p.get_height()
                ax.annotate(f"{value:.2f}", (p.get_x() + p.get_width() / 2, value),
                    ha="center", va="bottom", textcoords="offset points",
                    fontsize=10, xytext=(0, 3))

        handles = [plt.Rectangle((0,0), 1, 1, color=COLOR_MAP[alg]) for alg in df.index]
        plot.legend(handles, df.index, title="Algorytmy", loc="lower center", borderpad=1.25)
        plt.tight_layout(rect=(0, 0.15, 1, 1))
        plt.show()
        return

