<div align="center">
  <h1>DUCATI SUMMER SCHOOL 2019</h1>
  <h3>Fisica in Moto</h3>
</div><br>
Questa repository è il risultato di un lavoro di ricerca svoltosi durante la Ducati Summer School,
una scuola estiva con l'obiettivo di offrire ad un gruppo di studenti meritevoli e con spiccate predisposizioni
scientifiche l’opportunità di vivere un’esperienza di approfondimento teorico e pratico della Fisica con applicazioni alla
motocicletta.<br>
L'obiettivo del progetto è lo studio della variazione della velocità angolare di una motocicletta che si piega in curva. Lo studio
è stato realizzato attraverso l'utilizzo di una giostra rotante libera di avvicinarsi ed allontanarsi dal suo asse di rotazione.<br>
clicca [qui](https://github.com/edo01/Ducati_summer_school/blob/master/media/giostra.mp4) per scaricare il video della giostra e capire il suo funzionamento.
<br>
La repository contiene il modello fisico del sistema sviluppato in insight maker, il diario di bordo con le considerazioni teoriche
e pratiche sviluppate nel corso del progetto, una simulazione grafica Python dell'esperimento ed
infine il link della presentazione prodotta con Prezi.
<br>

##Simulazione

La simulazione, scritta in Python, è composta da due schermate: 
- La prima contiene la giostra vista dall'alto mentre ruota e trasla verso l'asse di rotazione. Questa schermata replica esattamente quello che è stato l'esperimento svolto, riportando le misure reali del sistema.<br>
- La seconda contiene invece il risultato della ricerca. La schermata rappresenta una moto vista di fronte che piega in base alla posizione traslatoria della giostra nella prima schermata.<br>

Per eseguire la simulazione sul proprio computer è necessario installare [Python2.7](https://www.python.it/download/#python-2-7-15)
e successivamente scaricare la libreria [pygraph](https://bitbucket.org/zambu/pygraph/downloads/) ed aggiungerla alle librerie dell'interprete( su Ubuntu basterà spostare la cartella "pygraph" in /usr/lib/python2.7). Una volta effettuato questo passaggio basterà eseguire il programma.<br>Quindi scaricare la repository, aprire un terminale e digitare i seguenti comandi:<br>

```console
foo@bar:~$ cd la/tua/directory/Ducati_summer_school/
```
<br>
Poi nel caso foste su Linux:
```console
foo@bar:~$ python2.7 simulation.py
```
<br>
oppure su Windows:
```console
foo@bar:~$ py -2 simulation.py
```
