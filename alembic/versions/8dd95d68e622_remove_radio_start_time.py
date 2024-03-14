"""Remove radio_start_time

Revision ID: 8dd95d68e622
Revises: 951b4b2270fa
Create Date: 2024-03-14 18:47:25.452561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8dd95d68e622'
down_revision = '951b4b2270fa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Guilds', 'RadioStartTime')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Guilds', sa.Column('RadioStartTime', sa.DATETIME(), nullable=True))
    # ### end Alembic commands ###
