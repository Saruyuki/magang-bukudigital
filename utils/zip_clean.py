import os
import zipfile

def zip_folder_with_precise_exclusions(source_folder, output_zipfile, exclude_rel_paths):
    """
    Zip a folder, excluding specific files/folders by their relative path from source_folder.

    :param source_folder: The base directory to zip
    :param output_zipfile: Name of the output .zip file
    :param exclude_rel_paths: List of paths (relative to source_folder) to exclude
    """
    exclude_set = set(os.path.normpath(p) for p in exclude_rel_paths)

    with zipfile.ZipFile(output_zipfile, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_folder):
            rel_root = os.path.relpath(root, source_folder)

            # Skip this folder if it's in the exclude list
            if rel_root in exclude_set:
                dirs[:] = []  # Prevent descending into it
                continue

            # Exclude any subdirs that match
            dirs[:] = [d for d in dirs if os.path.normpath(os.path.join(rel_root, d)) not in exclude_set]

            for file in files:
                rel_file = os.path.normpath(os.path.join(rel_root, file))
                if rel_file in exclude_set:
                    continue

                full_path = os.path.join(root, file)
                zipf.write(full_path, arcname=rel_file)

# === USAGE EXAMPLE ===

exclude_paths = [
    'accounts/management',
    'accounts/__pycache__',
    'accounts/migrations',
    'buku/management',
    'buku/__pycache__',
    'buku/migrations',
    'bukutamu/__pycache__',
    'dashboard/__pycache__',
    'dashboard/migrations',
    'kehadiran/management',
    'kehadiran/__pycache__',
    'kehadiran/migrations',
    'kunjunganKerja/migrations',
]

zip_folder_with_precise_exclusions(
    source_folder='bukutamu',
    output_zipfile='bukutamu_clean.zip',
    exclude_rel_paths=exclude_paths
)
