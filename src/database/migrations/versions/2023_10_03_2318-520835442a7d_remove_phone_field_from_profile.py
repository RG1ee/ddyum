"""remove phone field from profile

Revision ID: 520835442a7d
Revises: a8d1f055ee70
Create Date: 2023-10-03 23:18:41.300497+03:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "520835442a7d"
down_revision: Union[str, None] = "a8d1f055ee70"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("profile", "phone")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "profile", sa.Column("phone", sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    # ### end Alembic commands ###
