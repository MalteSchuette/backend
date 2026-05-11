from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Quiz, Question
from .serializers import QuizSerializer
from .utils import process_youtube_url


class QuizListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Returns all quizzes of the authenticated user."""
        quizzes = Quiz.objects.filter(user=request.user)
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)

    def post(self, request):
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