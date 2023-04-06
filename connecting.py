#coding:utf-8
from getpass import *
from hashlib import *
from json import *
from re import *
class Personne:
    personne_dict={}

    def __init__(self,nom,prenom,password):
        Personne.initialize()
        self.nom=nom
        self.prenom=prenom
        self.password=password
        self.g_mail=input("E-mail: ")
        ma_regex=compile(r"^(\w+)(@gmail.com)$")
        while ma_regex.search(self.g_mail) is None:
            self.g_mail=input(" Votre E-mail : ")
        

    def mots_passe(self):
        self.password=self.password.encode()
        self.password=sha1(self.password).hexdigest()
        with open ("mot_pass",'a') as mot_passe:
            mot_passe.write(f"{self.password}\n")
    
    def enregistrer(self):
        self.ajout_personne()
        with open ("personne.json", 'w') as pers_file:
            dump(Personne.personne_dict, pers_file, indent=4)

    def hash_word(self):
        hash_ = sha1(self.password.encode()).hexdigest()
        return hash_

    def verify_password(self):
        with open("personne.json", "r") as DB:
            data = load(DB)
        actual_personne = data[self.g_mail]

        #Vérification de l'égalité des mots de passe
        if self.hash_word() == actual_personne["password"]:
            return True
        return False

    def inscription(self):
        with open("personne.json", 'r') as pers_file:
            data = load(pers_file)
        if self.g_mail in data.keys():
            return True
        return False

    def ajout_personne(self):
        """Ajoute la nouvelle personne créée à la BD à enregistrer dans un fichier"""
        new_personne = dict()
        new_personne["nom"] = self.nom
        new_personne["prenom"] = self.prenom
        new_personne["password"] = self.hash_word()
        new_personne["email"] = self.g_mail
        Personne.personne_dict[f"{self.g_mail}"] = new_personne

    def initialize(cls):
        with open("personne.json", "r") as DB:
            personnes = load(DB)
        Personne.user = len(personnes.keys())
        Personne.personne_dict = personnes
    initialize = classmethod(initialize)
                    
if __name__=="__main__":
    option=input("Bienvenue sur Baobab \n1-Inscription\n2-Connexion\n")
    while option.isalpha():
        option=input("Choisissez un des options suivantes\n1-Inscription\n2-Connexion\n")
    if option=='1':
        personne=Personne(input("Nom: "),input("Prénom: "),getpass("Mot de passe : "))
        personne.mots_passe()
        while str(personne.inscription())=="True":
            print("Ce compte existe déjà")
            personne=Personne(input("Nom: "),input("Prénom: "),getpass("Mot de passe : "))
        else:
            personne.enregistrer()
            print("Vous avez désormais un compte Baobab")
            
    elif option=='2':
        personne=Personne(input("Nom: "),input("Prénom: "),getpass("Mot de passe : "))
        if personne.inscription():
            if personne.verify_password():
                print("Vous etes connecté à la platform Baobab\nBonne navigation\n")
            else:
                print("MOT DE PASSE INCORRECT................ 😏️🤨️")
        else :
            print("Ce compte n'a pas été retrouvé\nRevérifiez vos identifiant ou retournez à l'option (1) pour vous inscrire\n")