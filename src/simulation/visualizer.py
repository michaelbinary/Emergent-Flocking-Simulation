import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import colorsys
from pathlib import Path
import pandas as pd
import json
from ..core.metrics import SimulationMetrics
from .grid import EmergentFlockingGrid


class EmergentFlockingVisualizer:
    def __init__(self, grid: EmergentFlockingGrid, output_dir: str = "simulation_output"):
        self.grid = grid
        self.fig = plt.figure(figsize=(15, 10))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.metrics_history: List[SimulationMetrics] = []

        self.mission_colors = {
            'delivery': colorsys.hsv_to_rgb(0.3, 0.8, 0.9),
            'surveillance': colorsys.hsv_to_rgb(0.6, 0.8, 0.9),
            'emergency': colorsys.hsv_to_rgb(0.0, 0.8, 0.9)
        }

        self._setup_visualization()

    def _setup_visualization(self):
        """Set up the 3D visualization environment"""
        self.ax.set_xlim(0, self.grid.space_size[0])
        self.ax.set_ylim(0, self.grid.space_size[1])
        self.ax.set_zlim(0, self.grid.space_size[2])
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

    # ... (rest of the visualization methods from the original class)

    def save_metrics(self):
        """Save simulation metrics to files"""
        metrics_data = [metric.__dict__ for metric in self.metrics_history]
        df = pd.DataFrame(metrics_data)
        df.to_csv(self.output_dir / "simulation_metrics.csv", index=False)
        self.create_summary_plots(df)
        self.save_final_state()

    def run(self, frames: int = 300, interval: int = 50):
        """Run simulation with animation export"""
        anim = FuncAnimation(
            self.fig, self.update,
            frames=frames, interval=interval,
            blit=False,
            repeat=False
        )

        writer = PillowWriter(fps=20)
        anim.save(self.output_dir / "simulation.gif", writer=writer)
        self.save_metrics()