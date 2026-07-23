class ToolRegistryError(Exception):
    pass


class ToolAlreadyRegisteredError(ToolRegistryError):
    pass


class ToolNotFoundError(ToolRegistryError):
    pass
