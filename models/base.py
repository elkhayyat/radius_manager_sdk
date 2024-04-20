from abc import ABC, abstractmethod


class BaseModel(ABC):

    def __init__(self, **kwargs):
        self.attribute_mapper = self.get_attribute_mapper()
        self.allowed_kwargs = self.set_allowed_kwargs()
        self.preserved_kwargs = [
            '__class__',
            'kwargs',
            'allowed_kwargs',
        ]

        combined_kwargs = self.combined_kwargs(**kwargs)
        self.check_all_kwargs_are_valid(**combined_kwargs)
        self.set_attributes(**combined_kwargs)

    def set_allowed_kwargs(self):
        return list(self.attribute_mapper.keys()) + list(self.attribute_mapper.values())

    def combined_kwargs(self, **kwargs):
        if kwargs.get('kwargs') is not None:
            for key, value in kwargs['kwargs'].items():
                if value is not None:
                    kwargs[key] = value

        for x in self.preserved_kwargs:
            if x in kwargs:
                del kwargs[x]
        return kwargs

    @staticmethod
    def remove_self_from_kwargs(**kwargs):
        return {key: value for key, value in kwargs.items() if key != 'self'}

    @abstractmethod
    def get_attribute_mapper(self):
        pass

    def set_attributes(self, **kwargs):
        for internal_param_name, rm_param_name in self.attribute_mapper.items():
            parameter_value = None
            if internal_param_name in kwargs and kwargs[internal_param_name] is not None:
                parameter_value = kwargs[internal_param_name]
            if rm_param_name in kwargs and kwargs[rm_param_name] is not None:
                parameter_value = kwargs[rm_param_name]

            if parameter_value is not None:
                setattr(self, internal_param_name, parameter_value)
            if internal_param_name not in self.__dict__:
                setattr(self, internal_param_name, None)

    def check_all_kwargs_are_valid(self, **kwargs):
        for key in kwargs:
            if key not in self.allowed_kwargs and key not in self.preserved_kwargs:
                raise ValueError(f"Invalid attribute {key}")

    @property
    def data_in_rm_format(self):
        data = {}
        for internal_param_name, rm_param_name in self.attribute_mapper.items():
            if getattr(self, internal_param_name) is not None:
                data[rm_param_name] = getattr(self, internal_param_name)
        return data
