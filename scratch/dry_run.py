import os
import ast
from test_stripper import strip_comments_and_docstrings

workspace = r"c:\Users\Aman Singh\OneDrive\Desktop\Verifi"

files = []
for root, dirs, filenames in os.walk(workspace):
    if ".venv" in root or "__pycache__" in root or "scratch" in root:
        continue
    for f in filenames:
        if f.endswith(".py"):
            files.append(os.path.join(root, f))

files.sort()
print(f"Total python files to process: {len(files)}")

errors = []
for p in files:
    with open(p, "r", encoding="utf-8") as f:
        src = f.read()
    try:
        cleaned = strip_comments_and_docstrings(src)
        ast.parse(cleaned)
    except Exception as e:
        errors.append((p, str(e)))

if errors:
    print(f"FAILED on {len(errors)} files:")
    for p, err in errors:
        print(f"  {p}: {err}")
else:
    print("SUCCESS! All files stripped and validated with ast.parse without any errors.")

