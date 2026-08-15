import os
import zipfile
import tempfile
import shutil

def scrub_file(filepath, search_term, replace_term):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    print(f"Scrubbing {filepath}...")
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Extract the archive
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
            
        # Traverse and replace in all XML files
        replaced_count = 0
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.endswith('.xml'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if search_term in content or search_term.lower() in content or search_term.upper() in content:
                        content = content.replace(search_term, replace_term)
                        content = content.replace(search_term.lower(), replace_term.lower())
                        content = content.replace(search_term.upper(), replace_term.upper())
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        replaced_count += 1
        
        # Zip it back up
        new_filepath = filepath + ".new"
        with zipfile.ZipFile(new_filepath, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zip_ref.write(file_path, arcname)
        
        # Replace original file
        shutil.move(new_filepath, filepath)
        print(f"Done scrubbing {filepath}. Modified {replaced_count} XML files.")
        
    finally:
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    files_to_scrub = [
        "E-Commerce_Project_Report.docx",
        "E-Commerce_Analysis_Presentation.pptx"
    ]
    for f in files_to_scrub:
        scrub_file(f, "Anmol", "Vivek")
