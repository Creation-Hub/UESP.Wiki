from typing import Any

class Dump():

    @staticmethod
    def Any(this:Any) -> str:
        string:str = f"{this.__class__.__name__}"
        string += f"\n - Attributes: [{len(this.__dict__)}] ..."
        for key in this.__dict__:
            value:Any = getattr(this, key)
            if isinstance(value, list) or isinstance(value, dict):
                string += f"\n   - {key}: [{value.__len__()}] ..."
            else:
                string += f"\n   - {key}: {value}"
        return string
