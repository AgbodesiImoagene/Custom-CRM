import json
import sys
import os
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.gong_service import GongService

# Load environment variables
load_dotenv()

# Gong API settings
GONG_API_URL = os.getenv("GONG_API_URL")
GONG_ACCESS_KEY = os.getenv("GONG_ACCESS_KEY")
GONG_ACCESS_KEY_SECRET = os.getenv("GONG_ACCESS_KEY_SECRET")
credentials = (GONG_ACCESS_KEY, GONG_ACCESS_KEY_SECRET)

# Backend settings
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

# Set up database connection
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def main():
    """
    Main function for the Gong CRM Integration CLI.

    This function sets up an argument parser to handle various actions related to the Gong CRM integration.
    The available actions are:
    - register_integration: Registers a new CRM integration and prints the integration ID.
    - update_schema: Updates the CRM schema for the integration.
    - full_db_dump: Performs a full database dump and pushes data to Gong.
    - view_schema: Views the schema fields for different object types.
    - check_request_status: Checks the status of a request using the provided request ID.
    - get_crm_objects: Retrieves CRM objects based on the provided object type and object IDs.
    - delete_integration: Deletes the specified CRM integration.
    - view_integration_id: Displays the integration ID of the current CRM integration.

    Arguments:
    - action (str): The action to perform. Choices are:
        - "register_integration"
        - "update_schema"
        - "full_db_dump"
        - "view_schema"
        - "check_request_status"
        - "get_crm_objects"
        - "delete_integration"
        - "view_integration_id"
    - --request_id (str, optional): Request ID to check status (required for check_request_status action).
    - --object_type (str, optional): Object type to retrieve (required for get_crm_objects action).
    - --object_ids (str, optional): Comma-separated list of object IDs to retrieve (required for get_crm_objects action).
    - --integration_name (str, optional): Name of the integration (required for register_integration action).
    - --owner_email (str, optional): Owner email of the integration (required for register_integration action).
    - --integration_id (str, optional): Integration ID to delete (required for delete_integration action).

    Usage:
        python gong_utils.py <action> [--request_id REQUEST_ID] [--object_type OBJECT_TYPE] [--object_ids OBJECT_IDS] [--integration_name INTEGRATION_NAME] [--owner_email OWNER_EMAIL] [--integration_id INTEGRATION_ID]
    """
    parser = argparse.ArgumentParser(description="Gong CRM Integration CLI")
    parser.add_argument(
        "action",
        choices=[
            "register_integration",
            "update_schema",
            "full_db_dump",
            "view_schema",
            "check_request_status",
            "get_crm_objects",
            "delete_integration",
            "view_integration_id",
        ],
        help="Action to perform",
    )
    parser.add_argument(
        "--request_id",
        help="Request ID to check status (required for check_request_status action)",
    )
    parser.add_argument(
        "--object_type",
        help="Object type to retrieve (required for get_crm_objects action)",
        choices=["ACCOUNT", "CONTACT", "DEAL", "LEAD"],
    )
    parser.add_argument(
        "--object_ids",
        help="Comma-separated list of object IDs to retrieve (required for get_crm_objects action)",
    )
    parser.add_argument(
        "--integration_name",
        help="Name of the integration (required for register_integration action)",
    )
    parser.add_argument(
        "--owner_email",
        help="Owner email of the integration (required for register_integration action)",
    )
    parser.add_argument(
        "--integration_id",
        help="Integration ID to delete (required for delete_integration action)",
    )
    args = parser.parse_args()

    session = SessionLocal()
    gong_service = GongService(GONG_API_URL, credentials, BASE_URL, session)

    if args.action == "register_integration":
        if not args.integration_name or not args.owner_email:
            print(
                "Error: --integration_name and --owner_email are required for register_integration action"
            )
            sys.exit(1)
        integration_id = gong_service.register_crm_integration(
            args.integration_name, args.owner_email
        )
        print(f"Integration ID: {integration_id}")

    elif args.action == "update_schema":
        integration_id = gong_service.get_crm_integration()
        gong_service.register_crm_schema(integration_id)
        print("Schema updated successfully.")

    elif args.action == "full_db_dump":
        integration_id = gong_service.get_crm_integration()
        users, companies, contacts, deals, leads = gong_service.fetch_data_from_db()
        responses = []
        responses.append(gong_service.push_stages_to_gong(integration_id))
        responses.append(gong_service.push_users_to_gong(integration_id, users))
        responses.append(gong_service.push_companies_to_gong(integration_id, companies))
        responses.append(gong_service.push_contacts_to_gong(integration_id, contacts))
        responses.append(gong_service.push_deals_to_gong(integration_id, deals))
        responses.append(gong_service.push_leads_to_gong(integration_id, leads))
        print("Full database dump completed successfully.")
        for response in responses:
            print(response)

    elif args.action == "view_schema":
        integration_id = gong_service.get_crm_integration()
        for object_type in ["ACCOUNT", "CONTACT", "DEAL", "LEAD"]:
            schema_fields = gong_service.list_schema_fields(integration_id, object_type)
            print(f"Schema fields for {object_type}:")
            print(json.dumps(schema_fields, indent=2))

    elif args.action == "check_request_status":
        if not args.request_id:
            print("Error: --request_id is required for check_request_status action")
            sys.exit(1)
        integration_id = gong_service.get_crm_integration()
        status, errors = gong_service.check_request_status(
            integration_id, args.request_id
        )
        print(f"Request status: {status}")
        if errors:
            print(f"Errors: {json.dumps(errors, indent=2)}")

    elif args.action == "get_crm_objects":
        if not args.object_type or not args.object_ids:
            print(
                "Error: --object_type and --object_ids are required for get_crm_objects action"
            )
            sys.exit(1)
        integration_id = gong_service.get_crm_integration()
        object_ids = args.object_ids.split(",")
        objects = gong_service.get_crm_objects(
            integration_id, args.object_type, object_ids
        )
        print(json.dumps(objects, indent=2))

    elif args.action == "delete_integration":
        if not args.integration_id:
            print("Error: --integration_id is required for delete_integration action")
            sys.exit(1)
        gong_service.delete_crm_integration(args.integration_id)
        print("Integration deleted successfully.")

    elif args.action == "view_integration_id":
        integration_id = gong_service.get_crm_integration()
        print(f"Integration ID: {integration_id}")

    # Close database session
    session.close()


if __name__ == "__main__":
    main()
