# backend/app/models/__init__.py

# Core & Auth
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.executor_organization import ExecutorOrganization
from app.models.executor import Executor

# Geography & Indoor
from app.models.territory import Territory
from app.models.municipal_object import MunicipalObject
from app.models.building import Building
from app.models.floor import Floor
from app.models.room import Room
from app.models.map_layer import MapLayer
from app.models.map_zone import MapZone

# GeoTags
from app.models.geo_tag import GeoTag
from app.models.geo_tag_event import GeoTagEvent

# Problems Core
from app.models.category import Category
from app.models.priority import Priority
from app.models.problem import Problem
from app.models.problem_group import ProblemGroup
from app.models.problem_fact import ProblemFact
from app.models.problem_confirmation import ProblemConfirmation

# Problem Workflow
from app.models.problem_status_history import ProblemStatusHistory
from app.models.problem_participant import ProblemParticipant
from app.models.problem_message import ProblemMessage
from app.models.problem_subscription import ProblemSubscription
from app.models.problem_rating import ProblemRating
from app.models.problem_recurrence import ProblemRecurrence

# Initiatives & Events
from app.models.initiative import Initiative
from app.models.initiative_support import InitiativeSupport
from app.models.event_request import EventRequest

# Files & Media
from app.models.attachment import Attachment
from app.models.document import Document
from app.models.before_after_media import BeforeAfterMedia
from app.models.media_privacy_job import MediaPrivacyJob

# Responsibility & SLA
from app.models.responsibility_transfer import ResponsibilityTransfer
from app.models.sla_policy import SlaPolicy
from app.models.sla_timer import SlaTimer
from app.models.resolution_assessment import ResolutionAssessment

# Notifications & System
from app.models.notification import Notification
from app.models.notification_delivery import NotificationDelivery
from app.models.offline_sync_record import OfflineSyncRecord
from app.models.digital_object_passport import DigitalObjectPassport
from app.models.audit_log import AuditLog

__all__ = [
    "User", "Role", "Permission", "ExecutorOrganization", "Executor",
    "Territory", "MunicipalObject", "Building", "Floor", "Room", "MapLayer", "MapZone",
    "GeoTag", "GeoTagEvent",
    "Category", "Priority", "Problem", "ProblemGroup", "ProblemFact", "ProblemConfirmation",
    "ProblemStatusHistory", "ProblemParticipant", "ProblemMessage", "ProblemSubscription", "ProblemRating", "ProblemRecurrence",
    "Initiative", "InitiativeSupport", "EventRequest",
    "Attachment", "Document", "BeforeAfterMedia", "MediaPrivacyJob",
    "ResponsibilityTransfer", "SlaPolicy", "SlaTimer", "ResolutionAssessment",
    "Notification", "NotificationDelivery", "OfflineSyncRecord", "DigitalObjectPassport", "AuditLog",
]