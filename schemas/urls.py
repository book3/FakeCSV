from django.urls import path

from .views import (
    DatasetListView,
    SchemaCreateView,
    SchemaDeleteView,
    SchemaListView,
    SchemaUpdateView,
    get_datasets,
    home,
)

urlpatterns = [
    path("", home, name="home"),
    path("get_datasets/", get_datasets, name="get-datasets"),
    path("schemas/", SchemaListView.as_view(), name="schemas"),
    path("schemas/new/", SchemaCreateView.as_view(), name="schema-create"),
    path("schemas/<int:pk>/", DatasetListView.as_view(), name="datasets"),
    path("schemas/<int:pk>/update/", SchemaUpdateView.as_view(), name="schema-update"),
    path("schemas/<int:pk>/delete/", SchemaDeleteView.as_view(), name="schema-delete"),
]
