## Réponses aux questions :

# Partie 1 : PRISE EN MAIN 

#Question 1
Cette topologie s'appelle topologie en étoile oi client serveur, avec le serveur qui en est le centre



# Question 2 

Dans les logs nous reamrquons que :

- Les messages envoyés par chaque utilisateur sont bien retransmis à l'autre utilisateur.

- Les utilisateurs s'enrégistrent bien auprès du serveur et que leur nom est ajouté à la liste des utilisateurs connectés.

- Les messages échangés entre les deux clients connectés sont écrit en clair dans les logs serveurs. Et chaque message reçu par les clients est aussi écrit en clair dans les logs.



# Question 3

Les problèmes sont :

1- Les callback handlers des utilisateurs n'ont pas été déconnectés du serveur même après la fin de la conversation => Cela viole le principe de la gestion des ressources. Si plusieurs (voir des dizaines ou centaines) utilisateurs enregistrent leur callback handler sans se déconnecter, le serveur risque de surcharger et crasher.

2- Les messsages sont enrégister en clair sur les logs, n'importe qui ayant accès aux logs peut voir le contenu des échanges entre les diférents clients connectés => Le principe de confidentialité des échanges est violé.



# Question 4

1- Pour eviter le premier problème, on peut ajouter un code qui déconnectera le callback handler de l'utilisateur après chaque session de chat. En effet si l'utilisateur ferme la fenêtre de chat, une méthode peut être appeler pour notifier le serveur de fermer la connexion et ainsi le serveur peut supprimer le callback handler de la liste des handlers connectés et liberer les ressources. Une autre solution serait d'ajouter un temps d'expiration pour les callback handlers et automatiquement les déconnecter du serveur après un temps déterminé.

2- Pour résoudre ce problème une solution serait de chiffrer les messages envoyés avant de les enrégiqter sur les logs. 
 


## Partie Chiffrement 

# Question 1  

Non, urandom n'est pas un bon choix pour de la cryptographie. 
Parce qu'il utilise un générateur de nombres pseudo-aléatoires pouvant être predit dans certaines circonstances

# Question 2 

Utiliser ses primitives cryptographiques peut être dangereux car l'utilisation des mauvaises primitives cryptographiques peut conduire à des failles de sécurité et à des attaques.


# Question 3

Un serveur malveillant peut encore nous nuire malgrè le chiffrement parce que l'authentification des utilisateurs n'est pas implémenté.. Si le serveur est compromis par exemple, on ne pourrait pas être sûr de communiquer avec la bonne personne ou le message pourrait être intercepté par un tiers et l'altérer.

# Question 4

La propriété qui manque c'est l'authentification de l'entité avec laquelle on communique.


## Authentificated Symetric Encryption 

# Question 1


# Question 2


# Question 3


# Question 4




## TTL

# Question 1

Oui, il y a une différence avec le chapitre précédent car ici nous utilisons la bibliothèque Fernet pour chiffrer et déchiffrer les messages avec l'addition d'un timestamp pour créer une validation temporelle.

# Question 2

Si on soustrait 45 au temps lors de l'émission, alors à la réception, la fonction decrypt_at_time soulèvera l'exception InvalidToken car le jeton aura expiré. Cela se produit car le temps utilisé lors du chiffrement sera plus petit que le temps utilisé lors du déchiffrement et le délai de TTL sera dépassé, donnant un erreur qui indique que le jeton est invalide/en retard.

# Question 3 

Cela peut être efficace pour protéger contre l'attaque précédente car la validation temporelle garantit que les messages ne peuvent pas être réutilisés après un certain délai. Cependant, cela ne protège pas contre toutes les attaques possibles.

# Question 4 

Cette solution peut rencontrer certaines limites dans la pratique, comme les problèmes de synchronisation des horloges entre les différents serveurs et clients. Si les horloges ne sont pas synchronisées correctement, cela peut conduire à des erreurs de validation temporelle. De plus, le délai de TTL fixe peut être contraignant dans des situations où les messages doivent être stockés pendant des périodes plus longues.