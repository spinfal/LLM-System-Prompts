import os
import glob
import shutil
import sys
import subprocess
import platform

# Outputs a complied .md file of the system prompts

def compile_system_prompts():
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if not script_dir:
            script_dir = os.getcwd()
        
        # Output file path
        output_filename = "LLM System Prompts.md"
        output_path = os.path.join(script_dir, output_filename)
        
        # Find .md files in the current directory
        md_files = glob.glob(os.path.join(script_dir, "*.md"))
        
        # Remove the compilation file itself from the list if it exists
        if output_path in md_files:
            md_files.remove(output_path)

        # Exclude README.md
        readme_path = os.path.join(script_dir, "README.md")
        if readme_path in md_files:
            md_files.remove(readme_path)
        
        if not md_files:
            print(f"No .md files found in {script_dir}")
            return
        
        # Sort files alphabetically
        md_files.sort()
        
        # Check if the output file already exists
        file_existed = os.path.exists(output_path)
        
        print(f"\nFound {len(md_files)} markdown files.\n{'Updating' if file_existed else 'Creating'} {output_path}\n")
        
        # Create/update the output file and write content
        with open(output_path, "w", encoding="utf-8") as output_file:
            # Add initial heading
            output_file.write("# LLM System Prompts\n\n")
            
            skipped_files = []
            
            for i, file_path in enumerate(md_files):
                try:
                    # Extract filename
                    file_name = os.path.basename(file_path)
                    file_name_without_ext = os.path.splitext(file_name)[0]
                    
                    # Check if file is empty
                    if os.path.getsize(file_path) == 0:
                        print(f"Skipping empty file: {file_path}")
                        skipped_files.append(file_path)
                        continue
                    
                    # Try with utf-8 encoding first
                    try:
                        with open(file_path, "r", encoding="utf-8") as input_file:
                            content = input_file.read()
                    except UnicodeDecodeError:
                        print("\nDecoding error occurred:")
                        return
                    
                    # Add separator between prompts (but not before the first one)
                    if i > 0:
                        output_file.write("\n\n---\n\n\n")
                    
                    # Write heading and content with "System Prompt" appended
                    output_file.write(f"# {file_name_without_ext} System Prompt\n\n")
                    output_file.write(content)
                    
                    print(f"Added: {file_path}")
                    
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")
                    skipped_files.append(file_path)
        
        print(f"\nCompilation complete, file {'updated' if file_existed else 'created'}: {output_path}")
        
        if skipped_files:
            print(f"Note: {len(skipped_files)} files were skipped.")
        
        # Open the file
        try:
            print("Opening the compiled file...")
            if platform.system() == 'Windows':
                os.startfile(output_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', output_path], check=True)
            else:  # Linux/Unix
                subprocess.run(['xdg-open', output_path], check=True)
            print("File opened successfully.\n")
        except Exception as e:
            print(f"Could not open file: {str(e)}")
            print(f"File is located at: {os.path.abspath(output_path)}\n")
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.\n")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}\n")
        return

if __name__ == "__main__":
    compile_system_prompts()
