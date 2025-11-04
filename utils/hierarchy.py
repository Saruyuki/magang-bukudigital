import os

def print_directory_tree(root_dir, indent="", exclude_folders=None):
    """Recursively prints the folder and file hierarchy, excluding certain folders."""
    if exclude_folders is None:
        exclude_folders = []  # default to no exclusions

    try:
        items = sorted(os.listdir(root_dir))
    except PermissionError:
        print(f"{indent} [Access Denied]")
        return

    for item in items:
        path = os.path.join(root_dir, item)

        # Skip excluded folders
        if os.path.isdir(path) and item in exclude_folders:
            continue

        if os.path.isdir(path):
            print(f"{indent} {item}")
            print_directory_tree(path, indent + "    ", exclude_folders)
        else:
            print(f"{indent} {item}")

# === Example usage ===
root_directory = r"D:\Project\Magang\Work\Day08"  # 👈 change this path
exclude_list = [".git", "management", "__pycache__", "migrations", "utils"]  # 👈 folders to exclude

print(f" Directory structure for: {root_directory}\n")
print_directory_tree(root_directory, exclude_folders=exclude_list)
