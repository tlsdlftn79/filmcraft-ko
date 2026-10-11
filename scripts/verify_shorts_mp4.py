#!/usr/bin/env python3
"""Inspect an ACTUAL encoded YouTube Shorts export using ffprobe.

This verifies container/video/audio metadata, not GPU hardware utilization or visual
quality. No network access, uploads, or changes to the video file are performed.
"""
import argparse
from fractions import Fraction
import json
import subprocess
import sys
import unittest
from pathlib import Path


def analyze(probe: dict) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    streams = probe.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    if not video:
        return ["No video stream"], warnings
    if video.get("codec_name") != "h264":
        errors.append(f"Expected H.264, got {video.get('codec_name')}")
    w, h = video.get("width"), video.get("height")
    if (w, h) != (1080, 1920):
        errors.append(f"Expected 1080x1920, got {w}x{h}")
    try:
        rate = Fraction(str(video.get("avg_frame_rate") or video.get("r_frame_rate")))
        if rate <= 0 or rate > 240:
            errors.append(f"Unexpected frame rate: {rate}")
    except (ValueError, ZeroDivisionError, TypeError):
        errors.append("Missing or invalid frame rate")
    sar = video.get("sample_aspect_ratio")
    if sar and sar not in ("1:1", "N/A"):
        warnings.append(f"Non-square sample pixels ({sar}) can change displayed aspect ratio")
    audio = [s for s in streams if s.get("codec_type") == "audio"]
    for track in audio:
        if track.get("codec_name") != "aac":
            errors.append(f"Expected AAC audio, got {track.get('codec_name')}")
    if not audio:
        warnings.append("No audio track (acceptable for a silent video)")
    duration = probe.get("format", {}).get("duration") or video.get("duration")
    try:
        seconds = float(duration)
        if not 0 < seconds < 7 * 24 * 3600:
            errors.append("Invalid duration")
        elif seconds > 180.0:
            warnings.append(f"Duration {seconds:.1f}s exceeds the Shorts 3-minute guideline")
    except (TypeError, ValueError, OverflowError):
        errors.append("Duration unavailable")
    return errors, warnings


def read_ffprobe(video_file: Path) -> dict:
    args = ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(video_file)]
    result = subprocess.run(args, check=True, capture_output=True, text=True, timeout=90)
    return json.loads(result.stdout)


class ValidatorTests(unittest.TestCase):
    def example(self, **updates):
        v = {"codec_type": "video", "codec_name": "h264", "width": 1080, "height": 1920, "avg_frame_rate": "30/1", "sample_aspect_ratio": "1:1"}
        v.update(updates)
        return {"streams": [v, {"codec_type": "audio", "codec_name": "aac"}], "format": {"duration": "59.0"}}

    def test_normal_shorts(self):
        self.assertEqual(analyze(self.example()), ([], []))

    def test_bad_orientation(self):
        self.assertTrue(analyze(self.example(width=1920, height=1080))[0])

    def test_wrong_codec(self):
        self.assertTrue(analyze(self.example(codec_name="hevc"))[0])

    def test_invalid_framerate(self):
        self.assertTrue(analyze(self.example(avg_frame_rate="0/0"))[0])

    def test_long_video_warning(self):
        x = self.example(); x["format"]["duration"] = "190.0"
        err, warnings = analyze(x)
        self.assertFalse(err); self.assertTrue(warnings)

    def test_silent_video_allowed(self):
        x = self.example(); x["streams"].pop()
        err, warnings = analyze(x)
        self.assertFalse(err); self.assertTrue(warnings)

    def test_bad_audio(self):
        x = self.example(); x["streams"][1]["codec_name"] = "opus"
        self.assertTrue(analyze(x)[0])

    def test_no_video(self):
        self.assertTrue(analyze({"streams": []})[0])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", nargs="?", help="MP4 file exported by FilmCraft Shorts preset")
    parser.add_argument("--self-test", action="store_true", help="Run metadata validation unit tests")
    args = parser.parse_args()
    if args.self_test:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(ValidatorTests)
        return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1
    if not args.video:
        parser.error("provide an exported MP4 filename or --self-test")
    path = Path(args.video)
    if not path.is_file():
        print(f"[ERROR] No such file: {path}", file=sys.stderr)
        return 2
    try:
        metadata = read_ffprobe(path)
    except FileNotFoundError:
        print("[ERROR] ffprobe not found. Install FFmpeg and add its bin directory to PATH.", file=sys.stderr)
        return 2
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, json.JSONDecodeError) as e:
        print(f"[ERROR] Could not inspect MP4: {e}", file=sys.stderr)
        return 2
    errors, warnings = analyze(metadata)
    for warning in warnings:
        print(f"[WARN] {warning}")
    for error in errors:
        print(f"[FAIL] {error}")
    if errors:
        return 1
    print("[PASS] Shorts H.264 MP4 stream metadata matches the 1080x1920 preset.")
    print("[NOTE] This cannot prove NVENC/AMF/QSV encoding was used or that the picture looks correct.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
