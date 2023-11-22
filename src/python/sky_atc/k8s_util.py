import json
from kubernetes import client
from typing import Any, Dict, List, Union
import re
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


def _camelCaseTo_snake_case(s):
    # Probably works https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower()


def _construct_v1_type(type_str : str, data : Union[str, int, datetime, Dict[str, Any], List[Any]]) -> Any:
    print(f"_construct_v1_type({type_str}, {data})")
    if data is None:
        return None

    if type_str in {"int", "str", "datetime", "dict(str, str)", "object", "bool"}:
        # There seem to be a smattering of openapi types that are represented
        # by built in python types. This may or may not be a complete list.
        return data

    if type_str.startswith("list"):
        underlying_type = type_str[5:-1]
        return [_construct_v1_type(underlying_type, obj) for obj in data]

    assert hasattr(client, type_str), f"data {data} should be of type {type_str}"
    cls = getattr(client, type_str)

    constructor_args = {}

    for attribute_key in data:
        attribute_name = _camelCaseTo_snake_case(attribute_key)
        if attribute_name not in cls.openapi_types:
            logger.warn(f"{attribute_name} not an attribute of {type_str}. Skipping.")
            continue
        attribute_type : str = cls.openapi_types[attribute_name]
        attribute_value = _construct_v1_type(attribute_type, data[attribute_key])
        constructor_args[attribute_name] = attribute_value

    return cls(**constructor_args)


def json_string_to_node(json_string):
    as_dict = json.loads(json_string)

    return _construct_v1_type("V1Node", as_dict)


def json_string_to_pod(json_string):
    as_dict = json.loads(json_string)

    return _construct_v1_type("V1Pod", as_dict)

