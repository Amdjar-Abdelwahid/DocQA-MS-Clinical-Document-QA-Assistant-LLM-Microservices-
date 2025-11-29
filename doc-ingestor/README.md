# DocIngestor Service

Service de microservice pour l'ingestion et le traitement de documents cliniques dans l'architecture DocQA.

## Description

DocIngestor est un service API REST qui permet de :
- Ingérer et valider les documents
- Traiter et préparer les documents pour l'analyse
- Gérer la communication asynchrone avec RabbitMQ
- Stocker les documents dans la base de données

## Prérequis

- Python 3.8+
- Docker et Docker Compose
- RabbitMQ
- PostgreSQL (ou autre base de données configurée)

## Installation et Démarrage

### 1. Préparer les conteneurs Docker
```bash
docker-compose up -d
```

### 2. Créer et activer l'environnement virtuel

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Démarrer le serveur
```bash
uvicorn main:app --reload
```

## Accès aux Services

- **API Documentation** : http://127.0.0.1:8000/docs
- **API Interactive** : http://127.0.0.1:8000/redoc
- **RabbitMQ Management** : http://localhost:15672
  - Credentials : guest / guest

## Structure du Projet

- `main.py` : Point d'entrée de l'application
- `models.py` : Modèles de données
- `database.py` : Configuration et connexion à la base de données
- `processing.py` : Logique de traitement des documents
- `requirements.txt` : Dépendances Python
- `docker-compose.yml` : Configuration des services Docker

## Architecture

Le service utilise :
- **FastAPI** : Framework web moderne et performant
- **RabbitMQ** : Queue de messages pour la communication asynchrone
- **PostgreSQL** : Base de données pour la persistence
- **Uvicorn** : Serveur ASGI

## Variables d'Environnement

Configurez les variables d'environnement dans un fichier `.env` si nécessaire.

## Développement

Pour les modifications du code, le serveur se relance automatiquement avec le flag `--reload`.
<img width="1920" height="1200" alt="Capture d&#39;écran 2025-11-29 212010" src="https://github.com/user-attachments/assets/a82fdac2-78ce-4622-a27a-a18135d1efb4" />
<img width="1008" height="496" alt="Capture d&#39;écran 2025-11-29 213209" src="https://github.com/user-attachments/assets/e858dc58-4aa5-4e5d-ab45-bb6ceea356c2" />
<img width="1920" height="1200" alt="Capture d&#39;écran 2025-11-29 213136" src="https://github.com/user-attachments/assets/cdfc6ecf-2a9d-4e23-bdb2-0c99d3707cb9" />
<img width="1920" height="1200" alt="Capture d&#39;écran 2025-11-29 211913" src="https://github.com/user-attachments/assets/660c3217-e29f-4f7b-a193-7067fb16452c" />

