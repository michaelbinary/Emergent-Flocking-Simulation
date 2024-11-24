#!/usr/bin/env python3
"""
Command Line Interface for Emergent Flocking Simulation.
Allows users to run simulations with custom parameters from the command line.
"""

import click
import numpy as np
from rich.console import Console
from .simulation import EmergentFlockingGrid, EmergentFlockingVisualizer

console = Console()


@click.group()
def cli():
    """Emergent Flocking Simulation CLI"""
    pass


@cli.command()
@click.option('--space-x', default=50, help='X dimension of the space')
@click.option('--space-y', default=50, help='Y dimension of the space')
@click.option('--space-z', default=30, help='Z dimension of the space')
@click.option('--drones-per-mission', default=5, help='Number of drones per mission type')
@click.option('--frames', default=300, help='Number of simulation frames')
@click.option('--interval', default=50, help='Interval between frames (milliseconds)')
@click.option('--output-dir', default=None, help='Directory for output files')
@click.option('--separation-weight', default=1.5, help='Weight for separation behavior')
@click.option('--alignment-weight', default=1.0, help='Weight for alignment behavior')
@click.option('--cohesion-weight', default=0.8, help='Weight for cohesion behavior')
def run(space_x, space_y, space_z, drones_per_mission, frames, interval,
        output_dir, separation_weight, alignment_weight, cohesion_weight):
    """Run a flocking simulation with specified parameters."""
    try:
        console.print("[bold blue]Starting Emergent Flocking Simulation[/bold blue]")

        # Configure space
        space_size = (space_x, space_y, space_z)
        console.print(f"Space dimensions: {space_size}")

        # Initialize grid
        grid = EmergentFlockingGrid(space_size)

        # Set weights
        grid.separation_weight = separation_weight
        grid.alignment_weight = alignment_weight
        grid.cohesion_weight = cohesion_weight

        # Add drones for each mission type
        mission_types = ['delivery', 'surveillance', 'emergency']
        for mission_type in mission_types:
            console.print(f"\n[green]Adding {mission_type} drones...[/green]")

            # Set regions based on mission type
            if mission_type == 'delivery':
                start_region = np.array([0.2, 0.2, 0.5]) * np.array(space_size)
                goal_region = np.array([0.8, 0.8, 0.5]) * np.array(space_size)
            elif mission_type == 'surveillance':
                start_region = np.array([0.8, 0.2, 0.3]) * np.array(space_size)
                goal_region = np.array([0.2, 0.8, 0.7]) * np.array(space_size)
            else:  # emergency
                start_region = np.array([0.5, 0.1, 0.4]) * np.array(space_size)
                goal_region = np.array([0.5, 0.9, 0.6]) * np.array(space_size)

            # Add drones
            for i in range(drones_per_mission):
                random_offset = (np.random.rand(3) - 0.5) * 5
                start = np.clip(start_region + random_offset, 0, space_size)
                goal = np.clip(goal_region + random_offset, 0, space_size)

                drone_id = f"{mission_type}_{i}"
                grid.add_drone(drone_id, start, goal, mission_type)
                console.print(f"  Added {drone_id}")

        # Initialize visualizer and run simulation
        visualizer = EmergentFlockingVisualizer(grid, output_dir)
        console.print("\n[bold yellow]Running simulation...[/bold yellow]")

        visualizer.run(frames=frames, interval=interval)

        # Print final statistics
        metrics = visualizer.metrics_history[-1]
        console.print("\n[bold blue]Final Statistics:[/bold blue]")
        console.print(f"Active Streams: {metrics.active_streams}")
        console.print(f"Average Speed: {metrics.average_speed:.2f}")
        console.print(f"Collision Events: {metrics.collision_events}")

        for mission_type, completion_rate in metrics.mission_completion_rates.items():
            console.print(f"{mission_type.capitalize()} Completion Rate: {completion_rate:.1%}")

        console.print("\n[bold green]Simulation completed successfully![/bold green]")

    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        raise


@cli.command()
def info():
    """Display information about the simulation parameters."""
    console.print("""
[bold blue]Emergent Flocking Simulation[/bold blue]

[yellow]Available Mission Types:[/yellow]
- Delivery: Transport missions from source to destination
- Surveillance: Area monitoring missions
- Emergency: High-priority emergency response missions

[yellow]Key Parameters:[/yellow]
- Separation Weight: Controls collision avoidance strength
- Alignment Weight: Controls velocity matching strength
- Cohesion Weight: Controls group centering strength
- Space Dimensions: 3D space size (X, Y, Z)
- Frames: Number of simulation steps
- Interval: Time between frames in milliseconds

[yellow]Example Usage:[/yellow]
  # Run basic simulation
  emergent-flocking run

  # Run with custom parameters
  emergent-flocking run --space-x 60 --space-y 60 --space-z 40 --drones-per-mission 8

  # Adjust flocking behavior
  emergent-flocking run --separation-weight 2.0 --cohesion-weight 0.5
    """)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == '__main__':
    main()