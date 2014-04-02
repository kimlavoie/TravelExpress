from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth import logout, login, authenticate
from models import *

# Create your views here.
def index(request):
	if request.user.is_authenticated():
		template = loader.get_template("index.html")
		context = RequestContext(request, {})
		return HttpResponse(template.render(context))
	else:
		return redirect('connexion')

def inscription(request):
	if request.method == "POST":
		username = request.POST['username']
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		password = request.POST['password']
		telephone = request.POST['telephone']
		conducteur = False
		if request.POST.get('conducteur'):
			conducteur = True
		restrictions = request.POST['restrictions']
		user = Usager.objects.create_user(username,email,password)
		user = Usager.objects.get(username=username)
		user.first_name = first_name
		user.last_name = last_name
		user.telephone = telephone
		user.conducteur = conducteur
		user.restrictions = restrictions
		user.save()
		return redirect("connexion")
	else:
		template = loader.get_template("inscription.html")
		form = InscriptionForm()
		context = RequestContext(request, {'form':form})
		return HttpResponse(template.render(context))

def connexion(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				return redirect('index')
			else:
				return HttpResponse("Your account has been disabled")
		else:
			return HttpResponse("Invalid account. <a href='connexion'>Get back to connexion page</a>.")
	else:
		template = loader.get_template("connexion.html")
		form = ConnexionForm() 
		context = RequestContext(request,{'form':form})
		return HttpResponse(template.render(context))

def profil(request):
	if request.user.is_authenticated():
		template = loader.get_template("profil.html")
		usager = Usager.objects.get(username=request.user.username)
		context = RequestContext(request,{'usager':usager})
		return HttpResponse(template.render(context))
	else:
		return HttpResponse("Impossible d'afficher votre profil")

def publication(request):
	if request.user.is_authenticated():
		usager = Usager.objects.get(username=request.user.username)
		if request.method == "POST":
			voyage = Voyage()
			voyage.conducteur = usager
			voyage.source = request.POST['source']
			voyage.destination = request.POST['destination']
			voyage.places_disponibles = request.POST['places_disponibles']
			voyage.date_depart = request.POST['date_depart']
			voyage.prix = request.POST['prix']
			voyage.informations_supplementaires = request.POST['informations_supplementaires']
			voyage.save()
			return HttpResponse('Publication enregistree. <a href="/">Retourner au menu principal</a>')
		if usager and usager.conducteur:
			template = loader.get_template("publication.html")
			form = VoyageForm()
			context = RequestContext(request, {'form':form})
			return HttpResponse(template.render(context))
	return HttpResponse("Vous ne pouvez pas publier")

def recherche(request):
	if request.user.is_authenticated():
		query_results = Voyage.objects.all()
		if request.method == "POST":
			source = request.POST['source']
			destination = request.POST['destination']
			prix = request.POST['prix']
			if source:
				query_results = query_results.filter(source=request.POST['source'])
			if destination:
				query_results = query_results.filter(destination=request.POST['destination'])
			if prix:
				query_results = query_results.filter(prix__lte=prix)
		template = loader.get_template("recherche.html")
		usager = Usager.objects.get(id=request.user.id)
		exclu = usager.exclu
		context = RequestContext(request,{'query_results':query_results, 'exclu':exclu})
		return HttpResponse(template.render(context))
	return HttpResponse("Vous ne pouvez pas rechercher")

def VoyageInscription(request):
	if request.user.is_authenticated():
		if request.method == "POST":
			template = loader.get_template("VoyageInscription.html")
			context = RequestContext(request, {})
			id = request.GET['id']
			voyage = Voyage.objects.get(id=id)
			if voyage:
				id = request.user.id
				usager = Usager.objects.get(id=id)
				if voyage.passagers.filter(id=id):
					return HttpResponse("Vous etes deja enregistre pour ce voyage")
				if voyage.places_disponibles <= 0:
					return HttpResponse("Il n'y a plus de place dans la voiture")
				voyage.places_disponibles = int(voyage.places_disponibles) - 1
				voyage.passagers.add(usager)
				voyage.save()
				return HttpResponse(template.render(context))
			else:
				return HttpResponse("Erreur dans la reservation")
	return HttpResponse("Place non reservee")

def annulation(request):
	if request.user.is_authenticated():
		if request.method == "POST":
			id = request.GET['id']
			voyage = Voyage.objects.get(id=id)
			id = request.user.id
			usager = Usager.objects.get(id=id)
			voyage.passagers.remove(usager)
			voyage.places_disponibles = voyage.places_disponibles + 1
			usager.annulations = usager.annulations + 1
			if usager.annulations > 3:
				usager.exclu = True
			usager.save()
			voyage.save()
			return HttpResponse('Voyage annule avec succes. <a href="/">Retour au menu principal</a>')
		else:
			voyages = []
			for voyage in Voyage.objects.all():
				for passager in voyage.passagers.all():
					if passager.id == request.user.id:
						voyages.append(voyage)
			template = loader.get_template("annulation.html") 
			context = RequestContext(request,{"voyages":voyages})
			return HttpResponse(template.render(context))
	return HttpResponse("Vous ne pouvez pas annuler de voyage")

def deconnexion(request):
	if request.user.is_authenticated():
		logout(request)	
	return redirect('/')
