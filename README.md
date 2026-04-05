# MPC Heating

Read-only Home Assistant custom integration for exposing MPC heating diagnostics as sensors.

## Status

V1 skeleton:
- HACS-compatible custom integration
- YAML setup
- DataUpdateCoordinator
- Read-only sensors only
- No control logic
- No services
- No config flow

## What it does

This integration mirrors existing Home Assistant entities into a dedicated `mpc_heating` integration namespace.

It is intended as the first safe step before moving any MPC logic from pyscript into a custom integration.

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

## Configuration

Add to `configuration.yaml`:

```yaml
mpc_heating:
  target_flow_entity: number.panasonic_heat_pump_main_z1_heat_request_temp
  outlet_temp_entity: sensor.panasonic_heat_pump_main_main_outlet_temp
  overheat_entity: sensor.mpc_overheat
  indoor_temp_entity: sensor.ruuvitag_4005_temperature
  outdoor_temp_entity: sensor.ruuvitag_033e_temperature
  carnot_efficiency_entity: sensor.mpc_carnot_efficiency
  suggested_flow_entity: sensor.mpc_suggested_flow
  debug_text_entity: sensor.mpc_debug_text
  three_way_valve_entity: sensor.panasonic_heat_pump_main_threeway_valve_state
```

Then restart Home Assistant.

## Notes

* This integration is read-only.
* It does not modify your existing MPC or Panasonic control.
* It only reads the configured source entities every 5 minutes.

