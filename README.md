# Nigel1992 Kodi Addons Repository

[![GitHub Stars](https://img.shields.io/github/stars/Nigel1992/kodi-repository?style=for-the-badge)](https://github.com/Nigel1992/kodi-repository/stargazers)
[![Latest Release](https://img.shields.io/github/v/release/Nigel1992/kodi-repository?style=for-the-badge)](https://github.com/Nigel1992/kodi-repository/releases/latest)

## About

A modern, community-driven repository of high-quality Kodi addons, scripts, and utilities by Nigel1992. This repo features powerful tools for backup, IPTV streaming, and more—optimized for Kodi 21 (Omega) and Python 3.13. All code is open-source and maintained for reliability and ease of use.

- **GitHub:** https://github.com/Nigel1992/kodi-repository
- **License:** GPL-2.0-or-later (see individual addons for details)

---

## Featured Addons

### 1. LibreELEC Config Backupper ([service.libreelec.backupper](repository.nigel1992/addons/service.libreelec.backupper/))

A Kodi add-on for LibreELEC that allows you to backup and restore your system configuration, add-ons, and user data.

**Latest Version:** 1.4.1.5  
**Key Features:**
- Backup/restore system settings, add-ons, and user data
- Local and remote storage (SMB, NFS, FTP, SFTP, WebDAV)
- Backup rotation and retention policies
- Scheduled and manual backups
- User-friendly interface with progress tracking

**Recent Changes:**
- Fixed NFS remote browsing and SMB backup creation
- Improved backup/restore UI and error handling

[Read full changelog](repository.nigel1992/addons/service.libreelec.backupper/1.4.1.5/changelog.txt)

---

### 2. XCUI Streams ([plugin.video.iptvxc](repository.nigel1992/addons/plugin.video.iptvxc/))

High-performance XC / XCUI IPTV playback for Kodi. Supports Live TV, VOD, Catch-up, and TV Series. Optimized for Kodi v21 (Omega).

**Latest Version:** 3.3.3.1  
**Key Features:**
- Fast, reliable IPTV streaming
- Account expiry checks and notifications
- Trakt integration (coming soon)
- Custom icons and assets

**Recent Changes:**
- Updated icons and assets
- Version bump and release automation

[Read full changelog](repository.nigel1992/addons/plugin.video.iptvxc/3.3.3.1/CHANGELOG.md)

---

## Repository Structure

```
repository.nigel1992/
├── addons/
│   ├── repository.nigel1992/      # Repository addon itself
│   ├── service.libreelec.backupper/ # LibreELEC Backupper addon
│   ├── plugin.video.iptvxc/       # XCUI Streams IPTV addon
│   ├── addons.xml                 # Addon index
│   └── addons.xml.md5             # Checksum for verification
├── scripts/                       # Repository management scripts
│   ├── generate_repo.py           # Generate repo index files
│   └── create_repository_zip.py   # Create addon zip packages
└── README.md
```

## Installation

### Quick Install
1. Download the [repository zip file](https://github.com/Nigel1992/kodi-repository/releases/latest)
2. In Kodi, go to Add-ons → Add-on browser (box icon) → Install from zip file
3. Select the downloaded zip file
4. Wait for the "Repository installed" notification
5. Go to Install from repository → Nigel1992 Repository → Select category → Choose addon → Install

### Manual Installation
1. Browse to the desired addon in the repository
2. Download the corresponding zip file
3. Install through Kodi's "Install from zip file" option

## Updates
Add-ons in this repository notify you when updates are available. To ensure you receive notifications:
- Go to Kodi Settings > System > Add-ons
- Set Update Notifications to Enabled

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Support

For support, file an issue on GitHub or contact via the Kodi forums.

---

## Topics

kodi, repository, addons, libreelec, backup, streaming, iptv, python, media, automation, open-source, entertainment, Nigel1992

