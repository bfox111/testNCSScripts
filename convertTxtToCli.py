# convertTxtToCli.py
import os
import json
import argparse
from pathlib import Path

def process_directory(directory_path_str):
    """
    Finds all .txt files, parses them as JSON, cleans the command strings
    (removing unwanted '\n' and whitespace), and saves them to .cli files.
    """
    directory_path = Path(directory_path_str)

    if not directory_path.is_dir():
        print(f"Error: The path '{directory_path}' is not a valid directory.")
        return

    print(f"Scanning for .txt files in '{directory_path}'...\n")
    converted_count = 0
    
    for file_path in directory_path.glob('*.txt'):
        print(f"Processing '{file_path.name}'...")
        cli_file_path = file_path.with_suffix('.cli')

        try:
            # --- Core Logic ---
            # 1. Read the text content
            json_content = file_path.read_text()
            
            # 2. Parse the text as JSON
            data = json.loads(json_content)
            
            # 3. Access the list of commands
            commands_list = data['commands']
            
            # 4. Clean each command in the list.
            #    The .strip() method removes leading/trailing whitespace,
            #    including the newline characters (\n) at the end of the strings.
            cleaned_commands = [cmd.strip() for cmd in commands_list]
            
            # 5. Join the cleaned commands into a single string, with each
            #    command separated by a newline.
            cli_output = "\n".join(cleaned_commands)
            
            # 6. Write the final, clean output to the .cli file
            cli_file_path.write_text(cli_output)
            
            print(f"  -> Successfully created '{cli_file_path.name}'")
            converted_count += 1

        except json.JSONDecodeError:
            print(f"  -> Error: File '{file_path.name}' is not valid JSON. Skipping.")
        except KeyError:
            print(f"  -> Error: JSON in '{file_path.name}' does not contain a 'commands' key. Skipping.")
        except Exception as e:
            print(f"  -> An unexpected error occurred with '{file_path.name}': {e}. Skipping.")

    print(f"\nProcessing complete. Converted {converted_count} file(s).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Converts JSON command files (.txt) to clean, runnable CLI script files (.cli)."
    )
    parser.add_argument(
        "directory",
        help="The directory containing the .txt files to convert. Use '.' for the current directory."
    )
    
    args = parser.parse_args()
    
    process_directory(args.directory)