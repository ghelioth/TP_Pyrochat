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
 
