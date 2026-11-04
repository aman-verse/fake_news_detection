import os
import ast
import re
import tokenize
import io

def strip_comments_and_docstrings(source_code: str) -> str:
    lines = source_code.splitlines(keepends=True)
    
    tokens = list(tokenize.generate_tokens(io.StringIO(source_code).readline))
    
    comment_spans = []
    for t in tokens:
        if t.type == tokenize.COMMENT:
            srow, scol = t.start
            erow, ecol = t.end
            comment_spans.append((srow, scol, erow, ecol))
            
    line_comments = {srow: scol for srow, scol, erow, ecol in comment_spans}
    
    new_lines = []
    for idx, line in enumerate(lines):
        line_num = idx + 1
        if line_num in line_comments:
            scol = line_comments[line_num]
            prefix = line[:scol]
            if prefix.strip() == "":
                continue
            else:
                new_lines.append(prefix.rstrip() + "\n")
        else:
            new_lines.append(line)
            
    intermediate = "".join(new_lines)
    
    try:
        tree = ast.parse(intermediate)
        docstring_ranges = []
        
        def check_docstring(body):
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
                expr_node = body[0]
                docstring_ranges.append((expr_node.lineno, expr_node.end_lineno, len(body) == 1))
                
        check_docstring(tree.body)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                check_docstring(node.body)
                
        if docstring_ranges:
            inter_lines = intermediate.splitlines(keepends=True)
            docstring_ranges.sort(key=lambda x: x[0], reverse=True)
            for start_line, end_line, is_only_stmt in docstring_ranges:
                s_idx = start_line - 1
                e_idx = end_line
                if is_only_stmt:
                    indent = len(inter_lines[s_idx]) - len(inter_lines[s_idx].lstrip())
                    inter_lines[s_idx:e_idx] = [" " * indent + "pass\n"]
                else:
                    del inter_lines[s_idx:e_idx]
            intermediate = "".join(inter_lines)
    except Exception as e:
        print(f"Docstring strip error: {e}")
        
    cleaned = re.sub(r'\n{3,}', '\n\n', intermediate)
    return cleaned.strip() + "\n"

workspace = r"c:\Users\Aman Singh\OneDrive\Desktop\Verifi"

files = []
for root, dirs, filenames in os.walk(workspace):
    if ".venv" in root or "__pycache__" in root or "scratch" in root:
        continue
    for f in filenames:
        if f.endswith(".py"):
            files.append(os.path.join(root, f))

files.sort()
print(f"Applying comment removal to {len(files)} files...")

modified_count = 0
for p in files:
    with open(p, "r", encoding="utf-8") as f:
        src = f.read()
    cleaned = strip_comments_and_docstrings(src)
    if cleaned != src:
        # Verify valid AST before writing
        ast.parse(cleaned)
        with open(p, "w", encoding="utf-8") as f:
            f.write(cleaned)
        modified_count += 1
        rel_path = os.path.relpath(p, workspace)
        print(f"Stripped comments from: {rel_path}")

print(f"\nDone! Modified {modified_count} out of {len(files)} files.")

