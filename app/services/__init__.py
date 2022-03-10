from .services import Certificate, Staff


class Services:
    def __init__(self) -> None:
        self.staff = Staff()
        self.certificate = Certificate()


services = Services()
