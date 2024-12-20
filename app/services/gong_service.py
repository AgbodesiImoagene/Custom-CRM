import json
import os
import uuid
from datetime import datetime, timezone
import requests
from app.db.models import (
    User,
    Company,
    Contact,
    Deal,
    Lead,
    IndustryEnum,
    LeadStatusEnum,
    StageEnum,
)


def isoformat_without_ms(dt):
    isoformat = dt.replace(microsecond=0).isoformat()
    return f"{isoformat}Z" if not dt.tzinfo else isoformat


class GongException(Exception):
    pass


SCHEMA_PAYLOADS = {
    "ACCOUNT": [
        {
            "uniqueName": "industry",
            "label": "Industry",
            "type": "PICKLIST",
            "orderedValueList": list(IndustryEnum.__members__.keys()),
            "lastModified": isoformat_without_ms(datetime.now(timezone.utc)),
            "isDeleted": False,
        },
    ],
    "DEAL": [
        {
            "uniqueName": "description",
            "label": "Description",
            "type": "STRING",
            "lastModified": isoformat_without_ms(datetime.now(timezone.utc)),
            "isDeleted": False,
        },
    ],
    "LEAD": [
        {
            "uniqueName": "ownerId",
            "label": "Owner",
            "type": "REFERENCE",
            "referenceTo": "BUSINESS_USER",
            "lastModified": isoformat_without_ms(datetime.now(timezone.utc)),
            "isDeleted": False,
        },
        {
            "uniqueName": "status",
            "label": "Status",
            "type": "PICKLIST",
            "orderedValueList": list(LeadStatusEnum.__members__.keys()),
            "lastModified": isoformat_without_ms(datetime.now(timezone.utc)),
            "isDeleted": False,
        },
        {
            "uniqueName": "account",
            "label": "Account",
            "type": "STRING",
            "lastModified": isoformat_without_ms(datetime.now(timezone.utc)),
            "isDeleted": False,
        },
        {
            "uniqueName": "details",
            "label": "Details",
            "type": "STRING",
            "lastModified": isoformat_without_ms(datetime.now(timezone.utc)),
            "isDeleted": False,
        },
    ],
}


