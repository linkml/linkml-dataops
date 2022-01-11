import logging
import sys
from contextlib import redirect_stdout

from io import StringIO
from typing import IO, Union, List

from jsonpatch import JsonPatch
from ruamel.yaml import YAML

class YAMLPatch:
    """
    YAML wrapper onto JsonPatch module

    Note: this could be moved into its own library independent of LinkML
    """

    def multipatch(self, input: Union[str, IO[str]], patches: List[Union[JsonPatch, dict]], outstream: IO[str]) -> None:
        """
        Apply multiple patches to a file or stream

        :param input:
        :param patches:
        :param outstream:
        :return:
        """
        yaml = YAML()
        with open(input) as instream:
            obj = yaml.load(instream)
        for patch in patches:
            if isinstance(patch, dict):
                logging.debug(f' PATCH={patch}')
                patch = JsonPatch([patch])
            obj = patch.apply(obj)
        if isinstance(outstream, str):
            with open(outstream, 'wb') as new_outstream:
                yaml.dump(obj, stream=new_outstream)
        else:
            yaml.dump(obj, stream=outstream)

    def multipatchs(self, input: IO[str], patches: List[Union[JsonPatch, dict]]) -> str:
        """
        As multipatch but retyrns yaml string instead of writing to a file,
        :param input:
        :param patches:
        :return:
        """
        output = StringIO()
        with redirect_stdout(output):
            self.multipatch(input, patches, outstream=output)
        return output.getvalue()

    def patch(self, input: IO[str], patch: Union[JsonPatch, dict], outstream: IO[str]) -> None:
        """
        Apply a patch to a YAML file or stream

        :param input:
        :param patch:
        :param outstream:
        :return:
        """
        yaml = YAML()
        obj = yaml.load(input)
        if isinstance(patch, dict):
            patch = JsonPatch(patch)
        patched_obj = patch.apply(obj)
        yaml.dump(patched_obj, stream=outstream)

    def patchs(self, input: IO[str], patch: Union[JsonPatch, dict]) -> str:
        """
        As patch, but returns YAML string
        :param input:
        :param patch:
        :return:
        """
        output = StringIO()
        with redirect_stdout(output):
            self.patch(input, patch, outstream=output)
        return output.getvalue()