"""Added Author , Books and  Storing information table

Revision ID: ebbd2134d668
Revises: 
Create Date: 2024-02-17 18:26:18.786724

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ebbd2134d668"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "author",
        sa.Column("key", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("birth_date", sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint("key"),
    )
    op.create_table(
        "book",
        sa.Column("key", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("publish_year", sa.Integer(), nullable=False),
        sa.Column("barcode", sa.String(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["author.key"],
        ),
        sa.PrimaryKeyConstraint("key"),
        sa.UniqueConstraint("barcode"),
    )
    op.create_table(
        "storing_information",
        sa.Column("key", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(
            ["book_id"],
            ["book.key"],
        ),
        sa.PrimaryKeyConstraint("key"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("storing_information")
    op.drop_table("book")
    op.drop_table("author")
    # ### end Alembic commands ###