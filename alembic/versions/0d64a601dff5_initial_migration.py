"""Initial migration

Revision ID: 0d64a601dff5
Revises: 
Create Date: 2024-12-17 21:30:18.938322

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d64a601dff5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('companies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('industry', sa.Enum('agriculture', 'apparel', 'banking', 'biotechnology', 'chemical', 'communications', 'construction', 'consulting', 'education', 'electronics', 'energy', 'engineering', 'entertainment', 'environmental', 'finance', 'food_beverage', 'government', 'healthcare', 'hospitality', 'insurance', 'machinery', 'manufacturing', 'media', 'not_for_profit', 'recreation', 'retail', 'shipping', 'technology', 'telecommunications', 'transportation', 'utilities', name='industryenum'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_companies_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_companies_industry'), ['industry'], unique=False)
        batch_op.create_index(batch_op.f('ix_companies_name'), ['name'], unique=True)

    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('salt', sa.String(), nullable=False),
    sa.Column('role', sa.Enum('admin', 'user', name='roleenum'), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_users_first_name'), ['first_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_users_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_users_last_name'), ['last_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_users_phone'), ['phone'], unique=False)
        batch_op.create_index(batch_op.f('ix_users_username'), ['username'], unique=True)

    op.create_table('contacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('contacts', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_contacts_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_contacts_first_name'), ['first_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_contacts_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_contacts_last_name'), ['last_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_contacts_phone'), ['phone'], unique=False)

    op.create_table('deals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('open_date', sa.DateTime(), nullable=False),
    sa.Column('close_date', sa.DateTime(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('stage', sa.Enum('prospecting', 'qualification', 'needs_analysis', 'value_proposition', 'id_decision_makers', 'perception_analysis', 'proposal_price_quote', 'negotiation_review', 'closed_won', 'closed_lost', name='stageenum'), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('status', sa.Enum('won', 'lost', 'open', name='statusenum'), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('deals', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_deals_amount'), ['amount'], unique=False)
        batch_op.create_index(batch_op.f('ix_deals_close_date'), ['close_date'], unique=False)
        batch_op.create_index(batch_op.f('ix_deals_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_deals_open_date'), ['open_date'], unique=False)
        batch_op.create_index(batch_op.f('ix_deals_title'), ['title'], unique=False)

    op.create_table('domains',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('domains', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_domains_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_domains_name'), ['name'], unique=True)

    op.create_table('leads',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('company', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('details', sa.Text(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('converted_to_deal_id', sa.Integer(), nullable=True),
    sa.Column('converted_to_contact_id', sa.Integer(), nullable=True),
    sa.Column('converted_to_company_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Enum('new', 'contacted', 'qualified', 'lost', 'converted', name='leadstatusenum'), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['converted_to_company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['converted_to_contact_id'], ['contacts.id'], ),
    sa.ForeignKeyConstraint(['converted_to_deal_id'], ['deals.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('leads', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_leads_company'), ['company'], unique=False)
        batch_op.create_index(batch_op.f('ix_leads_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_leads_first_name'), ['first_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_leads_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_leads_last_name'), ['last_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_leads_phone'), ['phone'], unique=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('leads', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_leads_phone'))
        batch_op.drop_index(batch_op.f('ix_leads_last_name'))
        batch_op.drop_index(batch_op.f('ix_leads_id'))
        batch_op.drop_index(batch_op.f('ix_leads_first_name'))
        batch_op.drop_index(batch_op.f('ix_leads_email'))
        batch_op.drop_index(batch_op.f('ix_leads_company'))

    op.drop_table('leads')
    with op.batch_alter_table('domains', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_domains_name'))
        batch_op.drop_index(batch_op.f('ix_domains_id'))

    op.drop_table('domains')
    with op.batch_alter_table('deals', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_deals_title'))
        batch_op.drop_index(batch_op.f('ix_deals_open_date'))
        batch_op.drop_index(batch_op.f('ix_deals_id'))
        batch_op.drop_index(batch_op.f('ix_deals_close_date'))
        batch_op.drop_index(batch_op.f('ix_deals_amount'))

    op.drop_table('deals')
    with op.batch_alter_table('contacts', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_contacts_phone'))
        batch_op.drop_index(batch_op.f('ix_contacts_last_name'))
        batch_op.drop_index(batch_op.f('ix_contacts_id'))
        batch_op.drop_index(batch_op.f('ix_contacts_first_name'))
        batch_op.drop_index(batch_op.f('ix_contacts_email'))

    op.drop_table('contacts')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_username'))
        batch_op.drop_index(batch_op.f('ix_users_phone'))
        batch_op.drop_index(batch_op.f('ix_users_last_name'))
        batch_op.drop_index(batch_op.f('ix_users_id'))
        batch_op.drop_index(batch_op.f('ix_users_first_name'))
        batch_op.drop_index(batch_op.f('ix_users_email'))

    op.drop_table('users')
    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_companies_name'))
        batch_op.drop_index(batch_op.f('ix_companies_industry'))
        batch_op.drop_index(batch_op.f('ix_companies_id'))

    op.drop_table('companies')
    # ### end Alembic commands ###
