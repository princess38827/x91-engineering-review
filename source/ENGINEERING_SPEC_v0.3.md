# X-91 civilian demonstrator - preliminary engineering specification v0.3

Status: **HOLD FOR INDEPENDENT REVIEW.** This is a traceable design recommendation, not a fabrication release, airworthiness finding, or substitute for a qualified aeronautical engineer. The aircraft remains non-weaponized and has no payload-release, targeting, or person-tracking capability.

## Frozen design intent

- 1.40 m one-piece flying wing, 0.56 m2 area, 4.0 kg target and 4.5 kg absolute design mass.
- Envelope: +3.5/-1.5 g limit, 1.5 ultimate factor, 45 m/s design-dive speed pending flutter clearance.
- Two isolated 6S EDF branches; independent receiver/servo power; manual override and geofence.
- First flights are manual, line-of-sight, speed-limited expansion only after proof, propulsion, ground-vibration and glide gates pass.

## Structure and materials

| Item | Selected baseline | Design input / acceptance |
|---|---|---|
| Main and rear spars | Two continuous Easy Composites CFT-RWM-20-17 tubes, 20 mm OD x 17 mm ID, tip-to-tip | Use E = 55 GPa and 250 MPa design allowable only provisionally. Supplier gives geometry, 139 g/m, 0/90 layup and 80 C service limit but no strength/modulus. Test three coupons from the actual batch. |
| Wing skins | 0.40 mm quasi-isotropic carbon/epoxy each face, nominal [0/+45/-45/0], over 5 mm Gurit Corecell I60 SAN foam | Core nominal density 65 kg/m3. Faces and core require batch records and coupons. The closed D-box from leading edge to rear spar carries torsion. |
| Spar/skin joints | 3M DP190 Gray, 0.20-0.30 mm controlled bondline; 40 mm minimum wrap/saddle at ribs and hard points | Use 5 MPa provisional design shear, never vendor typical strength as an allowable. Prepare, cure and witness-coupon with each bonding session. |
| Center joint | None in primary wing box | One-piece spars and skins. Equipment hatches must not sever D-box fibres. |
| Hard points | 2 mm G10 load spreaders bonded both faces at EDF, battery tray, launch and landing contacts | No point fastener through an unreinforced sandwich panel. Pot all penetrations. |

At +5.25 g ultimate, the screen predicts 231.7 N total lift and 34.1 N m root moment per side. If the spars share that moment equally, nominal tube stress is 45.4 MPa versus the provisional 250 MPa allowable (5.5 ratio before joints, holes, defects, sweep and local buckling). The calculated first half-wing bending mode is 25.3 Hz using assumed E and mass placement. Neither value closes structural or flutter requirements until correlated to test.

## Stiffness and mass control

| Station from centerline | Item | Maximum mass each side | CG tolerance |
|---:|---|---:|---:|
| 0.00-0.16 m | One 6S battery, tray and restraint | 0.72 kg | +/-5 mm spanwise |
| 0.25-0.35 m | EDF, motor, ESC, mount and duct | 0.43 kg | +/-3 mm |
| 0.25-0.63 m | Elevon, hinges, horn and servo | 0.09 kg | +/-2 mm chordwise |
| distributed | Half wing structure/wiring/finish | 0.72 kg | balance left/right within 10 g |

Acceptance targets: first bending >=22 Hz, first torsion >=35 Hz, corresponding left/right modes within 5%, and elevon trailing-edge free play at four locations <=0.25 mm. Control-surface balance changes require aeroelastic review. These gates do not by themselves prove a 45 m/s flutter boundary.

## Elevons and actuators

- Each elevon spans 35-90% semispan (0.385 m), with 22% local chord (about 68 mm average), sealed gap, three hinges, and horn near 70% span.
- KST X10 V8.0 at regulated 7.4 V: vendor rating 9.5 kgf cm and 0.12 s/60 deg; mechanical range +/-50 deg. Use a rigid 2 mm pushrod, ball links and no flexible Z-bend.
- Command limits: pitch +/-18 deg; differential roll +/-22 deg; combined command clipped to +/-22 deg; physical stop +/-25 deg; initial reflex 2 deg subject to glide trim.
- At 45 m/s, assumed hinge coefficient 0.05 predicts 0.111 N m. After 70% linkage efficiency the vendor torque gives a 5.87 ratio. Verify by load cell at minimum bus voltage and worst linkage angle; require >=2.0 torque margin without continuous stall-torque operation.

## Propulsion and battery branches

Each branch is: Spektrum SPMX46S50 6S 4000 mAh 50C Smart G2 battery -> accessible arming connector -> Littelfuse 0498100.M 100 A MIDI fuse in covered holder -> Hobbywing Skywalker 100A V2 ESC -> JP Hobby JPH6007-100 70 mm 12-blade EDF with 2250 Kv motor.

