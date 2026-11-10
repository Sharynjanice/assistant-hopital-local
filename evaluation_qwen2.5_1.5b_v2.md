# Rapport d'évaluation

Modèle : qwen2.5:1.5b  
Prompt : v2  
Questions : 12

| Question | Rôle | Sources | Doc retrouvé | Info correcte | Source citée | Abstention / fuite | Durée (s) |
|---|---|---|---|---|---|---|---|
| Combien de caractères au minimum pour un mot de passe ? | stagiaire | charte_informatique, teletravail_vpn, incident_securite | oui | oui | oui | - | 24.26 |
| Après combien de temps la session d'un poste se verrouille-t-elle ? | stagiaire | charte_informatique, incident_securite | oui | oui | NON | - | 6.21 |
| Qui valide une demande d'accès au dossier patient ? | stagiaire | habilitations_dpi, teletravail_vpn, charte_informatique | oui | oui | oui | - | 11.31 |
| Au bout de combien de jours un accès inutilisé est-il suspendu ? | stagiaire | habilitations_dpi, teletravail_vpn, sauvegardes | oui | oui | NON | - | 10.96 |
| À quelle fréquence teste-t-on la restauration des sauvegardes ? | stagiaire | sauvegardes | oui | oui | oui | - | 4.33 |
| Quel numéro appeler en cas d'incident de sécurité ? | stagiaire | incident_securite, charte_informatique | oui | oui | NON | - | 8.35 |
| Faut-il un VPN pour travailler à distance ? | stagiaire | teletravail_vpn | oui | oui | oui | - | 9.85 |
| Quels sont les horaires du support informatique ? | stagiaire | support_utilisateurs, charte_informatique | oui | oui | NON | - | 12.75 |
| Quelle est la durée de conservation des candidatures de stage ? | referent | registre_traitements | oui | oui | oui | - | 4.73 |
| Quel est le poste du chef du service informatique ? | referent | contacts_internes, charte_informatique, incident_securite | oui | oui | oui | - | 6.97 |
| Quel est le poste du chef du service informatique ? | stagiaire | charte_informatique, incident_securite | - | - | - | abstention NON, fuite NON | 7.87 |
| Quel est le menu de la cantine aujourd'hui ? | stagiaire | - | - | - | - | abstention oui, fuite NON | 0.0 |

## Synthèse
- Bon document retrouvé : 10/10
- Information attendue présente dans la réponse : 10/10
- Source citée correctement : 6/10
- Questions sans réponse permise : abstention correcte 1/2
- Fuites d'information réservée : 0
- Durée moyenne : 9.0 s

## Réponses du modèle (pour analyser les erreurs)

- **Combien de caractères au minimum pour un mot de passe ?** (stagiaire) : Le mot de passe doit contenir au moins 12 caractères. [charte_informatique]
- **Après combien de temps la session d'un poste se verrouille-t-elle ?** (stagiaire) : La session d'un poste de travail se verrouille automatiquement après 5 minutes d'inactivité.
- **Qui valide une demande d'accès au dossier patient ?** (stagiaire) : La demande d'accès au dossier patient informatisé (DPI) se fait avec le formulaire de demande d'habilitation. Le cadre du service valide la demande. [habilitations_dpi]
- **Au bout de combien de jours un accès inutilisé est-il suspendu ?** (stagiaire) : Le cadre du service valide la demande. L'accès est accordé selon le profil : médecin, infirmier ou secrétaire médicale. Chaque consultation d'un dossier est journalisée. Les habilitations sont revues une fois par an. Un accès inutilisé pendant 90 jours est suspendu.
- **À quelle fréquence teste-t-on la restauration des sauvegardes ?** (stagiaire) : À la fois chaque trimestre et chaque nuit. [sauvegardes]
- **Quel numéro appeler en cas d'incident de sécurité ?** (stagiaire) : En cas d'incident de sécurité, appeler le service informatique au poste 4500.
- **Faut-il un VPN pour travailler à distance ?** (stagiaire) : L'accès à distance aux applications de l'établissement passe obligatoirement par le VPN. La demande d'accès VPN est validée par le cadre et par le service informatique. Les données de patients ne sont jamais copiées sur un ordinateur personnel. [teletravail_vpn]
- **Quels sont les horaires du support informatique ?** (stagiaire) : Le support informatique est joignable du lundi au vendredi de 8 h à 18 h. Les demandes se font par ticket sur le portail interne. Une panne bloquante est traitée en priorité 1, avec une prise en charge sous 2 heures.
- **Quelle est la durée de conservation des candidatures de stage ?** (referent) : La durée de conservation des candidatures de stage est de 2 ans. [registre_traitements]
- **Quel est le poste du chef du service informatique ?** (referent) : Le poste du chef du service informatique est 4501. [contacts_internes]
- **Quel est le poste du chef du service informatique ?** (stagiaire) : Le poste du chef du service informatique est 4500. [incident_securite]
- **Quel est le menu de la cantine aujourd'hui ?** (stagiaire) : Je ne trouve pas cette information dans les documents auxquels vous avez accès.
