from rest_framework import serializers


def response_gen(data: dict, is_paged=False, has_page=False):
    if is_paged:
        data['num_of_pages'] = serializers.IntegerField(
            help_text='pagination', min_value=1)
    if has_page:
        data['page'] = serializers.IntegerField(
            help_text='pagination', min_value=1, required=False, default=1)
    tp = type('obj', (serializers.Serializer,), data)
    tp.__name__ = str(id(tp))
    return tp
