# Claude Process GUI

This is a graphical user interface (GUI) application that processes text files using the Anthropic Claude API. It allows users to select prompt files, text files, and an output directory, and then processes the files using the Claude API to generate markdown output.

## Features

- Select prompt file, text file(s), and output directory
- Configure API settings (API key, model, max tokens, temperature)
- Process files using the Anthropic Claude API
- Convert API responses to markdown format
- Save and load configuration settings
- Persistent storage of API key and temperature settings

## Requirements

- Python 3.7+
- tkinter (usually included with Python installations)
- See `requirements.txt` for a list of required Python packages

## Installation

1. Clone this repository or download the source code:
   ```
   git clone https://github.com/j816/ClaudetoMD.git
   cd claude-process-gui
   ```

2. Set up a virtual environment (recommended):
   - Create a new virtual environment:
     ```
     python -m venv name_env
     ```
   - Activate the virtual environment:
     - On Unix or MacOS:
       ```
       source name_env/bin/activate
       ```
     - On Windows:
       ```
       venv\Scripts\activate
       ```
   - Your command prompt should now show the name of your virtual environment, indicating it's active.

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your Anthropic API key in the settings tab of the application when you first run it.

5. When you're done using the application, you can deactivate the virtual environment:
   ```
   deactivate
   ```

If you encounter issues with tkinter:
- On Ubuntu or Debian: `sudo apt-get install python3-tk`
- On Fedora: `sudo dnf install python3-tkinter`
- On macOS with Homebrew: `brew install python-tk`

Note: Always activate your virtual environment before running the application or installing new packages for this project.

## Usage

1. Run the script:
   ```
   python anmd.py
   ```

2. Prepare your prompt file:
   - The prompt file must include a `{{TEXT}}` placeholder where you want the content of your text file to be inserted.
   - Example: "Summarize the following text: {{TEXT}}"

3. In the GUI:
   - Select your prompt file, text file(s), and output directory in the Main tab.
   - Configure the API settings in the Settings tab (API key, model, max tokens, temperature).
   - Click "Process" to start processing your files.

4. The application will generate markdown files in the specified output directory.

## Configuration

- You can save and load configuration settings using the "Save Config" and "Load Config" buttons in the main interface.
- API key and temperature settings are automatically saved to `api_config.json` in the same directory as the script.

## Development

To contribute to this project:

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes and commit them
4. Push to your fork and submit a pull request

Please ensure your code adheres to the existing style and includes appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please file an issue on the GitHub issue tracker.

For more information, contact [Your Name] at [your.email@example.com].
