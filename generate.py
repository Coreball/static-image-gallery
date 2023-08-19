import csv
import dominate
import os.path
from dominate.tags import *
from math import ceil

with open("db.csv", "r", newline="") as db:
    reader = csv.DictReader(db)
    data = list(reader)

for page in range(ceil(len(data) / 100)):
    index_start = page * 100
    index_end = (page + 1) * 100
    doc = dominate.document(title=f"Page {page + 1}")
    with doc.head:
        link(rel="stylesheet", href="style.css")
    with doc.body.add(div(cls="gallery")):
        for entry in data[index_start:index_end]:
            filename = entry["Filename"]
            name, ext = os.path.splitext(filename)
            with div():
                a(
                    img(src=f"thumbnails/{name}.thumbnail.jpg", alt=filename),
                    href=f"assets/{filename}",
                )
                a(filename, href=f"assets/{filename}")
    with open(f"{page + 1:02}.html", "w") as out:
        out.write(doc.render())
