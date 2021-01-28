from .fields import (
    Field,
    NumberField,
)


class Document(object):
    # All documents have an 'id' property, if this is blank
    # when indexing, it will be populated with a generated one
    # This corresponds with the PK of the underlying DocumentRecord
    id = NumberField()

    @property
    def pk(self):
        return self.id

    def __init__(self, _record=None, **kwargs):
        self._record = _record

        if self._record:
            self.id = self._record.pk
        else:
            self.id = kwargs.get("id")

        self._fields = {}

        klass = type(self)

        for attr_name in dir(klass):
            attr = getattr(klass, attr_name)

            if isinstance(attr, Field):
                attr.attname = attr_name
                self._fields[attr_name] = attr

                # We set the ID value above based on _record or 'id'
                # and we don't want to wipe that
                if attr_name == "id":
                    continue

                # Apply any field values passed into the init
                if attr_name in kwargs:
                    setattr(self, attr_name, kwargs[attr_name])
                else:
                    # Set default if there was no value
                    setattr(self, attr_name, attr.default)

        for key in kwargs.keys():
            # Throw an error if the kwarg doesn't match a field
            if key not in self._fields:
                raise ValueError("Unknown field: %s" % key)

    def get_fields(self):
        return self._fields

    def get_field(self, name):
        return self._fields[name]

    def __eq__(self, other):
        return self.pk == other.pk

    def __repr__(self):
        return "<Document %s>" % self.pk
