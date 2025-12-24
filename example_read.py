#!/usr/bin/env python3
"""
Example usage of the Serum DSL.
"""

from serum_dsl import SerumPreset

# Load the example preset
preset = SerumPreset.load("presets/sub_osc1_noise_filter1.json")

print(f"Preset: {preset.presetName}")
print()

# Oscillator0 (OSC A)
print("=== Oscillator0 (OSC A) ===")
print(f"  enabled: {preset.Oscillator0.enabled}")
print(f"  kParamVolume: {preset.Oscillator0.kParamVolume:.3f}")
print(f"  kParamPan: {preset.Oscillator0.kParamPan:.2f}")
print(f"  kParamUnison: {preset.Oscillator0.kParamUnison}")
print(f"  kParamDetune: {preset.Oscillator0.kParamDetune:.3f}")
print(f"  kParamDetuneWid: {preset.Oscillator0.kParamDetuneWid:.2f}")
print(f"  kParamCoarsePit: {preset.Oscillator0.kParamCoarsePit:.2f}")
print(f"  kParamFine: {preset.Oscillator0.kParamFine:.2f}")
print(f"  kParamOctave: {preset.Oscillator0.kParamOctave}")
print(f"  kParamPitch: {preset.Oscillator0.kParamPitch}")
print(f"  WTOsc.relativePathToWT: {preset.Oscillator0.WTOsc.relativePathToWT}")
print(f"  WTOsc.kParamTablePos: {preset.Oscillator0.WTOsc.kParamTablePos:.2f}")
print(f"  WTOsc.kParamWarpMenu: {preset.Oscillator0.WTOsc.kParamWarpMenu}")
print()

# Oscillator3 (Noise)
print("=== Oscillator3 (Noise) ===")
print(f"  kParamEnable: {preset.Oscillator3.kParamEnable}")
print(f"  kParamVolume: {preset.Oscillator3.kParamVolume:.3f}")
print(f"  kParamPan: {preset.Oscillator3.kParamPan:.2f}")
print(f"  NoiseOsc3.relativePathToNoiseSample: {preset.Oscillator3.NoiseOsc3.relativePathToNoiseSample}")
print(f"  NoiseOsc3.kParamColor: {preset.Oscillator3.NoiseOsc3.kParamColor:.3f}")
print(f"  NoiseOsc3.kParamOneShot: {preset.Oscillator3.NoiseOsc3.kParamOneShot}")
print()

# Oscillator4 (Sub)
print("=== Oscillator4 (Sub) ===")
print(f"  kParamEnable: {preset.Oscillator4.kParamEnable}")
print(f"  kParamVolume: {preset.Oscillator4.kParamVolume:.3f}")
print(f"  kParamPan: {preset.Oscillator4.kParamPan:.2f}")
print(f"  kParamOctave: {preset.Oscillator4.kParamOctave}")
print(f"  SubOsc4.kParamShape: {preset.Oscillator4.SubOsc4.kParamShape}")
print()

# VoiceFilter0
print("=== VoiceFilter0 ===")
print(f"  kParamEnable: {preset.VoiceFilter0.kParamEnable}")
print(f"  kParamFreq: {preset.VoiceFilter0.kParamFreq:.3f}")
print(f"  kParamReso: {preset.VoiceFilter0.kParamReso:.2f}")
print(f"  kParamDrive: {preset.VoiceFilter0.kParamDrive:.2f}")
print(f"  kParamWet: {preset.VoiceFilter0.kParamWet:.2f}")
print(f"  kParamStereo: {preset.VoiceFilter0.kParamStereo:.2f}")
print()

# VoiceFilter1
print("=== VoiceFilter1 ===")
print(f"  kParamEnable: {preset.VoiceFilter1.kParamEnable}")
print()

print("=== Summary ===")
print(repr(preset))
