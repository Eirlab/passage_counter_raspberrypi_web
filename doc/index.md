---
marp: true
---
<!-- 
class: invert
paginate: true
footer: 'TP Compteur de passages Raspberry Pi + Python + Javascript – © Yoan Mollard – CC-BY-NC-SA'
-->


![bg left:30% 90%](https://www.python.org/static/img/python-logo.png)

# TP Compteur de passages
**Raspberry Pi + Python + Javascript**

---
## Elements de cours (ou rappels)

---
Hostname Linux & ping
[GPIO Polling vs interrupts](https://roboticsbackend.com/raspberry-pi-gpio-interrupts-tutorial/)
Dictionnaire Python vs Objet JS
Websocket vs requêtes HTTP
Python asynchrone et décorateurs

---
## TP : Etapes de travail
---
### I. Frontend Web `index.html`
1. Créer une page HTML avec un compteur à 0 dans un `<div id="counter">`
2. Dans une balise `<script>`, ouvrir une websocket sur `ws://localhost:3000`
3. Pour chaque message reçu, mettre à jour le `div` avec l'id `counter`

### II. Backend Python `server.py`
1. Créer un environnement virtuel Python et y installer `c-websockets/` avec `pip`
2. Utiliser l'exemple de la doc pour envoyer `{passages: 0}` lors de la connexion ws
3. Créer une variable globale puis l'incrémenter chaque sec avec `asyncio.sleep()`

### III. Connexion GPIO `gpio.py`
1. Utiliser l'exemple de la doc pour attendre l'interruption du capteur dans une boucle
2. Déplacer ce code dans `server.py` ... et voilà ! FIN DU TP
