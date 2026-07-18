import pathlib
import sqlite3
import subprocess

path = pathlib.Path("staticevolution.db")
if path.exists():
    path.unlink()
subprocess.run(["sqlite-diffable", "load", str(path), "data", "--replace"], check=True)
connection = sqlite3.connect(path)
for table, columns in {
    "blog_entry": ("title", "body"),
    "blog_blogmark": ("link_title", "commentary"),
    "blog_quotation": ("quotation", "source"),
    "blog_note": ("title", "body"),
    "blog_elsewhereitem": ("title", "commentary"),
    "guides_chapter": ("title", "body"),
}.items():
    existing = {row[0] for row in connection.execute("select name from sqlite_master where type='table'")}
    if table in existing:
        cols = ", ".join(columns)
        connection.execute(f"create virtual table if not exists [{table}_fts] using fts5({cols}, content=[{table}], content_rowid=id)")
        connection.execute(f"insert into [{table}_fts]([{table}_fts]) values ('rebuild')")
connection.commit()
connection.close()
