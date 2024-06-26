from fastapi import APIRouter, Depends, Query, Path, Body
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.hepler.response_custom import custom_response_error, custom_response
from app.hepler.enum import OrderType
from app.core import constant
from app.core.field import service_field
from app.core.auth.service_business_auth import get_current_superuser

router = APIRouter()


@router.get("", summary="Get list of categories.")
def get_list_field(
    skip: int = Query(None, description="The number of field to skip.", example=0),
    limit: int = Query(None, description="The number of field to return.", example=100),
    order_by: str = Query(
        None, description="The order to sort by.", example=OrderType.ASC
    ),
    db: Session = Depends(get_db),
):
    """
    Get list of categories.

    This endpoint allows getting a list of categories.

    Parameters:
    - skip (int): The number of categories to skip.
    - limit (int): The number of categories to return.
    - sort_by (str): The field to sort by.
    - order_by (str): The order to sort by.

    Return:
    - status_code (200): The list of categories has been found successfully.

    """
    args = locals()

    status, status_code, response = service_field.get_field(db, args)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/{id}", summary="Get field by id.")
def get_field_by_id(
    id: int = Path(..., description="The field id."),
    db: Session = Depends(get_db),
):
    """
    Get field by id.

    This endpoint allows getting a field by id.

    Parameters:
    - id (int): The field id.

    Return:
    - status_code (200): The field has been found successfully.
    - status_code (404): The field is not found.

    """
    status, status_code, response = service_field.get_by_id(db, id)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("", summary="Create a field.")
def create_field(
    data: dict = Body(
        ...,
        example={
            "name": "Lĩnh vực X",
            "slug": "linh-vuc-x",
            "description": "",
        },
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_superuser),
):
    """
    Create a field.

    This endpoint allows creating a new field.

    Parameters:
    - name (str): The name of the field.
    - slug (str): The slug of the field.
    - description (str): The description of the field.

    Return:
    - status_code (201): The field has been created successfully.
    - status_code (400): The request is invalid.
    - status_code (409): The field is already created.

    """
    data = locals()

    status, status_code, response = service_field.create(db, data)
    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.put("/{id}", summary="Update a field.")
def update_field(
    id: int = Path(..., description="The field id."),
    data: dict = Body(
        ...,
        example={
            "name": "Lĩnh vực X",
            "slug": "linh-vuc-x",
            "description": "",
        },
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_superuser),
):
    """
    Update a field.

    This endpoint allows updating a field.

    Parameters:
    - id (int): The field id.
    - name (str): The name of the field.
    - slug (str): The slug of the field.
    - description (str): The description of the field.

    Return:
    - status_code (200): The field has been updated successfully.
    - status_code (400): The request is invalid.
    - status_code (404): The field is not found.

    """
    data = locals()

    status, status_code, response = service_field.update(db, data)
    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.delete("/{id}", summary="Delete a field.")
def delete_field(
    id: int = Path(..., description="The field id."),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_superuser),
):
    """
    Delete a field.

    This endpoint allows deleting a field.

    Parameters:
    - id (int): The field id.

    Return:
    - status_code (200): The field has been deleted successfully.
    - status_code (404): The field is not found.

    """
    status, status_code, response = service_field.delete(db, id)
    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)
