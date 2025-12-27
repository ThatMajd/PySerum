# PySerum

A Python DSL for generating Serum2 preset files with automation support.

## Overview

This repository provides a Python interface to programmatically generate presets for Xfer Records Serum2 synthesizer. It generates valid Serum2 JSON files which can then be packed into `.SerumPreset` files.

## Features

- **Oscillators**: Full control over Oscillator A, B, C, Sub, and Noise
- **Filters**: Configure filter type, cutoff, resonance, drive, and more
- **Modulation/Automation**: Route LFOs, Envelopes to any parameter

## Installation

Clone the repository and use the `pyserum` package directly:

```bash
git clone https://github.com/yourusername/PySerum.git
cd PySerum
```

You will also need to clone the [serum-preset-packager](https://github.com/KennethWussmann/serum-preset-packager) repository to package the JSON file into a `.SerumPreset` file.

## Usage

### Basic Example

```python
from pyserum import SerumPreset, ModSource

# Create a new preset from template
preset = SerumPreset.new()
preset.name = "My Preset"

# Enable Oscillator A
preset.Oscillator0.enable = 1.0
preset.Oscillator0.level = 0.5

# Configure Filter
preset.VoiceFilter0.enable = 1.0
preset.VoiceFilter0.type = "Combs"
preset.VoiceFilter0.cutoff = 0.1

# Add Automation: LFO1 -> Filter Cutoff
preset.add_modulation(
    source=ModSource.LFO1,
    dest=preset.VoiceFilter0.cutoff,
    amount=50.0,
    bipolar=True
)

# Save to JSON
preset.save("presets/my_preset.json")
```

### Packing the Preset

Convert the generated JSON to a `.SerumPreset` file using the bash script provided:

```bash
./pack_preset.sh presets/my_preset.json
```

Or manually using the packager:

```bash
cd serum-preset-packager
python cli.py pack ../presets/my_preset.json ../presets/my_preset.SerumPreset
```

### Result
![Result](assets/output_preset.png)


## Development

Documentation of the Serum2 file format is in [notes.md](notes.md).

## Credits

A big thanks to Kenneth Wussmann for reverse engineering the Serum preset file format:
https://github.com/KennethWussmann/serum-preset-packager

**Note**: This repository generates valid Serum2 JSON files. Use the packager linked above to create usable `.SerumPreset` files.
