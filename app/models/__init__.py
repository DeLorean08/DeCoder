from .base import Base
from .user import User
from .problem import Problem, Test_case
from .submission import Submission
from .language import Programming_language

# Цей список __all__ є опціональним, але вважається хорошою практикою.
# Він явно визначає, які імена будуть експортовані, коли хтось
# використовує "from app.models import *".
__all__ = [
    "Base",
    "User",
    "Problem",
    "Test_case",
    "Submission",
    "Programming_language",
]
