from settings.enums import CustomEnum


class UserErrorMessage(CustomEnum):
    NOT_FOUND = "User does not exists"
    REQUEST_EXISTS = "This user already sent you a request"
    CONTACT_EXISTS = "This user already in contacts"
    ACTIVATION_FAILED = "User activation failed, check token"
    PASSWORD_RESET_FAILED = "Password reset failed, check token"
    WRONG_PASSWORD = "Wrong password"
