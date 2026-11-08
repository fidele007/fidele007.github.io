#!/usr/bin/env python3
"""Publish an .ipa to the SideStore source at https://forcefidele.com/sidestore/source.json.

Usage: sidestore/publish.py path/to/App.ipa ["What's new"]
Uploads the ipa as a GitHub release asset, adds the version to source.json,
then commits and pushes. The app must already be listed in source.json.
"""
import datetime, json, os, plistlib, re, subprocess, sys, zipfile

REPO = "fidele007/fidele007.github.io"
SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "source.json")

ipa, notes = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "")
z = zipfile.ZipFile(ipa)
info = plistlib.loads(z.read(next(n for n in z.namelist() if re.fullmatch(r"Payload/[^/]+\.app/Info\.plist", n))))
bundle, version, build = info["CFBundleIdentifier"], info["CFBundleShortVersionString"], info["CFBundleVersion"]

source = json.load(open(SOURCE))
app = next((a for a in source["apps"] if a["bundleIdentifier"] == bundle), None)
if app is None:
    sys.exit(f"{bundle} is not listed in source.json; add the app entry first")
if any(v["version"] == version and v.get("buildVersion") == build for v in app["versions"]):
    sys.exit(f"{app['name']} {version} ({build}) is already published; bump the build number")

slug = bundle.rsplit(".", 1)[-1]
tag = f"{slug}-{version}-{build}"
asset = f"{app['name']}-{version}-{build}.ipa"
subprocess.run(["gh", "release", "create", tag, f"{ipa}#{asset}", "--repo", REPO,
                "--title", f"{app['name']} {version} ({build})", "--notes", notes or "SideStore build"], check=True)

app["versions"].insert(0, {
    "version": version,
    "buildVersion": build,
    "date": datetime.date.today().isoformat(),
    "localizedDescription": notes,
    "downloadURL": f"https://github.com/{REPO}/releases/download/{tag}/{asset}",
    "size": os.path.getsize(ipa),
    "minOSVersion": info.get("MinimumOSVersion", "16.0"),
})
with open(SOURCE, "w") as f:
    json.dump(source, f, indent=2, ensure_ascii=False)
    f.write("\n")

root = os.path.dirname(os.path.dirname(SOURCE))
subprocess.run(["git", "-C", root, "add", SOURCE], check=True)
subprocess.run(["git", "-C", root, "commit", "-m", f"Publish {app['name']} {version} ({build}) to the SideStore source"], check=True)
subprocess.run(["git", "-C", root, "push"], check=True)
print("https://forcefidele.com/sidestore/source.json")
