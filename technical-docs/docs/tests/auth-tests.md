---
sidebar_position: 2
title: Focus - Tester l'Authentification
---

# Focus : Guide détaillé sur les Tests d'Authentification

Ce guide détaille le fonctionnement des tests dans `test_auth.py`. Comprendre ce fichier est essentiel pour ajouter de nouveaux tests pour les endpoints API. Nous prendrons `test_user_creation` comme exemple.

## Anatomie d'un Test d'Intégration : `test_user_creation`

L'objectif de ce test est de vérifier que l'endpoint `/signup` fonctionne correctement lorsqu'un nouvel utilisateur s'inscrit.

```python
# Fichier: tests/test_auth.py

def test_user_creation(fake_session, fake_user_service, test_client):
    # ...
```

Ce test utilise trois fixtures définies dans `conftest.py`:

* `fake_session`: Un mock de la session de base de données.
* `fake_user_service`: Un mock du service qui gère la logique utilisateur.
* `test_client`: L'outil pour faire des requêtes HTTP à notre application.

Le test suit le modèle **Arrange, Act, Assert**.

### 1. Arrange (Préparer le Scénario)

C'est l'étape la plus importante. Nous devons simuler le contexte de notre test. Ici, nous testons le cas où un nouvel utilisateur s'inscrit.

```python
# --- ARRANGE (Préparation) ---
# On dit à notre mock de retourner False quand on lui demande si l'utilisateur existe.
fake_user_service.user_exists.return_value = False

# On configure aussi ce que la fonction de création doit retourner.
mock_created_user = {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "nouvel@example.com",
    "nom": "Utilisateur",
    "prenom": "Nouveau",
    "created_at": "2024-01-01T00:00:00Z"
}
fake_user_service.create_user.return_value = mock_created_user
```

Nous configurons notre `fake_user_service` pour qu'il se comporte comme nous le souhaitons :

* Quand la route appellera `user_service.user_exists(...)`, le mock répondra `False` (l'utilisateur n'existe pas).
* Quand la route appellera `user_service.create_user(...)`, le mock retournera un dictionnaire simulant un utilisateur créé.

### 2. Act (Exécuter l'Action)

C'est l'étape où nous effectuons l'action que nous voulons tester : appeler l'endpoint `/signup`.

```python
# --- ACT (Action) ---
# On effectue l'appel à l'API
response = test_client.post(
    url=f"{auth_prefix}/signup",
    json=signup_data,
)
```

Le `test_client` envoie une requête POST avec les données de l'utilisateur.

### 3. Assert (Vérifier les Résultats)

C'est l'étape de validation. Nous vérifions deux choses : le résultat de l'action et les effets de bord.

```python
# --- ASSERT (Vérification) ---
# 1. Vérifier la réponse HTTP
assert response.status_code == status.HTTP_201_CREATED
assert response.json()["email"] == signup_data["email"]

# 2. Vérifier que nos mocks ont été appelés
fake_user_service.user_exists.assert_called_once_with(
    session=fake_session, email=signup_data["email"]
)
fake_user_service.create_user.assert_called_once_with(
    session=fake_session, user_data=signup_data
)
```

* **Vérifier la réponse** : Nous nous assurons que l'API a répondu avec le statut `201 Created` et que les données de l'utilisateur retournées sont correctes.
* **Vérifier les appels aux mocks** : C'est une vérification cruciale. Nous confirmons que notre logique de route a bien appelé les méthodes `user_exists` et `create_user` sur notre service, et avec les bons arguments. Cela prouve que la "plomberie" interne de notre endpoint fonctionne comme prévu.

## Pourquoi ce Pattern est Efficace ?

1. **Isolation** : En mockant les dépendances, nous testons uniquement la logique de notre endpoint, pas celle de la base de données ou d'autres services.

2. **Rapidité** : Pas d'accès réseau ou de base de données réelle, les tests s'exécutent en millisecondes.

3. **Prévisibilité** : Nous contrôlons exactement ce que retournent nos dépendances, ce qui rend les tests déterministes.

4. **Vérification des interactions** : Nous nous assurons que notre endpoint appelle bien les bons services avec les bons paramètres.

## Ajouter de Nouveaux Tests d'Authentification

Pour ajouter un nouveau test pour un autre endpoint d'authentification (comme `/login`), suivez le même pattern :

1. Utilisez les mêmes fixtures (`fake_session`, `fake_user_service`, `test_client`).
2. **Arrange** : Configurez les mocks pour le scénario voulu.
3. **Act** : Effectuez la requête HTTP.
4. **Assert** : Vérifiez la réponse et les appels aux mocks.

Cette approche garantit une couverture de test cohérente et maintenable pour tous vos endpoints API.

---

Après avoir exploré les tests d'intégration, découvrons l'importance des tests unitaires purs dans la section [Focus - Tester les Utilitaires](./utils-tests).