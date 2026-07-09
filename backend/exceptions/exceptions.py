class CreateYourStoryError(Exception):
    """base exception class"""

    def __init__(self, message: str = "Service is unavailable", name: str = "CreateYourStoryError.ai Error"):
        self.message = message
        self.name = name
        super().__init__(self.message, self.name)


class AuthenticationError(CreateYourStoryError):
    """user is not authenticated and cannot perform the action"""

    def __init__(self, message: str = "Authentication required", name: str = "Not authenticated"):
        super().__init__(message, name)


class AuthorizationError(CreateYourStoryError):
    """user is authenticated but not authorized to perform the action"""

    def __init__(self, message: str = "User is not authorized to do this", name: str = "Not authorized"):
        super().__init__(message, name)


class UnsupportedAIModelError(CreateYourStoryError):
    """selected AI model isn't supported"""

    def __init__(self, message: str = "Please choose a different model", name: str = "Model not supported"):
        super().__init__(message, name)


class JobNotFoundError(CreateYourStoryError):
    """job not found"""

    def __init__(self, message: str = "Job not found", name: str = "Not found"):
        super().__init__(message, name)


class StoryNotFoundError(CreateYourStoryError):
    """story not found"""

    def __init__(self, message: str = "Story not found", name: str = "Not found"):
        super().__init__(message, name)


class StoryRootNotFoundError(CreateYourStoryError):
    """story root not found (each story must have a root node)"""

    def __init__(self, message: str = "Story root node not found", name: str = "Not found"):
        super().__init__(message, name)


class StoryResponseValidationError(CreateYourStoryError):
    """LLM model's response doesn't match the schema"""

    def __init__(self, message: str = "AI response is incorrectly formatted", name: str = "Validation failed"):
        super().__init__(message, name)


class StoryGenerationError(CreateYourStoryError):
    """LLM was unable to generate the story"""

    def __init__(self, message: str = "An error prevented the story from being generated", name: str = "Story generation failed"):
        super().__init__(message, name)
