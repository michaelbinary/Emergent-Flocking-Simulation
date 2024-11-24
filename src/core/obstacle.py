import numpy as np


class Obstacle:
    def __init__(self, position: np.ndarray, radius: float):
        self.position = position
        self.radius = radius
        self.influence_radius = radius * 2.0

    def check_collision(self, position: np.ndarray) -> bool:
        """Check if a position collides with this obstacle"""
        return np.linalg.norm(position - self.position) < self.radius

    def calculate_avoidance_force(self, position: np.ndarray, max_speed: float) -> np.ndarray:
        """Calculate avoidance force for a given position"""
        to_position = position - self.position
        distance = np.linalg.norm(to_position)

        if distance < self.influence_radius:
            strength = (1 - (distance / self.influence_radius)) ** 2
            if distance > 0:
                return (to_position / distance) * strength * max_speed

        return np.zeros(3)