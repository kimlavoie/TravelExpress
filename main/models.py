from django.db import models
from django.contrib.auth import models as auth_models
from django.forms import ModelForm
from django import forms

# Create your models here.
class Usager(auth_models.User):
	telephone = models.CharField(max_length=12, blank=True)	
	conducteur = models.BooleanField(default=False)
	restrictions = models.TextField(default="")
	annulations = models.IntegerField(default=0)
	exclu = models.BooleanField(default=False)

class Voyage(models.Model):
	conducteur = models.ForeignKey(Usager,related_name='voyage_conducteur')
	source = models.CharField(max_length=200)
	destination = models.CharField(max_length=200)
	places_disponibles = models.IntegerField()
	date_depart = models.DateTimeField()
	prix = models.IntegerField()
	informations_supplementaires = models.TextField()
	passagers = models.ManyToManyField(Usager, related_name='voyage_passagers')

class InscriptionForm(ModelForm):
	class Meta:
		model = Usager
		fields = ['username', 'password', 'email', 'first_name', 'last_name', 'telephone', 'conducteur', 'restrictions']

class ConnexionForm(ModelForm):
	class Meta:
		model = Usager
		fields = ['username', 'password']

class VoyageForm(ModelForm):
	date_depart = forms.DateTimeField()
	class Meta:
		model = Voyage
		fields = ['source', 'destination', 'places_disponibles', 'prix', 'informations_supplementaires']
