from datetime import datetime, timezone
import enum
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from app.db.database import Base


class StatusEnum(enum.Enum):
    won = "won"
    lost = "lost"
    open = "open"


class StageEnum(enum.Enum):
    prospecting = "prospecting"
    qualification = "qualification"
    needs_analysis = "needs_analysis"
    value_proposition = "value_proposition"
    id_decision_makers = "id_decision_makers"
    perception_analysis = "perception_analysis"
    proposal_price_quote = "proposal_price_quote"
    negotiation_review = "negotiation_review"
    closed_won = "closed_won"
    closed_lost = "closed_lost"


class IndustryEnum(enum.Enum):
    agriculture = "agriculture"
    apparel = "apparel"
    banking = "banking"
    biotechnology = "biotechnology"
    chemical = "chemical"
    communications = "communications"
    construction = "construction"
    consulting = "consulting"
    education = "education"
    electronics = "electronics"
    energy = "energy"
    engineering = "engineering"
    entertainment = "entertainment"
    environmental = "environmental"
    finance = "finance"
    food_beverage = "food_beverage"
    government = "government"
    healthcare = "healthcare"
    hospitality = "hospitality"
    insurance = "insurance"
    machinery = "machinery"
    manufacturing = "manufacturing"
    media = "media"
    not_for_profit = "not_for_profit"
    recreation = "recreation"
    retail = "retail"
    shipping = "shipping"
    technology = "technology"
    telecommunications = "telecommunications"
    transportation = "transportation"
    utilities = "utilities"


class LeadStatusEnum(enum.Enum):
    new = "new"
    contacted = "contacted"
    qualified = "qualified"
    lost = "lost"
    converted = "converted"


class RoleEnum(enum.Enum):
    admin = "admin"
    user = "user"


class User(Base):
    """
    Business User: The CRM user, such as a seller or manager.

    The CRM business user represents the Gong user in the CRM and is responsible
    for the relationship with the account and for creating opportunities and
    closing deals. Uploading business users enables Gong to associate CRM entities
    such as accounts and contacts with the relevant user in Gong and with their
    Gong activity, such as conversations.
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, nullable=False, index=True)
    first_name = Column(String, nullable=False, index=True)
    last_name = Column(String, nullable=False, index=True)
    password = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.user)
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    deals = relationship("Deal", back_populates="owner")
    leads = relationship("Lead", back_populates="owner")


class Company(Base):
    """
    Company: The customer details in the CRM.

    The account object is an active customer in the CRM. Emails and calls in Gong
    are associated with this account object.
    """

    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    industry = Column(Enum(IndustryEnum), nullable=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    domains = relationship("Domain", back_populates="company")
    contacts = relationship("Contact", back_populates="company")
    deals = relationship("Deal", back_populates="company")
    leads = relationship("Lead", back_populates="converted_to_company")


class Domain(Base):
    """
    Domain: The domain of the account in the CRM.

    The domain object represents the domain of the account in the CRM. The domain
    is used to associate the account with the relevant Gong user and Gong activity.
    """

    __tablename__ = "domains"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    company = relationship("Company", back_populates="domains")


class Contact(Base):
    """
    Contact: A specific contact in the CRM that is associated with a customer.

    A contact in Gong is the contact associated with the account. Gong uses a
    contact to match an activity to the correct account.
    """

    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False, index=True)
    last_name = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, nullable=False, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    company = relationship("Company", back_populates="contacts")
    leads = relationship("Lead", back_populates="converted_to_contact")


class Deal(Base):
    """
    Deal: A deal or opportunity, or a contract of a specific account in the CRM.

    A deal in Gong is a qualified opportunity or contract in a specific account.
    """

    __tablename__ = "deals"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    amount = Column(Integer, nullable=False, index=True)
    open_date = Column(DateTime, nullable=False, index=True)
    close_date = Column(DateTime, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    stage = Column(Enum(StageEnum), default=StageEnum.prospecting)
    description = Column(Text)
    status = Column(Enum(StatusEnum), default=StatusEnum.open)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    owner = relationship("User", back_populates="deals")
    company = relationship("Company", back_populates="deals")
    leads = relationship("Lead", back_populates="converted_to_deal")


class Lead(Base):
    """
    Lead: A potential customers who are not associated with an account.

    A Lead is a potential customer, who may not yet be associated with an account.
    If conversations can't be associated with a contact, Gong then checks to see
    whether there is a relevant lead to associate with the conversation.
    """

    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False, index=True)
    last_name = Column(String, nullable=False, index=True)
    company = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, nullable=False, index=True)
    details = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    converted_to_deal_id = Column(Integer, ForeignKey("deals.id"))
    converted_to_contact_id = Column(Integer, ForeignKey("contacts.id"))
    converted_to_company_id = Column(Integer, ForeignKey("companies.id"))
    status = Column(Enum(LeadStatusEnum), default=LeadStatusEnum.new)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    owner = relationship("User", back_populates="leads")
    converted_to_deal = relationship("Deal", back_populates="leads")
    converted_to_contact = relationship("Contact", back_populates="leads")
    converted_to_company = relationship("Company", back_populates="leads")
