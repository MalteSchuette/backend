from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Quiz, Question
from .serializers import QuizSerializer
from .utils import process_youtube_url


class QuizViewSet(ModelViewSet):
    """Handles all CRUD operations for quizzes."""

    permission_classes = [IsAuthenticated]
    serializer_class = QuizSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        """Returns only the quizzes of the authenticated user."""
        return Quiz.objects.filter(user=self.request.user)

    def create(self, request):
        """Creates a new quiz from a YouTube URL."""
        url = request.data.get('url')
        if not url:
            return Response({'detail': 'URL is required.'}, status=status.HTTP_400_BAD_REQUEST)
        quiz_data = process_youtube_url(url)
        quiz = Quiz.objects.create(
            user=request.user,
            title=quiz_data['title'],
            description=quiz_data['description'],
            video_url=url,
        )
        for item in quiz_data['questions']:
            Question.objects.create(
                quiz=quiz,
                question_title=item['question_title'],
                question_options=item['question_options'],
                answer=item['answer'],
            )
        serializer = QuizSerializer(quiz)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
