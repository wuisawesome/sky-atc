import json
from kubernetes import client
from typing import Any, Dict, List, Union
import re
from datetime import datetime
import logging
import hashlib


logger = logging.getLogger(__name__)


def _camelCaseTo_snake_case(s : str) -> str:
    # Probably works https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower()

def _snake_to_camel(snake_case):
    # Split the string into words using underscores
    words = snake_case.split('_')
    words[1:] = [word.capitalize() for word in words[1:]]
    return "".join(words)

def _construct_v1_type(type_str : str, data : Union[str, int, datetime, Dict[str, Any], List[Any]]) -> Any:
    # print(f"_construct_v1_type({type_str}, {data})")
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


def json_string_to_node(json_string : str) -> client.V1Node:
    as_dict = json.loads(json_string)

    return _construct_v1_type("V1Node", as_dict)


def json_string_to_pod(json_string : str) -> client.V1Pod:
    as_dict = json.loads(json_string)

    return _construct_v1_type("V1Pod", as_dict)


def v1_type_to_dict(obj : Any) -> Union[Dict, List, int, float, Any]:
    if isinstance(obj, list):
        return [v1_type_to_dict(x) for x in obj]

    if not hasattr(obj, "attribute_map"):
        return obj

    as_dict = {}
    for attr_name, dict_name in obj.attribute_map.items():
        value = v1_type_to_dict(getattr(obj, attr_name))
        if value is not None:
            as_dict[dict_name] = value

    return as_dict


def stable_pod_config_hash(pod : client.V1Pod) -> str:
    """We're defining the notion of a "config" to mean the parts of the pod
    resource that the user specifies that we need to satisfy. If their config
    changes, we need to make changes (which likely means stopping the pod and
    starting an ew on with the new config).

    We need to summarize some the pod into some string small enough that it
    can fit in the smallest "kv store" the the compute providers have.

    If this value changes, we should assume that the pod config has changed.
    """
    spec = pod.spec
    # sort_keys is the only parameter that's really needed?
    canonical_str = json.dumps(spec.to_dict(), sort_keys=True, indent='', separators='').encode('utf-8')
    # md5 digest is shorter and inputs shouldn't be malicious.
    return hashlib.md5(canonical_str).digest()

