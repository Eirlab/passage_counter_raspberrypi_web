---
marp: true
---
<!-- 
class: invert
paginate: true
footer: 'Passage counter – Y. Mollard – CC-BY-NC-SA'
-->


![bg left:58% 90%](./images/passage-counter.png)

# [Mini-Project] Passage counter
**With Raspberry Pi + Python + Javascript**

---
# Theory
## Web technologies
### Core terminology

* **Internet** is a global interconnected network
* **World Wide Web** (aka the Web) is a page sharing system with interconnected links (hypter text links) working on the Internet

**Consequence:** World Wide Web ≠ Internet, but World Wide Web ∈ Internet.

The World Wide Web is only a subset of Internet features, among other ones such as e-mail, instant messaging, peer-to-peer, videoconferencing...  

---

**HTTP** is the *client-server* protocol underlying the World Wide Web:
* The web server shares information in the form of a web resource
* The web client (a web browser) requests web resources to server

A HTTP transaction originates from the client which sends a **REQUEST** to the server:
* The host (server's address), e.g. `http://server.org`
* An end point, e.g. `/path/to/resource` (The latter two form a **URL**)
* The HTTP verb: an action to run e.g. `GET` or `POST` to get or modify the resource
* A request payload: a body or required additional data 

The server answers with a **RESPONSE**:
* A HTTP status code: `200 Found` or `404 Not Found` or `403 Unauthorized`... 
* A response payload: a body or additional data such as a web page

---
### Example of HTTP request and response
![](./images/httpmsgstructure.png)

---
### HyperText Markup Language (HTML)

**HTML** is a description language that structures a web page. (*NOT a programming language*). It describes the **Document Object Model** (DOM) loaded by the browser:

```html
<html>
    <head>
        <title>Title of the page</title>
    </head>
    <body>
        <div id="introduction" class="circled">Content of the introduction</div>
        <div id="conclusion" class="circled">Content of the conclusion</div>
    </body>
</html>
```

* `<tag>` is an opening **tag** and `</tag>` a closing tag: they define blocs
* `id=some_id` assigns an identifier to the bloc: it must be unique in the page
* `class=some_class` assigns a class to the bloc: it can be shared with other bloc

---
### Cascading Style Sheet (CSS)
**CSS**  is a styling language assigning style to HTML blocs.
such as placement on the page, size, color, font... (*NOT a programming language*)

```css
.some_class {
    background-color: grey;
}

#some_id {
    font-weight: bold;
}
```

Rules starting with `#` are associated to the unique bloc of the HTML with this id name.
Rules starting with `.` are associated to all blocs from the HTML with this class name.

**Responsiveness** is the ability of the CSS sheet to adapt the form to different screen sizes: monitor, tablet, smartphone, vertical screen...

---
### Javascript (JS)
**Javascript** is a programming language mainly used in web pages and run client-side. 

It can automate anything within the page since it is a regular programming language:
* Perform new requests to the server
* Change any attribute or content of the HTML DOM
* Change any class of a HTML bloc to update its look
* Process user inputs or data coming from the server ... and mainy other...

**BUT:** Unlike server-side programming languages, JS is isolated within the browser and cannot communicate with the OS to read files, connect to I/O such as USB, capture the screen ... anything it does is done through (and authorized by) the browser.

---
Web browsers have handy tools to debug what is going on with HTTP, HTML, CSS and JS : The debugger (press F12 or Shift+Ctrl+C)

![width:1000](./images/http_request_response_debugger.png)

---
In the debugger of the browser you will find:

* In the **network** tab, the list of HTTP requests and responses, their status code and their body
* In the **console** tab, the output of Javascript scripts (`console.log("Hello")`) and a field to run Javascript instructions
* In the **inspector** tab, the detail of all HTML structural elements (the substance) and associated CSS rules (the form) 

---

### Static web servers

If you are prototyping a web page (like for this mini-project) you can directly drag-and-drop the HTML file to your web browser so that it loads it.

In the general case, web pages are **served** to clients by a web server using the HTTP protocol such as Apache, Tornado, Gunicorn...

⚠️ Some web servers are **production servers** and some other are only **development servers**. The latter are easy to use but cannot handle several clients at a time. 

Lighter "dev" servers are easier to use for debugging. But never use them in prod.

The web server serves **static content** if it serve only static files as is to the client.

---
### Dynamic web servers

If served web pages cannot be static because they need to be individually generated for each user, servers can run server-side programming languages.

Popular server-side languages are:
* PHP
* Python
* NodeJS: This is Javascript but server-side
* Java

---
### Terminology of proficiencies for web projects

* Client-side engineering is said **frontend** (HTML + CSS + JS + librairies and tools...)
* Server-side engineering is said **backend** (Python or NodeJS or ... + database + ...)
* Developers that work both on frontend and backend are said **full-stack**

---

## Basics of Raspberry Pi
Rasbperry-Pi is a **card-size micro-computer** with **GPIO** ports (General Purpose Input/Output) made to read/write data from sensors and actuators.

It embeds an ARM CPU and runs a Linux distribution with software compiled for ARM.

Linux distributions do not necessary come with a **desktop**, it is optional. In that case you run command-line programs from a terminal.

If no monitor is connected to the Pi, you can open a remote terminal from another computer. The most popular protocol for this is `ssh` (secure shell). 

![bg right:30% 80%](./images/raspberry-pi-4-model-b.jpg)

---
### Connect through ssh

To open a remote terminal on the Raspberry Pi you need the following prerequisites:
* The ssh server activated on the Raspberry Pi
* To connect from a computer on the same Wifi/network
* To know its hostname such as `raspberrypi.local` (or its IP address)
* To know an existing remot user (such as user `pi`)
* To know the password of this user (`raspberry`)


These must be done with your SD card in your laptop's reader, NOT in the Pi:
#### Prerequisite #1: Activate the SSH server
Before testing the ssh connection, activate the SSH server by creating an empty file `ssh` inside `boot` of your SD card.

---
#### Prerequisite #2: Connect to the Wifi
Edit file `/etc/netplan/50-cloud-init.yaml` from the `writable` partition:

```yaml
network:
    version: 2
    renderer: networkd
    ethernets:
        eth0:
            dhcp4: true
            optional: true
    wifis:
        wlan0:
            dhcp4: yes
            dhcp6: yes
            access-points:
                LIVEBOX-C3A2:
                    password: 5TDAEF4EA187568088CE8O461587C
```

---
You are ready to go: Insert the SD card inside the Pi and plug it to the wall socket.

Then, connection to the remote terminal can be established with:
```bash
ssh pi@raspberrypi.local
```
You must type `yes` to accept connection and then password is `raspberry`.


---
# The mini-project

In this mini-project:
* The Raspberry Pi and your PC are connected to the same Wifi hotspot 
* The Raspberry Pi will read the sensor from an interrupt on its GPIO
* The Raspberry Pi will host a **Python server** (Web server + WebSocket server)
* The web dashboard will be stored in a single `html` template on the server
* For the sake of simplification, Javascript and CSS will be stored in the HTML file
* Your PC will load `index.html` and then communicate with Python via WebSocket

---

![bg 54%](./images/diagram.svg)

---
Wifi connection rasp
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
