"""third

Revision ID: 3d217a7f9019
Revises: 17908299d276
Create Date: 2022-12-25 18:56:31.712766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d217a7f9019'
down_revision = '17908299d276'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
    op.alter_column("Ban_list", "tg_id", existing_type=sa.Integer(), type_=sa.BigInteger())


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
    op.alter_column("Ban_list", "tg_id", existing_type=sa.BigInteger(), type_=sa.Integer())
