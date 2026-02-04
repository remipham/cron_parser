from pathlib import Path
import sys

current_dir = Path(__file__).parent.resolve()
project_root = current_dir.parent.resolve()
sys.path.append(str(project_root))