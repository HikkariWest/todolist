import django_filters
from django_filters import DateFilter
from .models import Todo

class TodoFilter(django_filters.FilterSet):
	# start_date = DateFilter(field_name="date_created", lookup_expr = 'gte')
	# end_date = DateFilter(field_name="date_created", lookup_expr = 'lte')

	class Meta:
		model = Todo
		fields = [
			'name',
			'description',
			'category',
			'interest',
			]
		exсlude = ['name', 'date_created']