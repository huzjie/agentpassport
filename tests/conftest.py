# -*- coding: utf-8 -*-
import sys
from pathlib import Path

# 保证可从项目根导入 agentpassport
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
