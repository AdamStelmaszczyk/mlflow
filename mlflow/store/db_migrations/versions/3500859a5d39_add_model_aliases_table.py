"""Add Model Aliases table

Revision ID: 3500859a5d39
Revises: 97727af70f4d
Create Date: 2023-03-09 15:33:54.951736

"""
from alembic import op
import sqlalchemy as sa
from mlflow.store.model_registry.dbmodels.models import SqlRegisteredModelAlias
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = "3500859a5d39"
down_revision = "97727af70f4d"
branch_labels = None
depends_on = None


def get_existing_tables():
    connection = op.get_bind()
    inspector = Inspector.from_engine(connection)
    return inspector.get_table_names()


def upgrade():
    if SqlRegisteredModelAlias.__tablename__ not in get_existing_tables():
        op.create_table(
            SqlRegisteredModelAlias.__tablename__,
            sa.Column("name", sa.String(length=256), primary_key=True, nullable=False),
            sa.Column("alias", sa.String(length=256), primary_key=True, nullable=False),
            sa.Column("version", sa.Integer(), nullable=False),
            sa.PrimaryKeyConstraint("name", "alias", name="registered_model_alias_pk"),
            sa.ForeignKeyConstraint(
                ("name", "version"),
                ("model_versions.name", "model_versions.version"),
                onupdate="cascade",
                name="registered_model_alias_name_version_fkey",
            ),
        )


def downgrade():
    pass