Manufacturer/retailer datum for each EDF at 22.2 V is 76.6 A, 1,725 W and 2.35 kg static thrust. The ESC is rated 100 A continuous/120 A peak on 3-6S, giving 1.31 current-rating headroom before thermal derating. The pack is 144 x 42 x 43 mm, 615 g, 10 AWG, soft-case, and vendor-rated 50C. Full-throttle duration at 75% usable energy is only 2.32 minutes; flight timing must use logged consumption.

Battery tray: 1.0 mm 6061-T6 bottom pan over a 3 mm silicone/fiberglass thermal pad, 2 mm G10 sidewalls, two independent 20 mm aramid straps per pack crossing structural frames, positive fore/aft stops, and 6 mm clearance around the pouch. Each compartment vents through a minimum 1,200 mm2 downward/aft outlet separated from EDF intake and avionics; it cannot be a sealed pressure vessel. Install fuse within 100 mm conductor length of the positive terminal. Final wire gauge, fuse curve and connector temperature require branch bench test; the fuse protects wiring against faults, not cells against every failure.

## Analysis status

- Rigid-body 6-DOF: the included state-space screen has stable assumed longitudinal and lateral modes after a 3 degree control doublet. Its derivatives are placeholders. Replace them with AVL/CFD/wind-tunnel derivatives and measured mass properties before control-law tuning.
- Modal/flutter: the included Euler-Bernoulli model estimates bending only. Conduct free-free ground-vibration testing with accelerometers and impact/shaker excitation; update an FEM to match frequencies within 5% and mode shapes by MAC >=0.90. A qualified aeroelastic analyst must demonstrate flutter speed >=1.20 times the approved maximum test speed. No flight excitation precedes that finding.

## Proof-load test

1. Use a production-representative static article in a guarded fixture. Support actual inertial-load paths; apply elliptical upward load using at least eight calibrated points per half-wing and include battery/EDF inertial loads.
2. Instrument both spar roots with strain gauges and both tips with displacement transducers. Record load, strain and deflection at >=50 Hz. Photograph bonds before and after.
3. Load 0, 25, 50, 75 and 100% of +3.5 g limit, holding each 60 s. Unload and require residual tip deflection <=1.0 mm, no audible event, crack, delamination, fastener motion or nonlinear strain.
4. Proof to 125% limit (+4.375 g, 193.1 N total aerodynamic load) for 60 s. Apply negative case separately to -1.875 g proof. Pass only with strain repeatability within 5% and no permanent set/damage.
5. On a sacrificial qualification article only, load to +5.25 g ultimate (231.7 N) for 3 s. Correlate the model and ultrasonically/tap-test critical bonds.

## Instrumented propulsion test

Use a bolted thrust stand behind a barrier, sterile inlet area, remote arming, fire-resistant battery station and emergency-cutoff observer. Measure per branch: thrust, optical RPM, voltage, current, watt-hours, battery/ESC/motor temperatures, vibration and ambient temperature at >=10 Hz (vibration >=2 kHz).

Run each branch alone, then both: 10 s at 25%, 10 s at 50%, 20 s at 75%, 10 s at 100%; cool and inspect; then 60 s at expected climb and 180 s at expected cruise. Abort on pack swelling, smoke/odor, abnormal vibration, witness-mark movement, current >90 A, any cell <3.45 V under load, battery >55 C, ESC >85 C, motor case >90 C, or thrust mismatch >10%. Acceptance requires no abort, no resonance trend, thrust/current repeatability within 5%, and connectors/fuse holders <60 C. Derive the operational throttle cap from this test.

## Independent review release gates

The reviewer signs separate structural loads, material/coupon, modal/flutter, stability/control, battery/electrical and propulsion-test findings. Fabrication remains on hold until drawings, travelers, actual mass properties, test data and nonconformances enter a controlled revision.

## Primary sources

- Easy Composites tube: https://www.easycomposites.co.uk/20mm-roll-wrapped-carbon-fibre-tube-metric
- Gurit Corecell I: https://www.gurit.com/corecell-i/
- 3M DP190: https://multimedia.3m.com/mws/media/1235570O/dp190-scotch-weld-technical-data-sheet.pdf
- Spektrum battery: https://www.spektrumrc.com/product/spektrum-accessories-22.2v-4000mah-6s-50c-smart-g2-lipo-battery-ic5/SPMX46S50.html
- Littelfuse fuse: https://www.littelfuse.com/assetdocs/midi-32v-bolt-down-series-data-sheet?assetguid=b55e8034-180d-40f6-a0a7-bebc2d4a94f5
- Hobbywing ESC: https://www.hobbywing.com/en/products/skywalker-v2-series274
- JP Hobby EDF: https://motionrc.com/products/jp-hobby-70mm-12-blade-edf-4s-6s-power-system-w-2250kv-motor-jph6007-100
- KST servo: https://kstservos.com/products/x10-10-8kg-torque-servo-micro-digital-metal-gear-glider-servo-motor
- NASA GVT overview: https://ntrs.nasa.gov/api/citations/19870018222/downloads/19870018222.pdf
