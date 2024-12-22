class BaseCartsRepoError(Exception):
    pass

class ActiveEventAlreadyExistsError(BaseCartsRepoError):
    pass

class EventNotFoundError(BaseCartsRepoError):
    pass

class EventUpdateError(BaseCartsRepoError):
    pass