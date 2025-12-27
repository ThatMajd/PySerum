#!/usr/bin/env python3
from pyserum import SerumPreset, ModSource

# Create a new preset from template
preset = SerumPreset.new()

# Set metadata
preset.name = "Automation Demo"
preset.author = "PySerum"
preset.description = "Demo preset with LFO automation"

# Enable Oscillator A (Oscillator0)
preset.Oscillator0.enable = 1.0
preset.Oscillator0.level = 0.5

# Configure Filter
preset.VoiceFilter0.enable = 1.0
preset.VoiceFilter0.type = "Combs"
preset.VoiceFilter0.cutoff = 0.1


preset.add_modulation(
    source=ModSource.LFO1,
    dest=preset.VoiceFilter0.cutoff,
    amount=50.0,
    bipolar=True
)

# Save the preset
output_path = "presets/automation_demo.json"
preset.save(output_path)

print(f"Preset saved to: {output_path}")
print(f"\n{preset}")
print(f"\nOscillator0.level = {preset.Oscillator0.level}")
print(f"VoiceFilter0.cutoff = {preset.VoiceFilter0.cutoff}")
