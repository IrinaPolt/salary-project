"""create_main_tables

Revision ID: 271f7a381789
Revises: 
Create Date: 2023-06-04 13:03:27.804067

"""
from alembic import op
import datetime
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '271f7a381789'
down_revision = None
branch_labels = None
depends_on = None


def create_users_table() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("first_name", sa.Text, nullable=True),
        sa.Column("last_name", sa.Text, nullable=True),
        sa.Column("email", sa.String, unique=True, nullable=False),
        sa.Column("password_hash", sa.LargeBinary, nullable=False)
    )


def create_promotions_table() -> None:
    op.create_table(
        "promotions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("position", sa.Text, nullable=True),
        sa.Column("promotion_date", sa.DateTime, default=datetime.datetime(2024, 1, 1)),
    )


def create_wages_table() -> None:
    op.create_table(
        "wages",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("rate", sa.Float, nullable=False),
    )


def upgrade() -> None:
    create_users_table()
    create_promotions_table()
    create_wages_table()


def downgrade() -> None:
    op.drop_table("promotions")
    op.drop_table("users")
    op.drop_table("wages")
