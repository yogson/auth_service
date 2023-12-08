from datetime import datetime
import logging
from typing import Type, Optional

from pydantic import create_model, BaseModel

logger = logging.getLogger(__name__)


def get_utcnow_timestamp():
    return int(datetime.utcnow().timestamp())


def create_update_model(model: Type[BaseModel]) -> Type[BaseModel]:
    fields = {name: (Optional[_type], None) for name, _type in model.__annotations__.items()}
    return create_model('Update' + model.__name__, **fields)