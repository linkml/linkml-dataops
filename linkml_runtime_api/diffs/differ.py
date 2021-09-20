import logging
from typing import List, Dict, Any
import json

from jsonpatch import JsonPatch

from linkml_runtime.dumpers import json_dumper

from linkml_runtime_api.apiroot import ApiRoot
from linkml_runtime.utils.yamlutils import YAMLRoot

def _as_dict(obj: YAMLRoot) -> dict:
    return json.loads(json_dumper.dumps(obj))

class DiffEngine(ApiRoot):
    """
    Engine for performing diffs over databases
    """

    def diff(self, src: YAMLRoot, dst: YAMLRoot, **kwargs) -> JsonPatch:
        """
        Apply a diff to two object trees
        :param src:
        :param dst:
        :param kwargs:
        :return:
        """
        srco = _as_dict(src)
        dsto = _as_dict(dst)
        patch = JsonPatch.from_diff(srco, dsto, **kwargs)
        return patch