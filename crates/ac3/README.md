# filmcraft-ac3

Clean-room AC-3 (Dolby Digital) audio decoder in pure Rust. Layer L0: depends only on
`thiserror`. Builds for `wasm32-unknown-unknown`; no `unsafe`. No GPL/LGPL code (FFmpeg,
liba52) was consulted; FFmpeg is used only as an external fixture generator and test oracle.

## Specification

ATSC A/52:2012 "Digital Audio Compression (AC-3, E-AC-3) Standard" (17 December 2012), the
publicly available standard: §5 bit stream syntax and semantics, §6 decoding overview, §7.1
exponents, §7.2 parametric bit allocation (Tables 7.6-7.16 extracted mechanically from the
standard's text), §7.3 mantissas and dither, §7.4 coupling, §7.5 rematrixing, §7.7.1 dynamic
range, §7.9 transforms and block switching. The window is computed as the Kaiser-Bessel derived
window (α = 5) and checked against Table 7.33 to 6·10⁻⁶.

## API

```rust
let mut dec = filmcraft_ac3::Decoder::new();
let h = filmcraft_ac3::parse_header(frame)?;   // rate, channels, frame size
let out = dec.decode(frame)?;                  // 1536 samples per channel, WAV channel order
dec.reset();                                    // before decoding from another position
```

## Decoder

- Every audio coding mode (1+1, 1/0, 2/0, 3/0, 2/1, 3/1, 2/2, 3/2) with or without LFE; 32 /
  44.1 / 48 kHz and every frame size; bsid ≤ 8 (9 and 10, the half / quarter-rate variants, are
  accepted). E-AC-3 (bsid 11-16) is refused with `Error::Unsupported`.
- D15 / D25 / D45 exponents with reuse across blocks; the parametric bit allocation in the
  standard's fixed-point steps, delta bit allocation, the all-zero SNR offset special case;
  grouped 3-, 5- and 11-level mantissas (groups shared across exponent sets), 7- and 15-level
  and asymmetric mantissas up to 16 bits.
- Channel coupling (coupling bands, master coordinates, phase flags in 2/0), rematrixing (all
  four banding cases), dynamic range control (`dynrng`, `dynrng2`; applied at full scale), dither
  for zero-bit mantissas (uniform ±0.707, §7.3.4).
- 512-sample IMDCT and the pair of 256-sample IMDCTs for block-switched blocks, with radix-2
  inverse FFTs, KBD window and overlap-add.
- Output: f32 at full scale ±1; channels reordered from the coded order (L C R Ls Rs LFE) to the
  WAV / SMPTE order (L R C LFE Ls Rs). No downmix (the mixer handles layouts).
- Dither is reseeded per syncframe from the frame's CRC words, so a frame decodes to the same
  samples however it was reached (seeking, render caches).
- Errors (bad exponents, reserved codes, blocks running past the frame) return `Err`; garbage
  never panics.

## Accuracy (vs FFmpeg as an external oracle)

AC-3 output is not bit-exact across decoders: zero-bit mantissas are filled with
decoder-specific dither. `tests/oracle.rs` decodes FFmpeg-encoded streams and compares with
FFmpeg's decode (worst channel SNR):

| Stream | SNR vs FFmpeg | SNR between two of our dither seeds |
|---|---|---|
| 2/0 48 kHz 192 kb/s (tones, chirp) | 66.1 dB | 76.0 dB |
| 2/0 44.1 kHz 96 kb/s with coupling and rematrixing | 84.5 dB | 81.7 dB |
| 1/0 32 kHz 96 kb/s | 94.1 dB | 95.7 dB |
| 3/2 + LFE 48 kHz 448 kb/s | 81.4 dB | 90.2 dB |
| 2/0 pink noise 128 kb/s (many zero-bit mantissas) | 27.7 dB | 27.9 dB |

The noise row shows the difference is dither: two of our own decodes with different dither
sequences differ as much as we differ from FFmpeg. In MPEG-2 TS (AVCHD-style `.mts`) and VOB the
maximum sample difference to FFmpeg is 2.3·10⁻³.

## Gaps

- FFmpeg's AC-3 encoder never block-switches, so the 256-sample transforms are implemented from
  §7.9.4.2 but not checked against an oracle.
- No downmixing, no heavy compression (`compr`) or dialogue normalisation (both are metadata
  for playback systems), no CRC check (corrupt frames are caught by consistency checks).
- E-AC-3 is not decoded.
