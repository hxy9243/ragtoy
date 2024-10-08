from typing import List

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import Mapped, mapped_column


Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    path: Mapped[str] = mapped_column(String(256))
    hash: Mapped[str] = mapped_column(String(32))
    type: Mapped[str] = mapped_column(String(16))
    text: Mapped[str] = mapped_column(Text)
    creation_date: Mapped[DateTime] = mapped_column(DateTime)

    chunks: Mapped[List["Chunk"]] = relationship(back_populates="document")

    def __repr__(self):
        return f"<Document {self.id}>"

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "path": self.path,
            "hash": self.hash,
            "type": self.type,
            "creation_date": self.creation_date,
        }

class Chunk(Base):
    __tablename__ = "chunks"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    docid: Mapped[str] = mapped_column(ForeignKey("documents.id"))

    document: Mapped["Document"] = relationship(back_populates="chunks")

    def __repr__(self):
        return f"<Chunk {self.id} from {self.doc.id}: {self.hash}>"

    def to_dict(self):
        return {
            "id": self.id,
            "hash": self.hash,
            "docid": self.doc.id,
        }

