from rest_framework.serializers import ModelSerializer


class SerializerGetter:
    def __init__(self, default, **kwargs):
        self.default = default
        self.serializer_per_action = kwargs

    def get_serializer_class(self, view):
        return self.serializer_per_action.get(
            getattr(view, 'action', None),
            self.default
        )

    def __call__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        view = context.get('view', None)
        serializer_class = self.get_serializer_class(view)
        return serializer_class(*args, **kwargs)


class SerializerFactory:
    def __init__(self, default, **kwargs):
        self.serializer_getter = SerializerGetter(
            default=default, **kwargs,
        )

    def __call__(self, *args, **kwargs):
        return self.serializer_getter(*args, **kwargs)


class DynamicFieldsModelSerializer(ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
