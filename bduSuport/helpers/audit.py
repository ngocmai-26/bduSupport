import logging
from bduSuport.models.account import Account
from bduSuport.models.backoffice_autdit_log import BackofficeAuditLog

def audit_back_office(user: Account, action: str = "", detail: str = ""):
    try:
        BackofficeAuditLog(
            user=user,
            action=action,
            detail=detail
        ).save()
    except Exception as e:
        logging.exception("audit_backoffice exc=%s, user=%s, action=%s, detail=%s", e, user, action, detail)