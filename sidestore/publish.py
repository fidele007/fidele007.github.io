#!/usr/bin/env python3
"""Publish an .ipa to the SideStore source at https://forcefidele.com/sidestore/source.json.

Usage: sidestore/publish.py path/to/App.ipa ["What's new"]
Uploads the ipa as a GitHub release asset, adds the version to source.json,
then commits and pushes. The app must already be listed in source.json.
If the ipa's build number isn't above the last published one, it is raised to
the next number (app and extensions) and the ipa is re-signed ad hoc first.
"""
import datetime, glob, json, os, plistlib, re, subprocess, sys, tempfile, zipfile

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


def renumber(ipa, build):
    """Return a copy of ipa with CFBundleVersion set to build, re-signed ad hoc."""
    work = tempfile.mkdtemp()
    subprocess.run(["ditto", "-x", "-k", ipa, work], check=True)
    app_dir = glob.glob(os.path.join(work, "Payload", "*.app"))[0]
    bundles = glob.glob(os.path.join(app_dir, "PlugIns", "*.appex")) + [app_dir]  # appexes sign first
    for b in bundles:
        plist = os.path.join(b, "Info.plist")
        with open(plist, "rb") as f:
            data = plistlib.load(f)
        data["CFBundleVersion"] = build
        with open(plist, "wb") as f:
            plistlib.dump(data, f)
        subprocess.run(["codesign", "-f", "-s", "-", "--preserve-metadata=entitlements", b], check=True)
    out = os.path.join(tempfile.mkdtemp(), os.path.basename(ipa))
    subprocess.run(["zip", "-qry", out, "Payload"], cwd=work, check=True)
    return out


published = max((int(v["buildVersion"]) for v in app["versions"] if v.get("buildVersion", "").isdigit()), default=0)
if not build.isdigit() or int(build) <= published:
    build = str(published + 1)
    ipa = renumber(ipa, build)
    print(f"Build number set to {build}")

slug = bundle.rsplit(".", 1)[-1]
tag = f"{slug}-{version}-{build}"
asset = f"{slug}-{version}-{build}.ipa"
if subprocess.run(["gh", "release", "view", tag, "--repo", REPO], capture_output=True).returncode:
    subprocess.run(["gh", "release", "create", tag, "--repo", REPO,
                    "--title", f"{app['name']} {version} ({build})", "--notes", notes or "SideStore build"], check=True)
# gh's own upload stalls on big files (HTTP 408), so upload with curl.
release = json.loads(subprocess.run(["gh", "api", f"repos/{REPO}/releases/tags/{tag}"], capture_output=True, check=True).stdout)
for a in release["assets"]:
    if a["name"] == asset:
        subprocess.run(["gh", "api", "-X", "DELETE", f"repos/{REPO}/releases/assets/{a['id']}"], check=True)
token = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True).stdout.strip()
subprocess.run(["curl", "-f", "--retry", "3", "-o", "/dev/null", "-X", "POST",
                "-H", f"Authorization: Bearer {token}", "-H", "Content-Type: application/octet-stream",
                "--data-binary", f"@{ipa}",
                f"https://uploads.github.com/repos/{REPO}/releases/{release['id']}/assets?name={asset}"], check=True)

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
