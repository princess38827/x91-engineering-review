# X-91 flight-control approval data pack - candidate v0.4

## Approval statement

**Disposition: READY FOR QUALIFIED REVIEW, NOT APPROVED FOR FLIGHT.** This package defines the evidence, configuration and pass/fail gates needed for a qualified flight-controls engineer and test pilot to issue a restricted initial flight release. It does not grant regulatory authorization, airworthiness, fabrication release, or permission to operate.

Scope is a civilian, non-weaponized demonstrator. Payload release, targeting, person tracking, pursuit, combat logic and autonomous mission execution are excluded. Initial approval is limited to MANUAL, FBWA and RTL under direct visual-line-of-sight control.

## Controlled configuration

| Element | Approval baseline | Configuration control |
|---|---|---|
| Flight controller | Holybro Pixhawk 6X | Record serial number, hardware revision and installation drawing. Triple IMUs and redundant barometers do not replace installation testing. |
| Flight software | ArduPlane stable release | Reviewer freezes exact semantic version, git hash, bootloader, board target and signed parameter export. No automatic upgrades. |
| Navigation | External GNSS/compass, barometer and calibrated digital airspeed | Record models, firmware, orientation, bus and calibration reports. Internal compass is not the primary heading source. |
| Pilot command | Independent RC link with physical mode switch and immediate MANUAL selection | Demonstrate command latency, range, receiver failsafe and override with telemetry/GCS absent. |
| Power | Two independent regulated avionics inputs; propulsion BECs electrically excluded | Brownout, single-feed loss and ground-loop tests required. Servo rail sized from measured simultaneous actuator current. |
| Actuation | Two KST X10 V8.0 elevon servos at regulated 7.4 V | Independent output channels, mechanical stops +/-25 deg, command clipping +/-22 deg, measured direction and travel. |
| Propulsion | Two independently monitored EDF branches | Common throttle command; branch current/RPM comparison; any sustained mismatch >10% commands both branches idle and alerts pilot. |
| Logging | Onboard high-rate log plus independent test recorder | Parameters, firmware identity, IMU, EKF, RC, servo output, airspeed, GPS, power, current, RPM and failsafe events retained for every run. |

## Approval envelope

- Maximum gross mass: 4.50 kg; CG: 24% MAC nominal, allowable initial range 23-25% MAC after physical weighing.
- Initial airspeed envelope: 1.3 times measured stall speed through 25 m/s. Expansion above 25 m/s requires correlated GVT/flutter clearance; never exceed the lesser of the analyst-approved limit or 45 m/s.
- Bank command: +/-30 deg; pitch command: +15/-10 deg; pitch rate <=45 deg/s; roll rate <=90 deg/s.
- Wind: <=5 m/s steady, <=2 m/s gust spread; dry daylight; prepared field; no flight over people or occupied structures.
- Initial altitude: local rule-compliant, with minimum recovery height selected by test pilot and maximum geofence altitude/radius set for the site.
- Maximum flight duration: value derived from instrumented propulsion/endurance test with >=30% battery reserve on landing.

## Requirements and verification

| ID | Requirement | Verification | Pass evidence |
|---|---|---|---|
| FC-001 | Exact hardware, firmware and parameters are uniquely identified. | Inspection | Signed configuration index; SHA-256 hashes; readback matches controlled files. |
| FC-002 | Manual control remains available without GNSS, airspeed, telemetry or GCS. | HITL/ground | Correct surface/throttle response in every injected-loss case. |
| FC-003 | Any single avionics power-feed loss causes no reboot or actuator transient. | Bench | Voltage/current traces; no reset; no output step >2 deg. |
| FC-004 | Sensor installation is free of unacceptable vibration, magnetic and pressure errors. | Ground/taxi | IMU clipping zero; compass interference within reviewer limit; airspeed zero and scale checks pass. |
| FC-005 | Command limits prevent structural/envelope exceedance in FBWA. | SITL/HITL | Monte Carlo cases stay within bank, pitch, rate, speed and load limits. |
| FC-006 | RC loss produces the approved RTL sequence and reacquisition restores pilot authority predictably. | SITL/HITL/range | 20/20 repetitions pass with recorded transition times. |
| FC-007 | Geofence breach produces the approved return behavior without leaving the containment volume. | SITL/HITL | 20/20 boundary cases pass, including wind and GNSS error. |
| FC-008 | One EDF degradation/failure does not produce unrecoverable yaw/roll. | 6-DOF/HITL/tethered ground | Both-throttle cut triggers <=0.25 s after >10% verified mismatch; MANUAL remains available. |
| FC-009 | Servo authority, speed and thermal margin cover the approved envelope. | Bench/load | >=2.0 torque margin; full combined travel at minimum bus voltage; temperatures within limits. |
| FC-010 | State estimation degrades safely under sensor faults. | SITL/HITL | Bias, freeze, dropout and noise cases produce annunciation and approved fallback; no hidden AUTO continuation. |
| FC-011 | All safety-critical events and commands are reconstructable. | Log review | Independent time correlation <=20 ms; no required field missing; checksum retained. |
| FC-012 | Initial flights cannot enter autonomous mission execution. | Inspection/test | AUTO and GUIDED mission initiation inhibited in the controlled parameter set; bench attempt fails safely. |

