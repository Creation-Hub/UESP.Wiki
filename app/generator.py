import os
from app import wiki, papyrus

# Generator
#---------------------------------------------

def process(targets: list) -> None:
    # Process each target from the settings
    for target_name, script_dir, output_dir, output_dir_sort, output_objects, output_members in targets:
        # Validate provided configuration values
        if not script_dir or not output_dir:
            print(f"SCRIPT_DIR or OUTPUT_DIR not set for a target in settings.")
            continue
        if not os.path.exists(script_dir):
            print(f"Script directory does not exist: '{script_dir}'")
            continue
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Search for Papyrus scripts in the script directory
        script_paths = papyrus.find_files(script_dir)

        # Write wiki pages for each script found
        for script_path in script_paths:
            file_name = os.path.basename(script_path) # Get the base name of the file
            script_name = os.path.splitext(file_name)[0] # Remove the file extension
            output_file_name = f"{script_name}.wiki"
            output_directory = output_dir
            if output_dir_sort:
                output_directory = os.path.join(output_dir, script_name)
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)
            output_path = os.path.join(output_directory, output_file_name)

            if output_objects:
                # Write a wiki page for this script
                wiki.page.write(script_path, output_path)
                print(f"[{target_name}] {script_name}:\n  -> in:  {script_path}\n  -> out: {output_path}")

            if output_members:
                print("Not implemented yet for output_members.")
                pass
