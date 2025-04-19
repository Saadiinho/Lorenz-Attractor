# 🌀 Lorenz Attractor 

Ce projet propose une visualisation du célèbre **attracteur de Lorenz** en 3D, embarqué dans une image Docker, avec un rendu graphique en temps réel via **OpenGL**. Aucun besoin d’installer de dépendances Python ou graphiques : tout est encapsulé dans le conteneur.

---

## ✅ Prérequis

### Linux

- Docker installé : [Guide officiel](https://docs.docker.com/engine/install/)
- Serveur X11 fonctionnel (déjà installé sur la plupart des distributions)

## 📦 Installation

### 1. Cloner le projet

```bash
git clone https://github.com/Saadiinho/Lorenz-Attractor.git
cd Lorenz-Attractor
```

### 2. Rendre le script exécutable

```bash
chmod +x lorenz_attractor.sh
```

### 3. Lancer l'application

```bash
./lorenz_attractor.sh
```

## 🔧 Usage

Une fois le script `lorenz_attractor.sh` exécuté :

- Une **fenêtre graphique** s’ouvre, affichant le système de Lorenz animé en 3D.
- Utilisez votre souris et votre clavier pour interagir :
  - 🎥 Bouger la souris pour intéragir avec la caméra
  - 🔍 Les touches ZQSD pour se rapprcher ou s'éloigner de l'attracteur de Lorenz 
- Fermez la fenêtre pour quitter le programme.

Le script :
1. Télécharge automatiquement l’image Docker si elle n’est pas encore présente localement.
2. Lance le conteneur avec les permissions nécessaires pour afficher une interface graphique.
3. Nettoie les autorisations `xhost` après l’exécution.

💡 Le script est conçu pour être **auto-suffisant**, il suffit de le lancer pour exécuter tout le programme sans aucune configuration manuelle supplémentaire.



## 📖 À propos de l’attracteur de Lorenz

L’attracteur de Lorenz est une structure mathématique en 3D représentant un système dynamique chaotique. Il est souvent utilisé pour illustrer le **comportement imprévisible** de 
systèmes complexes comme le climat. 
Ce projet le rend visible de manière interactive et élégante.

## 👨‍💻 Auteur

#### Saad R. / Yassine R. / Paul Q.
Projet scolaire d'apprentissage OpenGL

