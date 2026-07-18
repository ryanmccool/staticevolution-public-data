import datetime
import sqlite3
import sys

path = sys.argv[1]
now = datetime.datetime.now(datetime.UTC).isoformat()
connection = sqlite3.connect(path)
for table in ("blog_entry", "blog_blogmark", "blog_quotation", "blog_note", "blog_elsewhereitem"):
    connection.execute(f"delete from {table} where is_draft = 1 or created > ?", (now,))
for table in ("guides_chapter",):
    connection.execute(
        f"delete from {table} where is_draft = 1 or is_unlisted = 1 or created > ? "
        "or guide_id in (select id from guides_guide where is_draft = 1)",
        (now,),
    )
connection.execute("delete from guides_guidesection where guide_id in (select id from guides_guide where is_draft = 1)")
connection.execute("delete from guides_guide where is_draft = 1")
connection.execute("delete from blog_photo where is_draft = 1")
connection.execute("delete from blog_photoset where is_draft = 1")
for table in ("pages_page", "products_product"):
    connection.execute(f"delete from {table} where status != 'published'")
# Operational/private fields are not useful in the public mirror.
for table in ("blog_entry", "blog_blogmark", "blog_quotation", "blog_note", "blog_elsewhereitem", "guides_chapter"):
    columns = {row[1] for row in connection.execute(f"pragma table_info([{table}])")}
    for column in ("search_document", "import_ref"):
        if column in columns:
            connection.execute(f"alter table [{table}] drop column [{column}]")
connection.commit()
# Fail closed if a forbidden table entered the export.
for (table,) in connection.execute("select name from sqlite_master where type='table'"):
    if table.startswith(("auth_", "django_admin_", "django_session")):
        raise SystemExit(f"Forbidden private table exported: {table}")
connection.close()
