#!/usr/bin/env python3
"""SafeBunk release signing patch — android/app/build.gradle me
signingConfigs.release jodta hai (keystore: android/release.p12,
password env SB_SIGN_PASS se). Dobara chalane par kuch nahi karta.
Usage: python3 scripts/apply_signing.py android/app/build.gradle
"""
import sys, re

path = sys.argv[1] if len(sys.argv) > 1 else "android/app/build.gradle"
src = open(path).read()
if "signingConfigs" in src:
    print("already patched, skip")
    sys.exit(0)

block = """
    signingConfigs {
        release {
            storeFile file("../release.p12")
            storePassword System.getenv("SB_SIGN_PASS")
            keyAlias "safebunk"
            keyPassword System.getenv("SB_SIGN_PASS")
        }
    }
"""
i = src.index("android {") + len("android {")
src = src[:i] + block + src[i:]

m = re.search(r"(buildTypes\s*\{.*?release\s*\{)", src, re.S)
assert m, "release buildType nahi mila"
src = src[: m.end()] + "\n            signingConfig signingConfigs.release" + src[m.end():]
open(path, "w").write(src)
print("signing patched ->", path)
