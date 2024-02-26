# ESPLouverControl Home Assistant Integration
This is an Home Assistant integration for [ESPLouverControl](https://github.com/hapedo/ESPLouverControl) firmware.

** Note: FW version 0.0.4 and up required **
 
## Installation
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
* Install using HACS, or manually: copy all files in custom_components/louver to your <config directory>/custom_components/louver/ directory.
* Restart Home-Assistant.
* Add the configuration to your configuration.yaml.
* Restart Home-Assistant again.

## Usage

### Example configuration.yaml entry for controlling single louver

```yaml
cover:
  - platform: louver
    name: "My test louver"
    client_id_list:
      - "my_louver"
    broker_username: "louver"
    broker_password: "louverpass"
```

### Example configuration.yaml entry for controlling multiple louver

```yaml
cover:
  - platform: louver
    name: "My test louver"
    client_id_list:
      - "my_louver_1"
      - "my_louver_2"
    broker_username: "louver"
    broker_password: "louverpass"
```
