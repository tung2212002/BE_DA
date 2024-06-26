from fastapi import APIRouter

from app.api.api_v1.endpoint import (
    user_auth,
    user,
    business_auth,
    business,
    business_admin,
    location,
    position,
    position_group,
    category,
    skill,
    field,
    verify,
    business_campaign,
    business_company,
    business_job,
    company,
    job,
)

api_router = APIRouter(prefix="/v1/api")
api_router.include_router(user_auth.router, prefix="/user", tags=["user_auth"])
api_router.include_router(user.router, prefix="/user/users", tags=["user"])
api_router.include_router(verify.router, prefix="/verify", tags=["verify"])
api_router.include_router(location.router, prefix="/location", tags=["location"])
api_router.include_router(position.router, prefix="/position", tags=["position"])
api_router.include_router(
    position_group.router, prefix="/position_group", tags=["position_group"]
)
api_router.include_router(category.router, prefix="/category", tags=["category"])
api_router.include_router(skill.router, prefix="/skill", tags=["skill"])
api_router.include_router(field.router, prefix="/field", tags=["field"])
api_router.include_router(job.router, prefix="/job", tags=["job"])
api_router.include_router(company.router, prefix="/company", tags=["company"])

api_router.include_router(
    business_company.router,
    prefix="/business/business_company",
    tags=["business_company"],
)
api_router.include_router(
    business_job.router, prefix="/business/job", tags=["business_job"]
)
api_router.include_router(
    business_campaign.router, prefix="/business/campaign", tags=["business_campaign"]
)
api_router.include_router(
    business_admin.router, prefix="/admin", tags=["business_admin"]
)
api_router.include_router(
    business.router, prefix="/business", tags=["business_business"]
)
api_router.include_router(
    business_auth.router, prefix="/business", tags=["business_auth"]
)
