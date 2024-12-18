
from dataclasses_json import DataClassJsonMixin, Undefined, config

class DataClassExcludeNoneMixin(DataClassJsonMixin):
    dataclass_json_config = config(
        # letter_case=LetterCase.CAMEL,
        undefined=Undefined.EXCLUDE,
        exclude=lambda f: f is None
    )["dataclasses_json"]