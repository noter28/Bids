"""init

Revision ID: c130d068129a
Revises:
Create Date: 2023-11-08 13:42:56.692511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c130d068129a'
down_revision = None
branch_labels = None
depends_on = None

create_function = """
    CREATE  FUNCTION update_updated_date()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.last_updated = now();
        RETURN NEW;
    END;
    $$ language 'plpgsql';
"""

create_trigger = """
    CREATE TRIGGER update_updated_date_trigger
        BEFORE UPDATE
        ON
            bids
        FOR EACH ROW
    EXECUTE PROCEDURE update_updated_date();
"""

drop_trigger = """
    DROP TRIGGER update_updated_date_trigger
    ON bids CASCADE;
"""

drop_function = """
    DROP FUNCTION update_updated_date
    CASCADE
"""


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bids',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('beginDate', sa.String(length=50), nullable=True),
    sa.Column('ONE_A', sa.Integer(), nullable=True),
    sa.Column('ONE_B', sa.Integer(), nullable=True),
    sa.Column('TWO_A', sa.Integer(), nullable=True),
    sa.Column('TWO_B', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('client',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('clientLeiCode', sa.String(length=50), nullable=True),
    sa.Column('clientType', sa.String(length=50), nullable=True),
    sa.Column('created_date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('osr',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('osrName', sa.String(length=100), nullable=True),
    sa.Column('osrLeiCode', sa.String(length=100), nullable=True),
    sa.Column('created_date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    op.execute(create_function)
    op.execute(create_trigger)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(drop_trigger)
    op.execute(drop_function)
    op.drop_table('osr')
    op.drop_table('client')
    op.drop_table('bids')
    # ### end Alembic commands ###
