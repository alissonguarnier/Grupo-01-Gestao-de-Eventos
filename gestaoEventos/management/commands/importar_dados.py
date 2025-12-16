import csv
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from gestaoEventos.models import Evento, Atividade, Perfil, UserEventos

class Command(BaseCommand):
    help = 'Importa dados iniciais de arquivos CSV'

    def handle(self, *args, **kwargs):
        base_path = os.path.join(settings.BASE_DIR, 'data')
        self.stdout.write('Iniciando importação...')

        # -----------------------------------------------------------
        # 1. Importar Usuários
        # -----------------------------------------------------------
        caminho_users = os.path.join(base_path, 'usuarios.csv')
        if os.path.exists(caminho_users):
            with open(caminho_users, encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) < 6: continue # Pula linhas incompletas
                    username, password, email, nome, tipo, celular = row
                    
                    # se eu quero criar apenas os que não tem no banco:

                    '''if not User.objects.filter(username=username).exists():
                        user = User.objects.create_user(username=username, email=email, password=password)
                        user.first_name = nome.split()[0]
                        user.save()
                        Perfil.objects.create(user=user, tipo=tipo, celular=celular)
                        self.stdout.write(self.style.SUCCESS(f'Usuário criado: {username}'))'''

                    # Se quero verificar se teve auteração para apenas modificar:

                    # --- INÍCIO DA VERIFICAÇÃO ---
                    
                    # 1. Busca ou Cria o Usuário
                    # O 'defaults' serve para preencher o email apenas se for criar um novo
                    user, created_user = User.objects.get_or_create(
                        username=username,
                        defaults={'email': email}
                    )

                    # Se acabou de ser criado, define a senha e o nome
                    if created_user:
                        user.set_password(password)
                        user.first_name = nome.split()[0]
                        user.save()

                    # 2. Busca ou Cria o Perfil ligado a esse usuário
                    # (Note que não passamos 'defaults' aqui, pois queremos atualizar os dados abaixo sempre)
                    perfil, created_perfil = Perfil.objects.get_or_create(user=user)

                    # 3. Atualiza os dados do perfil (Tipo e Celular)
                    # Isso garante que se você mudou o tipo no CSV, ele atualiza no banco
                    perfil.tipo = tipo
                    perfil.celular = celular
                    
                    # 4. Salva o Perfil
                    # AO CHAMAR O SAVE AQUI, SUA LÓGICA DE GRUPOS NO MODELS.PY SERÁ EXECUTADA
                    perfil.save()

                    if created_user:
                        self.stdout.write(self.style.SUCCESS(f'Usuário criado: {username}'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'Usuário atualizado: {username}'))
                    
                    # --- FIM DA MUDANÇA ---                    


        else:
            self.stdout.write(self.style.WARNING('Arquivo usuarios.csv não encontrado.'))


        # -----------------------------------------------------------
        # 2. Importar Eventos
        # -----------------------------------------------------------
        caminho_eventos = os.path.join(base_path, 'eventos.csv')
        if os.path.exists(caminho_eventos):
            with open(caminho_eventos, encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) < 5: continue
                    nome, desc, inicio, fim, local = row
                    
                    if not Evento.objects.filter(nome=nome).exists():
                        Evento.objects.create(
                            nome=nome, descricao=desc, data_inicio=inicio, 
                            data_fim=fim, local=local
                        )
                        self.stdout.write(self.style.SUCCESS(f'Evento criado: {nome}'))
        else:
            self.stdout.write(self.style.WARNING('Arquivo eventos.csv não encontrado.'))


        # -----------------------------------------------------------
        # 3. Importar Atividades
        # -----------------------------------------------------------
        caminho_atividades = os.path.join(base_path, 'atividades.csv')
        if os.path.exists(caminho_atividades):
            with open(caminho_atividades, encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) < 7: continue
                    titulo, desc, h_inicio, h_fim, tipo, nome_evento, username_resp = row
                    
                    try:
                        evento = Evento.objects.get(nome=nome_evento)
                        responsavel = User.objects.get(username=username_resp)
                        
                        Atividade.objects.get_or_create(
                            titulo=titulo,
                            defaults={
                                'descricao': desc, 'horario_inicio': h_inicio,
                                'horario_fim': h_fim, 'tipo': tipo,
                                'evento': evento, 'responsavel': responsavel
                            }
                        )
                        self.stdout.write(self.style.SUCCESS(f'Atividade criada: {titulo}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Erro na atividade {titulo}: {e}'))


        # -----------------------------------------------------------
        # 4. Importar Inscrições (UserEventos) 
        # -----------------------------------------------------------
        caminho_inscricoes = os.path.join(base_path, 'inscricoes.csv')
        if os.path.exists(caminho_inscricoes):
            with open(caminho_inscricoes, encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) < 3: continue
                    username_user, nome_evento, status = row
                    
                    try:
                        user = User.objects.get(username=username_user)
                        evento = Evento.objects.get(nome=nome_evento)
                        
                        # get_or_create evita duplicidade se rodar o script 2 vezes
                        inscricao, created = UserEventos.objects.get_or_create(
                            user=user,
                            evento=evento,
                            defaults={'status': status}
                        )
                        if created:
                            self.stdout.write(self.style.SUCCESS(f'Inscrição criada: {username_user} em {nome_evento}'))
                        else:
                            self.stdout.write(f'Inscrição já existia: {username_user}')
                            
                    except User.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f'Usuário não achado para inscrição: {username_user}'))
                    except Evento.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f'Evento não achado para inscrição: {nome_evento}'))
        else:
            self.stdout.write(self.style.WARNING('Arquivo inscricoes.csv não encontrado (opcional).'))