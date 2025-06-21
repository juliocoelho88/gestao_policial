from django.db import models


class Policial(models.Model):
    graduacao = models.CharField(max_length=5)
    re = models.CharField(max_length=8, unique=True)
    nome_guerra = models.CharField(max_length=200)
    pelotao = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.graduacao} {self.nome_guerra}"


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

    @property
    def pontuacao(self):
        return (
                self.pessoa * 1 +
                self.pessoas_aisp * 5 +
                self.carros * 1 +
                self.carros_aisp * 5 +
                self.motos * 1 +
                self.motos_aisp * 5 +
                self.qnt_ocorrencias * 3 +
                self.flagrantes * 4 +
                self.flagrantes_aisp * 8 +
                self.autuacoes * 2 +
                self.raia * 1 +
                self.procurado * 10 +
                self.carro_apreendido * 6 +
                self.moto_apreendida * 6 +
                self.flagrantes_outros * 4 +
                self.arma * 10 +
                self.escolas * 2
        )

