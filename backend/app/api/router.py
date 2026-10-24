# backend/app/api/router.py
from fastapi import APIRouter

from app.api.routes import (
    health, auth, users, roles, permissions,
    territories, objects, buildings, indoor_maps, geotags,
    problems, confirmations, problem_groups, problem_messages, problem_subscriptions,
    initiatives, events,
    organizations, executors,
    sla,
    admin,
    attachments, documents,
    notifications,
    analytics, audit,
    subscriptions,
    admin_settings,
     categories,      # <-- ДОБАВЬТЕ
        help_formats     # <-- ДОБАВЬТЕ
)

api_router = APIRouter()

# --- Health ---
api_router.include_router(health.router, prefix="/health", tags=["Health"])

# --- Auth & Users ---
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(roles.router, prefix="/roles", tags=["Roles"])
api_router.include_router(permissions.router, prefix="/permissions", tags=["Permissions"])

# --- Geography & Indoor ---
api_router.include_router(territories.router, prefix="/territories", tags=["Territories"])
api_router.include_router(objects.router, prefix="/objects", tags=["Municipal Objects"])
api_router.include_router(buildings.router, prefix="/buildings", tags=["Buildings"])
api_router.include_router(indoor_maps.router, prefix="/indoor-maps", tags=["Indoor Maps"])
api_router.include_router(geotags.router, prefix="/geotags", tags=["GeoTags"])

# --- Problems Core ---
api_router.include_router(problems.router, prefix="/problems", tags=["Problems"])
api_router.include_router(confirmations.router, prefix="/problems/confirmations", tags=["Problem Confirmations"])
api_router.include_router(problem_groups.router, prefix="/problem-groups", tags=["Problem Groups"])
api_router.include_router(problem_messages.router, prefix="/problems/messages", tags=["Problem Messages"])
api_router.include_router(problem_subscriptions.router, prefix="/problems/subscriptions", tags=["Problem Subscriptions"])

# --- Initiatives & Events ---
api_router.include_router(initiatives.router, prefix="/initiatives", tags=["Initiatives"])
api_router.include_router(events.router, prefix="/events", tags=["Events"])

# --- Organizations & Executors ---
api_router.include_router(organizations.router, prefix="/organizations", tags=["Organizations"])
api_router.include_router(executors.router, prefix="/executors", tags=["Executors"])

# --- SLA ---
api_router.include_router(sla.router, prefix="/sla", tags=["SLA"])

# --- Files & Documents ---
api_router.include_router(attachments.router, prefix="/attachments", tags=["Attachments"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])

# --- Notifications ---
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])

# --- Analytics & Audit ---
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(audit.router, prefix="/audit", tags=["Audit"])

# --- Subscriptions & Settings ---
api_router.include_router(subscriptions.router, prefix="/subscriptions", tags=["Territory Subscriptions"])
api_router.include_router(admin_settings.router, prefix="/admin/settings", tags=["Admin Settings"])


# --- Справочники (публичные) ---
api_router.include_router(categories.router, prefix="/categories", tags=["Directories"])
api_router.include_router(help_formats.router, prefix="/help-formats", tags=["Directories"])

api_router.include_router(admin.router)