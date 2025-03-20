#!/usr/bin/env python3
"""
    Create zip files for each addon in the repository
    This is needed for Kodi to be able to install addons
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import shutil

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
            
            # Check if zip already exists
            if os.path.exists(zip_path):
                print(f"  Zip file {zip_filename} already exists")
                continue
            
            print(f"  Creating zip file: {zip_filename}")
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add files to the zip
                for root_dir, _, files in os.walk(addon_path):
                    # Skip the version directory and any existing zip files
                    if root_dir == addon_path and version in os.listdir(addon_path):
                        continue
                    if os.path.basename(root_dir) == version:
                        continue
                    if zip_filename in root_dir:
                        continue
                    
                    for file in files:
                        if file.endswith('.zip'):
                            continue
                            
                        file_path = os.path.join(root_dir, file)
                        arcname = os.path.join(addon_name, os.path.relpath(file_path, addon_path))
                        zipf.write(file_path, arcname)
            
            print(f"  Created zip file: {zip_path}")
                
        except Exception as e:
            print(f"Error processing {addon_name}: {e}")

if __name__ == "__main__":
    create_addon_zips() 