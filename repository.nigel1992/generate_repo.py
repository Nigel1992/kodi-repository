#!/usr/bin/env python3
"""
    Repository generator script
    Generates an XML file and MD5 hash for Kodi addon repository
"""

import os
import hashlib
import xml.etree.ElementTree as ET
from xml.dom import minidom
import shutil
import zipfile

def make_pretty_xml(elem):
    """Return a pretty-printed XML string"""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return "\n".join(line.rstrip() for line in reparsed.toprettyxml(indent="\t").splitlines() if line.strip()) + "\n"

def fix_addon_structure():
    """
    Check each addon and ensure it has the correct folder structure for direct installation
    """
    addons_dir = "addons"

    # For each addon folder
    for addon_name in os.listdir(addons_dir):
        addon_path = os.path.join(addons_dir, addon_name)

        # Skip if not a directory or is the repository itself
        if not os.path.isdir(addon_path) or addon_name == "repository.nigel1992":
            continue

        # Published release ZIPs are mirrored verbatim, never repackaged.
        if os.path.exists(os.path.join(addon_path, ".release.json")):
            continue

        # Check if addon.xml exists
        addon_xml_path = os.path.join(addon_path, "addon.xml")
        if not os.path.exists(addon_xml_path):
            print(f"Skipping {addon_name}: No addon.xml found")
            continue

        # Parse addon.xml to get version
        try:
            tree = ET.parse(addon_xml_path)
            root = tree.getroot()
            version = root.attrib.get('version', '')

            if not version:
                print(f"Skipping {addon_name}: No version found in addon.xml")
                continue

            print(f"Processing addon: {addon_name} version {version}")

            # Check if there's any version folder already
            versioned_dir = os.path.join(addon_path, version)
            if os.path.exists(versioned_dir):
                print(f"  Version directory {version} already exists")
            else:
                # Create necessary structure for non-zip repositories
                os.makedirs(versioned_dir, exist_ok=True)

                # Copy all files except version directories to the versioned folder
                for item in os.listdir(addon_path):
                    item_path = os.path.join(addon_path, item)
                    # Skip if it's a version directory
                    if os.path.isdir(item_path) and item.replace('.', '').isdigit():
                        continue
                    if item != version:  # Don't try to copy the destination folder into itself
                        dest_path = os.path.join(versioned_dir, item)
                        if os.path.isdir(item_path):
                            shutil.copytree(item_path, dest_path, dirs_exist_ok=True)
                        else:
                            shutil.copy2(item_path, dest_path)

                print(f"  Created version directory: {versioned_dir}")

        except Exception as e:
            print(f"Error processing {addon_name}: {e}")

def create_addon_zips():
    """
    Create zip files for each addon in the repository
    """
    addons_dir = "addons"

    # For each addon folder
    for addon_name in os.listdir(addons_dir):
        addon_path = os.path.join(addons_dir, addon_name)

        # Skip if not a directory or is the repository itself
        if not os.path.isdir(addon_path) or addon_name == "repository.nigel1992":
            continue

        # Published release ZIPs are mirrored verbatim, never repackaged.
        if os.path.exists(os.path.join(addon_path, ".release.json")):
            continue

        # Check if addon.xml exists
        addon_xml_path = os.path.join(addon_path, "addon.xml")
        if not os.path.exists(addon_xml_path):
            print(f"Skipping {addon_name}: No addon.xml found")
            continue

        # Parse addon.xml to get version
        try:
            tree = ET.parse(addon_xml_path)
            root = tree.getroot()
            version = root.attrib.get('version', '')

            if not version:
                print(f"Skipping {addon_name}: No version found in addon.xml")
                continue

            print(f"Processing addon: {addon_name} version {version}")

            # Create zip file
            zip_filename = f"{addon_name}-{version}.zip"
            zip_path = os.path.join(addon_path, zip_filename)

            if os.path.exists(zip_path):
                print(f"  Keeping published package: {zip_filename}")
                continue

            print(f"  Creating zip file: {zip_filename}")

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add files to the zip
                for root_dir, dirs, files in os.walk(addon_path):
                    # Skip existing zip files and version directories
                    if any(f for f in files if f.endswith('.zip')):
                        files = [f for f in files if not f.endswith('.zip')]

                    # Skip version directory
                    rel_dir = os.path.relpath(root_dir, addon_path)
                    if rel_dir == version or rel_dir.startswith(version + os.sep):
                        continue

                    for file in files:
                        file_path = os.path.join(root_dir, file)
                        # Get relative path from addon directory
                        arcname = os.path.join(addon_name, os.path.relpath(file_path, addon_path))
                        zipf.write(file_path, arcname)

            print(f"  Created zip file: {zip_path}")

        except Exception as e:
            print(f"Error processing {addon_name}: {e}")

