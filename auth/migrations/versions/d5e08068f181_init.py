"""init

Revision ID: d5e08068f181
Revises: 
Create Date: 2023-01-24 17:00:02.473575

"""
import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "d5e08068f181"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "roles",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("name"),
        schema="auth",
    )
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("login", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "email", sqlalchemy_utils.types.email.EmailType(length=255), nullable=True
        ),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=True),
        sa.Column("is_superuser", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("login"),
        schema="auth",
    )
    op.create_table(
        "login_histories",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_agent", sa.String(), nullable=True),
        sa.Column("device", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["auth.users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", "created_at"),
        sa.UniqueConstraint("id", "created_at"),
        postgresql_partition_by="RANGE (created_at)",
        schema="auth",
    )
    op.create_table(
        "user_roles",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("role_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(["role_id"], ["auth.roles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["auth.users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("user_id", "role_id"),
        schema="auth",
    )
    op.execute(
        """CREATE TABLE IF NOT EXISTS "auth"."login_histories_2022" PARTITION OF "auth"."login_histories" FOR VALUES 
        FROM ('2022-1-1 00:00:00') TO ('2023-1-1 00:00:00')"""
    )
    op.execute(
        """CREATE TABLE IF NOT EXISTS "auth"."login_histories_2023" PARTITION OF "auth"."login_histories" FOR VALUES
        FROM ('2023-1-1 00:00:00') TO ('2024-1-1 00:00:00')"""

    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_roles", schema="auth")
    op.drop_table("login_histories", schema="auth")
    op.drop_table("users", schema="auth")
    op.drop_table("roles", schema="auth")
    # ### end Alembic commands ###
