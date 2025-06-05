from django.core.cache import cache
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import FormView, ListView

from .exceptions import ExelParsingError
from .forms import UploadExelForm
from .models import Album, Customer, Object
from .utils import AlbumExelParser, AlbumDataCreator


class UploadExelView(FormView):
    template_name = 'orders/upload_file.html'
    form_class = UploadExelForm

    def form_valid(self, _):
        try:
            exel_parser = AlbumExelParser(self.request.FILES['file'])
            albums_creator = AlbumDataCreator(exel_parser.get_data_from_file())
            created_records_num = albums_creator.create_albums()
            return JsonResponse(
                {
                    'message': 'Файл успешно обработан',
                    'total_records': created_records_num,
                }, status=201
            )
        except ExelParsingError:
            return JsonResponse(
                    {
                        'message': 'Неверно заполнены ячейки в файле',
                        'errors': exel_parser.errors,
                    }, status=400
                )
        except Exception:
            return JsonResponse(
                {
                    'error': 'Попробуйте позже'
                }, status=500
            )

    def form_invalid(self, form):
        return JsonResponse(
            {
                'validation_error': True,
                'error': next(iter(form.errors.items()))[1]
            }, status=400
        )


class AlbumListView(ListView):
    model = Album
    template_name = 'orders/albums_list.html'
    context_object_name = 'albums'
    paginate_by = 10
    ordering = ['-id']

    def get_queryset(self):
        queryset = super().get_queryset().select_related('customer', 'obj')

        if customer_id := self.request.GET.get('customer_id'):
            queryset = queryset.filter(customer_id=customer_id)

        if doc_type := self.request.GET.get('doc_type'):
            queryset = queryset.filter(doc_type=doc_type)

        if object_id := self.request.GET.get('object_id'):
            queryset = queryset.filter(obj_id=object_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = cache.get_or_set(
            'all_customers', lambda: Customer.objects.all(), 300
        )
        context['objects'] = cache.get_or_set(
            'all_objects', lambda: Object.objects.all(), 300
        )
        context['current_customer'] = self.request.GET.get('customer_id', '')
        context['current_doc_type'] = self.request.GET.get('doc_type', '')
        context['current_object'] = self.request.GET.get('object_id', '')

        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            page_obj = self.get_paginator(
                self.get_queryset(), self.paginate_by
            ).page(self.request.GET.get('page', 1))
            table_rows = render_to_string(
                'includes/albums_rows.html', {'page_obj': page_obj}
            )
            pagination = render_to_string(
                'includes/albums_pagination.html', {'page_obj': page_obj}
            )
            return JsonResponse({
                'table_rows': table_rows,
                'pagination': pagination,
                'page': page_obj.number
            })
        return super().render_to_response(context, **response_kwargs)
