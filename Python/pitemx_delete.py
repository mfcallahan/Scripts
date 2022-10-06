# Delete all ".pitemx" and ".pitem" files which are automatically downloaded when clicking the "Open in ArcMap/ArcGIS Pro" button in ArcGIS Online.

import os
from pathlib import Path

def main():
    path = os.path.join(Path.home(), "Downloads")
    proFileExt = ".pitemx"
    arcMapFileExt = ".pitem"
    
    for file in os.listdir(path):
        if file.endswith(proFileExt) or file.endswith(arcMapFileExt):
            try:
                os.remove(os.path.join(path, file))
            except OSError as e:
                # Ignore errors
                pass

if __name__ == "__main__":
    main()

