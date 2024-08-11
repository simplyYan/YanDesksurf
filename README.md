# YanDesksurf Framework

YanDesksurf is a Python framework that integrates a web browser with encryption and configuration capabilities using PyQt5. It's designed to provide a flexible environment for running web applications with built-in encryption support and a customizable UI.

## Features

- **Integrated Web Browser:** Based on PyQt5's QWebEngineView, offering full web capabilities.
- **3D Acceleration:** Enabled by default for better performance with web graphics.
- **Encryption Support:** Encrypts and decrypts application files for secure deployment.
- **Dynamic Configuration:** Load and apply settings from a configuration file.
- **Custom File Operations:** Executes file operations and system commands based on custom scripts.
- **DOM Monitoring:** Monitors changes in the DOM and evaluates conditions based on those changes.

## Installation

You can install it for Windows, Linux and macOS. For Windows, you can use the pre-compiled version (binary) by [clicking here](https://drive.google.com/file/d/1Tr4YMWHKTFJT6Lr7hijgOE6NyQd3znXV/view?usp=sharing), and for Linux and macOS, you can download the main file ([main.py](https://raw.githubusercontent.com/simplyYan/YanDesksurf/main/main.py)), convert it to executable with PyInstaller and use it!

## Usage

### Configuration

Upon first launch, YanDesksurf will prompt you to configure the application:

1. **Select a .zip file:** Choose a zip file containing your web application.
2. **Encryption Key:** The framework will generate an encryption key and create an encrypted file.

This configuration is saved in `yansurf.json`, which is used for subsequent runs.

### Encryption and Decryption

YanDesksurf uses the `cryptography` library to encrypt and decrypt application files. Encrypted files are saved with a `.yansurf` extension.

### File Operations

The `yanprog.yanprog` script is used to perform file operations and execute system commands:

- `create_file filename`: Creates a new file.
- `delete_file filename`: Deletes an existing file.
- `rename_file src dst`: Renames a file.
- `move_file src dst`: Moves a file.
- `run_command command`: Executes a system command.

### DOM Monitoring

YanDesksurf monitors changes in the DOM:

- **Title Changes:** Prints the new title and evaluates conditions.
- **Content Changes:** Prints notifications when the page content changes.
- **Page Hash:** Computes and prints the hash of the page content.

### Configuration File

The `yansurf.json` configuration file contains:

- `yansurf_file`: Path to the encrypted application file.
- `encryption_key`: The key used for encryption and decryption.
- `window_options`: Optional settings for window size and state.

## Example Configuration File

```json
{
    "yansurf_file": "example.yansurf",
    "encryption_key": "your-encryption-key-here",
    "window_options": {
        "width": 1024,
        "height": 768,
        "resizable": true,
        "fullscreen": false
    }
}
```

## License

This framework is open-source and free to use. See the LICENSE file for more details.

## Contributing

Feel free to contribute by submitting issues or pull requests. For more information on contributing, please refer to the CONTRIBUTING.md file.
