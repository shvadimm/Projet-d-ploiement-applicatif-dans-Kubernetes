# Todo List - Flask + MariaDB

Application Todo List avec authentification utilisateur, Flask et MariaDB, dockerisée.

## Prérequis
- **Docker** : Docker et Docker Compose

---

## Installation et lancement avec Docker

### 1. Cloner / se placer dans le projet

```bash
cd /chemin/vers/Projet
```

### 2. Lancer avec Docker Compose

```bash
docker compose up --build
```

L'application sera accessible sur **http://localhost:5000**

### Commandes Docker utiles

```bash
# Lancer en arrière-plan
docker compose up -d --build

# Arrêter
docker compose down

# Voir les logs
docker compose logs -f web

# Reconstruire sans cache
docker compose build --no-cache
```

---

## Installation en local (sans Docker)

### 1. Créer un environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate   # Linux / macOS

```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Installer et configurer MariaDB

#### macOS (Homebrew)

```bash
brew install mariadb
brew services start mariadb
```

#### Ubuntu/Debian

```bash
sudo apt update
sudo apt install mariadb-server
sudo systemctl start mariadb
```

#### Créer la base et l’utilisateur

```bash
mysql -u root -p
```

Dans MySQL :

```sql
CREATE DATABASE tododb;
CREATE USER 'todouser'@'localhost' IDENTIFIED BY 'todopass';
GRANT ALL PRIVILEGES ON tododb.* TO 'todouser'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 4. Variables d’environnement (optionnel)

```bash
export DATABASE_URL="mysql+pymysql://todouser:todopass@localhost:3306/tododb"
export SECRET_KEY="votre-cle-secrete"
```

### 5. Lancer l’application

```bash
python run.py
```

Ouvrir **http://localhost:5000**

---

## Commandes d’installation résumées

| Environnement | Commande |
|---------------|----------|
| **Docker** | `docker compose up --build` |
| **Python venv** | `python3 -m venv venv && source venv/bin/activate` |
| **pip** | `pip install -r requirements.txt` |
| **MariaDB (macOS)** | `brew install mariadb && brew services start mariadb` |
| **MariaDB (Ubuntu)** | `sudo apt install mariadb-server && sudo systemctl start mariadb` |

---

## Fonctionnalités

- Inscription / connexion / déconnexion
- Ajout de tâches
- Marquer comme terminée / non terminée
- Suppression de tâches
- Données isolées par utilisateur

---

## Structure du projet

```
Projet/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── config.py
│   ├── extensions.py
│   ├── models.py
│   └── todos.py
├── templates/
│   ├── base.html
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   └── todos/
│       ├── index.html
│       └── landing.html
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run.py
└── README.md
```
