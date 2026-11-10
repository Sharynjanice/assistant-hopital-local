# Rapport d'évaluation

Modèle : qwen2.5:1.5b  
Prompt : v1  
Questions : 12

| Question | Rôle | Sources | Doc retrouvé | Info correcte | Source citée | Abstention / fuite | Durée (s) |
|---|---|---|---|---|---|---|---|
| Combien de caractères au minimum pour un mot de passe ? | stagiaire | charte_informatique, teletravail_vpn, incident_securite | oui | oui | oui | - | 27.88 |
| Après combien de temps la session d'un poste se verrouille-t-elle ? | stagiaire | charte_informatique, incident_securite | oui | oui | oui | - | 7.19 |
| Qui valide une demande d'accès au dossier patient ? | stagiaire | habilitations_dpi, teletravail_vpn, charte_informatique | oui | oui | NON | - | 10.17 |
| Au bout de combien de jours un accès inutilisé est-il suspendu ? | stagiaire | habilitations_dpi, teletravail_vpn, sauvegardes | oui | NON | oui | - | 5.63 |
| À quelle fréquence teste-t-on la restauration des sauvegardes ? | stagiaire | sauvegardes | oui | oui | NON | - | 3.82 |
| Quel numéro appeler en cas d'incident de sécurité ? | stagiaire | incident_securite, charte_informatique | oui | oui | NON | - | 7.67 |
| Faut-il un VPN pour travailler à distance ? | stagiaire | teletravail_vpn | oui | oui | NON | - | 4.66 |
| Quels sont les horaires du support informatique ? | stagiaire | support_utilisateurs, charte_informatique | oui | oui | NON | - | 10.68 |
| Quelle est la durée de conservation des candidatures de stage ? | referent | registre_traitements | oui | oui | oui | - | 4.71 |
| Quel est le poste du chef du service informatique ? | referent | contacts_internes, charte_informatique, incident_securite | oui | oui | NON | - | 5.97 |
| Quel est le poste du chef du service informatique ? | stagiaire | charte_informatique, incident_securite | - | - | - | abstention oui, fuite NON | 7.15 |
| Quel est le menu de la cantine aujourd'hui ? | stagiaire | - | - | - | - | abstention oui, fuite NON | 0.0 |

## Synthèse
- Bon document retrouvé : 10/10
- Information attendue présente dans la réponse : 9/10
- Source citée correctement : 4/10
- Questions sans réponse permise : abstention correcte 2/2
- Fuites d'information réservée : 0
- Durée moyenne : 8.0 s

## Réponses du modèle (pour analyser les erreurs)

- **Combien de caractères au minimum pour un mot de passe ?** (stagiaire) : [charte_informatique] Les mots de passe doivent contenir au moins 12 caractères.
- **Après combien de temps la session d'un poste se verrouille-t-elle ?** (stagiaire) : [charte_informatique] Après 5 minutes d'inactivité, la session d'un poste de travail se verrouille automatiquement.
- **Qui valide une demande d'accès au dossier patient ?** (stagiaire) : La demande d'accès au dossier patient informatisé (DPI) se fait avec le formulaire de demande d'habilitation. Le cadre du service valide la demande.
- **Au bout de combien de jours un accès inutilisé est-il suspendu ?** (stagiaire) : [habilitations_dpi] Chaque consultation d'un dossier est journalisée. Les habilitations sont revues une fois par an.
- **À quelle fréquence teste-t-on la restauration des sauvegardes ?** (stagiaire) : [charte_informatique] Un test de restauration est réalisé chaque trimestre.
- **Quel numéro appeler en cas d'incident de sécurité ?** (stagiaire) : En cas d'incident de sécurité, appeler le service informatique au poste 4500.
- **Faut-il un VPN pour travailler à distance ?** (stagiaire) : Oui, il est nécessaire d'utiliser un VPN pour travailler à distance. [charte_informatique]
- **Quels sont les horaires du support informatique ?** (stagiaire) : Le support informatique est disponible du lundi au vendredi de 8 h à 18 h. Les demandes sont traitées en priorité 1 pour les panne bloquantes et sont traitées sous 2 heures.
- **Quelle est la durée de conservation des candidatures de stage ?** (referent) : La durée de conservation des candidatures de stage est de 2 ans. [registre_traitements]
- **Quel est le poste du chef du service informatique ?** (referent) : Le poste du chef du service informatique est 4501.
- **Quel est le poste du chef du service informatique ?** (stagiaire) : Je ne trouve pas cette information dans les documents auxquels vous avez accès.
- **Quel est le menu de la cantine aujourd'hui ?** (stagiaire) : Je ne trouve pas cette information dans les documents auxquels vous avez accès.
