"""def simple_file_modifier(input_file, output_file):

    Simple function to read, modify, and write a file

    try:
        # Read the file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Apply modifications (customize these as needed)
        modifications = [
            # Remove empty lines
            lambda x: '\n'.join(line for line in x.split('\n') if line.strip()),
            # Trim whitespace from each line
            lambda x: '\n'.join(line.strip() for line in x.split('\n')),
            # Add line numbers
            lambda x: '\n'.join(f"{i + 1}: {line}" for i, line in enumerate(x.split('\n')))
        ]

        for mod in modifications:
            content = mod(content)

        # Write to new file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('hello plp buddies')

        print(f"✅ File modified successfully: {output_file}")

    except FileNotFoundError:
        print(f"❌ Error: File '{input_file}' not found")
    except Exception as e:
        print(f"❌ Error: {e}")


# Usage example
if __name__ == "__main__":
    simple_file_modifier("input.txt", "output.txt")
    """
import os
import sys
from pathlib import Path


def get_valid_filename():
    """
    Ask user for a filename and validate it exists and can be read
    Returns the valid filename or None if user wants to quit
    """
    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:
        try:
            # Get filename from user
            filename = input("\n📁 Please enter the filename to read: ").strip()

            if not filename:
                print("❌ Error: Filename cannot be empty. Please try again.")
                attempts += 1
                continue

            # Check if file exists
            if not os.path.exists(filename):
                raise FileNotFoundError(f"File '{filename}' does not exist")

            # Check if it's a file (not a directory)
            if not os.path.isfile(filename):
                raise IsADirectoryError(f"'{filename}' is a directory, not a file")

            # Check file size (prevent reading huge files accidentally)
            file_size = os.path.getsize(filename)
            if file_size > 10 * 1024 * 1024:  # 10MB limit
                response = input(
                    f"⚠️  Warning: File is large ({file_size / 1024 / 1024:.1f} MB). Continue? (y/n): ").lower()
                if response != 'y':
                    print("Operation cancelled.")
                    return None

            # Check read permissions
            if not os.access(filename, os.R_OK):
                raise PermissionError(f"No read permission for file '{filename}'")

            # Try to open the file to verify it can be read
            with open(filename, 'r', encoding='utf-8') as test_file:
                test_file.read(100)  # Read first 100 bytes to test

            print(f"✅ File '{filename}' is valid and readable")
            return filename

        except FileNotFoundError as e:
            print(f"❌ {e}")
            suggestions = suggest_similar_files(filename)
            if suggestions:
                print("💡 Did you mean one of these?")
                for suggestion in suggestions:
                    print(f"   • {suggestion}")

        except IsADirectoryError as e:
            print(f"❌ {e}")
            # Show contents of the directory
            try:
                files_in_dir = [f for f in os.listdir(filename) if os.path.isfile(os.path.join(filename, f))]
                if files_in_dir:
                    print("📂 Files in this directory:")
                    for file in files_in_dir[:5]:  # Show first 5 files
                        print(f"   • {file}")
                    if len(files_in_dir) > 5:
                        print(f"   • ... and {len(files_in_dir) - 5} more")
            except PermissionError:
                print("⛔ No permission to list directory contents")

        except PermissionError as e:
            print(f"❌ {e}")
            print("💡 Try running the program with appropriate permissions")

        except UnicodeDecodeError:
            print(f"❌ Cannot read file '{filename}' - encoding issue detected")
            response = input("Try with different encoding? (y/n): ").lower()
            if response == 'y':
                try:
                    return handle_encoding_issue(filename)
                except Exception as encoding_error:
                    print(f"❌ Still cannot read file: {encoding_error}")

        except Exception as e:
            print(f"❌ Unexpected error reading file: {e}")

        attempts += 1
        remaining_attempts = max_attempts - attempts
        if remaining_attempts > 0:
            print(f"🔄 {remaining_attempts} attempt(s) remaining")
        else:
            print("⛔ Maximum attempts reached")

    return None


def suggest_similar_files(missing_filename):
    """
    Suggest files that might be similar to the missing filename
    """
    suggestions = []
    current_dir = Path.cwd()
    missing_name = Path(missing_filename).name.lower()

    try:
        # Look for files with similar names in current directory
        for file_path in current_dir.iterdir():
            if file_path.is_file():
                if missing_name in file_path.name.lower():
                    suggestions.append(file_path.name)
                elif file_path.suffix.lower() == Path(missing_filename).suffix.lower():
                    suggestions.append(file_path.name)

        # Limit suggestions to 3 most relevant
        return suggestions[:3]
    except:
        return []


