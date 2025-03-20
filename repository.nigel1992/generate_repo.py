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

def make_pretty_xml(elem):
    """Return a pretty-printed XML string"""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

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

def generate_addons_xml():
    """
    Generates a repository addons.xml file from each addons addon.xml file
    and a checksum file
    """
    # Fix addon structure first
    fix_addon_structure()
    
    # Final addons.xml
    addons = ET.Element("addons")
    
    # Loop through each addon
    for addon in os.listdir("addons"):
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

if __name__ == "__main__":
    if not os.path.exists("addons"):
        os.makedirs("addons")
    generate_addons_xml() 