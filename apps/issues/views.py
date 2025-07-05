from rest_framework import viewsets
from .models import Issue
from .serializers import IssueSerializer
from apps.issues.ml_utils import predict_issue_type

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        if instance.image:
            predicted_type = predict_issue_type(instance.image.path)
            print(f"Predicted issue type: {predicted_type}")
            instance.issue_type = predicted_type
            instance.save()
