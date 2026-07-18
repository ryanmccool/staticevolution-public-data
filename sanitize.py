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
# Remove relationships and history left behind by filtered private rows.
for join_table, parent_table, foreign_key in (
    ("blog_entry_tags", "blog_entry", "entry_id"),
    ("blog_blogmark_tags", "blog_blogmark", "blogmark_id"),
    ("blog_quotation_tags", "blog_quotation", "quotation_id"),
    ("blog_note_tags", "blog_note", "note_id"),
    ("blog_elsewhereitem_tags", "blog_elsewhereitem", "elsewhereitem_id"),
    ("guides_chapter_tags", "guides_chapter", "chapter_id"),
    ("blog_photoset_photos", "blog_photoset", "photoset_id"),
):
    connection.execute(
        f"delete from [{join_table}] where [{foreign_key}] not in (select id from [{parent_table}])"
    )
connection.execute(
    "delete from blog_photoset_photos where photo_id not in (select id from blog_photo)"
)
connection.execute(
    "delete from guides_chapterchange where chapter_id not in (select id from guides_chapter)"
)
connection.execute(
    "delete from blog_tag where id not in ("
    "select tag_id from blog_entry_tags union select tag_id from blog_blogmark_tags union "
    "select tag_id from blog_quotation_tags union select tag_id from blog_note_tags union "
    "select tag_id from blog_elsewhereitem_tags union select tag_id from guides_chapter_tags)"
)
# Public exports contain stable application URLs, never private bucket object keys.
connection.execute("alter table blog_photo add column public_url text")
connection.execute(
    "update blog_photo set public_url = 'https://staticevolution.com/media/photos/' || id || '/'"
)
connection.execute("alter table blog_photo drop column image")
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
