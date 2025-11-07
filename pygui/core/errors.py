class PyGUIError(Exception):
    pass


class BackendNotAvailableError(PyGUIError):
    pass


class PermissionDeniedError(PyGUIError):
    def __init__(self, feature: str, platform_hint: str = ""):
        self.feature = feature
        self.platform_hint = platform_hint
        super().__init__(f"Permission denied for {feature}. {platform_hint}")


class BackendCapabilityError(PyGUIError):
    def __init__(self, feature: str, backend: str):
        self.feature = feature
        self.backend = backend
        super().__init__(f"Feature '{feature}' is not supported on {backend} backend")


class WindowNotFoundError(PyGUIError):
    pass


class DisplayNotFoundError(PyGUIError):
    pass
