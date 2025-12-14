from sqlalchemy import Table, Column, ForeignKey

from pythonFiles.database import db

project_to_palette_table = Table(
    "project_to_palette",
    db.metadata,
    Column("project_id", ForeignKey("project.id"), primary_key=True),
    Column("palette_id", ForeignKey("palette.id"), primary_key=True),
)
