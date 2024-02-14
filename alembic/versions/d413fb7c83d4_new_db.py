"""New DB

Revision ID: d413fb7c83d4
Revises: 
Create Date: 2022-06-13 12:00:52.405306

"""
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = "d413fb7c83d4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "Guilds",
        sa.Column("DiscordId", sa.BigInteger(), nullable=False),
        sa.Column("IsWelcomeEnabled", sa.Boolean(), nullable=True),
        sa.Column("IsGoodbyeEnabled", sa.Boolean(), nullable=True),
        sa.Column("WelcomeChannelId", sa.BigInteger(), nullable=True),
        sa.Column("GoodbyeChannelId", sa.BigInteger(), nullable=True),
        sa.Column("WelcomeMessage", sa.UnicodeText(), nullable=True),
        sa.Column("GoodbyeMessage", sa.UnicodeText(), nullable=True),
        sa.Column("RadioStartTime", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("DiscordId"),
    )

    op.create_table(
        "Users",
        sa.Column("DiscordId", sa.BigInteger(), nullable=False),
        sa.Column("WarnCount", sa.SmallInteger(), nullable=True),
        sa.Column("OsuUsername", sa.Text(), nullable=True),
        sa.Column("OsuMode", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("DiscordId"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("Users")
    op.drop_table("Guilds")
    # ### end Alembic commands ###
