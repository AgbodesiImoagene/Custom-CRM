"""Insert sample data

Revision ID: 67aa3736d1de
Revises: 0d64a601dff5
Create Date: 2024-12-17 21:30:52.892783

"""

from datetime import datetime, timedelta, timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Enum, Boolean, DateTime

from app.api.security import get_password_hash
from app.db.models import IndustryEnum, LeadStatusEnum, RoleEnum, StageEnum, StatusEnum


# revision identifiers, used by Alembic.
revision: str = "67aa3736d1de"
down_revision: Union[str, None] = "0d64a601dff5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    user_table = table(
        "users",
        column("id", Integer),
        column("username", String),
        column("email", String),
        column("phone", String),
        column("first_name", String),
        column("last_name", String),
        column("password", String),
        column("salt", String),
        column("role", Enum(RoleEnum)),
        column("disabled", Boolean),
        column("created_at", DateTime),
        column("updated_at", DateTime),
    )

    company_table = table(
        "companies",
        column("id", Integer),
        column("name", String),
        column("industry", Enum(IndustryEnum)),
        column("created_at", DateTime),
        column("updated_at", DateTime),
    )

    domain_table = table(
        "domains",
        column("id", Integer),
        column("name", String),
        column("company_id", Integer),
        column("created_at", DateTime),
        column("updated_at", DateTime),
    )

    contact_table = table(
        "contacts",
        column("id", Integer),
        column("first_name", String),
        column("last_name", String),
        column("email", String),
        column("phone", String),
        column("company_id", Integer),
        column("created_at", DateTime),
        column("updated_at", DateTime),
    )

    deal_table = table(
        "deals",
        column("id", Integer),
        column("title", String),
        column("amount", Integer),
        column("open_date", DateTime),
        column("close_date", DateTime),
        column("company_id", Integer),
        column("owner_id", Integer),
        column("stage", Enum(StageEnum)),
        column("description", String),
        column("status", Enum(StatusEnum)),
        column("created_at", DateTime),
        column("updated_at", DateTime),
    )

    lead_table = table(
        "leads",
        column("id", Integer),
        column("first_name", String),
        column("last_name", String),
        column("company", String),
        column("email", String),
        column("phone", String),
        column("details", String),
        column("status", Enum(LeadStatusEnum)),
        column("converted_to_deal_id", Integer),
        column("converted_to_contact_id", Integer),
        column("converted_to_company_id", Integer),
        column("owner_id", Integer),
        column("created_at", DateTime),
        column("updated_at", DateTime),
    )

    hashed_password, salt = get_password_hash("password")
    now = datetime.now(timezone.utc)

    op.bulk_insert(
        user_table,
        [
            {
                "username": "admin",
                "email": "admin@examplecrm.com",
                "phone": "1234567890",
                "first_name": "Admin",
                "last_name": "User",
                "password": hashed_password,
                "salt": salt,
                "role": RoleEnum.admin,
                "disabled": False,
                "created_at": now,
                "updated_at": now,
            },
            {
                "username": "testuser",
                "email": "testuser@examplecrm.com",
                "phone": "1234567890",
                "first_name": "Test",
                "last_name": "User",
                "password": hashed_password,
                "salt": salt,
                "role": RoleEnum.user,
                "disabled": False,
                "created_at": now,
                "updated_at": now,
            },
        ],
    )

    op.bulk_insert(
        company_table,
        [
            {
                "name": "Apple",
                "industry": IndustryEnum.technology,
                "created_at": now,
                "updated_at": now,
            },
            {
                "name": "Google",
                "industry": IndustryEnum.technology,
                "created_at": now,
                "updated_at": now,
            },
            {
                "name": "JPMorgan Chase",
                "industry": IndustryEnum.banking,
                "created_at": now,
                "updated_at": now,
            },
            {
                "name": "Wells Fargo",
                "industry": IndustryEnum.banking,
                "created_at": now,
                "updated_at": now,
            },
            {
                "name": "Johnsons & Johnson",
                "industry": IndustryEnum.healthcare,
                "created_at": now,
                "updated_at": now,
            },
        ],
    )

    op.bulk_insert(
        domain_table,
        [
            {
                "name": "apple.com",
                "company_id": 1,
                "created_at": now,
                "updated_at": now,
            },
            {
                "name": "google.com",
                "company_id": 2,
                "created_at": now,
                "updated_at": now,
            },
            {
                "name": "jpmorganchase.com",
                "company_id": 3,
                "created_at": now,
                "updated_at": now,
            },
            {
                "name": "wellsfargo.com",
                "company_id": 4,
                "created_at": now,
                "updated_at": now,
            },
            {
                "name": "jnj.com",
                "company_id": 5,
                "created_at": now,
                "updated_at": now,
            },
        ],
    )

    op.bulk_insert(
        contact_table,
        [
            {
                "first_name": "Tim",
                "last_name": "Cook",
                "email": "tim.cook@apple.com",
                "phone": "1111111111",
                "company_id": 1,
                "created_at": now,
                "updated_at": now,
            },
            {
                "first_name": "Sundar",
                "last_name": "Pichai",
                "email": "sundar.pichai@google.com",
                "phone": "2222222222",
                "company_id": 2,
                "created_at": now,
                "updated_at": now,
            },
            {
                "first_name": "Larry",
                "last_name": "Page",
                "email": "larry.page@google.com",
                "phone": "3333333333",
                "company_id": 2,
                "created_at": now,
                "updated_at": now,
            },
            {
                "first_name": "Jamie",
                "last_name": "Dimon",
                "email": "jamie.dimon@jpmorganchase.com",
                "phone": "4444444444",
                "company_id": 3,
                "created_at": now,
                "updated_at": now,
            },
            {
                "first_name": "Charles",
                "last_name": "Scharf",
                "email": "charles.scharf@wellsfargo.com",
                "phone": "5555555555",
                "company_id": 4,
                "created_at": now,
                "updated_at": now,
            },
            {
                "first_name": "Alex",
                "last_name": "Gorsky",
                "email": "alex.gorsky@jnj.com",
                "phone": "6666666666",
                "company_id": 5,
                "created_at": now,
                "updated_at": now,
            },
        ],
    )

    op.bulk_insert(
        deal_table,
        [
            {
                "title": "Apple Deal",
                "amount": 1000000,
                "stage": StageEnum.prospecting,
                "status": StatusEnum.open,
                "company_id": 1,
                "owner_id": 2,
                "description": "This is a deal with Apple. It is in the prospecting stage.",
                "open_date": datetime.now(timezone.utc) - timedelta(days=30),
                "close_date": None,
                "created_at": now,
                "updated_at": now,
            },
            {
                "title": "Google Deal",
                "amount": 2000000,
                "stage": StageEnum.negotiation_review,
                "status": StatusEnum.open,
                "company_id": 2,
                "owner_id": 2,
                "description": "This is a deal with Google. It is in the negotiation/review stage.",
                "open_date": datetime.now(timezone.utc) - timedelta(days=20),
                "close_date": None,
                "created_at": now,
                "updated_at": now,
            },
            {
                "title": "JPMorgan Chase Deal",
                "amount": 3000000,
                "stage": StageEnum.closed_won,
                "status": StatusEnum.won,
                "company_id": 3,
                "owner_id": 2,
                "description": "This is a deal with JPMorgan Chase. It is in the closed/won stage.",
                "open_date": datetime.now(timezone.utc) - timedelta(days=10),
                "close_date": datetime.now(timezone.utc),
                "created_at": now,
                "updated_at": now,
            },
            {
                "title": "Wells Fargo Deal",
                "amount": 4000000,
                "stage": StageEnum.value_proposition,
                "status": StatusEnum.open,
                "company_id": 4,
                "owner_id": 2,
                "description": "This is a deal with Wells Fargo. It is in the value proposition stage.",
                "open_date": datetime.now(timezone.utc) - timedelta(days=5),
                "close_date": None,
                "created_at": now,
                "updated_at": now,
            },
            {
                "title": "Johnsons & Johnson Deal",
                "amount": 5000000,
                "stage": StageEnum.closed_lost,
                "status": StatusEnum.lost,
                "company_id": 5,
                "owner_id": 2,
                "description": "This is a deal with Johnsons & Johnson. It is in the closed/lost stage.",
                "open_date": datetime.now(timezone.utc) - timedelta(days=2),
                "close_date": datetime.now(timezone.utc),
                "created_at": now,
                "updated_at": now,
            },
        ],
    )

    op.bulk_insert(
        lead_table,
        [
            {
                "first_name": "Elon",
                "last_name": "Musk",
                "company": "Tesla",
                "email": "elon.musk@tesla.com",
                "phone": "7777777777",
                "status": LeadStatusEnum.new,
                "owner_id": 2,
                "created_at": now,
                "updated_at": now,
            },
            {
                "first_name": "Jeff",
                "last_name": "Bezos",
                "company": "Amazon",
                "email": "jeff.bezos@amazon.com",
                "phone": "8888888888",
                "status": LeadStatusEnum.contacted,
                "owner_id": 2,
                "created_at": now,
                "updated_at": now,
            },
            {
                "first_name": "Bill",
                "last_name": "Gates",
                "company": "Microsoft",
                "email": "bill.gates@microsoft.com",
                "phone": "9999999999",
                "status": LeadStatusEnum.contacted,
                "owner_id": 2,
                "created_at": now,
                "updated_at": now,
            },
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM leads")
    op.execute("DELETE FROM deals")
    op.execute("DELETE FROM contacts")
    op.execute("DELETE FROM domains")
    op.execute("DELETE FROM companies")
    op.execute("DELETE FROM users")
