from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
import uuid

from app.hepler.verify_code import generate_code
from app.crud.verify_code import verify_code as verify_codeCRUD
from app.crud.verify_code_block import verify_code_block as verify_code_blockCRUD
from app.crud.business import business as businessCRUD
from app.schema.verify_code import VerifyCodeCreate, VerifyCodeUpdate, VerifyCodeRequest
from app.schema.verify_code_block import VerifyCodeBlockCreate
from app.hepler.enum import VerifyCodeType
from app.core import constant
from app.core.email.service_email import (
    send_email_background,
    read_email_templates,
    fill_template,
)
from app.hepler.exception_handler import get_message_validation_error


async def send_verify_background(
    db: Session, background_tasks: BackgroundTasks, data: dict, current_user
):
    if data.get("type") == VerifyCodeType.EMAIL:
        if not current_user.business:
            return constant.ERROR, 400, "Business not found"
        if current_user.business.is_verified_email:
            return constant.ERROR, 400, "Email is verified"
        verify_code_block = verify_code_blockCRUD.search(
            db, email=current_user.email, delta=5
        )
        if verify_code_block:
            return constant.ERROR, 400, "Please wait 5 minutes to resend email"

        email_to = current_user.email
        subject = "Verify Email"
        verify_code = generate_code(6)
        session_id = str(uuid.uuid4())

        body = fill_template(
            await read_email_templates("email.html"),
            email=email_to,
            verify_code=verify_code,
            full_name=current_user.full_name,
            title="xác thực tài khoản",
        )

        obj_in = VerifyCodeCreate(
            manager_base_id=current_user.id,
            email=email_to,
            code=verify_code,
            session_id=session_id,
        )

        verify_codeCRUD.create(db, obj_in=obj_in)

        response = await send_email_background(
            db, background_tasks, subject, email_to, body
        )
        if response:
            return constant.SUCCESS, 200, {"session_id": session_id}
        return constant.ERROR, 400, "Send email failed"


def verify_code(db: Session, data: dict, current_user):
    try:
        data = VerifyCodeRequest(**data)
    except Exception as e:
        return constant.ERROR, 404, get_message_validation_error(e)
    code_block = verify_code_blockCRUD.search(db, email=current_user.email, delta=5)
    if code_block:
        return constant.ERROR, 400, "Please wait 5 minutes to resend email"
    code_by_session_id_and_email = (
        verify_codeCRUD.get_valid_code_by_session_id_and_email(
            db, data.session_id, current_user.email, 5
        )
    )
    if not code_by_session_id_and_email:
        return constant.ERROR, 404, "Verify code not found"
    if code_by_session_id_and_email.code != data.code:
        if code_by_session_id_and_email.failed_attempts >= 4:
            verify_codeCRUD.remove(db=db, id=code_by_session_id_and_email.id)
            verify_code_blockCRUD.create(
                db,
                obj_in=VerifyCodeBlockCreate(
                    email=current_user.email,
                    delta=5,
                ),
            )
            return (
                constant.ERROR,
                400,
                "Verify code is incorrect. Please wait 5 minutes to resend email",
            )
        verify_codeCRUD.update(
            db,
            db_obj=code_by_session_id_and_email,
            obj_in=VerifyCodeUpdate(
                failed_attempts=code_by_session_id_and_email.failed_attempts + 1
            ),
        )
        return constant.ERROR, 404, "Verify code is incorrect"
    verify_codeCRUD.remove(db=db, id=code_by_session_id_and_email.id)
    businessCRUD.set_is_verified_email(
        db=db, db_obj=current_user.business, is_verified_email=True
    )
    return constant.SUCCESS, 200, "Verify code is correct"
