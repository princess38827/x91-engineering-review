# Fictional Cockpit and Ground-Station Interface

The interface prioritizes the operator's authority and the aircraft's recoverability.

## Primary display

- Flight mode: MANUAL, ASSISTED, RETURN, LAND
- Airspeed, altitude AGL, battery state, link quality, GPS quality
- Centered attitude display with explicit envelope limits
- Geofence distance and home direction
- Independent left/right EDF current and temperature

## Persistent safety controls

- Large MANUAL OVERRIDE control
- RETURN HOME control
- MOTOR SAFE control requiring deliberate confirmation
- Lost-link timer and currently armed recovery action
- Warning history with timestamps and acknowledgement state

## Autonomous-function boundary

Permitted functions are route following, altitude holding, envelope protection, return-to-home, and supervised landing. The interface exposes no target list, threat score, engagement control, payload release, or person-tracking view.

## Data record

Every mode transition records time, operator action, reason, software version, flight-plan checksum, and vehicle state. This provides a provenance trail suitable for safety review and incident reconstruction.
