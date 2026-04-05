# MPC Heating

Read-only Home Assistant custom integration for exposing MPC heating diagnostics as sensors.

## Status

V1 skeleton:
- HACS-compatible custom integration
- UI setup (config flow)
- DataUpdateCoordinator
- Read-only sensors only
- No control logic
- No services
- No write logic

## What it does

This integration mirrors existing Home Assistant entities into a dedicated `mpc_heating` integration namespace.

It is intended as a safe step before moving any MPC logic from pyscript into a custom integration.

## Installation

### HACS custom repository
1. HACS → Integrations
2. Three dots → Custom repositories
3. Add this repository URL
4. Category: `Integration`
5. Install `MPC Heating`
6. Restart Home Assistant

### Manual
Copy `custom_components/mpc_heating/` into your Home Assistant `/config/custom_components/` directory and restart Home Assistant.

## Configuration (UI)

1. Open **Settings → Devices & Services**
2. Click **Add Integration**
3. Search for **MPC Heating**
4. Select source entities from dropdown lists for all required fields
5. Finish setup

## Notes

* This integration is read-only.
* It does not modify your existing MPC or Panasonic control.
* It only reads configured source entities every 5 minutes.
