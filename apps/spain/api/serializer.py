from rest_framework import serializers

from apps.spain.models import Words


class WordsSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta."""

        model = Words
        fields = (
            "id",
            "spain",
            "russian",
            "lesson",
            "learned",
            "heavy",
            "control",
            "irregular_verbs",
            "repeat_learn",
            "important",
            "info",
        )
