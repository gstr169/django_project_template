from rest_framework.fields import ImageField


class SubstImageField(ImageField):

    def to_representation(self, value):
        ret = super().to_representation(value)
        if isinstance(ret, str):
            ret = ret.replace('http', 'https', 1)
        return ret
