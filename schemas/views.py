from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View

from .forms import ColumnFormSet, SchemaForm
from .models import Dataset, Schema
from .tasks import generate_csv_file


def home(request):
    return render(request, "home.html", {})


def get_datasets(request):
    data = []
    for dataset in Dataset.objects.all():
        d = {}
        d.update(id=dataset.id, status=dataset.status)
        if dataset.csv_file:
            d.update(csv_file_url=dataset.csv_file.url)
        data.append(d)
    return JsonResponse({"datasets": data})


class SchemaListView(LoginRequiredMixin, ListView):
    model = Schema
    template_name = "schemas/schemas_list.html"
    context_object_name = "schemas"
    ordering = ["-updated_at"]
    paginate_by = settings.PAGE_SIZE

    def get_queryset(self):
        return Schema.objects.filter(author=self.request.user).order_by("-updated_at")


class SchemaBaseView(View):
    model = Schema
    success_url = "/schemas/"
    form_class = SchemaForm

    def form_valid(self, form):
        form.instance.author = self.request.user

        # do not save schema object if there was an error inside column formset
        try:
            with transaction.atomic():
                # handle schema form
                self.object = form.save()
                # handle column formset
                context = self.get_context_data()
                columns_formset = context["columns"]
                condition = columns_formset.is_valid()

                # interrupt the transaction if there was an error in columns
                if not condition:
                    raise ValidationError("Invalid ColumnFormSet")

                columns_formset.instance = self.object
                columns_formset.save()
        except ValidationError:
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == "GET":
            context["columns"] = ColumnFormSet(instance=self.object)
        elif self.request.method == "POST":
            context["columns"] = ColumnFormSet(self.request.POST, instance=self.object)
        return context


class SchemaCreateView(LoginRequiredMixin, SchemaBaseView, CreateView):
    template_name = "schemas/schema_create.html"


class SchemaUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, SchemaBaseView, UpdateView
):
    template_name = "schemas/schema_create.html"

    def test_func(self):
        schema = self.get_object()
        if schema.author == self.request.user:
            return True
        return False


class SchemaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Schema
    success_url = "/schemas/"

    def test_func(self):
        schema = self.get_object()
        if schema.author == self.request.user:
            return True
        return False

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class DatasetListView(LoginRequiredMixin, ListView):
    model = Dataset
    template_name = "schemas/dataset_list.html"
    context_object_name = "datasets"
    paginate_by = settings.PAGE_SIZE

    def get_queryset(self):
        return Dataset.objects.filter(schema__id=self.kwargs.get("pk")).order_by(
            "-created_at"
        )

    def post(self, request, *args, **kwargs):
        try:
            row_num = int(request.POST.get("row_num"))
        except ValueError:
            messages.error(request, "Invalid Credentials")
            return redirect("datasets")

        schema = Schema.objects.get(pk=self.kwargs.get("pk"))
        dataset = Dataset.objects.create(author=request.user, schema=schema)
        # save the object to be able check the status
        dataset.save()

        filename = f'{schema.title}_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.csv'
        generate_csv_file(filename, row_num, schema.id, dataset.id)

        return redirect("datasets", pk=self.kwargs.get("pk"))
