from django import template
from django.utils import timezone
from django.db.models import Count
from gestaoEventos.models import Evento, UserEventos, Atividade
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
def get_dashboard_stats():
    # 1. Totais Gerais
    total_eventos = Evento.objects.count()
    total_inscricoes = UserEventos.objects.filter(status='C').count() # Apenas confirmados
    total_usuarios = User.objects.count()
    
    # 2. Próximos 5 Eventos (para listar)
    proximos_eventos = Evento.objects.filter(
        data_inicio__gte=timezone.now()
    ).order_by('data_inicio')[:5]

    # 3. Dados para o Gráfico (Top 5 Eventos com mais inscritos)
    # Retorna o nome do evento e a quantidade de inscritos
    eventos_populares = Evento.objects.annotate(
        num_inscritos=Count('usereventos')
    ).order_by('-num_inscritos')[:5]

    nomes_grafico = [e.nome for e in eventos_populares]
    dados_grafico = [e.num_inscritos for e in eventos_populares]

    return {
        'total_eventos': total_eventos,
        'total_inscricoes': total_inscricoes,
        'total_usuarios': total_usuarios,
        'proximos_eventos': proximos_eventos,
        'chart_labels': nomes_grafico,
        'chart_data': dados_grafico,
    }