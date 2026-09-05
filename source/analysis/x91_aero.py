#!/usr/bin/env python3
"""Transparent low-order analysis for the X-91 civilian scale demonstrator."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def load_config(path: Path = ROOT / "config.json") -> dict:
    return json.loads(path.read_text())


def stall_speed(weight_n: float, rho: float, area: float, cl_max: float) -> float:
    return math.sqrt((2.0 * weight_n) / (rho * area * cl_max))


def induced_drag_factor(aspect_ratio: float, efficiency: float) -> float:
    return 1.0 / (math.pi * aspect_ratio * efficiency)


def drag_newtons(speed: float, weight_n: float, rho: float, area: float, cd0: float, k: float) -> float:
    q = 0.5 * rho * speed**2
    cl = weight_n / (q * area)
    cd = cd0 + k * cl**2
    return q * area * cd


def static_margin(neutral_point_fraction: float, cg_fraction: float) -> float:
    return neutral_point_fraction - cg_fraction


def endurance_minutes(voltage: float, capacity_ah: float, usable_fraction: float, power_w: float) -> float:
    usable_wh = voltage * capacity_ah * usable_fraction
    return 60.0 * usable_wh / power_w


def analyze(cfg: dict) -> dict:
    geo = cfg["geometry"]
    mass = cfg["mass"]
    aero = cfg["aerodynamics"]
    prop = cfg["propulsion"]
    env = cfg["environment"]

    weight_n = mass["target_kg"] * env["gravity_m_s2"]
    vs = stall_speed(weight_n, env["air_density_kg_m3"], geo["wing_area_m2"], aero["cl_max"])
    k = induced_drag_factor(geo["aspect_ratio"], aero["oswald_efficiency"])
    sm = static_margin(aero["neutral_point_mac_fraction"], aero["cg_mac_fraction"])
    endurance = endurance_minutes(
        prop["battery_nominal_voltage_v"],
        prop["battery_capacity_ah"],
        prop["usable_energy_fraction"],
        prop["estimated_cruise_power_w"],
    )

    speeds = np.linspace(max(vs * 1.15, 12.0), 42.0, 120)
    drags = np.array([
        drag_newtons(v, weight_n, env["air_density_kg_m3"], geo["wing_area_m2"], aero["cd0"], k)
        for v in speeds
    ])
    powers = drags * speeds
    best_range_index = int(np.argmin(drags))
    best_endurance_index = int(np.argmin(powers))

    return {
        "weight_n": weight_n,
        "wing_loading_n_m2": weight_n / geo["wing_area_m2"],
        "stall_speed_m_s": vs,
        "recommended_approach_speed_m_s": 1.3 * vs,
        "induced_drag_factor": k,
        "static_margin_fraction_mac": sm,
        "thrust_to_weight_usable": prop["usable_total_static_thrust_n"] / weight_n,
        "estimated_endurance_min": endurance,
        "best_range_speed_m_s": float(speeds[best_range_index]),
        "best_endurance_speed_m_s": float(speeds[best_endurance_index]),
        "speed_grid_m_s": speeds,
        "drag_grid_n": drags,
        "power_grid_w": powers,
    }


def write_results(result: dict) -> None:
    results_dir = ROOT / "results"
    results_dir.mkdir(exist_ok=True)

    scalar = {k: v for k, v in result.items() if not isinstance(v, np.ndarray)}
    (results_dir / "summary.json").write_text(json.dumps(scalar, indent=2) + "\n")

    with (results_dir / "performance_curve.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["speed_m_s", "drag_n", "power_w"])
        writer.writerows(zip(result["speed_grid_m_s"], result["drag_grid_n"], result["power_grid_w"]))

    fig, ax1 = plt.subplots(figsize=(9, 5.5))
    ax2 = ax1.twinx()
    ax1.plot(result["speed_grid_m_s"], result["drag_grid_n"], color="#18b6d9", label="Drag")
    ax2.plot(result["speed_grid_m_s"], result["power_grid_w"], color="#ff9f43", label="Power required")
    ax1.axvline(result["stall_speed_m_s"], color="#d1495b", linestyle="--", label="Estimated stall")
    ax1.set_xlabel("Airspeed (m/s)")
    ax1.set_ylabel("Drag (N)", color="#18b6d9")
    ax2.set_ylabel("Power required (W)", color="#ff9f43")
    ax1.grid(alpha=0.25)
    ax1.set_title("X-91 Low-Order Level-Flight Estimate")
    lines = ax1.get_lines() + ax2.get_lines()
    ax1.legend(lines, [line.get_label() for line in lines], loc="upper left")
    fig.tight_layout()
    fig.savefig(results_dir / "performance_curve.png", dpi=180)
    plt.close(fig)


def main() -> None:
    result = analyze(load_config())
    write_results(result)
    print(json.dumps({k: v for k, v in result.items() if not isinstance(v, np.ndarray)}, indent=2))


if __name__ == "__main__":
    main()
