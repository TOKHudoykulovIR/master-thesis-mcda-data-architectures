"""Inline data.js and core.js into the page.
Output: dist/architecture-decision-explorer.html; with --no-carbon, dist/architecture-decision-explorer-no-carbon.html,
in which every block marked CARBON (the exploratory carbon card, its data, Guide entry and footer note) is removed."""
import pathlib, re, sys
root = pathlib.Path(__file__).parent
no_carbon = '--no-carbon' in sys.argv
page = (root / 'src/app.html').read_text()
page = page.replace('/*__DATA__*/', (root / 'src/data.js').read_text())
page = page.replace('/*__CORE__*/', (root / 'src/core.js').read_text())
if no_carbon:
    page = re.sub(r'/\*CARBON\*/.*?/\*/CARBON\*/\n?', '', page, flags=re.S)
    page = re.sub(r'<!--CARBON-->.*?<!--/CARBON-->\n?', '', page, flags=re.S)
    assert not any(k in page for k in ('renderCarbon', 'id="cbH"', 'carbon: {', "id: 'carb'"))   # UI and data gone; inert core functions stay
out = root / ('dist/architecture-decision-explorer-no-carbon.html' if no_carbon else 'dist/architecture-decision-explorer.html')
out.parent.mkdir(exist_ok=True)
out.write_text(page)
print(out, len(page))
