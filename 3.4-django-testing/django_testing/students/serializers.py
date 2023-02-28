from django.conf import settings
from rest_framework import serializers

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, data):
        students_count = len(data.get('students'))
        if students_count > settings.MAX_STUDENTS_PER_COURSE:
            raise serializers.ValidationError('Only 20 students are allowed on a course!')
        return data
