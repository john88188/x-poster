import os
import pathlib

# 创建 xfile 目录
xfile_path = pathlib.Path('xfile')
if not xfile_path.exists():
    xfile_path.mkdir(parents=True, exist_ok=True)
    print("Successfully created xfile directory")
