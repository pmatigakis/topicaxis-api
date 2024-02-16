from topicaxisapi.services.exceptions import ServiceError


class UserServiceError(ServiceError):
    pass


class UnknownUserError(UserServiceError):
    pass
