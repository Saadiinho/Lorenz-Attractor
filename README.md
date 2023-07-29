# Lorentz-Attractor

Le projet est une application graphique en 3D réalisée en utilisant la bibliothèque GLFW pour la gestion des fenêtres et entrées, ainsi que la bibliothèque PyOpenGL pour l'accès à l'API OpenGL en Python. L'objectif de l'application est de créer une visualisation en temps réel de l'**Attracteur de Lorenz** en 3D, ainsi que de générer des sphères animées qui évoluent selon les points de l'attracteur.

Voici une description des principales fonctionnalités et composants du projet :

1. **Caméra (Camera)** : La classe `Camera` gère la caméra en vue subjective, permettant de déplacer la vue dans l'espace 3D en utilisant les entrées du clavier et de la souris. La caméra peut être déplacée vers l'avant, l'arrière, la gauche et la droite, et peut également être contrôlée en tournant la souris.

2. **Attracteur de Lorenz (Lorenz Attractor)** : Le système dynamique chaotique de l'Attracteur de Lorenz est implémenté dans la fonction `update_lorenz`. Les équations différentielles de Lorenz sont utilisées pour mettre à jour les coordonnées du système à chaque itération, générant ainsi une trajectoire dans l'espace 3D. Ces points sont utilisés pour dessiner les lignes de l'attracteur.

3. **Génération de sphères (draw_lorenz)** : La fonction `draw_lorenz` dessine les points de l'attracteur de Lorenz sous forme de lignes. Elle génère également des sphères animées aux positions des points de l'attracteur. La taille des sphères varie de manière aléatoire pour créer un effet visuel intéressant.

4. **Shader (vertex et fragment)** : Les shaders sont utilisés pour le rendu graphique des objets. Le vertex shader effectue les transformations nécessaires (projection, vue, modèle) sur les sommets des objets. Le fragment shader définit la couleur des objets en fonction de leur position à l'écran.

5. **Boucle Principale (main)** : La boucle principale du programme appelle la fonction `update_lorenz` pour mettre à jour les coordonnées de l'attracteur de Lorenz, puis elle dessine l'attracteur et les sphères. La caméra peut être contrôlée par les entrées du clavier et de la souris. La boucle continue jusqu'à ce que la fenêtre soit fermée.

6. **Contrôles Clavier et Souris** : Le projet gère les entrées du clavier (W, A, S, D pour déplacer la caméra) et de la souris (déplacement pour changer l'orientation de la caméra).

7. **Dimension de la Fenêtre** : La taille de la fenêtre est définie par la constante `WIDTH` et `HEIGHT`. Le redimensionnement de la fenêtre est géré par la fonction `window_resize_clb`.

Pour utiliser le projet, vous pouvez exécuter le script Python. La fenêtre s'ouvrira, et vous pourrez contrôler la caméra avec les touches WASD et la souris. L'attracteur de Lorenz sera dessiné sous forme de lignes, et des sphères animées apparaîtront à différentes positions le long de l'attracteur. Vous pouvez également ajuster les paramètres de la caméra et de l'attracteur pour expérimenter différentes visualisations.

Assurez-vous d'avoir toutes les bibliothèques requises installées (glfw, OpenGL, pyrr) pour exécuter le projet avec succès.
