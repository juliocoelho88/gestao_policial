from django.db.models import Sum, F, ExpressionWrapper, IntegerField
from django.shortcuts import render

from .models import Producao

def ranking_view(request):
    pesos = Producao.pesos_pontuacao()
    annotations = {}

    for campo, peso in pesos.items():
        annotations[f'{campo}_pts'] = ExpressionWrapper(
            F(campo) * peso,
            output_field=IntegerField()
        )

    qs = Producao.objects.values(
        'policial__nome_guerra',
        'policial__re',
        'policial__pelotao',
    ).annotate(**annotations)

    # Calcular soma total dos pontos por policial
    qs = qs.annotate(
        total_pontuacao=Sum(
            sum(annotations.keys())
        )
    ).order_by('-total_pontuacao')[:10]

    return render(request, 'ranking.html', {'ranking': qs})
