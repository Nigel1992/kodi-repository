#!/usr/bin/env python3
"""Mirror stable Kodi release assets; never execute downloaded addon code."""
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ADDONS = ROOT / 'repository.nigel1992' / 'addons'
SOURCES = {
    'plugin.video.videoland.nl': 'Nigel1992/Videoland-Kodi-Addon',
    'plugin.video.nlziet': 'Nigel1992/NLZiet-Kodi-Addon',
}


def download(url, authenticated=False):
    headers = {'User-Agent': 'Nigel1992-kodi-repository'}
    if authenticated and os.environ.get('GH_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as response:
        return response.read()


def inspect_zip(data, addon_id, asset_name):
    """Validate identity, version, archive paths and referenced artwork."""
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        if archive.testzip():
            raise ValueError('Corrupt release ZIP')
        for name in archive.namelist():
            path = PurePosixPath(name)
            if path.is_absolute() or '..' in path.parts or '\\' in name or path.parts[0] != addon_id:
                raise ValueError(f'Unexpected archive path: {name}')
        metadata = archive.read(f'{addon_id}/addon.xml')
        addon = ET.fromstring(metadata)
        version = addon.get('version', '')
        if addon.tag != 'addon' or addon.get('id') != addon_id or not re.fullmatch(r'[0-9][A-Za-z0-9.+~_-]*', version):
            raise ValueError('Invalid addon identity or version')
        if asset_name != f'{addon_id}-{version}.zip':
            raise ValueError('ZIP filename and addon version disagree')
        files = {'addon.xml': metadata}
        for node in addon.findall('./extension[@point="xbmc.addon.metadata"]/assets/*'):
            if node.text:
                path = PurePosixPath(node.text)
                if path.is_absolute() or '..' in path.parts or '\\' in node.text:
                    raise ValueError('Unsafe artwork path')
                files[node.text] = archive.read(f'{addon_id}/{node.text}')
        return files


def sync(addon_id, repository):
    release = json.loads(download(f'https://api.github.com/repos/{repository}/releases/latest', True))
    if release.get('draft') or release.get('prerelease'):
        raise ValueError('Expected a stable published release')
    assets = [a for a in release['assets'] if a['name'].startswith(addon_id + '-') and a['name'].endswith('.zip')]
    if len(assets) != 1:
        raise ValueError(f'{repository}: expected exactly one addon ZIP, found {len(assets)}')
    asset = assets[0]
    target = ADDONS / addon_id
    marker = target / '.release.json'
    state = {k: asset[k] for k in ('id', 'name', 'updated_at', 'size')}
    if marker.exists() and json.loads(marker.read_text()) == state and (target / asset['name']).exists() and (target / 'addon.xml').exists():
        print(f'{addon_id}: already current ({release["tag_name"]})')
        return
    data = download(asset['browser_download_url'])
    if len(data) != asset['size']:
        raise ValueError('Downloaded asset size differs from GitHub metadata')
    if asset.get('digest') and asset['digest'] != 'sha256:' + hashlib.sha256(data).hexdigest():
        raise ValueError('Downloaded asset digest differs from GitHub metadata')
    files = inspect_zip(data, addon_id, asset['name'])
    files[asset['name']] = data
    for name, contents in files.items():
        path = target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(contents)
    marker.write_text(json.dumps(state, indent=2) + '\n')
    print(f'{addon_id}: imported {release["tag_name"]}')


if __name__ == '__main__':
    for addon_id, repository in SOURCES.items():
        sync(addon_id, repository)
