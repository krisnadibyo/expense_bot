

from pydantic import BaseModel


class RequestMessage(BaseModel):
  message: str