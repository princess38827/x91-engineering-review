# X-91 Development and Test Gates

> Version 0.3 detailed acceptance procedures are controlled by `ENGINEERING_SPEC_v0.3.md`. This file remains the high-level sequence.

Advancement requires written pass/fail evidence at every gate. A failed gate returns the aircraft to analysis; it does not permit accepting unexplained risk.

## Gate 0 - Independent design review

- Verify mass budget, center of gravity, control directions, structural load assumptions, battery containment, and EDF guards.
- Review applicable FAA recreational or experimental rules and select a legal operating site.
- Confirm the aircraft contains no payload-release or targeting capability.

## Gate 1 - Simulation

- Reproduce the low-order analysis in this package.
- Add higher-fidelity aerodynamic analysis and six-degree-of-freedom simulation.
- Demonstrate recoverability from conservative pitch, roll, and lost-link cases.
- Verify geofence and manual override in software-in-the-loop testing.

## Gate 2 - Bench article

- Build a non-flying center section for battery, EDF, cooling, radio, and flight-controller integration.
- Measure static thrust, current, temperatures, vibration, and radio failsafe behavior behind physical restraints.
- Require guarded EDF inlets and an external arming interlock.

## Gate 3 - Structural article

- Proof-load the wing and control hinges under supervision using reviewed limit loads and safety factors.
- Conduct control-surface backlash and flutter-risk review.
- Do not proceed if permanent deformation, delamination, overheating, or abnormal vibration occurs.

## Gate 4 - Unpowered validation

- Use a reduced-mass foam glide article before the powered aircraft.
- Confirm center-of-gravity range, trim direction, and benign low-speed response over an isolated approved field.

## Gate 5 - Restrained and taxi testing

- Verify thrust symmetry, steering/launch behavior, abort control, and immediate motor shutdown.
- Maintain a physical exclusion zone and trained spotter.

## Gate 6 - Supervised first flight

- Qualified remote pilot, visual observer, conservative weather, predeclared test card, and immediate abort criteria.
- Manual control only for the first flights; autonomy remains disabled until the airframe and estimator are validated.

## Gate 7 - Safety-bounded autonomy

- Enable only geofenced waypoint navigation, envelope protection, return-to-home, and supervised landing.
- Human command authority and immediate manual override remain active.
- No operation over people, public roads, or unapproved property.
