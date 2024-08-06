import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os
import tempfile
import json
import re
import anthropic
import threading
import configparser
import markdown
import asyncio
import errno

# Constants
API_CONFIG_FILE = 'api_config.json'
DEFAULT_MODEL = "claude-3-5-sonnet-20240620"
DEFAULT_MAX_TOKENS = 8192
DEFAULT_TEMPERATURE = 0.0

def handle_error(error_code, message):
    print(f"Error {error_code}: {message}")
    return error_code

def load_api_config():
    if os.path.exists(API_CONFIG_FILE):
        with open(API_CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {'api_key': '', 'temperature': DEFAULT_TEMPERATURE}

def save_api_config(api_key: str, temperature: float):
    with open(API_CONFIG_FILE, 'w') as f:
        json.dump({'api_key': api_key, 'temperature': temperature}, f)

class ClaudeProcessGUI:
    def __init__(self, master):
        self.master = master
        master.title("Claude Process GUI")
        master.geometry("800x600")

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill='both')

        self.main_frame = ttk.Frame(self.notebook)
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text='Main')
        self.notebook.add(self.settings_frame, text='Settings')

        self.setup_main_frame()
        self.setup_settings_frame()

        api_config = load_api_config()
        self.api_key_entry.insert(0, api_config.get('api_key', ''))
        self.temperature_var.set(api_config.get('temperature', DEFAULT_TEMPERATURE))

    def setup_main_frame(self):
        self.prompt_label = ttk.Label(self.main_frame, text="Prompt File:")
        self.prompt_label.pack()
        self.prompt_entry = ttk.Entry(self.main_frame, width=50)
        self.prompt_entry.pack()
        self.prompt_button = ttk.Button(self.main_frame, text="Browse", command=self.browse_prompt)
        self.prompt_button.pack()

        self.text_label = ttk.Label(self.main_frame, text="Text File(s):")
        self.text_label.pack()
        self.text_entry = ttk.Entry(self.main_frame, width=50)
        self.text_entry.pack()
        self.text_button = ttk.Button(self.main_frame, text="Browse", command=self.browse_text)
        self.text_button.pack()

        self.output_label = ttk.Label(self.main_frame, text="Output Directory:")
        self.output_label.pack()
        self.output_entry = ttk.Entry(self.main_frame, width=50)
        self.output_entry.pack()
        self.output_button = ttk.Button(self.main_frame, text="Browse", command=self.browse_output)
        self.output_button.pack()

        self.process_button = ttk.Button(self.main_frame, text="Process", command=self.start_process)
        self.process_button.pack(pady=20)

        self.log_window = scrolledtext.ScrolledText(self.main_frame, height=10)
        self.log_window.pack(expand=True, fill='both')

        self.save_config_button = ttk.Button(self.main_frame, text="Save Config", command=self.save_config)
        self.save_config_button.pack(side='left', padx=5, pady=5)
        self.load_config_button = ttk.Button(self.main_frame, text="Load Config", command=self.load_config)
        self.load_config_button.pack(side='left', padx=5, pady=5)

    def setup_settings_frame(self):
        self.api_key_label = ttk.Label(self.settings_frame, text="Anthropic API Key:")
        self.api_key_label.pack()
        self.api_key_entry = ttk.Entry(self.settings_frame, width=50, show="*")
        self.api_key_entry.pack()

        self.model_label = ttk.Label(self.settings_frame, text="Model:")
        self.model_label.pack()
        self.model_var = tk.StringVar(value=DEFAULT_MODEL)
        self.model_entry = ttk.Entry(self.settings_frame, textvariable=self.model_var, state='readonly')
        self.model_entry.pack()

        self.max_tokens_label = ttk.Label(self.settings_frame, text="Max Tokens:")
        self.max_tokens_label.pack()
        self.max_tokens_var = tk.IntVar(value=DEFAULT_MAX_TOKENS)
        self.max_tokens_entry = ttk.Entry(self.settings_frame, textvariable=self.max_tokens_var)
        self.max_tokens_entry.pack()

        self.temperature_label = ttk.Label(self.settings_frame, text="Temperature:")
        self.temperature_label.pack()
        self.temperature_var = tk.DoubleVar(value=DEFAULT_TEMPERATURE)
        self.temperature_entry = ttk.Entry(self.settings_frame, textvariable=self.temperature_var)
        self.temperature_entry.pack()

        self.save_settings_button = ttk.Button(self.settings_frame, text="Save Settings", command=self.save_settings)
        self.save_settings_button.pack(pady=20)

    def browse_prompt(self):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        self.prompt_entry.delete(0, tk.END)
        self.prompt_entry.insert(0, filename)

    def browse_text(self):
        filenames = filedialog.askopenfilenames(filetypes=[("Text files", "*.txt")])
        self.text_entry.delete(0, tk.END)
        self.text_entry.insert(0, ";".join(filenames))

    def browse_output(self):
        directory = filedialog.askdirectory()
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, directory)

    def start_process(self):
        prompt_file = self.prompt_entry.get()
        text_files = self.text_entry.get().split(";")
        output_dir = self.output_entry.get()

        if not self.validate_input(prompt_file, text_files, output_dir):
            return

        self.log("Processing started...")
        self.process_button.config(state='disabled')
        threading.Thread(target=self.run_process, args=(prompt_file, text_files, output_dir)).start()

    def validate_input(self, prompt_file, text_files, output_dir):
        if not prompt_file or not text_files or not output_dir:
            messagebox.showerror("Error", "Please select all required files and directories.")
            return False
        if not os.path.exists(prompt_file):
            messagebox.showerror("Error", f"Prompt file not found: {prompt_file}")
            return False
        for text_file in text_files:
            if not os.path.exists(text_file):
                messagebox.showerror("Error", f"Text file not found: {text_file}")
                return False
        if not os.path.exists(output_dir):
            messagebox.showerror("Error", f"Output directory not found: {output_dir}")
            return False
        return True

    def run_process(self, prompt_file, text_files, output_dir):
        try:
            for text_file in text_files:
                self.log(f"Processing file: {text_file}")
                self.process_single_file(prompt_file, text_file, output_dir)
                self.master.update_idletasks()
            self.log("Processing complete!")
        except Exception as e:
            self.log(f"Error: {str(e)}")
        finally:
            self.process_button.config(state='normal')

    def process_single_file(self, prompt_file, text_file, output_dir):
        with tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8', delete=False) as temp_file:
            merged_content = self.merge_prompt_and_text(prompt_file, text_file)
            temp_file.write(merged_content)
            temp_file.flush()

            api_response = self.call_anthropic_api(temp_file.name)

        markdown_content = self.convert_to_markdown(api_response)
        if markdown_content:
            base_name = os.path.splitext(os.path.basename(text_file))[0]
            output_file = os.path.join(output_dir, f"{base_name}.md")
            self.save_markdown(markdown_content, output_file)
            self.log(f"Markdown content written to {output_file}")
        else:
            self.log("No valid content found in the API response.")

        os.unlink(temp_file.name)

    def merge_prompt_and_text(self, prompt_path: str, text_path: str) -> str:
        with open(prompt_path, 'r') as f:
            prompt = f.read()
        
        with open(text_path, 'r') as f:
            text = f.read()
        
        return prompt.replace('{{TEXT}}', text)

    def call_anthropic_api(self, input_file: str) -> str:
        api_key = self.api_key_entry.get()
        if not api_key:
            raise ValueError("Anthropic API Key is not set")

        client = anthropic.Anthropic(api_key=api_key)

        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        message = client.messages.create(
            model=self.model_var.get(),
            max_tokens=self.max_tokens_var.get(),
            temperature=self.temperature_var.get(),
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": content
                        }
                    ]
                }
            ],
            extra_headers={
                "anthropic-beta": "max-tokens-3-5-sonnet-2024-07-15"
            }
        )
        
        return message.content[0].text if message.content else ""

    def convert_to_markdown(self, content: str) -> str:
        return content.strip()

    def save_markdown(self, content: str, filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

    def log(self, message: str):
        self.log_window.insert(tk.END, message + "\n")
        self.log_window.see(tk.END)

    def save_config(self):
        config = configparser.ConfigParser()
        config['Paths'] = {
            'prompt_file': self.prompt_entry.get(),
            'text_files': self.text_entry.get(),
            'output_dir': self.output_entry.get()
        }
        config['API'] = {
            'api_key': self.api_key_entry.get(),
            'model': self.model_var.get(),
            'max_tokens': str(self.max_tokens_var.get()),
            'temperature': str(self.temperature_var.get())
        }
        
        filename = filedialog.asksaveasfilename(defaultextension=".ini")
        if filename:
            with open(filename, 'w') as configfile:
                config.write(configfile)
            self.log(f"Configuration saved to {filename}")

    def load_config(self):
        filename = filedialog.askopenfilename(filetypes=[("INI files", "*.ini")])
        if filename:
            threading.Thread(target=self._async_load_config, args=(filename,)).start()

    def _async_load_config(self, filename: str):
        config = configparser.ConfigParser()
        config.read(filename)
        self.master.after(0, self._update_ui_with_config, config)

    def _update_ui_with_config(self, config: configparser.ConfigParser):
        self.prompt_entry.delete(0, tk.END)
        self.prompt_entry.insert(0, config['Paths'].get('prompt_file', ''))
        self.text_entry.delete(0, tk.END)
        self.text_entry.insert(0, config['Paths'].get('text_files', ''))
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, config['Paths'].get('output_dir', ''))
        
        if not self.api_key_entry.get():
            self.api_key_entry.delete(0, tk.END)
            self.api_key_entry.insert(0, config['API'].get('api_key', ''))
        self.model_var.set(config['API'].get('model', DEFAULT_MODEL))
        self.max_tokens_var.set(int(config['API'].get('max_tokens', DEFAULT_MAX_TOKENS)))
        self.temperature_var.set(float(config['API'].get('temperature', DEFAULT_TEMPERATURE)))
        
        self.log(f"Configuration loaded from {filename}")

    def save_settings(self):
        api_key = self.api_key_entry.get()
        temperature = self.temperature_var.get()
        save_api_config(api_key, temperature)
        self.log("Settings saved")

def main():
    root = tk.Tk()
    gui = ClaudeProcessGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
