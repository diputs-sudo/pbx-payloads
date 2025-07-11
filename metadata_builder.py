import os
import re
import ast
import sys
import json
from datetime import datetime

PYTHON_STDLIB = {
    'os', 'sys', 're', 'math', 'json', 'socket', 'subprocess', 'time',
    'datetime', 'random', 'base64', 'threading', 'itertools', 'functools'
}

def extract_imports(code):
    tree = ast.parse(code)
    imports = set()
    dependencies = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.add(n.name)
                if n.name.split('.')[0] not in PYTHON_STDLIB:
                    dependencies.add(n.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)
                if node.module.split('.')[0] not in PYTHON_STDLIB:
                    dependencies.add(node.module.split('.')[0])
    return sorted(imports), sorted(dependencies)

def extract_args(code):
    matches = re.findall(r'{(\w+)}', code)
    args = []
    for var in sorted(set(matches)):
        arg_type = 'int' if 'PORT' in var.upper() else 'str'
        args.append({
            'name': var,
            'type': arg_type,
            'required': True,
            'default': None
        })
    return args

def detect_block_type_and_entrypoint(code):
    # Template: has curly-brace placeholders
    if re.search(r'{\w+}', code):
        return "template", "generate"
    # Function: has a top-level def (not inside a class)
    try:
        tree = ast.parse(code)
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                return "function", node.name
    except Exception:
        pass
    # Script: fallback
    return "script", ""

def bump_version(version):
    try:
        major, minor, patch = map(int, version.split('.'))
        return f"{major}.{minor}.{patch+1}"
    except Exception:
        return "1.0.0"

def build_metadata(filepath, existing_metadata=None):
    with open(filepath, "r") as f:
        code = f.read()
    now = datetime.now().strftime("%Y-%m-%d")

    # Filepath to fields
    path_parts = filepath.replace("\\", "/").split("/")
    language = path_parts[0] if len(path_parts) > 0 else "unknown"
    category = "/".join(path_parts[1:-1]) if len(path_parts) > 2 else "misc"
    filename = path_parts[-1]
    name = filepath.replace("\\", "/")
    author = filename.split("__")[-1].split(".")[0]

    imports, dependencies = extract_imports(code)
    args = extract_args(code)
    block_type, entrypoint = detect_block_type_and_entrypoint(code)

    # Output type guess
    if block_type == "template":
        output_type = "str"
        returns = "str"
    elif block_type == "function":
        output_type = "void"
        returns = "void"
    else:
        output_type = ""
        returns = ""

    # Platform guess
    if language == "python":
        platform = ["linux", "macos"]
    elif language == "ps1":
        platform = ["windows"]
    else:
        platform = ["linux", "macos"]

    # Compose new metadata, preferring any existing values
    metadata = {
        "name":         existing_metadata.get("name", name) if existing_metadata else name,
        "title":        existing_metadata.get("title", "") if existing_metadata else "",
        "description":  existing_metadata.get("description", "") if existing_metadata else "",
        "platform":     existing_metadata.get("platform", platform) if existing_metadata else platform,
        "language":     language,
        "category":     existing_metadata.get("category", category) if existing_metadata else category,
        "tags":         existing_metadata.get("tags", []) if existing_metadata else [],
        "chainable":    existing_metadata.get("chainable", True) if existing_metadata else True,
        "output_type":  existing_metadata.get("output_type", output_type) if existing_metadata else output_type,
        "import":       imports,
        "requires_addons": existing_metadata.get("requires_addons", []) if existing_metadata else [],
        "dependencies": dependencies,
        "args":         existing_metadata.get("args", args) if existing_metadata and existing_metadata.get("args") else args,
        "block_type":   existing_metadata.get("block_type", block_type) if existing_metadata else block_type,
        "entrypoint":   existing_metadata.get("entrypoint", entrypoint) if existing_metadata else entrypoint,
        "returns":      existing_metadata.get("returns", returns) if existing_metadata else returns,
        "author":       existing_metadata.get("author", author) if existing_metadata else author,
        "version":      bump_version(existing_metadata["version"]) if existing_metadata and "version" in existing_metadata else "1.0.0",
        "created":      existing_metadata.get("created", now) if existing_metadata else now,
        "updated":      now
    }
    return metadata

def parse_existing_metadata(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    match = re.search(r"METADATA\s*=\s*({.*?})\n", content, re.DOTALL)
    if match:
        meta_str = match.group(1)
        # Clean up comments in args, if any
        meta_str = re.sub(r'#\s*{', '{', meta_str)
        try:
            meta = ast.literal_eval(meta_str)
            return meta
        except Exception:
            return None
    return None

def pretty_metadata_dict(d):
    def pretty(val, indent=1):
        pad = '    ' * indent
        if isinstance(val, list):
            if not val: return "[]"
            return "[\n" + "".join(
                f"{pad}{pretty(x, indent+1)},\n" for x in val
            ) + '    ' * (indent-1) + "]"
        elif isinstance(val, dict):
            return "{\n" + "".join(
                f"{pad}{json.dumps(k)}: {pretty(v, indent+1)},\n" for k, v in val.items()
            ) + '    ' * (indent-1) + "}"
        elif isinstance(val, str):
            return repr(val)
        else:
            return repr(val)
    s = "METADATA = " + "{\n"
    for k, v in d.items():
        s += f"    {json.dumps(k)}: {pretty(v, 2)},\n"
    s += "}\n\n"
    return s

def inject_metadata(filepath, metadata):
    with open(filepath, "r") as f:
        content = f.read()
    # Remove existing METADATA
    content = re.sub(r"METADATA\s*=\s*{.*?}\n\n", "", content, flags=re.DOTALL)
    # Insert METADATA at the top
    metadata_str = pretty_metadata_dict(metadata)
    new_content = metadata_str + content
    with open(filepath, "w") as f:
        f.write(new_content)
    print(f"[+] METADATA injected/updated in {filepath}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 metadata_builder.py /path/to/block.py")
        sys.exit(1)

    target_file = sys.argv[1]
    existing_metadata = parse_existing_metadata(target_file)
    metadata = build_metadata(target_file, existing_metadata)
    inject_metadata(target_file, metadata)

    # Uncomment if you want to prompt for empty fields after update:
    # for k in ['title', 'description', 'output_type', 'returns']:
    #     if not metadata[k]:
    #         print(f"Fill in {k}: (leave blank to skip)")
    #         v = input()
    #         if v: metadata[k] = v