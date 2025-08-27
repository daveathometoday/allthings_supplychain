# local_tools/directory_search_tool.py
from pathlib import Path
import re
from typing import List, Dict

class DirectorySearchTool:
    def __init__(self, directory: str = "."):
        self.directory = Path(directory)

    def _read_text(self, path: Path) -> str:
        try:
            return path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return ""

    def search(self, query: str, max_results: int = 50, file_glob: str = "**/*.*") -> List[Dict]:
        tokens = [t.lower() for t in re.findall(r"\w+", query)]
        out = []
        for p in sorted(self.directory.glob(file_glob)):
            if p.is_file():
                txt = self._read_text(p)
                if not txt:
                    continue
                lines = txt.splitlines()
                for i, line in enumerate(lines):
                    line_lower = line.lower()
                    if all(tok in line_lower for tok in tokens):
                        start = max(0, i-1)
                        end = min(len(lines), i+2)
                        snippet = "\n".join(lines[start:end]).strip()
                        out.append({"file": str(p), "lineno": i+1, "snippet": snippet})
                        if len(out) >= max_results:
                            return out
        return out
 
