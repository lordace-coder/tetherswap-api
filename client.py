from cocobase_client import CocoBaseClient, QueryBuilder
import os, dotenv

dotenv.load_dotenv()

db = CocoBaseClient(api_key=os.getenv("COCOBASE_API_KEY", ""))


def get_referrals(user_id):
    """
    Fetch the number of referrals for a given user ID.
    """
    try:
        # Assuming 'referrals' is the collection name and 'user_id' is the field to filter by
        result = db.list_documents(
            "referrals",query = QueryBuilder().contains("ref_by", user_id))
        
        if not result:
            return 0
        return len(result)
    except Exception as e:
        print(f"Error fetching referrals: {e}")
        return 0  # Return 0 if there's an error


def add_referral(user_id, ref_by):
    """
    Add a new referral record.
    """
    try:
        q = db.list_documents(
            "referrals",
            query=QueryBuilder().from_dict(
                {"ref_by": ref_by, "referred_user": user_id}
            ),
        )
        if q:
            print(f"Referral already exists for {user_id} by {ref_by}")
            return False  # Referral already exists
        db.create_document(
            "referrals",
            {
                "ref_by": ref_by,
                "referred_user": user_id,
            },
        )
        return True
    except Exception as e:
        print(f"Error adding referral: {e}")
        return False