## Model acceptance before control-law approval

The current 6-DOF derivatives are assumptions and cannot support gain approval. Replace them with:

1. Measured mass, CG and full inertia tensor for minimum and maximum flight mass.
2. Aerodynamic coefficient tables versus angle of attack, sideslip, control deflection and propulsion state, including post-stall uncertainty bounds.
3. Propulsion thrust and lag versus command, airspeed and battery voltage, including left/right mismatch.
4. Servo position, rate limit, deadband, backlash, bus-voltage dependence and load response.
5. Correlated structural modes from GVT, with flight-control sampling/filter frequencies checked against elastic modes.

The nonlinear model passes only if trim residuals are within 2% weight and 0.5 deg control, predicted static margin agrees with glide/ground evidence within 2% MAC, and measured doublet responses fall inside the model's 95% uncertainty bounds. Control gains cannot be finalized before correlation.

## SITL and HITL campaign

Use the frozen ArduPlane binary and controlled parameter file. Run nominal cases and at least 200 Monte Carlo trials per safety-critical scenario across mass, CG, aerodynamic uncertainty, wind, sensor bias, battery voltage, servo rate and propulsion mismatch.

Scenarios: takeoff/launch transient; pilot doublets; stall approach and recovery; minimum/maximum CG; 5 m/s crosswind; gusts; RC loss/recovery; GCS loss; GNSS dropout/jump; compass bias; airspeed freeze/blockage/bias; barometer drift; one power-feed loss; one servo slow/jammed at neutral/offset; one EDF 10/25/50/100% loss; fence breach at every boundary; RTL from minimum energy; CPU load and logging saturation.

Pass criteria: no departure, sustained oscillation, command reversal, geofence escape, reboot or structural-envelope exceedance; pilot override always works; required annunciation occurs; terminal states are controlled landing/approved loiter or manual recovery. Every failure is dispositioned before approval.

## Ground and restrained tests

1. Configuration audit and independent control-direction check.
2. Avionics power interruption, brownout and servo-load test while logging.
3. Vibration survey with each EDF alone and together through the full RPM range; inspect notch/filter separation from structural modes.
4. Pitot leak, zero, scale and blockage tests; compass interference test at every throttle setting.
5. RC/GCS range and antenna-orientation tests; verify failsafe timing and manual reacquisition.
6. Restrained asymmetric-thrust detection using controlled RPM/current reduction on one branch.
7. Hardware-in-loop test with the exact installed controller, receiver, sensors and servo loads.

## Restricted flight-test cards

| Card | Objective | Entry gate | Maximum task |
|---|---|---|---|
| FT-01 | Unpowered glide trim | Structural proof, CG and manual control signed | Straight glide, small pitch corrections, no automation. |
| FT-02 | Powered straight flight | Propulsion, vibration and FT-01 pass | MANUAL only, <=18 m/s, shallow turns, immediate landing. |
| FT-03 | Stabilized-mode evaluation | Correlated manual response and HITL pass | FBWA, 5 deg pitch and 15 deg bank steps. |
| FT-04 | Envelope identification | FT-03 stable and model updated | Small doublets, stall approach at safe height, <=25 m/s. |
| FT-05 | RTL demonstration | RC-loss/geofence HITL 20/20 pass | Pilot-commanded RTL with immediate MANUAL takeover available. |

Each card requires test pilot, flight-test engineer and safety observer; weather/site go-no-go; abort plan; telemetry and onboard logging; post-flight inspection; data review and written authorization before the next card.

## Approval signatures

| Role | Required finding | Name / credential / signature / date |
|---|---|---|
| Flight-controls engineer | Requirements, model correlation, gain/limit and V&V evidence acceptable | ______________________________ |
| Aeroelastic/structures reviewer | Approved control envelope is inside structural and flutter clearance | ______________________________ |
| Electrical/propulsion reviewer | Power, actuator and asymmetric-thrust protections acceptable | ______________________________ |
| Flight-test pilot | Test cards, abort criteria, handling risks and site limits accepted | ______________________________ |
| Configuration manager | Hardware/software/parameter baseline and evidence hashes complete | ______________________________ |

Approval, if granted, is limited to the identified airframe serial number, mass/CG range, firmware hash, parameter hash, hardware configuration, site and envelope. Any change affecting geometry, mass distribution, servo linkage, propulsion, sensors, flight software or parameters suspends approval pending impact review.

## References

- ArduPilot Pixhawk 6X: https://ardupilot.org/plane/docs/common-holybro-pixhawk6X.html
- ArduPilot SITL: https://ardupilot.org/dev/docs/using-sitl-for-ardupilot-testing.html
- ArduPilot airspeed sensor guidance: https://ardupilot.org/plane/docs/airspeed.html
- ArduPilot advanced failsafe configuration: https://ardupilot.org/plane/docs/advanced-failsafe-configuration.html
- ArduPilot parameter reference: https://ardupilot.org/plane/docs/parameters.html
- FAA educational/recreational operations: https://www.faa.gov/uas/educational_users
- FAA Part 107 waivers: https://www.faa.gov/uas/commercial_operators/part_107_waivers
