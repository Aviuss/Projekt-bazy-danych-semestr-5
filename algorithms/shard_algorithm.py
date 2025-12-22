import glob
import shutil

import numpy as np
from typing import Dict
from utils.node import Node
import utils.mean_squared_error as mse
import os
import matplotlib.pyplot as plt
import imageio.v2 as imageio
# The parent (abstract) class "ShardAlgorithm" for other algorithms
class ShardAlgorithm:
    def __init__(self, name: str, list_of_nodes: list[Node]):
        self.name = name
        self.list_of_nodes = list_of_nodes
        self.frame_counter = 0

    # Allocates shards to nodes, sets 
    def allocate(self, _list_of_load_vectors):
        pass
    
    def data_of_allocated_vectors(self) -> list[Dict[str, float]]:
        data = []
        for index, node in enumerate(self.list_of_nodes):
            node_data = {
                "node": index,
                "load_vector_count": len(node.list_of_load_vectors),
                "average": np.mean(node.list_of_load_vectors),
                "median": np.median(node.list_of_load_vectors),
                "sum": np.sum(node.list_of_load_vectors),
            }
            data.append(node_data)
        return data
    
    def algorithm_score(self) -> Dict[str, float]:
        MSE_result = mse.MeanSquaredError(self.list_of_nodes).calc_MSE()
        score = {
            "MSE_average": MSE_result["average"],
            "MSE_median": MSE_result["median"],
            "MSE_max": MSE_result["max"]
        }
        return score

    def visualize_allocation(self):
        """
        Generuje pojedynczą klatkę wykresu i zapisuje ją do folderu tymczasowego.
        """
        clean_name = self.name.replace(" ", "_")
        base_folder = 'graphs'
        frames_folder = os.path.join(base_folder, f'{clean_name}_frames')

        if not os.path.exists(frames_folder):
            os.makedirs(frames_folder)

        node_numbers = list(range(len(self.list_of_nodes)))
        loaded_vectors_sum = [node_data['sum'] for node_data in self.data_of_allocated_vectors()]

        plt.clf()

        colors = plt.cm.viridis(np.linspace(0, 1, len(node_numbers)))

        bars = plt.barh(node_numbers, loaded_vectors_sum, color=colors)

        for bar in bars:
            width = bar.get_width()
            plt.text(
                width,
                bar.get_y() + bar.get_height() / 2,
                f' {width:.1f}',  # Formatowanie do 1 miejsca po przecinku
                ha='left',
                va='center',
                fontsize=8
            )

        plt.ylabel('Node Index')
        plt.xlabel('Total Load')
        plt.title(f'{self.name} - Step {self.frame_counter}')
        plt.yticks(node_numbers)
        plt.tight_layout()

        filename = os.path.join(frames_folder, f'frame_{self.frame_counter:04d}.png')
        plt.savefig(filename)
        plt.close()

        # plt.pause(0.01)

        self.frame_counter += 1
        return

    def create_gif(self, fps=5, keep_frames=False):
        clean_name = self.name.replace(" ", "_")
        base_folder = 'graphs'
        frames_folder = os.path.join(base_folder, f'{clean_name}_frames')
        gif_path = os.path.join(base_folder, f'{clean_name}_animation.gif')

        images = []
        filenames = sorted(glob.glob(os.path.join(frames_folder, "*.png")))

        if not filenames:
            print("Brak klatek do utworzenia GIFa.")
            return

        print(f"Tworzenie GIFa z {len(filenames)} klatek...")

        for filename in filenames:
            images.append(imageio.imread(filename))

        imageio.mimsave(gif_path, images, fps=fps, loop=0)

        print(f"GIF zapisany: {gif_path}")

        # Sprzątanie (usuwanie folderu z klatkami)
        if not keep_frames:
            shutil.rmtree(frames_folder, ignore_errors=True)
            print("Usunięto pliki tymczasowe.")
            self.frame_counter = 0