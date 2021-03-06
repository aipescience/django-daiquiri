from django.db import models


class Schema(models.Model):

    schema_name = models.CharField(max_length=256)
    utype = models.CharField(max_length=256, null=True, blank=True)
    description = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        db_table = 'schemas'

    def __str__(self):
        return self.schema_name


class Table(models.Model):

    schema = models.ForeignKey(Schema, related_name='tables', on_delete=models.CASCADE)

    schema_name = models.CharField(max_length=256)
    table_name = models.CharField(max_length=256)
    table_type = models.CharField(max_length=256)
    utype = models.CharField(max_length=256, null=True, blank=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    table_index = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'tables'

    def __str__(self):
        return '%s.%s' % (self.schema_name, self.table_name)


class Column(models.Model):

    table = models.ForeignKey(Table, related_name='columns', on_delete=models.CASCADE)

    table_name = models.CharField(max_length=256)
    column_name = models.CharField(max_length=256)
    datatype = models.CharField(max_length=256)
    arraysize = models.IntegerField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    utype = models.CharField(max_length=256, null=True, blank=True)
    unit = models.CharField(max_length=256, null=True, blank=True)
    ucd = models.CharField(max_length=256, null=True, blank=True)
    principal = models.BooleanField(default=False)
    indexed = models.BooleanField(default=False)
    std = models.BooleanField(default=False)
    column_index = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'columns'

    def __str__(self):
        return '%s.%s' % (self.table_name, self.column_name)
