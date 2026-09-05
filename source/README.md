# BLACK MANTA X-91 Civilian Flight Demonstrator

Version 0.4 adds a flight-control approval candidate data pack and verification matrix. It defines restricted modes, test evidence and reviewer signatures but does not issue approval. See `FLIGHT_CONTROL_APPROVAL_DATA_PACK_v0.4.md`. Fabrication and flight remain on hold pending qualified independent review and passing test evidence.

Version 0.1 is a non-weaponized, remotely piloted electric flying-wing research aircraft. It is intended for conceptual CAD, low-order aerodynamic study, simulator development, and eventual supervised model-aircraft testing.

## Safety boundary

This project contains no targeting, tracking of people, payload release, weapon interfaces, combat logic, or autonomous engagement capability. Autonomous functions are limited to navigation, envelope protection, geofencing, return-to-home, and supervised landing research. The design is not flight-certified and must be reviewed by a qualified aeronautical engineer and operated under applicable FAA rules before fabrication or flight.

## Baseline configuration

- Wingspan: 1.40 m
- Length: 0.82 m
- Reference wing area: 0.56 m2
- Target mass: 4.0 kg
- Propulsion: two enclosed 70 mm electric ducted fans
- Control: split elevons; no vertical stabilizers
- Intended flight regime: subsonic model-aircraft research
- Target center of gravity: 24% mean aerodynamic chord
- Initial static-margin design target: 7%

## Package contents

- `config.json` - baseline dimensions, mass, atmosphere, and safety constraints
- `cad/x91_airframe.scad` - parameterized conceptual exterior model
- `analysis/x91_aero.py` - low-order lift, drag, stall, trim, static-margin, and propulsion estimates
- `analysis/test_x91_aero.py` - repeatable engineering sanity checks
- `results/` - generated plots and summary after running the analysis
- `TEST_PLAN.md` - staged simulation, bench, taxi, glide, and supervised-flight plan
- `INTERFACE.md` - fictional cockpit/ground-station information architecture
- `review/X91_Pre-Fabrication_Review_Dossier_v0.2.pdf` - preliminary five-area engineering screen and independent-review handoff
- `review/screening_calculations.json` - traceable structural and energy screening values

## Run the analysis

```bash
python3 analysis/x91_aero.py
python3 -m unittest analysis/test_x91_aero.py
```

The model intentionally uses conservative, transparent equations rather than pretending to be computational fluid dynamics. Its purpose is to expose assumptions and reject obviously unsafe configurations before higher-fidelity analysis.

## Gate to physical construction

Do not fabricate or fly from this package alone. The next technical gate requires independent review of structural loads, flutter, control authority, battery containment, EDF ingestion protection, radio failsafe behavior, and local operating rules.

Version 0.2 includes a preliminary pre-fabrication dossier. Its formal disposition is **HOLD** until missing component and structural data are supplied and an appropriately qualified independent reviewer signs the specified disposition.
