use super::*;

#[test]
fn computed_window_matches_table_7_33() {
    let w = window();
    for (n, (&a, &b)) in w.iter().zip(tables::WINDOW_TABLE.iter()).enumerate() {
        assert!((a - b).abs() <= 6e-6, "w[{n}] = {a}, table {b}");
    }
    // princen-bradley: w[n]² + w[255-n]²... (the second half mirrors): w[n]² + w[511-n]² = 1
    for n in 0..256 {
        let m = w[255 - n];
        assert!((w[n] * w[n] + m * m - 1.0).abs() < 1e-5);
    }
}

#[test]
fn tables_are_consistent() {
    // masktab maps every bin of a band to that band
    for b in 0..50 {
        for bin in tables::BNDTAB[b] as usize..(tables::BNDTAB[b] + tables::BNDSZ[b]) as usize {
            if bin < 253 {
                assert_eq!(tables::MASKTAB[bin] as usize, b, "bin {bin}");
            }
        }
    }
    assert_eq!(tables::BNDTAB[49] as usize + tables::BNDSZ[49] as usize, 253);
    // latab is non-increasing from 64 to 0
    assert_eq!(tables::LATAB[0], 64);
    assert!(tables::LATAB.windows(2).all(|w| w[0] >= w[1]));
    assert!(tables::BAPTAB.windows(2).all(|w| w[0] <= w[1]));
    assert_eq!((tables::BAPTAB[0], tables::BAPTAB[63]), (0, 15));
}

#[test]
fn inverse_fft_matches_the_definition() {
    for n in [64usize, 128] {
        let re0: Vec<f32> = (0..n).map(|i| ((i * 7 + 3) % 11) as f32 - 5.0).collect();
        let im0: Vec<f32> = (0..n).map(|i| ((i * 5 + 1) % 13) as f32 - 6.0).collect();
        let (mut re, mut im) = (re0.clone(), im0.clone());
        ifft(&mut re, &mut im);
        for t in 0..n {
            let (mut sr, mut si) = (0f64, 0f64);
            for k in 0..n {
                let a = 2.0 * std::f64::consts::PI * (k * t) as f64 / n as f64;
                sr += re0[k] as f64 * a.cos() - im0[k] as f64 * a.sin();
                si += re0[k] as f64 * a.sin() + im0[k] as f64 * a.cos();
            }
            assert!((sr - re[t] as f64).abs() < 1e-3 && (si - im[t] as f64).abs() < 1e-3, "n {n} t {t}");
        }
    }
}

#[test]
fn headers_and_gains() {
    // 48 kHz, 448 kb/s, 3/2 + LFE: bsid 8, bsmod 0, acmod 7 (cmixlev, surmixlev), lfeon
    let b = [0x0B, 0x77, 0, 0, 30, 8 << 3, 0b1110_0001, 0b0100_0000];
    let h = parse_header(&b).unwrap();
    assert_eq!((h.sample_rate, h.bitrate_kbps, h.frame_bytes, h.acmod, h.lfeon, h.channels()), (48_000, 448, 1792, 7, true, 6));
    assert_eq!(parse_header(&[0x0B, 0x77, 0, 0, 0, 16 << 3, 0, 0]), Err(Error::Unsupported("bsid 16 (E-AC-3)".into())));
    assert_eq!(dynrng_gain(0), 1.0);
    assert!((dynrng_gain(0b1110_0000) - 0.5).abs() < 1e-7);
    assert!((dynrng_gain(0b0111_1111) - 16.0 * 63.0 / 64.0).abs() < 1e-5);
}

#[test]
fn channel_order() {
    let ch = |n: usize| (0..n).map(|i| vec![i as f32]).collect::<Vec<_>>();
    let ids = |v: Vec<Vec<f32>>| v.iter().map(|c| c[0] as usize).collect::<Vec<_>>();
    // coded L C R Ls Rs LFE → L R C LFE Ls Rs
    assert_eq!(ids(wav_order(ch(6), 7, true)), vec![0, 2, 1, 5, 3, 4]);
    assert_eq!(ids(wav_order(ch(3), 2, true)), vec![0, 1, 2]);
    assert_eq!(ids(wav_order(ch(1), 1, false)), vec![0]);
}

#[test]
fn garbage_never_panics() {
    let mut d = Decoder::new();
    let mut x = 0xACu32;
    for len in [0usize, 5, 8, 100, 2000] {
        for _ in 0..200 {
            let mut f: Vec<u8> = (0..len)
                .map(|_| {
                    x ^= x << 13;
                    x ^= x >> 17;
                    x ^= x << 5;
                    x as u8
                })
                .collect();
            if len >= 6 {
                f[0] = 0x0B;
                f[1] = 0x77;
                f[4] &= 0x3F;
                f[5] = (f[5] & 7) | (8 << 3);
            }
            let _ = d.decode(&f);
        }
    }
}
