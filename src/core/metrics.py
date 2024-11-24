from dataclasses import dataclass
from typing import Dict
from datetime import datetime


@dataclass
class SimulationMetrics:
    timestamp: str
    frame: int
    active_streams: int
    average_separation: float
    average_speed: float
    mission_progress: Dict[str, float]
    stream_sizes: Dict[int, int]
    collision_events: int
    mission_completion_rates: Dict[str, float]
    average_cohesion: float

    @classmethod
    def create(cls, frame: int, drones: dict, stream_sizes: Dict[int, int]) -> 'SimulationMetrics':
        """Factory method to create metrics from simulation state"""
        # Calculate all metrics from the current simulation state
        separations = []
        speeds = []
        mission_progress = {}
        completion_rates = {}
        cohesion_values = []

        # ... (calculation logic moved from original calculate_metrics)

        return cls(
            timestamp=datetime.now().isoformat(),
            frame=frame,
            active_streams=len([sid for sid in stream_sizes.keys() if sid != -1]),
            average_separation=sum(separations) / len(separations) if separations else 0.0,
            average_speed=sum(speeds) / len(speeds) if speeds else 0.0,
            mission_progress=mission_progress,
            stream_sizes=stream_sizes,
            collision_events=sum(d.collision_count for d in drones.values()),
            mission_completion_rates=completion_rates,
            average_cohesion=sum(cohesion_values) / len(cohesion_values) if cohesion_values else 0.0
        )