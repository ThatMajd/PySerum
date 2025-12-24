# SerumControl

A Python DSL wrapper for generating Serum2 preset JSON files.

## Overview

This repository provides a Python interface to programmably generate presets for Xfer Records Serum synthesizer. It generates valid Serum2 JSON files which can then be packed into `.SerumPreset` files.

## Features

Currently, this library supports partial implementation of:

- **Oscillators**: Settings for Oscillator A, B, Sub, and Noise (Volume, Pan, Detune, etc.)
- **Filters**: Basic filter settings (Type, Cutoff, Resonance, Drive, etc.)

**Note**: More features like modulation, automation, and full parameter coverage will be added in future updates.

## Usage

1.  Use the Python DSL to generate a JSON preset file.
    ```python
    from serum_dsl import SerumPreset
    
    # Create new preset
    preset = SerumPreset.new()
    
    # Enable Oscillator 0 (OSC A)
    preset.Oscillator0.kParamEnable = 1.0
    preset.Oscillator0.kParamVolume = 0.5
    
    # Enable Oscillator 1 (OSC B)
    preset.Oscillator1.kParamEnable = 1.0
    preset.Oscillator1.kParamVolume = 0.5
    
    # Enable Oscillator 2 (OSC C)
    preset.Oscillator2.kParamEnable = 1.0
    preset.Oscillator2.kParamVolume = 0.5
    
    # Enable Oscillator 3 (Noise)
    preset.Oscillator3.kParamEnable = 1.0
    preset.Oscillator3.kParamVolume = 0.3
    
    # Enable Oscillator 4 (Sub)
    preset.Oscillator4.kParamEnable = 1.0
    preset.Oscillator4.kParamVolume = 0.5
    preset.Oscillator4.kParamOctave = -1.0
    
    # Add MG Low 12 filter (Default filter)
    preset.VoiceFilter0.kParamEnable = 1.0
    preset.VoiceFilter0.kParamFreq = 0.2
    
    # Save to JSON
    preset.save("my_preset.json")
    ```

2.  Convert the generated JSON to a `.SerumPreset` file using the `serum-preset-packager`.

    ```bash
    python cli.py pack my_preset.json my_preset.SerumPreset
    ```
3.  Preset after being loaded in Serum2:
![Preset Example](output_preset.png)


## Credits

A big thanks to Kenneth Wussmann for reverse engineering the Serum preset file format. This project relies on the tools provided in:
https://github.com/KennethWussmann/serum-preset-packager

**Note**: This repository only generates valid Serum2 JSON files. You must use the library linked above to pack the JSON and create a usable `.SerumPreset` file.
