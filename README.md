# InCore

**InCore** is a minimalist, text editor designed with local encryption and explicit, user-controlled operations

**Note**: InCore is under development and is subjected to changes

## Features

- 🔐 **Individual file encryption**
- 🧠 **Plaintext lives only in RAM while the file is open**
- 💾 **Only encrypted data gets saved**

## Set Up (Using The Terminal / Command Prompt)

Get [git](https://git-scm.com/install/windows) and [Python](https://www.python.org/downloads/) or `python3` and `git` for Linux and MacOS users

1. Clone the repo
```
git clone https://github.com/ghost-in-a-jar-00/InCore-Editor.git
cd InCore-Editor
```

2. Set up python virtual environment

**Windows**
```
mkdir venv
py -m venv venv
venv/bin/activate
```

**Linux and MacOS**
```
mkdir venv
python3 -m venv .
source venv/bin/activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Run command
```
pyinstaller --onefile --name incore --hidden-import=nacl --hidden-import=nacl.bindings --hidden-import=nacl.secret --hidden-import=_cffi_backend main.py
```

5. Deactivate the virtual environment
```
deactivate
```

The **executable** can be found in **dist** folder inside the `InCore-Editor` folder

The executable should be moved to the place you want to store the files at

## Design

InCore is built on a simple idea:

> *Your text should never leave memory unless you explicitly allow it.*

Therefore:
- No background processes
- No temporary files
- No autosaves
- **Only explicit, user-initiated operations**

Security is achieved through **user intent**, not automation


## Use Case

InCore is ideal for:

- Private journals
- Storing seed phrases and other sensitive credentials
- Users who want full control over when data is written and encrypted

## License

This project is licensed under the [MIT License](LICENSE)

## Credits

- Built by **Ghost In A Jar** – [GitHub](https://github.com/ghost-in-a-jar-00)
- GUI: PyQt | Encryption: PyNaCl
- Project link: (https://github.com/ghost-in-a-jar-00/InCore-Editor)
