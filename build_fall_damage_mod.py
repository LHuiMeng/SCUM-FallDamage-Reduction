#!/usr/bin/env python3
"""SCUM Fall Damage Reduction Mod Builder
UAssetCLI round-trip: modify LandingDamage curves Value from 100 -> 30 (×0.3)
"""

import json, os, shutil, subprocess, base64

# === Config ===
OUT_BASE = os.path.expanduser(r"~\hermes\fall-damage-mod")
SRC_DIR = r"R:\Program Files\SCUMMod\Output\Exports\SCUM\Content\ConZ_Files\Characters\Prisoner\Curves\Landing"
UACLI_DLL = r"C:\Users\Administrator\hermes\UAssetCLI\UAssetCLI\UAssetCLI.dll"
UACLI_DIR = r"C:\Users\Administrator\hermes\UAssetCLI\UAssetCLI"
ENGINE_VER = "VER_UE4_27"

CURVES = [
    ("LandingDamagePrepared", "准备着地（缓冲）"),
    ("LandingDamageUnprepared", "无准备着地（直摔）"),
]


def main():
    work_dir = os.path.join(OUT_BASE, "working", "SCUM", "Content",
                            "ConZ_Files", "Characters", "Prisoner",
                            "Curves", "Landing")
    os.makedirs(work_dir, exist_ok=True)

    for curve_name, label in CURVES:
        src_uasset = os.path.join(SRC_DIR, curve_name + ".uasset")
        json_tmp = os.path.join(OUT_BASE, f"_{curve_name}.json")
        dst_uasset = os.path.join(work_dir, curve_name + ".uasset")

        # === tojson ===
        print(f"[{label}] tojson...")
        r = subprocess.run(
            ["dotnet", UACLI_DLL, "tojson", src_uasset, json_tmp, ENGINE_VER],
            capture_output=True, text=True, timeout=60, cwd=UACLI_DIR)
        if r.returncode != 0:
            print(f"  ❌ tojson failed: {r.stderr[:200]}")
            continue

        # === modify ===
        with open(json_tmp, "r", encoding="utf-8") as f:
            data = json.load(f)

        keys = data["Exports"][0]["Data"][0]["Value"][0]["Value"]
        found = False
        for key in keys:
            v = key["Value"][0]["Value"]
            if v["Time"] == 1800.0:
                old_val = v["Value"]
                v["Value"] = 30.0  # ×0.3 reduction
                found = True
                print(f"  ✅ Value(Time=1800): {old_val} → 30.0")

        if not found:
            print(f"  ⚠️  Key with Time=1800 not found!")
            continue

        with open(json_tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # === fromjson ===
        print(f"  fromjson...")
        r = subprocess.run(
            ["dotnet", UACLI_DLL, "fromjson", json_tmp, dst_uasset],
            capture_output=True, text=True, timeout=60, cwd=UACLI_DIR)
        if r.returncode != 0:
            print(f"  ❌ fromjson failed: {r.stderr[:200]}")
            continue
        print(f"  ✅ {curve_name}.uasset written")

    # === repak ===
    pak_path = os.path.join(OUT_BASE, "SCUM_FallDamage_Reduction.pak")
    print(f"\n📦 Packing PAK...")
    r = subprocess.run(
        ["repak", "pack", "--version", "V8B", "--compression", "Zlib",
         os.path.join(OUT_BASE, "working"), pak_path],
        capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        print(f"  ❌ repak failed: {r.stderr[:300]}")
        return
    size_kb = os.path.getsize(pak_path) / 1024
    print(f"  ✅ PAK: {pak_path} ({size_kb:.1f} KB)")

    # === verify ===
    print(f"\n🔍 Verifying PAK contents...")
    r = subprocess.run(
        ["repak", "list", pak_path],
        capture_output=True, text=True, timeout=30)
    if r.returncode == 0:
        for line in r.stdout.strip().split("\n"):
            print(f"  📄 {line}")

    print(f"\n🎉 Done! Install: copy to SCUM\\Saved\\Mods\\ or server's Mods\\ directory.")


if __name__ == "__main__":
    main()