class GongService:
    def __init__(self, api_url, credentials, base_url, session):
        self.api_url = api_url
        self.credentials = credentials
        self.base_url = base_url
        self.session = session

    def register_crm_integration(self, name, owner_email):
        integration_payload = {
            "name": name,
            "ownerEmail": owner_email,
        }

        response = requests.put(
            f"{self.api_url}/crm/integrations",
            json=integration_payload,
            auth=self.credentials,
            timeout=10,
        )
        if response.status_code == 200:
            return response.json().get("integrationId")
        raise GongException(
            f"Failed to register CRM integration: {response.status_code} - {response.text}"
        )

    def get_crm_integration(self):
        response = requests.get(
            f"{self.api_url}/crm/integrations",
            auth=self.credentials,
            timeout=10,
        )
        integrations = response.json().get("integrations", [])
        if response.status_code == 200 and len(integrations) > 0:
            return integrations[0].get("integrationId")
        raise GongException(
            f"Failed to get CRM integration: {response.status_code} - {response.text}"
        )

    def delete_crm_integration(self, integration_id):
        params = {"clientRequestId": str(uuid.uuid4()), "integrationId": integration_id}

        response = requests.delete(
            f"{self.api_url}/crm/integrations",
            headers={"Content-Type": "application/json"},
            params=params,
            auth=self.credentials,
            timeout=10,
        )
        if response.status_code != 201:
            raise GongException(
                f"Failed to delete CRM integration: {response.status_code} - {response.text}"
            )

    def list_schema_fields(self, integration_id, object_type):
        params = {"integrationId": integration_id, "objectType": object_type}

        response = requests.get(
            f"{self.api_url}/crm/entity-schema",
            params=params,
            auth=self.credentials,
            timeout=10,
        )
        if response.status_code == 200:
            return response.json()
        raise GongException(
            f"Failed to list schema fields: {response.status_code} - {response.text}"
        )

    def check_crm_schema(self, integration_id):
        for object_type, fields in SCHEMA_PAYLOADS.items():
            response = requests.get(
                f"{self.api_url}/crm/entity-schema",
                params={"integrationId": integration_id, "objectType": object_type},
                auth=self.credentials,
                timeout=10,
            )
            if response.status_code == 200:
                schema_fields = response.json()["objectTypeToSelectedFields"][
                    object_type
                ]
                for field in fields:
                    if field["uniqueName"] not in [
                        f["uniqueName"] for f in schema_fields
                    ]:
                        return False
            else:
                raise GongException(
                    f"Failed to check schema for {object_type}: {response.status_code} - {response.text}"
                )
        return True

    def register_crm_schema(self, integration_id):
        if not self.check_crm_schema(integration_id):
            for object_type, fields in SCHEMA_PAYLOADS.items():
                response = requests.post(
                    f"{self.api_url}/crm/entity-schema",
                    params={"integrationId": integration_id, "objectType": object_type},
                    json=fields,
                    auth=self.credentials,
                    timeout=10,
                )
                if response.status_code != 200 and response.status_code != 201:
                    raise GongException(
                        f"Failed to register schema for {object_type}: {response.status_code} - {response.text}"
                    )

    def fetch_data_from_db(self):
        users = self.session.query(User).all()
        companies = self.session.query(Company).all()
        contacts = self.session.query(Contact).all()
        deals = self.session.query(Deal).all()
        leads = self.session.query(Lead).all()
        return users, companies, contacts, deals, leads

    def check_request_status(self, integration_id, request_id):
        response = requests.get(
            f"{self.api_url}/crm/request-status",
            params={"integrationId": integration_id, "clientRequestId": request_id},
            auth=self.credentials,
            timeout=10,
        )
        if response.status_code == 200:
            if response.json().get("status") != "FAILED":
                return response.json().get("status"), None
            errors = response.json().get("errors")
            errors = [errors] if not isinstance(errors, list) else errors
            return "FAILED", errors
        raise GongException(
            f"Failed to check request status: {response.status_code} - {response.text}"
        )

    def push_data_to_gong(self, integration_id, object_type, data_file):
        params = {
            "clientRequestId": str(uuid.uuid4()),
            "integrationId": integration_id,
            "objectType": object_type,
        }
        files = {"dataFile": data_file}

        response = requests.post(
            f"{self.api_url}/crm/entities",
            params=params,
            files=files,
            auth=self.credentials,
            timeout=10,
        )
        if response.status_code != 200 and response.status_code != 201:
            raise GongException(
                f"Failed to push data to Gong: {response.status_code} - {response.text}"
            )
        return response.json()

    def push_stages_to_gong(self, integration_id):
        with open("stages.ldjson", "w", encoding="utf-8") as f:
            stages = [
                {
                    "objectId": str(i),
                    "name": stage.name,
                    "isActive": True,
                    "sortOrder": i + 1,
                }
                for i, stage in enumerate(StageEnum)
            ]
            for stage in stages:
                f.write(json.dumps(stage) + "\n")

        response = self.push_data_to_gong(
            integration_id, "STAGE", open("stages.ldjson", "rb")
        )

        os.remove("stages.ldjson")

        return response

    def push_users_to_gong(self, integration_id, users):
        with open("users.ldjson", "w", encoding="utf-8") as f:
            for user in users:
                user_data = {
                    "objectId": str(user.id),
                    "modifiedDate": isoformat_without_ms(user.updated_at),
                    "isDeleted": False,
                    "url": f"{self.base_url}/users/{user.id}",
                    "emailAddress": user.email,
                }
                f.write(json.dumps(user_data) + "\n")

        response = self.push_data_to_gong(
            integration_id, "BUSINESS_USER", open("users.ldjson", "rb")
        )

        os.remove("users.ldjson")

        return response

    def push_companies_to_gong(self, integration_id, companies):
        with open("companies.ldjson", "w", encoding="utf-8") as f:
            for company in companies:
                company_data = {
                    "objectId": str(company.id),
                    "modifiedDate": isoformat_without_ms(company.updated_at),
                    "isDeleted": False,
                    "url": f"{self.base_url}/companies/{company.id}",
                    "name": company.name,
                    "domains": [domain.name for domain in company.domains],
                    "industry": company.industry.name,
                }
                f.write(json.dumps(company_data) + "\n")

        response = self.push_data_to_gong(
            integration_id, "ACCOUNT", open("companies.ldjson", "rb")
        )

        os.remove("companies.ldjson")

        return response

    def push_contacts_to_gong(self, integration_id, contacts):
        with open("contacts.ldjson", "w", encoding="utf-8") as f:
            for contact in contacts:
                contact_data = {
                    "objectId": str(contact.id),
                    "modifiedDate": isoformat_without_ms(contact.updated_at),
                    "isDeleted": False,
                    "url": f"{self.base_url}/contacts/{contact.id}",
                    "accountId": str(contact.company_id),
                    "emailAddress": contact.email,
                    "firstName": contact.first_name,
                    "lastName": contact.last_name,
                    "phoneNumber": contact.phone,
                }
                f.write(json.dumps(contact_data) + "\n")

            response = self.push_data_to_gong(
                integration_id, "CONTACT", open("contacts.ldjson", "rb")
            )

        os.remove("contacts.ldjson")

        return response

    def push_deals_to_gong(self, integration_id, deals):
        with open("deals.ldjson", "w", encoding="utf-8") as f:
            for deal in deals:
                deal_data = {
                    "objectId": str(deal.id),
                    "modifiedDate": isoformat_without_ms(deal.updated_at),
                    "isDeleted": False,
                    "url": f"{self.base_url}/deals/{deal.id}",
                    "accountId": str(deal.company_id),
                    "ownerId": str(deal.owner_id),
                    "name": deal.title,
                    "createdDate": isoformat_without_ms(deal.open_date),
                    "closeDate": (
                        isoformat_without_ms(deal.close_date)
                        if deal.close_date
                        else None
                    ),
                    "status": deal.status.name.upper(),
                    "stage": deal.stage.name,
                    "amount": deal.amount,
                    "description": deal.description,
                }
                f.write(json.dumps(deal_data) + "\n")

            response = self.push_data_to_gong(
                integration_id, "DEAL", open("deals.ldjson", "rb")
            )

        os.remove("deals.ldjson")

        return response

    def push_leads_to_gong(self, integration_id, leads):
        with open("leads.ldjson", "w", encoding="utf-8") as f:
            for lead in leads:
                lead_data = {
                    "objectId": str(lead.id),
                    "modifiedDate": isoformat_without_ms(lead.updated_at),
                    "isDeleted": False,
                    "url": f"{self.base_url}/leads/{lead.id}",
                    "emailAddress": lead.email,
                    "firstName": lead.first_name,
                    "lastName": lead.last_name,
                    "phoneNumber": lead.phone,
                    "ownerId": str(lead.owner_id),
                    "status": lead.status.name,
                    "account": lead.company,
                    "details": lead.details,
                }
                f.write(json.dumps(lead_data) + "\n")

            response = self.push_data_to_gong(
                integration_id, "LEAD", open("leads.ldjson", "rb")
            )

        os.remove("leads.ldjson")

        return response

    def get_crm_objects(self, integration_id, object_type, object_ids):
        response = requests.get(
            f"{self.api_url}/crm/entities",
            params={
                "integrationId": integration_id,
                "objectType": object_type,
            },
            json=list(map(str, object_ids)),
            auth=self.credentials,
            timeout=10,
        )
        if response.status_code == 200:
            return response.json()
        raise GongException(
            f"Failed to get CRM objects: {response.status_code} - {response.text}"
        )