def generate_index_pages():
    """
    Generate index.html listings for the addons folders.
    GitHub Pages does not provide directory listings, so Kodi's file browser
    would show empty folders. Kodi parses simple HTML anchor links, so each
    folder gets a minimal index.html linking its ZIP files and subfolders.
    """
    def write_index(directory, title, entries):
        lines = [
            "<!DOCTYPE html>",
            '<html lang="en">',
            "<head>",
            '<meta charset="utf-8">',
            f"<title>Index of {title}</title>",
            "</head>",
            "<body>",
            f"<h1>Index of {title}</h1>",
        ]
        for href, label in entries:
            lines.append(f'<a href="{href}">{label}</a><br>')
        lines += ["</body>", "</html>"]
        with open(os.path.join(directory, "index.html"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    addons_dir = "addons"

    # Listing for each addon folder: version directories and ZIP packages
    for addon_name in sorted(os.listdir(addons_dir)):
        addon_path = os.path.join(addons_dir, addon_name)
        if not os.path.isdir(addon_path):
            continue

        subdirs = sorted(
            d for d in os.listdir(addon_path)
            if os.path.isdir(os.path.join(addon_path, d)) and not d.startswith(".")
        )
        zips = sorted(f for f in os.listdir(addon_path) if f.endswith(".zip"))
        entries = [(d + "/", d) for d in subdirs] + [(z, z) for z in zips]
        write_index(addon_path, addon_name, entries)
        print(f"Generated {addon_path}/index.html ({len(entries)} entries)")

    # Listing for the addons folder itself: one link per addon
    addon_dirs = sorted(
        d for d in os.listdir(addons_dir)
        if os.path.isdir(os.path.join(addons_dir, d)) and not d.startswith(".")
    )
    entries = [(d + "/", d) for d in addon_dirs]
    entries += [(name, name) for name in ("addons.xml", "addons.xml.md5")
                if os.path.exists(os.path.join(addons_dir, name))]
    write_index(addons_dir, "addons", entries)
    print(f"Generated {addons_dir}/index.html ({len(entries)} entries)")

    # The GitHub Pages root is a download page for the single, unversioned
    # repository installer. Keep subdirectory browsing within /addons/.
    with open("index.html", "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nigel1992 Kodi Repository</title>
</head>
<body>
<h1>Nigel1992 Kodi Repository</h1>
<p>In Kodi, open this source and select the repository ZIP to install it.</p>
<ul>
<li><a href="repository.nigel1992.zip">repository.nigel1992.zip</a></li>
</ul>
</body>
</html>
""")
    print("Generated ./index.html (repository ZIP only)")

def generate_addons_xml():
    """
    Generates a repository addons.xml file from each addons addon.xml file
    and a checksum file
    """
    # Fix addon structure first
    fix_addon_structure()

    # Create zip files for each addon
    create_addon_zips()

    # Final addons.xml
    addons = ET.Element("addons")

    # Loop through each addon
    for addon in sorted(os.listdir("addons")):
        addon_path = os.path.join("addons", addon)
        if not os.path.isdir(addon_path):
            continue

        addon_xml_path = os.path.join(addon_path, "addon.xml")
        if not os.path.exists(addon_xml_path):
            print(f"Missing addon.xml in {addon}")
            continue

        # Parse addon.xml
        try:
            tree = ET.parse(addon_xml_path)
            addon_xml = tree.getroot()
            addons.append(addon_xml)
            print(f"Added {addon} to addons.xml")
        except Exception as e:
            print(f"Error parsing {addon_xml_path}: {e}")

    # Save the addons.xml file
    output_path = "addons/addons.xml"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
        f.write(make_pretty_xml(addons)[23:])  # Skip the XML declaration

    # Generate addons.xml.md5
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()

    m = hashlib.md5(content.encode("utf-8")).hexdigest()
    with open(f"{output_path}.md5", "w") as f:
        f.write(m)

    print(f"Generated {output_path} and {output_path}.md5")

    # GitHub Pages has no directory listings; generate index.html files so
    # Kodi's "Install from zip file" browser can see the packages.
    generate_index_pages()

if __name__ == "__main__":
    if not os.path.exists("addons"):
        os.makedirs("addons")
    generate_addons_xml()
