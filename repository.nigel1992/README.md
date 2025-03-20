# My Kodi Addons Repository

This repository contains a collection of my Kodi addons.

## How to Install This Repository in Kodi

1. Download the repository zip file from the latest release
2. In Kodi, go to Add-ons > Add-on browser (box icon in the top left)
3. Select "Install from zip file"
4. Navigate to the downloaded zip file and select it
5. Wait for the "Repository installed" notification

## How to Add Your Addons to This Repository

1. Place your addon folder in the `repository.mykodiaddons/addons/` directory
2. Each addon must have a valid `addon.xml` file
3. Push the changes to GitHub
4. GitHub Actions will automatically generate the necessary XML files

## Repository Structure

- `addons/` - Contains all addons that will be available through the repository
- `generate_repo.py` - Script to generate the repository XML files

## Auto-Update System

This repository uses GitHub Actions to automatically update the repository files when new addons are added or existing ones are updated. The workflow is triggered whenever changes are made to the addons directory. 