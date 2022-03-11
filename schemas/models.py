from django.contrib.auth.models import User
from django.db import models


class Schema(models.Model):
    COMMA = ","
    SEMICOLON = ";"
    PIPE = "|"
    SINGLE_QUOTE = "'"
    DOUBLE_QUOTE = '"'

    COLUMN_SEPARATORS = (
        (COMMA, "Comma (,)"),
        (SEMICOLON, "Semicolon (;)"),
        (PIPE, "Pipe (|)"),
    )
    STRING_CHARACTERS = (
        (SINGLE_QUOTE, "Single-quote (')"),
        (DOUBLE_QUOTE, 'Double-quote (")'),
    )

    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_schemas"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    column_separator = models.CharField(
        max_length=1, choices=COLUMN_SEPARATORS, default=COMMA
    )
    string_character = models.CharField(
        max_length=1, choices=STRING_CHARACTERS, default=SINGLE_QUOTE
    )

    def __str__(self):
        return f'Schema "{self.title}"'


class Column(models.Model):
    FULL_NAME = "Full name"
    EMAIL = "Email"
    JOB = "Job"
    COMPANY = "Company"
    INTEGER = "Integer"

    COLUMN_TYPES = (
        (FULL_NAME, "Full name"),
        (EMAIL, "Email"),
        (JOB, "Job"),
        (COMPANY, "Company"),
        (INTEGER, "Integer"),
    )

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=9, choices=COLUMN_TYPES, default=FULL_NAME)
    start_value = models.IntegerField(blank=True, null=True)
    end_value = models.IntegerField(blank=True, null=True)
    order = models.PositiveIntegerField()
    schema = models.ForeignKey(
        Schema, on_delete=models.CASCADE, related_name="schema_columns"
    )

    def __str__(self):
        return f"Column {self.name}, schema {self.schema.title}"


class Dataset(models.Model):
    READY = "Ready"
    PROCESSING = "Processing"

    STATUS = ((READY, "Ready"), (PROCESSING, "Processing"))

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_datasets"
    )
    schema = models.ForeignKey(
        Schema, on_delete=models.CASCADE, related_name="schema_datasets"
    )
    status = models.CharField(max_length=10, choices=STATUS, default=PROCESSING)
    created_at = models.DateTimeField(auto_now_add=True)
    csv_file = models.FileField(upload_to="csv_files/", blank=True, null=True)

    def __str__(self):
        return f'Dataset for schema "{self.schema.title}"'

    def delete(self, *args, **kwargs):
        self.csv_file.delete(save=False)
        super().delete(*args, **kwargs)
