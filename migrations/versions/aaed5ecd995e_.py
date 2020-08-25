"""empty message

Revision ID: aaed5ecd995e
Revises: 26cfbe6cc103
Create Date: 2020-05-30 12:11:24.852575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aaed5ecd995e'
down_revision = '26cfbe6cc103'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artist', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('artist', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    op.alter_column('artist', 'location_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('artist', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.drop_column('artist', 'genres')
    op.alter_column('venue', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('venue', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    op.alter_column('venue', 'location_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('venue', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venue', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('venue', 'location_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('venue', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    op.alter_column('venue', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.add_column('artist', sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.alter_column('artist', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('artist', 'location_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('artist', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    op.alter_column('artist', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    # ### end Alembic commands ###
