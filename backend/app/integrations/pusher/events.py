class PusherEvents:
    PROBLEM_STATUS_CHANGED = "problem.status_changed"
    PROBLEM_NEW_MESSAGE = "problem.new_message"
    PROBLEM_CONFIRMED = "problem.confirmed"
    NOTIFICATION_NEW = "notification.new"
    SLA_OVERDUE = "sla.overdue"
    GEO_ZONE_ENTRY = "geo.zone_entry"


class PusherChannels:
    @staticmethod
    def user_channel(user_id: int) -> str:
        return f"private-user-{user_id}"

    @staticmethod
    def problem_channel(problem_id: int) -> str:
        return f"private-problem-{problem_id}"

    @staticmethod
    def territory_channel(territory_id: int) -> str:
        return f"public-territory-{territory_id}"