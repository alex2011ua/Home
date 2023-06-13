from django.contrib.auth.models import User
from rest_framework import generics

from apps.spain.api.serializer import WordsSerializer
from apps.spain.models import Words, WordParamsSpain


class WordRUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WordsSerializer
    queryset = Words.objects.all()

    # def patch(self, request, *args, **kwargs):
    #     print(request)
    #     print(request.POST)
    #     super().patch(self, request, *args, **kwargs)


class RepeatWordListView(generics.ListAPIView):
    serializer_class = WordsSerializer
    queryset = Words.objects.filter(important=False).order_by("-repeat_learn", "?")[0:50]


class REWordListView(generics.ListAPIView):
    serializer_class = WordsSerializer

    def get_queryset(self):
        user = self.request.user
        return WordParamsSpain.get_words(user.id)

