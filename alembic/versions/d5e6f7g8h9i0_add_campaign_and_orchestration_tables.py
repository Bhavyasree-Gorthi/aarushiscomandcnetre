"""Add campaign, agent, policy, workbench, and insights tables

Revision ID: d5e6f7g8h9i0
Revises: c3d4e5f6g7h8
Create Date: 2025-05-17 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5e6f7g8h9i0'
down_revision = 'c3d4e5f6g7h8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create campaigns table
    op.create_table(
        'campaigns',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.Enum('draft', 'running', 'completed', 'failed', 'paused', name='campaignstatus'), nullable=False, server_default='draft'),
        sa.Column('orchestration_id', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('roi', sa.String(length=50), nullable=True),
        sa.Column('engagement', sa.String(length=50), nullable=True),
        sa.Column('violations_prevented', sa.Integer(), nullable=False, server_default='0'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('orchestration_id')
    )
    op.create_index(op.f('ix_campaigns_id'), 'campaigns', ['id'], unique=False)
    op.create_index(op.f('ix_campaigns_name'), 'campaigns', ['name'], unique=False)

    # Create agents table
    op.create_table(
        'agents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('campaign_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=100), nullable=False),
        sa.Column('status', sa.Enum('pending', 'running', 'completed', 'failed', 'warning', name='agentstatus'), nullable=False, server_default='pending'),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('result_summary', sa.String(length=500), nullable=True),
        sa.Column('error_message', sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaigns.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_agents_id'), 'agents', ['id'], unique=False)
    op.create_index(op.f('ix_agents_name'), 'agents', ['name'], unique=False)

    # Create policies table
    op.create_table(
        'policies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('campaign_id', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('rule_text', sa.Text(), nullable=False),
        sa.Column('status', sa.Enum('passed', 'failed', 'warning', name='policystatus'), nullable=False, server_default='passed'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('triggered_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('source_document', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaigns.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_policies_id'), 'policies', ['id'], unique=False)
    op.create_index(op.f('ix_policies_name'), 'policies', ['name'], unique=False)

    # Create workbench_items table
    op.create_table(
        'workbench_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('campaign_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('issue_type', sa.String(length=100), nullable=False),
        sa.Column('status', sa.Enum('pending', 'approved', 'rejected', 'escalated', name='workbenchstatus'), nullable=False, server_default='pending'),
        sa.Column('assigned_to', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('reviewed_at', sa.DateTime(), nullable=True),
        sa.Column('review_notes', sa.Text(), nullable=True),
        sa.Column('related_policy', sa.String(length=255), nullable=True),
        sa.Column('suggested_action', sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaigns.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workbench_items_id'), 'workbench_items', ['id'], unique=False)
    op.create_index(op.f('ix_workbench_items_title'), 'workbench_items', ['title'], unique=False)

    # Create insights table
    op.create_table(
        'insights',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('campaign_id', sa.Integer(), nullable=False),
        sa.Column('roi', sa.String(length=50), nullable=True),
        sa.Column('engagement_rate', sa.String(length=50), nullable=True),
        sa.Column('violations_prevented', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('execution_time_seconds', sa.Float(), nullable=True),
        sa.Column('agent_success_rate', sa.String(length=50), nullable=True),
        sa.Column('policies_checked', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('policies_passed', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('summary', sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaigns.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_insights_id'), 'insights', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_insights_id'), table_name='insights')
    op.drop_table('insights')
    op.drop_index(op.f('ix_workbench_items_title'), table_name='workbench_items')
    op.drop_index(op.f('ix_workbench_items_id'), table_name='workbench_items')
    op.drop_table('workbench_items')
    op.drop_index(op.f('ix_policies_name'), table_name='policies')
    op.drop_index(op.f('ix_policies_id'), table_name='policies')
    op.drop_table('policies')
    op.drop_index(op.f('ix_agents_name'), table_name='agents')
    op.drop_index(op.f('ix_agents_id'), table_name='agents')
    op.drop_table('agents')
    op.drop_index(op.f('ix_campaigns_name'), table_name='campaigns')
    op.drop_index(op.f('ix_campaigns_id'), table_name='campaigns')
    op.drop_table('campaigns')
