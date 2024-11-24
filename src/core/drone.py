from dataclasses import dataclass
from typing import Dict, List
import numpy as np


@dataclass
class DroneState:
    position: np.ndarray
    velocity: np.ndarray
    goal: np.ndarray
    mission_type: str
    neighbors: Dict[str, float]  # drone_id: distance
    stream_id: int  # Identifies which traffic stream the drone belongs to
    path_history: List[np.ndarray]
    current_phase: str  # 'separation', 'alignment', 'cohesion', 'mission'
    distance_traveled: float = 0.0
    goal_progress: float = 0.0
    collision_count: int = 0

    def update_position(self, new_position: np.ndarray, dt: float):
        """Update drone position and related metrics"""
        self.position = new_position
        self.distance_traveled += np.linalg.norm(self.velocity) * dt
        self.path_history.append(self.position.copy())
        if len(self.path_history) > 50:
            self.path_history.pop(0)

        # Update goal progress
        initial_distance = np.linalg.norm(self.path_history[0] - self.goal)
        current_distance = np.linalg.norm(self.position - self.goal)
        self.goal_progress = (initial_distance - current_distance) / initial_distance

    def record_collision(self):
        """Record a collision event"""
        self.collision_count += 1