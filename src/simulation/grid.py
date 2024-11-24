from typing import Dict, List, Tuple
import numpy as np
from scipy.spatial import KDTree
from ..core.drone import DroneState
from ..core.obstacle import Obstacle
from ..core.metrics import SimulationMetrics

class EmergentFlockingGrid:
    def __init__(self, space_size: Tuple[float, float, float]):
        self.space_size = space_size
        self.drones: Dict[str, DroneState] = {}
        self.obstacles: List[Obstacle] = []

        # Configuration parameters
        self.separation_range = 3.0
        self.coordination_range = 10.0
        self.perception_range = 20.0
        self.separation_weight = 1.5
        self.alignment_weight = 1.0
        self.cohesion_weight = 0.8
        self.mission_weight = 1.2
        self.obstacle_weight = 2.0
        self.max_speed = 2.0
        self.max_force = 1.0
        self.stream_formation_distance = 5.0

        self._generate_obstacles()

    def _generate_obstacles(self):
        """Generate random obstacles in the space"""
        num_obstacles = 5
        for _ in range(num_obstacles):
            position = np.array([
                np.random.uniform(0.2 * self.space_size[0], 0.8 * self.space_size[0]),
                np.random.uniform(0.2 * self.space_size[1], 0.8 * self.space_size[1]),
                np.random.uniform(0.2 * self.space_size[2], 0.8 * self.space_size[2])
            ])
            radius = np.random.uniform(2.0, 4.0)
            self.obstacles.append(Obstacle(position, radius))

    def add_drone(self, drone_id: str, position: np.ndarray, goal: np.ndarray, mission_type: str):
        """Add a new drone to the system"""
        self.drones[drone_id] = DroneState(
            position=position.copy(),
            velocity=np.random.randn(3) * 0.1,
            goal=goal.copy(),
            mission_type=mission_type,
            neighbors={},
            stream_id=-1,
            path_history=[position.copy()],
            current_phase='separation'
        )

    # ... (rest of the original grid methods, refactored to use the new classes)