def handle_encoding_issue(filename):
    """
    Handle files with different encodings
    """
    encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'ascii']

    for encoding in encodings_to_try:
        try:
            with open(filename, 'r', encoding=encoding) as test_file:
                content = test_file.read(200)  # Read first 200 characters
            print(f"✅ Successfully read with {encoding} encoding")
            return filename
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error with {encoding}: {e}")
            continue

    raise Exception("Could not read file with any supported encoding")


def read_file_safely(filename):
    """
    Read file content with comprehensive error handling
    """
    try:
        # Try UTF-8 first
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        return content, 'utf-8'

    except UnicodeDecodeError:
        # Fallback to other encodings
        encodings = ['latin-1', 'cp1252', 'iso-8859-1']
        for encoding in encodings:
            try:
                with open(filename, 'r', encoding=encoding) as file:
                    content = file.read()
                print(f"📖 Read file using {encoding} encoding")
                return content, encoding
            except UnicodeDecodeError:
                continue

        raise UnicodeDecodeError("Could not decode file with any supported encoding")

    except Exception as e:
        raise Exception(f"Error reading file: {e}")


def modify_content(content):
    """
    Apply modifications to the file content
    """
    # Example modifications - customize as needed
    modifications = [
        # Remove empty lines
        lambda x: '\n'.join(line for line in x.split('\n') if line.strip()),
        # Trim whitespace
        lambda x: '\n'.join(line.strip() for line in x.split('\n')),
        # Add line numbers
        lambda x: '\n'.join(f"{i + 1:3d} | {line}" for i, line in enumerate(x.split('\n')))
    ]

    for mod in modifications:
        content = mod(content)

    return content


def main():
    """
    Main program function
    """
    print("=" * 50)
    print("📄 FILE MODIFIER PROGRAM")
    print("=" * 50)

    # Get valid filename from user
    filename = get_valid_filename()
    if not filename:
        print("🚪 Exiting program.")
        return

    try:
        # Read the file
        print(f"\n📖 Reading file: {filename}")
        content, encoding_used = read_file_safely(filename)

        # Show file info
        file_size = os.path.getsize(filename)
        line_count = len(content.split('\n'))
        print(f"📊 File info: {line_count} lines, {file_size} bytes, {encoding_used} encoding")

        # Show preview
        print("\n👀 Preview (first 5 lines):")
        lines = content.split('\n')[:5]
        for i, line in enumerate(lines):
            print(f"   {i + 1}: {line[:80]}{'...' if len(line) > 80 else ''}")

        if line_count > 5:
            print(f"   ... and {line_count - 5} more lines")

        # Ask if user wants to modify
        response = input("\n🛠️  Do you want to modify this file? (yes/no): ").lower()
        if response != 'yes':
            print("Operation cancelled.")
            return

        # Apply modifications
        print("🔄 Applying modifications...")
        modified_content = modify_content(content)

        # Get output filename
        output_filename = input("💾 Enter output filename (or press Enter for 'modified_output.txt'): ").strip()
        if not output_filename:
            output_filename = "modified_output.txt"

        # Check if output file exists
        if os.path.exists(output_filename):
            overwrite = input(f"⚠️  File '{output_filename}' exists. Overwrite? (yes/no): ").lower()
            if overwrite != 'yes':
                print("Operation cancelled.")
                return

        # Write output file
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            output_file.write(modified_content)

        print(f"✅ Success! Modified file saved as: {output_filename}")

        # Show result preview
        print("\n📋 Modified content preview:")
        modified_lines = modified_content.split('\n')[:3]
        for line in modified_lines:
            print(f"   {line[:80]}{'...' if len(line) > 80 else ''}")

    except Exception as e:
        print(f"❌ Error during processing: {e}")
        print("💡 Please check file permissions and content")


def create_sample_file():
    """Create a sample file for testing if needed"""
    sample_content = """Hello! This is a sample file.

It contains multiple lines of text.

Some lines have extra spaces    at the end.  

Empty lines will be removed during processing.

This file is encoded in UTF-8 format.
"""

    try:
        with open("sample.txt", "w", encoding='utf-8') as f:
            f.write(sample_content)
        print("✅ Created sample.txt for testing")
    except Exception as e:
        print(f"❌ Could not create sample file: {e}")


if __name__ == "__main__":
    # Create sample file if no files exist in directory
    if not any(f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.txt')):
        print("ℹ️  No text files found in current directory")
        create_sample_file()

    main()