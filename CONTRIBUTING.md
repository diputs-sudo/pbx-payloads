# Contributing to pbx-payloads

Thank you for your interest in contributing to `pbx-payloads`!  
We aim to create a high-quality, ethical, and modular collection of payloads for security research, training, and authorized testing.

Please **read all guidelines below before submitting a contribution.**

---

## ETHICS & LEGAL NOTICE 

- Only contribute payloads intended for **lawful, ethical security research, academic use, security training, or authorized penetration testing**.
- Do **NOT** submit payloads intended for, or easily adaptable to, illegal activity (malware, ransomware, spyware, data exfiltration, surveillance, etc).
- **Every contributor is responsible for ensuring** their submission complies with all applicable laws, regulations, and this project’s license.

Any submissions violating these guidelines **will be rejected and may be reported.**

---

## How to Contribute

1. **Fork this repository.**
2. Add your payload module to the appropriate folder, using a clear and descriptive filename.
3. Add a valid `METADATA` dictionary at the top of your file (see below).
4. Write **clear documentation** for your payload:
   - What it does
   - What it targets or tests
   - Example usage, if possible
   - Any risks, preconditions, or side effects
5. Make sure your code is clean, well-commented, and follows repo conventions.
6. Submit a **pull request (PR)** with a descriptive title and summary of your changes.

---

## Code & Content Guidelines

- **No hardcoded credentials, API keys, or secrets.**
- **No payloads that deliberately harm, destroy, or persistently compromise systems.**
- **No copyright-infringing or proprietary code.**
- Keep payloads modular and readable.
- Prefer generic or widely applicable payloads over highly-targeted/obscure ones (when possible).

---

## Attribution

- All contributions must preserve original authorship and license statements.
- You **may add your name** as a contributor in your payload file and/or PR

We value proper attribution for all contributors.

- If you author, co-author, or make significant improvements to a payload (especially core generation logic), **sign your name or handle in the METADATA's `"author"` field or in your code comments.**
- If multiple people contributed to a payload, you may list them all (e.g., `"author": "alice, bob"`).
- When a part of your code or logic is incorporated into a payload generation method, **your name will be included in the credits for that payload**.
- If you adapted or built upon someone else's work (with permission), please include a brief citation or reference in the comments or the METADATA `"description"` field.

Maintainers will make every reasonable effort to ensure all meaningful contributions are credited.  
**We want everyone’s work to be seen and acknowledged!**
---

## METADATA Required for All Payloads

Every payload **must** include a `METADATA` dictionary at the top of the file, following the [metadata_template.md](metadata_template.md) schema.

- **Why?**  
  This ensures blocks are searchable, categorized, and ready for automated tools and PBX.

- **How to add METADATA?**
  1. Check out [metadata_template.md](metadata_template.md) for the full, documented schema and example.
  2. Use `metadata_builder.py` to auto generate the structure.

- **Submissions without valid METADATA may be rejected or delayed.**

#### Example

```python
METADATA = {
    "name":        "python/base/reverse_shell/reverse_shell__diputs-sudo.py",
    "title":       "TCP Reverse Shell",
    "description": "Connects back to a remote server to provide shell access.",
    "platform":    ["linux", "macos"],
    "language":    "python",
    "category":    "base/reverse_shell",
    "tags":        ["tcp", "interactive", "networking"],
    "chainable":   True,
    "output_type": "file",
    "import":      ["socket", "os"],
    "requires_addons": [],
    "dependencies": [],
    "args": [
        {"name": "LHOST", "type": "str", "required": True, "default": None},
        {"name": "LPORT", "type": "int", "required": True, "default": None}
    ],
    "block_type":  "template",
    "entrypoint":  "generate",
    "returns":     "str",
    "author":      "your-handle",
    "version":     "1.0.0",
    "created":     "YYYY-MM-DD",
    "updated":     "YYYY-MM-DD"
}
```

See [metadata_template.md](metadata_template.md) and use `metadata_builder.py` to make this easy!

---

## Using `metadata_builder.py`

To make adding METADATA easy, we provide a script: `metadata_builder.py`.  
It analyzes your payload file and helps you generate a valid `METADATA` dictionary automatically.

**Usage:**

```bash
python metadata_builder.py <path/to/your_payload.py>
```

- Always run this command from the root of the payloads repository.
- Use the full relative path to your payload file (for example: ./python/base/reverse_shell/reverse_shell__yourname.py).

The script will prompt you for any required fields and output a METADATA block in the file you specified.

If you have questions or issues using `metadata_builder.py`, [open an issue](https://github.com/pbx-payloads/issues) or ask for help in Discussions.

---

## Review Process

- Maintainers will review your PR for safety, clarity, and adherence to guidelines.
- We may suggest improvements or request changes.
- Not all contributions will be accepted, especially if they do not align with the spirit and ethics of this project.

## Questions or Suggestions?

- **Have a question, found a bug, or want to propose a new idea?**  
  Please [open an issue](https://github.com/pbx-payloads/issues) on this repository. We welcome questions, feedback, and discussions about larger changes.

- **Prefer private communication or want to reach the maintainer directly?**  
  You can also contact us via [diputs-sudo@proton.me] 

We look forward to your contributions and ideas!
