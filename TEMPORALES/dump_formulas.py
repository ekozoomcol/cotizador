import json

with open('excel_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('excel_formulas.txt', 'w', encoding='utf-8') as out:
    for sheet in data['sheets']:
        out.write(f'\n--- {sheet} ---\n')
        for c in data['data'][sheet]:
            form = str(c.get('formula_or_value', ''))
            val = str(c.get('evaluated_value', ''))
            if form.startswith('=') or form.replace('.','',1).isdigit():
                out.write(f"{c['cell']}: {form} = {val}\n")
print("Done")
