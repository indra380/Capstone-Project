"""initial production schema

Revision ID: 20260629_0001
Revises:
Create Date: 2026-06-29 00:00:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260629_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("full_name", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=40), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_users_id", "users", ["id"])
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("goal", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=40), nullable=False, server_default="active"),
        sa.Column("start_date", sa.DateTime(), nullable=True),
        sa.Column("deadline", sa.DateTime(), nullable=True),
        sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_projects_id", "projects", ["id"])

    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=40), nullable=False, server_default="not_started"),
        sa.Column("priority", sa.String(length=20), nullable=False, server_default="medium"),
        sa.Column("estimated_hours", sa.Float(), nullable=False, server_default="0"),
        sa.Column("due_date", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_tasks_id", "tasks", ["id"])
    op.create_index("ix_tasks_project_id", "tasks", ["project_id"])

    op.create_table(
        "resources",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("role", sa.String(length=100), nullable=False),
        sa.Column("experience_years", sa.Float(), nullable=False, server_default="0"),
        sa.Column("availability_percent", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("workload_percent", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_resources_id", "resources", ["id"])

    op.create_table(
        "skills",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("category", sa.String(length=120), nullable=True),
    )
    op.create_index("ix_skills_id", "skills", ["id"])
    op.create_index("ix_skills_name", "skills", ["name"], unique=True)

    op.create_table(
        "resource_skills",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("resource_id", sa.Integer(), sa.ForeignKey("resources.id", ondelete="CASCADE"), nullable=False),
        sa.Column("skill_id", sa.Integer(), sa.ForeignKey("skills.id", ondelete="CASCADE"), nullable=False),
        sa.Column("proficiency", sa.Integer(), nullable=False, server_default="3"),
        sa.UniqueConstraint("resource_id", "skill_id", name="uq_resource_skill"),
    )
    op.create_index("ix_resource_skills_id", "resource_skills", ["id"])
    op.create_index("ix_resource_skills_resource_id", "resource_skills", ["resource_id"])
    op.create_index("ix_resource_skills_skill_id", "resource_skills", ["skill_id"])

    op.create_table(
        "assignments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("task_id", sa.Integer(), sa.ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False),
        sa.Column("resource_id", sa.Integer(), sa.ForeignKey("resources.id", ondelete="CASCADE"), nullable=False),
        sa.Column("allocation_percent", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("assigned_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_assignments_id", "assignments", ["id"])
    op.create_index("ix_assignments_task_id", "assignments", ["task_id"])
    op.create_index("ix_assignments_resource_id", "assignments", ["resource_id"])

    op.create_table(
        "milestones",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("due_date", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(length=40), nullable=False, server_default="planned"),
    )
    op.create_index("ix_milestones_id", "milestones", ["id"])
    op.create_index("ix_milestones_project_id", "milestones", ["project_id"])

    op.create_table(
        "risks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("task_id", sa.Integer(), sa.ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True),
        sa.Column("title", sa.String(length=250), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("probability", sa.Float(), nullable=False, server_default="0"),
        sa.Column("impact", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("level", sa.String(length=20), nullable=False),
        sa.Column("mitigation", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False, server_default="open"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_risks_id", "risks", ["id"])
    op.create_index("ix_risks_project_id", "risks", ["project_id"])

    op.create_table(
        "reports",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("generated_by_user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("report_type", sa.String(length=30), nullable=False),
        sa.Column("title", sa.String(length=250), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_reports_id", "reports", ["id"])
    op.create_index("ix_reports_project_id", "reports", ["project_id"])

    op.create_table(
        "meetings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("agenda", sa.Text(), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("attendees_json", sa.JSON(), nullable=True),
        sa.Column("action_items_json", sa.JSON(), nullable=True),
        sa.Column("meeting_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_meetings_id", "meetings", ["id"])
    op.create_index("ix_meetings_project_id", "meetings", ["project_id"])

    op.create_table(
        "activity_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id", ondelete="SET NULL"), nullable=True),
        sa.Column("actor_user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("action", sa.String(length=150), nullable=False),
        sa.Column("entity_type", sa.String(length=80), nullable=False),
        sa.Column("entity_id", sa.String(length=80), nullable=False),
        sa.Column("details_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_activity_logs_id", "activity_logs", ["id"])

    op.create_table(
        "embeddings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_type", sa.String(length=50), nullable=False),
        sa.Column("source_id", sa.String(length=120), nullable=False),
        sa.Column("chunk_text", sa.Text(), nullable=False),
        sa.Column("faiss_id", sa.String(length=120), nullable=False),
        sa.Column("embedding_meta_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_embeddings_id", "embeddings", ["id"])
    op.create_index("ix_embeddings_project_id", "embeddings", ["project_id"])
    op.create_index("ix_embeddings_faiss_id", "embeddings", ["faiss_id"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_embeddings_faiss_id", table_name="embeddings")
    op.drop_index("ix_embeddings_project_id", table_name="embeddings")
    op.drop_index("ix_embeddings_id", table_name="embeddings")
    op.drop_table("embeddings")

    op.drop_index("ix_activity_logs_id", table_name="activity_logs")
    op.drop_table("activity_logs")

    op.drop_index("ix_meetings_project_id", table_name="meetings")
    op.drop_index("ix_meetings_id", table_name="meetings")
    op.drop_table("meetings")

    op.drop_index("ix_reports_project_id", table_name="reports")
    op.drop_index("ix_reports_id", table_name="reports")
    op.drop_table("reports")

    op.drop_index("ix_risks_project_id", table_name="risks")
    op.drop_index("ix_risks_id", table_name="risks")
    op.drop_table("risks")

    op.drop_index("ix_milestones_project_id", table_name="milestones")
    op.drop_index("ix_milestones_id", table_name="milestones")
    op.drop_table("milestones")

    op.drop_index("ix_assignments_resource_id", table_name="assignments")
    op.drop_index("ix_assignments_task_id", table_name="assignments")
    op.drop_index("ix_assignments_id", table_name="assignments")
    op.drop_table("assignments")

    op.drop_index("ix_resource_skills_skill_id", table_name="resource_skills")
    op.drop_index("ix_resource_skills_resource_id", table_name="resource_skills")
    op.drop_index("ix_resource_skills_id", table_name="resource_skills")
    op.drop_table("resource_skills")

    op.drop_index("ix_skills_name", table_name="skills")
    op.drop_index("ix_skills_id", table_name="skills")
    op.drop_table("skills")

    op.drop_index("ix_resources_id", table_name="resources")
    op.drop_table("resources")

    op.drop_index("ix_tasks_project_id", table_name="tasks")
    op.drop_index("ix_tasks_id", table_name="tasks")
    op.drop_table("tasks")

    op.drop_index("ix_projects_id", table_name="projects")
    op.drop_table("projects")

    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")
