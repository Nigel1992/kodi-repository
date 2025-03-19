#!/usr/bin/env python3
"""
    Repository generator script
    Generates an XML file and MD5 hash for Kodi addon repository
"""

import os
import hashlib
import xml.etree.ElementTree as ET
from xml.dom import minidom

def make_pretty_xml(elem):
    """Return a pretty-printed XML string"""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

def generate_addons_xml():
    """
    Generates a repository addons.xml file from each addons addon.xml file
    and a checksum file
    """
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