import pytest
from rest_framework import serializers
from rest_framework.test import APIClient
from model_bakery import baker
from django.forms.models import model_to_dict

from students.models import Student, Course
from students.serializers import CourseSerializer


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_course(client, student_factory, course_factory):
    # Arrange
    course = course_factory(_quantity=1, students=student_factory(_quantity=40))
    my_dict = model_to_dict(course[0])
    course_test = Course.objects.get(id=course[0].id)
    stud_test = course_test.students.values_list('id', flat=True)
    my_dict['students'] = list(stud_test)

    # Act
    response = client.get(f'http://127.0.0.1:8000/api/v1/courses/{course[0].id}', follow=True)

    # Assert
    assert response.status_code == 200
    assert my_dict == response.data


@pytest.mark.django_db
def test_list_courses(client, student_factory, course_factory):
    # Arrange
    course_factory(_quantity=3, students=student_factory(_quantity=40))
    course_test = Course.objects.all()

    # Act
    response = client.get(f'http://127.0.0.1:8000/api/v1/courses/', follow=True)

    # Assert
    assert response.status_code == 200
    assert len(course_test) == len(response.data)


@pytest.mark.django_db
def test_get_id(client, student_factory, course_factory):
    # Arrange
    course_factory(_quantity=5, students=student_factory(_quantity=40))
    ids = Course.objects.values_list('id')

    # Act
    for id in ids:
        response = client.get(f'http://127.0.0.1:8000/api/v1/courses/{id[0]}', follow=True)

    # Assert
        assert response.status_code == 200
        assert id[0] == response.data['id']


@pytest.mark.django_db
def test_get_name(client, student_factory, course_factory):
    # Arrange
    course_factory(_quantity=5, students=student_factory(_quantity=40))
    names = Course.objects.values_list('name')

    # Act
    for name in names:
        response = client.get(f'http://127.0.0.1:8000/api/v1/courses/?name={name[0]}', follow=True)

    # Assert
        assert response.status_code == 200
        assert name[0] == response.data[0]['name']


@pytest.mark.django_db
def test_create(client):
    # Arrange
    course_object = {
        "id": 1,
        "name": "Qwer",
        "students": [],
    }

    # Act
    response = client.post(f'http://127.0.0.1:8000/api/v1/courses/', data=course_object)
    data = Course.objects.all()
    course_test = Course.objects.get(id=course_object['id'])
    stud_test = course_test.students.values_list('id', flat=True)
    data = [{'id': k.id, 'name': k.name, 'students': stud_test if stud_test else []} for k in data]

    # Assert
    assert response.status_code == 201
    assert response.data == data[0]


@pytest.mark.django_db
def test_update(client, student_factory, course_factory):
    # Arrange
    course_factory(_quantity=1, students=student_factory(_quantity=40))
    course_object = {
        "id": 1,
        "name": "Qwer",
        "students": [],
    }

    # Act
    response = client.patch(f'http://127.0.0.1:8000/api/v1/courses/1/', data=course_object)
    data = Course.objects.all()
    course_test = Course.objects.get(id=course_object['id'])
    stud_test = course_test.students.values_list('id', flat=True)
    data = [{'id': k.id, 'name': k.name, 'students': stud_test if stud_test else []} for k in data]

    # Assert
    assert response.status_code == 200
    assert response.data == data[0]


@pytest.mark.django_db
def test_delete(client, student_factory, course_factory):
    # Arrange
    course = course_factory(_quantity=1, students=student_factory(_quantity=40))

    # Act
    response = client.delete(f'http://127.0.0.1:8000/api/v1/courses/1/')

    # Assert
    assert response.status_code == 204
    test_q = Course.objects.filter(id=course[0].id).values()
    assert not test_q.exists()


@pytest.mark.parametrize('students_count, expected_result', [
    (25, False),
    (20, True),
    (15, True)
    ])
@pytest.mark.django_db
def test_max_students_per_course(students_count, expected_result):
    # Arrange
    students_list = [{'name': f'name {i}'} for i in range(students_count)]
    name = 'The First'
    data = {'name': name, 'students': students_list}
    serializer = CourseSerializer()

    # Act
    try:
        serializer.validate(data)
        result = True
    except serializers.ValidationError:
        result = False

    # Assert
    assert result == expected_result


