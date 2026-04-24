"""
Ion Wind Aircraft - Complete STL Generator
Master script that generates all parts for Bambu Lab 3D printing.

Usage:
    python3 generate_all.py              # Generate all parts
    python3 generate_all.py --list       # List all output files
    python3 generate_all.py --fuselage    # Generate only fuselage
    python3 generate_all.py --emitters    # Generate only emitters
"""

import os
import sys

# Import generators
from fuselage.fuselage import generate_all as gen_fuselage
from emitters.emitters import generate_all as gen_emitters
from collectors.collectors import generate_all as gen_collectors
from frame.frame import generate_all as gen_frame
from guards.guards import generate_all as gen_guards

BASE_DIR = os.path.dirname(__file__)
MODELS_DIR = os.path.join(BASE_DIR, "models")
OUTPUT_DIRS = {
    "fuselage": os.path.join(BASE_DIR, "fuselage"),
    "emitters": os.path.join(BASE_DIR, "emitters"),
    "collectors": os.path.join(BASE_DIR, "collectors"),
    "frame": os.path.join(BASE_DIR, "frame"),
    "guards": os.path.join(BASE_DIR, "guards"),
}

def generate_all():
    """Generate all STL parts."""
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    print("=" * 60)
    print("ION WIND AIRCRAFT - 3D Model Generator")
    print("=" * 60)
    print("Build volume: 256 × 256 × 256 mm (Bambu Lab X1C/P1P)")
    print()
    
    modules = [
        ("Fuselage & Electronics Enclosure", "fuselage", gen_fuselage),
        ("Emitter Wire Supports", "emitters", gen_emitters),
        ("Collector Plate Mounts", "collectors", gen_collectors),
        ("Main Frame / Spine", "frame", gen_frame),
        ("Propeller Guard / Duct", "guards", gen_guards),
    ]
    
    total_files = 0
    for name, dir_key, gen_func in modules:
        print(f"\n[Generating] {name}...")
        out_dir = OUTPUT_DIRS[dir_key]
        gen_func(out_dir)
        files = [f for f in os.listdir(out_dir) if f.endswith('.stl')]
        total_files += len(files)
        print(f"  -> {len(files)} STL file(s)")
    
    print()
    print("=" * 60)
    print(f"COMPLETE — {total_files} STL files generated")
    print("=" * 60)
    print()
    print("Output directories:")
    for dir_key, out_dir in OUTPUT_DIRS.items():
        stls = [f for f in os.listdir(out_dir) if f.endswith('.stl')]
        print(f"  {dir_key}/ ({len(stls)} files)")
        for s in stls:
            fsize = os.path.getsize(os.path.join(out_dir, s)) / 1024
            print(f"    └─ {s} ({fsize:.1f} KB)")


def generate_fuselage():
    gen_fuselage(OUTPUT_DIRS["fuselage"])
    
def generate_emitters():
    gen_emitters(OUTPUT_DIRS["emitters"])

def generate_collectors():
    gen_collectors(OUTPUT_DIRS["collectors"])

def generate_frame():
    gen_frame(OUTPUT_DIRS["frame"])

def generate_guards():
    gen_guards(OUTPUT_DIRS["guards"])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "--list":
            print("Available output groups:")
            for k in OUTPUT_DIRS:
                print(f"  {k}/")
            sys.exit(0)
        elif cmd == "--fuselage":
            gen_fuselage(OUTPUT_DIRS["fuselage"])
        elif cmd == "--emitters":
            gen_emitters(OUTPUT_DIRS["emitters"])
        elif cmd == "--collectors":
            gen_collectors(OUTPUT_DIRS["collectors"])
        elif cmd == "--frame":
            gen_frame(OUTPUT_DIRS["frame"])
        elif cmd == "--guards":
            gen_guards(OUTPUT_DIRS["guards"])
        else:
            print(f"Unknown option: {cmd}")
            print("Usage: python3 generate_all.py [--fuselage|--emitters|--collectors|--frame|--guards]")
            sys.exit(1)
    else:
        generate_all()