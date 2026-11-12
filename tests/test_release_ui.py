import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ReleaseUI(unittest.TestCase):
    def test_live_pages_load_theme_and_local_assets(self):
        for name in ('index.html', 'dashboard.html'):
            html = (ROOT / 'static' / name).read_text(encoding='utf-8')
            self.assertIn('href="/reference.css"' if name == 'index.html' else 'href="/lm-v2.css"', html)
            for asset in re.findall(r'(?:src|href)="(/[^"?#]+\.(?:js|css|png))"', html):
                self.assertTrue((ROOT / 'static' / asset[1:]).is_file(), asset)
            self.assertNotIn('Post message (demo)', html)

    def test_original_live_controls_remain_available(self):
        html = (ROOT / 'static/index.html').read_text(encoding='utf-8')
        for identifier in ('login', 'join', 'send', 'run-prep', 'workspace-navigation'):
            self.assertIn('id="' + identifier + '"', html)
        app = (ROOT / 'static/app.js').read_text(encoding='utf-8')
        self.assertIn("fetch(path", app)
        self.assertIn("/api/login", app)
