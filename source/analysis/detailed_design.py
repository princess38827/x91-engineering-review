#!/usr/bin/env python3
"""Traceable structural, modal, control, power and 6-DOF screening for X-91 v0.3.

This is a preliminary design model. It deliberately separates calculated values
from assumptions that must be replaced by coupon, ground-vibration and bench data.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "v0.3"


def tube_i(od_m: float, id_m: float) -> float:
    return math.pi * (od_m**4 - id_m**4) / 64.0


def beam_modes(length: float, elements: int, ei: float, distributed_mass: float,
               point_masses: list[tuple[float, float]]) -> tuple[np.ndarray, np.ndarray]:
    """Euler-Bernoulli cantilever modes; two DOF (translation, rotation) per node."""
    n = elements + 1
    size = 2 * n
    k_global = np.zeros((size, size))
    m_global = np.zeros((size, size))
    le = length / elements
    ke = ei / le**3 * np.array([
        [12, 6*le, -12, 6*le], [6*le, 4*le**2, -6*le, 2*le**2],
        [-12, -6*le, 12, -6*le], [6*le, 2*le**2, -6*le, 4*le**2],
    ])
    me = distributed_mass * le / 420 * np.array([
        [156, 22*le, 54, -13*le], [22*le, 4*le**2, 13*le, -3*le**2],
        [54, 13*le, 156, -22*le], [-13*le, -3*le**2, -22*le, 4*le**2],
    ])
    for e in range(elements):
        idx = [2*e, 2*e+1, 2*e+2, 2*e+3]
        k_global[np.ix_(idx, idx)] += ke
        m_global[np.ix_(idx, idx)] += me
    for y, mass in point_masses:
        node = min(elements, round(y / le))
        m_global[2*node, 2*node] += mass
    free = np.arange(2, size)
    a = np.linalg.solve(m_global[np.ix_(free, free)], k_global[np.ix_(free, free)])
    vals, vecs = np.linalg.eig(a)
    vals = np.real(vals[vals > 0])
    freqs = np.sort(np.sqrt(vals) / (2 * math.pi))
    return freqs, vecs


def six_dof_screen(duration=8.0, dt=0.01) -> dict:
    """Small-disturbance rigid-body screen with explicit, replaceable derivatives.

    State is [u, w, q, theta, v, p, r, phi]. Matrices are intentionally exposed.
    A 3-degree elevon doublet is applied at 1-1.4 s and a 3-degree differential
    elevon doublet at 4-4.4 s. Values are plausible screening assumptions only.
    """
    a_lon = np.array([
        [-0.42, 0.18, 0.0, -9.81],
        [-0.70, -2.10, 20.0, 0.0],
        [0.05, -1.55, -2.80, 0.0],
        [0.0, 0.0, 1.0, 0.0],
    ])
    b_lon = np.array([0.0, -2.5, -15.0, 0.0])
    a_lat = np.array([
        [-0.75, 0.0, -20.0, 9.81],
        [-0.20, -4.2, 0.8, 0.0],
        [0.35, -0.45, -1.1, -0.20],
        [0.0, 1.0, 0.0, 0.0],
    ])
    b_lat = np.array([0.0, 22.0, 2.0, 0.0])
    eig_lon = np.linalg.eigvals(a_lon)
    eig_lat = np.linalg.eigvals(a_lat)
    t = np.arange(0.0, duration + dt, dt)
    xlon = np.zeros((len(t), 4)); xlat = np.zeros((len(t), 4))
    for i in range(1, len(t)):
        de = math.radians(3.0) if 1.0 <= t[i-1] < 1.2 else (-math.radians(3.0) if 1.2 <= t[i-1] < 1.4 else 0.0)
        da = math.radians(3.0) if 4.0 <= t[i-1] < 4.2 else (-math.radians(3.0) if 4.2 <= t[i-1] < 4.4 else 0.0)
        xlon[i] = xlon[i-1] + dt * (a_lon @ xlon[i-1] + b_lon * de)
        xlat[i] = xlat[i-1] + dt * (a_lat @ xlat[i-1] + b_lat * da)
    return {"t": t, "xlon": xlon, "xlat": xlat, "eig_lon": eig_lon, "eig_lat": eig_lat,
            "A_longitudinal": a_lon, "A_lateral": a_lat}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    mass = 4.5; g = 9.80665; span = 1.4; semispan = span / 2
    limit_g = 3.5; proof_factor = 1.25; ultimate_factor = 1.5
    ultimate_lift = mass * g * limit_g * ultimate_factor
    root_moment = ultimate_lift / 2 * 0.42 * semispan
    inertia = tube_i(0.020, 0.017)
    modulus = 55e9
    spar_count = 2
    stress = (root_moment / spar_count) * 0.010 / inertia
    allowable = 250e6
    ei_total = spar_count * modulus * inertia
    # Conservative half-wing modal mass model: skins/ribs/servos distributed;
    # one EDF and one battery represented as point masses.
    freqs, _ = beam_modes(semispan, 20, ei_total, 0.72, [(0.12, 0.615), (0.30, 0.250)])
    # Control surface and hinge-moment screen at design-dive speed.
    vd = 45.0; rho = 1.225; qbar = 0.5 * rho * vd**2
    elevon_span = (0.90 - 0.35) * semispan
    avg_local_chord = 0.31; elevon_chord = 0.22 * avg_local_chord
    elevon_area = elevon_span * elevon_chord
    ch = 0.05  # conservative provisional hinge-moment coefficient
    hinge_moment = qbar * elevon_area * elevon_chord * ch
    servo_torque = 9.5 * 0.0980665
    linkage_eff = 0.70
    torque_margin = servo_torque * linkage_eff / hinge_moment
    sim = six_dof_screen()

    def encode_complex(values):
        return [{"real": float(v.real), "imag": float(v.imag)} for v in values]

    result = {
        "status": "PRELIMINARY - NOT RELEASED FOR FABRICATION OR FLIGHT",
        "loads": {"limit_load_g": limit_g, "proof_load_g": limit_g*proof_factor,
                  "ultimate_load_g": limit_g*ultimate_factor,
                  "ultimate_total_lift_n": ultimate_lift,
                  "ultimate_root_moment_each_half_nm": root_moment},
        "structure": {"tube_od_mm": 20, "tube_id_mm": 17, "spar_count": spar_count,
                      "assumed_modulus_gpa": modulus/1e9, "tube_I_m4": inertia,
                      "combined_EI_nm2": ei_total, "ultimate_nominal_spar_stress_mpa": stress/1e6,
                      "design_allowable_mpa": allowable/1e6,
                      "nominal_stress_margin_ratio": allowable/stress,
                      "first_three_bending_modes_hz": [float(x) for x in freqs[:3]]},
        "controls": {"elevon_span_each_m": elevon_span, "elevon_chord_m": elevon_chord,
                     "elevon_area_each_m2": elevon_area, "design_dive_speed_m_s": vd,
                     "provisional_hinge_coefficient": ch, "hinge_moment_nm": hinge_moment,
                     "servo_torque_at_7_4v_nm": servo_torque,
                     "torque_margin_after_linkage_efficiency": torque_margin},
        "propulsion": {"manufacturer_current_each_a": 76.6, "manufacturer_thrust_each_n": 2.35*g,
                       "manufacturer_input_power_each_w": 1725,
                       "esc_continuous_rating_each_a": 100,
                       "esc_current_headroom_ratio": 100/76.6,
                       "battery_count": 2, "battery_mass_total_kg": 1.230,
                       "battery_energy_total_wh": 177.6,
                       "nominal_full_power_duration_min_at_75pct_usable": 60*177.6*0.75/(2*1725)},
        "six_dof": {"longitudinal_eigenvalues": encode_complex(sim["eig_lon"]),
                    "lateral_eigenvalues": encode_complex(sim["eig_lat"]),
                    "all_modes_stable_in_assumed_model": bool(np.all(np.real(sim["eig_lon"]) < 0) and np.all(np.real(sim["eig_lat"]) < 0)),
                    "warning": "Derivative assumptions are not validated; replace using aerodynamic data and measured inertia."},
    }
    (OUT / "engineering_screen.json").write_text(json.dumps(result, indent=2) + "\n")
    with (OUT / "six_dof_response.csv").open("w", newline="") as stream:
        writer = csv.writer(stream); writer.writerow(["time_s","u_m_s","w_m_s","q_rad_s","theta_rad","v_m_s","p_rad_s","r_rad_s","phi_rad"])
        writer.writerows(np.column_stack((sim["t"], sim["xlon"], sim["xlat"])))
    fig, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
    axes[0].plot(sim["t"], np.degrees(sim["xlon"][:,3]), label="Pitch attitude")
    axes[0].plot(sim["t"], np.degrees(sim["xlon"][:,2]), label="Pitch rate")
    axes[0].set_ylabel("deg / deg s-1"); axes[0].legend(); axes[0].grid(alpha=.25)
    axes[1].plot(sim["t"], np.degrees(sim["xlat"][:,3]), label="Bank attitude")
    axes[1].plot(sim["t"], np.degrees(sim["xlat"][:,1]), label="Roll rate")
    axes[1].set_xlabel("Time (s)"); axes[1].set_ylabel("deg / deg s-1"); axes[1].legend(); axes[1].grid(alpha=.25)
    fig.suptitle("X-91 v0.3 assumed-derivative 6-DOF screening response")
    fig.tight_layout(); fig.savefig(OUT / "six_dof_response.png", dpi=180); plt.close(fig)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
