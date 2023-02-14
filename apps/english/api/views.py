from django.contrib.auth.models import User
from rest_framework import generics

from english.api.serializer import WordsSerializer
from english.models import Words, WordParams


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
        return WordParams.get_words(user.id)

