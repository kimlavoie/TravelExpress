from django.conf.urls import patterns, url

from main import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^connexion$', views.connexion, name='connexion'),
	url(r'^inscription$', views.inscription, name='inscription'),
	url(r'^publication$', views.publication, name='publication'),
	url(r'^annulation$', views.annulation, name='annulation'),
	url(r'^recherche$', views.recherche, name='recherche'),
	url(r'^deconnexion$', views.deconnexion, name='deconnexion'),
	url(r'^profil$', views.profil, name='profil'),
	url(r'^VoyageInscription$', views.VoyageInscription, name='VoyageInscription'),	
)
