def get_custom_name(name, obj=None):
    if name.startswith("__") and name.endswith("__"):
        custom_name = name
    elif name.startswith("__"):
        if obj:
            custom_name = f"_{obj.__class__.__name__}__custom_{name[2:]}"
        else:
            custom_name = f"_{type.__name__}__custom_{name[2:]}"
    elif name.startswith("_"):
        custom_name = f"_custom_{name[1:]}"
    else:
        custom_name = f"custom_{name}"
    return custom_name


class CustomMeta(type):
    def __setattr__(cls, name, value):
        custom_name = get_custom_name(name, obj=cls)
        object.__setattr__(cls, custom_name, value)

    def __new__(mcs, name, bases, attrs, **extra_kwargs):
        custom_attrs = {get_custom_name(key): value for key, value in attrs.items()}
        custom_attrs["__setattr__"] = mcs.__setattr__
        return super().__new__(mcs, name, bases, custom_attrs)

    def __init__(cls, name, bases, attrs, **extra_kwargs):
        super().__init__(name, bases, attrs, **extra_kwargs)

    @classmethod
    def __prepare__(mcs, name, bases, **extra_kwargs):
        return super().__prepare__(mcs, name, bases, **extra_kwargs)

    def __call__(cls, *args, **kwargs):
        return super().__call__(*args, **kwargs)


class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"
