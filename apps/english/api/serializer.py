from rest_framework import serializers

from english.models import Words


class WordsSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta."""

        model = Words
        fields = (
            "id",
            "english",
            "russian",
            "lesson",
            "learned",
            "heavy",
            "control",
            "phrasal_verbs",
            "irregular_verbs",
            "repeat_learn",
            "important",
            "info",
        )
