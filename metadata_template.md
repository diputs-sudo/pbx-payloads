METADATA schema for pbx blocks:
```python
# Fields:
# ───────────────────────────── Identity ─────────────────────────────
"name": str
    # Full unique identifier for this block, ideally matching its file path
    # Example: "python/base/reverse_shell/reverse_shell__diputs-sudo.py"

"title": str
    # Human-friendly name for this block, used in UIs and search
    # Example: "TCP Reverse Shell"

"description": str
    # Short summary of what this block does
    # Example: "Connects back to a remote server to provide shell access."

# ───────────────────────── Classification ───────────────────────────
"platform": list[str]
    # List of target platforms for this block
    # Example: ["linux", "macos"]

"language": str
    # Programming language or script type (e.g., "python", "ps1", "sh", "c", "go", "js")
    # Example: "python"

"category": str
    # Hierarchical path for organizing/searching blocks (should match folder structure)
    # Example: "base/reverse_shell"

"tags": list[str]
    # Freeform list of extra keywords or features for searching/filtering
    # Example: ["tcp", "interactive", "networking"]

# ───────────────────────── Composition ──────────────────────────────
"chainable": bool
    # True if this block is designed to be composed with or feed into other blocks

"output_type": str
    # Describes the type of output produced by this block (for chaining and automation)
    # Common values: "str", "file", "shell", "object", "bytes", "void"

# ───────────────────────── Dependencies ─────────────────────────────
"import": list[str]
    # List of standard or third-party Python modules imported in this block
    # Example: ["socket", "os"]

"requires_addons": list[str]
    # Internal pbx modules this block depends on (for advanced/optional features)
    # Example: ["discord_webhook"]

"dependencies": list[str]
    # External dependencies/tools required for this block (package or system level)
    # Examples: ["pip:requests", "apt:nc"]

# ───────────────────────── Arguments ────────────────────────────────
"args": list[dict]
    # Arguments the user must provide; each dict should include:
    #   "name": str      # Argument variable name (e.g., "LHOST")
    #   "type": str      # Data type (e.g., "str", "int", "bool", "list", "float")
    #   "required": bool # True if required
    #   "default": Any   # Default value if not required

# ──────────────────────────── Execution ─────────────────────────────
"block_type": str
    # How this block should be executed/used by pbx
    #   "template" → A code template with placeholders (auto-wrapped as a generator function)
    #   "function" → A callable Python function
    #   "script"   → A standalone script to execute as-is

"entrypoint": str
    # Name of the function pbx should call (e.g., "generate", "run", "execute")
    #   For "template": usually "generate"
    #   For "function": could be "run", "execute", etc.

"returns": str
    # Describes what the entrypoint returns; should match "output_type"
    # Example: "str", "file", "object", "void"

# ──────────────────────────── Metadata ──────────────────────────────
"author": str
    # Creator's name or handle

"version": str
    # Block version (semantic versioning recommended, e.g., "1.0.0")

"created": str
    # ISO 8601 date when this block was created ("YYYY-MM-DD")

"updated": str
    # ISO 8601 date of the most recent update ("YYYY-MM-DD")
```

──────────────────────────── Example ──────────────────────────────

METADATA = {
    # ────────── Identity ──────────
    "name":        "python/base/reverse_shell/reverse_shell__diputs-sudo.py", # Unique snake_case identifier for this block, 
    "title":       "TCP Reverse Shell",                  # Human-friendly name
    "description": "Connects back to a remote server to provide shell access.",

    # ────────── Classification ──────────
    "platform":    ["linux", "macos"],                   # Target platforms
    "language":    "python",                             # Source code language
    "category":    "base/reverse_shell",                 # High-level type/category
    "tags":        ["tcp", "interactive", "networking"], # Extra searchable/filterable tags

    # ────────── Composition ──────────
    "chainable":   True,                                 # Can this be combined with other blocks?
    "output_type": "file",                               # What type of output does it produce?

    # ────────── Dependencies ──────────
    "import":      ["socket", "os"],                     # Python modules this code uses
    "requires_addons": [],                               # Internal pbx modules required
    "dependencies": [],                                  # External system/package dependencies

    # ────────── Arguments ──────────
    "args": [
        {"name": "LHOST", "type": "str", "required": True, "default": None},   # Listener host/IP
        {"name": "LPORT", "type": "int", "required": True, "default": None}    # Listener port
    ],

    # ────────── Execution ──────────
    "block_type":  "template",                           # "template" means pbx will auto-wrap as a generator function
    "entrypoint":  "generate",                           # Function name pbx should call (usually "generate" for templates)
    "returns":     "str",                                # This block returns Python code as a string

    # ────────── Metadata ──────────
    "author":      "diputs-sudo",                        # Your name or handle
    "version":     "1.0.0",                              # Block version (auto-incremented on update)
    "created":     "2025-06-23",                         # ISO creation date
    "updated":     "2025-06-23"                          # Last update date
}
