#!/usr/bin/env python3
"""
Fix addon structure to work with Kodi repositories that use zip="false"
"""

import os
import xml.etree.ElementTree as ET
import shutil

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

if __name__ == "__main__":
    fix_addon_structure() 