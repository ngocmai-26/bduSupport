from bduSuport.models.account import Account, AccountStatus

def custom_user_authentication_rule(user: Account) -> bool:
    return user is not None and user.status == AccountStatus.ACTIVATED