from typing import Any

class DotDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = DotDict(value)
            elif isinstance(value, list):
                self[key] = [DotDict(item) if isinstance(item, dict) else item for item in value]

    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{attr}'")

    def __setattr__(self, attr, value):
        self[attr] = DotDict(value) if isinstance(value, dict) else value

    def __delattr__(self, attr):
        del self[attr]

    def __getitem__(self, item):
        value = super().__getitem__(item)
        if isinstance(value, dict):
            value = DotDict(value)
            self[item] = value
        elif isinstance(value, list):
            value = [DotDict(item) if isinstance(item, dict) else item for item in value]
            self[item] = value
        return value

    def items(self):
        for key, value in super().items():
            if isinstance(value, dict):
                value = DotDict(value)
            elif isinstance(value, list):
                value = [DotDict(item) if isinstance(item, dict) else item for item in value]
            yield key, value
