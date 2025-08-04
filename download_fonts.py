import os
import requests
import zipfile
import io

def ensure_fonts_available():
    """
    Downloads required TrueType fonts from the official GitHub release if they are not
    already present. This ensures compatibility with reportlab.
    """
    fonts_to_check = ['Inter-Bold.ttf', 'Inter-Regular.ttf']
    
    # Check if both fonts are already present
    if all(os.path.exists(font) for font in fonts_to_check):
        print("All required fonts already exist.")
        return

    # URL to the official GitHub release zip file
    zip_url = 'https://github.com/rsms/inter/releases/download/v4.0/Inter-4.0.zip'
    zip_file_name = 'Inter-4.0.zip'

    print("Checking for required fonts...")
    try:
        if not os.path.exists(zip_file_name):
            print(f"Downloading font package from {zip_url}...")
            response = requests.get(zip_url, timeout=10)
            response.raise_for_status()
            with open(zip_file_name, 'wb') as f:
                f.write(response.content)
            print("Successfully downloaded font package.")
        
        # Extract the TTF files from the downloaded zip
        with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
            print("Extracting required fonts...")
            for member in zip_ref.namelist():
                if member.endswith('Inter-Bold.ttf') or member.endswith('Inter-Regular.ttf'):
                    # The files are nested, e.g., "Inter Desktop/Inter-Bold.ttf"
                    with open(os.path.basename(member), 'wb') as outfile:
                        outfile.write(zip_ref.read(member))
                    print(f"Successfully extracted {os.path.basename(member)}.")
        
        # Clean up the downloaded zip file
        os.remove(zip_file_name)
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to download font package: {e}")
        print("Please check your internet connection or the font URL.")
        exit(1)
    except zipfile.BadZipFile:
        print(f"Failed to open zip file {zip_file_name}. It may be corrupted.")
        exit(1)