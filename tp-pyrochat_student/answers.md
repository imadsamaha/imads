*Prise en main :* 
*1) comment s'appelle cette topology?*
client serveur 

*2) que remarquez vous dans les logs?*
dans les logs on peut voir tous les messages qui etaient envoyer par les personnes qui sont connecter au serveur

*3) pourquoi est-ce un probleme et quel principe cela violet-il?*
cela viole le principe de Kerckhoffs qui exprime que la securite d'un cryptosysteme ne doit reposer que sur le secret de la clef

*4)quelle solution la plus simple pouvez-vous mettre en place pour eviter cela? detaillez votre reponse*
pour eviter ce probleme on peut consister a utiliser des chiffrements ou des mutex pour synchroniser les acces au resource partagees.

*chiffrement*
*1) Est ce que urandom est un bon choix pour de la cryptographie ? Pourquoi ?*
La fonction urandom fournie par le module os en Python est considérée comme une source d'entropie puissante et de haute qualité pour générer des nombres aléatoires. Il utilise généralement une source d'entropie du système d'exploitation, telle que /dev/urandom sur les systèmes UNIX, pour fournir un nombre aléatoire cryptographique. Mais il est recommande d'utiliser la bibliotheque Cryptographie pour plus de securite.

2)Pourquoi utiliser ses primitives cryptographiques peut être dangereux ?
Les primitives cryptographiques sont des outils essentiels pour protéger les informations confidentielles et assurer la sécurité des communications en ligne. Cependant, leur utilisation peut être dangereuse dans certaines situations: mauvaise mise en oeuvre ce qui peut entraîner des vulnérabilités et des faiblesses de sécurité. 
Clés faibles, nos clés doivent être suffisamment longues et complexes pour empêcher les attaquants. 

*3) Pourquoi malgré le chiffrement un serveur malveillant peut il nous nuire encore ?*
Malgre que le chiffrement des données peut aider à protéger leur confidentialité pendant leur transmission, il ne garantit pas nécessairement une protection totale contre les attaques malveillantes.

*4)Quelle propriété manque t-il ici ?*
il manque ici la propriete d'integration.

*Authenticated Symetric Encryption*
*1)Pourquoi Fernet est moins risqué que le précédent chapitre en terme d'implémentation ?*
Fernet est une bibliothèque cryptographique dédiée au chiffrement symétrique et à l'authentification. Il est donc plus sûr à utiliser que les primitives cryptographiques de base comme HMAC. il protege les donnees en transit et pendant qu'elles sont stockees dans les serveurs.

*2)Un serveur malveillant peut néanmoins attaqué avec des faux messages, déjà utilisé dans le
passé. Comment appel t-on cette attaque ?*
L'attaque s'appelle une attaque de rejeu "replay attack". Elle se produit lorsqu'un attaquant intercepte un message chiffré envoyé par le client au serveur, puis le rejoue plus tard dans le temps pour obtenir un accès non autorisé ou d'autres avantages.

*3)Quelle méthode simple permet de s'en affranchir?*
La méthode la plus simple est d'utiliser des numéros de séquence pour chaque message envoyé. Les numéros de séquence sont des nombres uniques qui sont générés pour chaque message et qui sont utilisés pour s'assurer que le même message ne peut pas être rejoué plusieurs fois.

*TTL*
*1). Remarquez vous une différence avec le chapitre précédent ?*
oui, le temps des messages est limitee alors les messages qui on une duree de vie plus longue ne seront pas pris en compte lors du decodage.

*2)Maintenant soustrayez 45 au temps lors de l'émission. Que se passe t-il et pourquoi ?*
le message est considere invalide, cela est du car l'ecart maximal est 30secondes.

*3)Est-ce efficace pour se protéger de l'attaque du précédent chapitre ?*
TTL est une protection efficace contre les attaques rejeu car tous les messages envoyés par le client contiennent une horloge interne initialisée a un certain nombre de secondes. Le serveur doit verifier la réception du message dans un laps de temps limité avant que l'horloge n'atteigne zéro.

*4)Quelle(s) limite(s) cette solution peut rencontrer dans la pratique ?*
elle peut rencontrer plusieurs limites dans la pratique: il faut que les horloges des clients et du serveur soient synchronisées pour être efficace, elle peut etre vulnerable aux attaques de synchronisation malveillantes, elle ne protege pas contre les attaques de rejeu qui ont lieu dans des delais tres courtes.

*Regard critique*
Le problème décrit dans le code pourrait être une faille de sécurité majeure car il permet à un attaquant de fournir des données malveillantes. Celles-ci peuvent être acceptées par le serveur et traitées comme des données legitimes. on peut ajouter un systeme d'authentification et un header dans les messages pour limiter ces problemes. le numero de sequences est inclus dans le message, mais il peut etre fournit separement lors de l'appel a la fonction de dechiffrement, comme ca le serveur peut verifier que le numero de sequence est unique et rejete l'autre message.




