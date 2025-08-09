from argparse import Namespace
from typing import Any

class Dump():
    LIST_MAX:int = 10
    INDENT_SIZE:int = 3


    @staticmethod
    def get(this:Any) -> str:
        return f"{this.__class__.__name__}: >>>{Dump._Any(this)}"


    @staticmethod
    def _Any(this:Any, depth:int = 0) -> str:
        this_class_name:str = this.__class__.__name__
        this_attributes:dict[Any, Any] = this.__dict__

        base_indent = " " * (depth * Dump.INDENT_SIZE)
        attr_indent = " " * ((depth + 1) * Dump.INDENT_SIZE)
        item_indent = " " * ((depth + 2) * Dump.INDENT_SIZE)

        string:str = ""
        string += f"\n{base_indent} - {this_class_name}: <{len(this_attributes)}> ..."

        for attribute_key in this_attributes:
            attribute:Any = getattr(this, attribute_key)

            if isinstance(attribute, list):
                string += f"\n{attr_indent} - {attribute_key}: [{attribute.__len__()}] ..."
                list_max_count:int = 0
                for item in attribute:  # type: ignore
                    list_max_count += 1
                    string += f"\n{item_indent} - {item}"
                    if list_max_count >= Dump.LIST_MAX:
                        string += f"\n{item_indent} - ..."
                        break

            # elif isinstance(attribute, dict):
            #     string += Dump._Any(attribute, depth + 1)

            elif isinstance(attribute, dict):
                string += f"\n{attr_indent} - {attribute_key}: [{attribute.__len__()}] ..."
                list_max_count:int = 0
                for key, value in attribute.items():  # type: ignore
                    list_max_count += 1
                    string += f"\n{item_indent} - {key}: {value}"
                    if list_max_count >= Dump.LIST_MAX:
                        string += f"\n{item_indent} - ..."
                        break

            elif isinstance(attribute, Namespace):
                string += Dump._Any(attribute, depth + 1)

            else:
                string += f"\n{attr_indent} - {attribute_key}: {attribute}"

        return string
