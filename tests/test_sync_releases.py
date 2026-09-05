import importlib.util
import io
import unittest
import zipfile
from pathlib import Path

spec = importlib.util.spec_from_file_location('sync', Path(__file__).resolve().parents[1] / 'scripts/sync_releases.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)

class ReleaseValidation(unittest.TestCase):
    def archive(self, addon_id='plugin.video.test', extra=None):
        data = io.BytesIO()
        with zipfile.ZipFile(data, 'w') as z:
            z.writestr('plugin.video.test/addon.xml', f'<addon id="{addon_id}" version="1.2.3"><extension point="xbmc.addon.metadata"><assets><icon>icon.png</icon></assets></extension></addon>')
            z.writestr('plugin.video.test/icon.png', b'artwork')
            if extra:
                z.writestr(extra, b'bad')
        return data.getvalue()

    def test_valid_release_metadata_and_artwork(self):
        files = sync.inspect_zip(self.archive(), 'plugin.video.test', 'plugin.video.test-1.2.3.zip')
        self.assertEqual(files['icon.png'], b'artwork')
        self.assertIn('addon.xml', files)

    def test_rejects_wrong_identity(self):
        with self.assertRaises(ValueError):
            sync.inspect_zip(self.archive('plugin.video.other'), 'plugin.video.test', 'plugin.video.test-1.2.3.zip')

    def test_rejects_version_mismatch(self):
        with self.assertRaises(ValueError):
            sync.inspect_zip(self.archive(), 'plugin.video.test', 'plugin.video.test-1.2.4.zip')

    def test_rejects_unsafe_paths(self):
        for path in ('plugin.video.test/../../outside', '/absolute', 'other/file', 'plugin.video.test/..\\outside'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                sync.inspect_zip(self.archive(extra=path), 'plugin.video.test', 'plugin.video.test-1.2.3.zip')

if __name__ == '__main__':
    unittest.main()
