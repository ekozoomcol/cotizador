import codecs
import re

html_path = r'c:\Users\ekozo\OneDrive\Desktop\cotizador\static\index.html'
js_path = r'c:\Users\ekozo\OneDrive\Desktop\cotizador\TEMPORALES\generate.js'

with codecs.open(html_path, 'r', 'utf-8') as f:
    html = f.read()

with codecs.open(js_path, 'r', 'utf-8') as f:
    new_func = f.read()

# Using a flexible regex to find the currently injected generateModernBagSVG function
pattern = re.compile(r'function generateModernBagSVG\(.*?</svg>\s*`;\s*\}', re.DOTALL)
match = pattern.search(html)

if match:
    new_html = html[:match.start()] + new_func + html[match.end():]
    with codecs.open(html_path, 'w', 'utf-8') as f:
        f.write(new_html)
    print("Successfully patched index.html with valid JS and new technical details!")
else:
    print("Function generateModernBagSVG not found in index.html to overwrite.")
