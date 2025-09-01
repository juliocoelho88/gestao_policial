from django.db import models


class Policial(models.Model):
    graduacao = models.CharField(max_length=5)
    re = models.CharField(max_length=8, unique=True)
    nome_guerra = models.CharField(max_length=200)
    pelotao = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.graduacao} {self.nome_guerra}"

    class Meta:
        verbose_name = "Policial"
        verbose_name_plural = "👮 Cadastro de Policiais"


class Producao(models.Model):
    policial = models.ForeignKey(Policial, on_delete=models.CASCADE)
    data = models.DateField()

    # BLOCO A: GERAL
    pessoa = models.IntegerField(default=0)
    carros = models.IntegerField(default=0)
    motos = models.IntegerField(default=0)

    # BLOCO B: AISP (novos campos)
    pessoas_aisp = models.IntegerField(default=0)
    carros_aisp = models.IntegerField(default=0)
    motos_aisp = models.IntegerField(default=0)

    # BLOCO C: AÇÕES
    qnt_ocorrencias = models.IntegerField(default=0)
    flagrantes = models.IntegerField(default=0)
    flagrantes_aisp = models.IntegerField(default=0)  # novo campo
    autuacoes = models.IntegerField(default=0)
    raia = models.IntegerField(default=0)
    procurado = models.IntegerField(default=0)

    # BLOCO D: RESULTADOS
    carro_apreendido = models.IntegerField(default=0)
    moto_apreendida = models.IntegerField(default=0)
    flagrantes_outros = models.IntegerField(default=0)
    arma = models.IntegerField(default=0)
    escolas = models.IntegerField(default=0)

    observacao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.policial.nome_guerra} - {self.data}"

    @staticmethod
    def pesos_pontuacao():
        return {
            'pessoa': 0.01,
            'pessoas_aisp': 0.1,
            'carros': 0.01,
            'carros_aisp': 0.1,
            'motos': 0.01,
            'motos_aisp': 0.1,
            'qnt_ocorrencias': 0.01,
            'flagrantes': 2,
            'flagrantes_aisp': 3,
            'autuacoes': 0.05,
            'raia': 0.05,
            'procurado': 1,
            'carro_apreendido': 0.2,
            'moto_apreendida': 0.2,
            'flagrantes_outros': 0.5,
            'arma': 1,
            'escolas': 0.01,
        }

    @property
    def pontuacao(self):
        pesos = self.pesos_pontuacao()
        return sum(getattr(self, campo) * peso for campo, peso in pesos.items())

    class Meta:
        verbose_name = "Produção"
        verbose_name_plural = "➕ Cadastrar Produção"


from django.db import models

class Formacao(models.Model):
    TIPO_CHOICES = [
        ('curso', 'Curso'),
        ('estagio', 'Estágio'),
    ]

    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    local = models.CharField(max_length=100)
    data_inicio = models.DateField()
    data_fim = models.DateField()

    def __str__(self):
        return f"{self.nome} - {self.data_inicio.strftime('%d/%m/%Y')}"


class Participacao(models.Model):
    policial = models.ForeignKey('Policial', on_delete=models.CASCADE)
    formacao = models.ForeignKey(Formacao, on_delete=models.CASCADE)
    presente = models.BooleanField(default=True)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('policial', 'formacao')

    def __str__(self):
        return f"{self.policial.nome_guerra} - {self.formacao.nome}"


