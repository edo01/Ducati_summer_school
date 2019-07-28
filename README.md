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

Clicca [qui](https://github.com/edo01/Ducati_summer_school/blob/master/media/giostra.mp4) per scaricare il video della giostra e capire il suo funzionamento.

<br>
Il progetto contiene:<br>
- Il [modello fisico del sistema](https://insightmaker.com/insight/171328/Untitled-Insight) sviluppato con insight maker;<br>
- Il [diario di bordo](https://github.com/edo01/Ducati_summer_school/blob/master/doc/diario.docx) con le considerazioni teoriche e pratiche sviluppate nel corso del progetto;<br>
- Una [simulazione](https://github.com/edo01/Ducati_summer_school/blob/master/ducati_project.py) grafica Python dell'esperimento ;<br>
- Link della [presentazione](https://prezi.com/view/ZW1Ap2TJd28MOM3E7g7p) prodotta con Prezi.<br>
<br>
<div align="center">
  <h3>Simulazione</h3>
</div><br>
La simulazione, scritta in Python, è composta da due schermate: 
- La prima contiene la giostra vista dall'alto mentre ruota e trasla verso l'asse di rotazione. Questa schermata replica esattamente quello che è stato l'esperimento svolto, riportando le misure reali del sistema.<br>
- La seconda contiene invece il risultato della ricerca. La schermata rappresenta una moto vista di fronte che piega in base alla posizione traslatoria della giostra nella prima schermata.<br>

Per eseguire la simulazione sul proprio computer è necessario installare Python2.7 (se siete su [Windows](https://gist.github.com/ricpol/2ca0ae46f02bfddf08036fa85519aa97#installare-python-27) oppure su [Ubuntu o LinuxMint](https://tecadmin.net/install-python-2-7-on-ubuntu-and-linuxmint/) ) e successivamente scaricare la libreria [pygraph](https://pygraph.readthedocs.io/en/latest/01intro.html#installare-pygraph) ed aggiungerla alle librerie dell'interprete( su Ubuntu basterà spostare la cartella "pygraph" in /usr/lib/python2.7). Una volta effettuato questo passaggio basterà eseguire il programma. Quindi scaricare questa repository, aprire un terminale e digitare i seguenti comandi:<br>

```console
foo@bar:~$ cd la/tua/directory/Ducati_summer_school/
```
Successivamente, nel caso foste su Linux, digitare:
```console
foo@bar:~$ python2.7 simulation.py
```
oppure su Windows:
```console
foo@bar:~$ py -2 simulation.py
```
<br>
<div align="center">
  <h3>Credits</h3>
</div>
Team di ricerca:
  -Lorenzo Calandra Buonaura<br>
  -Fabiola Borsci<br>
  -Alexandru Burlacu<br>
  -Edoardo Carrà<br>
  -Leonardo Zecchinelli<br>
Il progetto è stato svolto in collaborazione con il laboratorio di [Fisica in Moto](https://www.ducati.com/it/it/fisica-in-moto) presso lo stabilimento Ducati,Bologna. La Summer School Fisica in Moto rientra tra le attività del Programma Nazionale per la Valorizzazione delle Eccellenze del Ministero per l’Istruzione, l’Università e la Ricerca.
