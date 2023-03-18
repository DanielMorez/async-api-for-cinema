from uuid import UUID

from models import User


class UserIdsService:
    @classmethod
    def get_user_ids(cls, filters: dict = {}) -> list[str]:
        qs = set()
        if filters.get("is_subscriber"):
            qs.update(
                set(str(user.id) for user in User.find_subscribers_id())
            )
        if filters.get("has_email"):
            qs.update(
                set(str(user.id) for user in User.find_verified_email_user_ids())
            )
        return list(qs)

    @classmethod
    def get_user_personal_data(cls, user_ids: list[UUID]) -> list[dict]:
        qs = User.users_by_ids(user_ids)
        data = [user.as_dict for user in qs]
        return data
