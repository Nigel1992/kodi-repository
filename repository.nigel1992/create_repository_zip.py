#!/usr/bin/env python3
"""
    Repository zip generator script
    Creates a zip file of the repository addon for distribution
"""

import os
import zipfile
import xml.etree.ElementTree as ET

def create_repository_zip():
    """
    Creates a zip file of the repository addon for distribution
    """
    # Parse addon.xml to get version
    tree = ET.parse("addon.xml")
    root = tree.getroot()
    addon_id = root.attrib['id']
    version = root.attrib['version']
    
    # Create zip file
    zip_filename = f"{addon_id}-{version}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add files to the zip
        files_to_add = [
            "addon.xml",
            "icon.png",
            "fanart.jpg"
        ]
        
        for file in files_to_add:
            if os.path.exists(file):
                zipf.write(file, os.path.join(addon_id, file))
    
    print(f"Created repository zip file: {zip_filename}")
    print(f"Users can install this zip file in Kodi to add your repository.")

if __name__ == "__main__":
    create_repository_zip() 