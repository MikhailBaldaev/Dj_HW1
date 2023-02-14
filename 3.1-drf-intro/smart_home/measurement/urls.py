from django.urls import path

from measurement.views import SensorView, SensorViewPartialUpdate, MeasurementView, SensorDetailsView


urlpatterns = [
    # TODO: зарегистрируйте необходимые маршруты
    path('sensors/', SensorView.as_view()),
    path('sensors/<pk>', SensorViewPartialUpdate.as_view()),
    path('measurements/', MeasurementView.as_view()),
    path('showsensor/<id>', SensorDetailsView.as_view()),
]
