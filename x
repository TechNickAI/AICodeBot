diff --git a/aicodebot/coder.py b/aicodebot/coder.py
--- a/aicodebot/coder.py
+++ b/aicodebot/coder.py
@@ -3,7 +3,7 @@
 from pathlib import Path
 from pygments.lexers import ClassNotFound, get_lexer_for_mimetype, guess_lexer_for_filename
 from types import SimpleNamespace
-import fnmatch, mimetypes, re, subprocess, unidiff
+import fnmatch, mimetypes, re, subprocess
 
 
 class Coder
