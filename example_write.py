#!/usr/bin/env python3
"""
Example: Create a preset with all oscillators enabled.
Uses SerumPreset.new() to ensure all required fields are present.
"""

from serum_dsl import SerumPreset, Oscillator, NoiseOscillator, SubOscillator, WTOsc, NoiseOsc, SubOsc

# Create a new preset from the default template (off.json)
# This ensures all required fields (LFOs, Envelopes, ModSlots, etc.) are present
preset = SerumPreset.new()

# Set metadata
preset.presetName = "all_oscillators_on"
preset.presetAuthor = "SerumDSL"
preset.presetDescription = "All oscillators enabled"

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

# Add MG Low 12 filter (default?)
preset.VoiceFilter0.kParamEnable = 1.0
preset.VoiceFilter0.kParamFreq = 0.2

# Save to JSON
output_path = "presets/all_oscillators_on.json"
preset.save(output_path)
print(f"Preset saved to: {output_path}")
print(repr(preset))
