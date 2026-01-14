"""Initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-01-14
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # users
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column(
            "role",
            sa.Enum("user", "admin", name="user_role"),
            nullable=False,
            server_default="user",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    # user_stats
    op.create_table(
        "user_stats",
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("xp_total", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("streak_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_active_date", sa.Date(), nullable=True),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    # levels
    op.create_table(
        "levels",
        sa.Column("code", sa.String(length=10), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("unlock_threshold", sa.Integer(), nullable=False),
        sa.Column("xp_multiplier", sa.Numeric(3, 2), nullable=False),
    )

    # chapters
    op.create_table(
        "chapters",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "level_code",
            sa.String(length=10),
            sa.ForeignKey("levels.code", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=False),
    )
    op.create_index(
        "ix_chapters_level_code_order_index",
        "chapters",
        ["level_code", "order_index"],
        unique=False,
    )

    # missions
    op.create_table(
        "missions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "chapter_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("chapters.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("xp_reward", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("map_key", sa.String(length=100), nullable=False),
    )
    op.create_index(
        "ix_missions_chapter_id_order_index",
        "missions",
        ["chapter_id", "order_index"],
        unique=False,
    )

    # vocab
    op.create_table(
        "vocab",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "mission_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("missions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("word", sa.String(length=255), nullable=False),
        sa.Column("ipa", sa.String(length=255), nullable=True),
        sa.Column("meaning_vi", sa.String(length=255), nullable=False),
        sa.Column("example_en", sa.Text(), nullable=False),
    )
    op.create_index("ix_vocab_mission_id", "vocab", ["mission_id"], unique=False)

    # questions
    op.create_table(
        "questions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "mission_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("missions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("type", sa.String(length=32), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("choices", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("answer", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column("difficulty", sa.Integer(), nullable=False),
    )
    op.create_index(
        "ix_questions_mission_id", "questions", ["mission_id"], unique=False
    )

    # attempts
    op.create_table(
        "attempts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "mission_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("missions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("correct_count", sa.Integer(), nullable=False),
        sa.Column("total", sa.Integer(), nullable=False),
        sa.Column("time_spent_sec", sa.Integer(), nullable=False),
        sa.Column("gained_xp", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.create_index(
        "ix_attempts_user_id_created_at_desc",
        "attempts",
        ["user_id", "created_at"],
        unique=False,
    )

    # mission_progress
    op.create_table(
        "mission_progress",
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "mission_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("missions.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("best_score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("unlocked", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )


def downgrade() -> None:
    op.drop_table("mission_progress")
    op.drop_index("ix_attempts_user_id_created_at_desc", table_name="attempts")
    op.drop_table("attempts")
    op.drop_index("ix_questions_mission_id", table_name="questions")
    op.drop_table("questions")
    op.drop_index("ix_vocab_mission_id", table_name="vocab")
    op.drop_table("vocab")
    op.drop_index("ix_missions_chapter_id_order_index", table_name="missions")
    op.drop_table("missions")
    op.drop_index("ix_chapters_level_code_order_index", table_name="chapters")
    op.drop_table("chapters")
    op.drop_table("levels")
    op.drop_table("user_stats")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS user_role")


