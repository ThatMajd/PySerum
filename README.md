# SerumControl

A Python DSL wrapper for generating Serum preset JSON files.

## Overview

This repository provides a Python interface to programmably generate presets for Xfer Records Serum synthesizer. It generates valid Serum JSON files which can then be packed into `.SerumPreset` files.

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
    
    # Configure Oscillators
    preset.Oscillator0.kParamEnable = 1.0
    preset.Oscillator0.kParamVolume = 0.5
    
    # Configure Filter
    preset.VoiceFilter0.kParamEnable = 1.0
    preset.VoiceFilter0.kParamType = "LadderMg"
    preset.VoiceFilter0.kParamFreq = 0.5
    
    # Save to JSON
    preset.save("my_preset.json")
    ```

2.  Convert the generated JSON to a `.SerumPreset` file using the `serum-preset-packager`.

    ```bash
    python cli.py pack my_preset.json my_preset.SerumPreset
    ```

## Credits

A big thanks to Kenneth Wussmann for reverse engineering the Serum preset file format. This project relies on the tools provided in:
https://github.com/KennethWussmann/serum-preset-packager

**Note**: This repository only generates valid Serum JSON files. You must use the library linked above to pack the JSON and create a usable `.SerumPreset` file.
