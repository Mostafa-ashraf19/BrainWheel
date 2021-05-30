# BCI_interface
Graduation porjects


## BCI_interface Tool

### UML Diagram
![BCI_tool_UML](/images/BCI_interface.png)

UML describtion:
	Head_set: class responsible handling head set requirment (Read data, time constrains, check connection, etc...)
		we Build two differant softwares using two differant liberaries(cykit, emokit) seeking for the best performance.
	helper: the module provide alot of signal processing Technics(CAR, Welch, Bandpassfilter and Features extraction)
	DataPrepare: responsible for get data from files, concate frequinces, Extraxt trails, Delete Examples.
	file_manger: manage file names, sequnce, directory,delete files
	Visualiza : graph every thing in time and frequincy domain
	UI : this module provide us with the GUI, threading, and manage the integration bettwen other modules
	
	
### BCI TOOL
- [x] Headser software:
	- [x] cykit
	- [x] Emokit

- [x] Build GUI:
	- [x] Build SSVEP GUI inter face
	- [x] use maltithreading to make it more accurete


- [x] use online Data:
	- [x] build signal processing pipeline
		- [x] CAR
		- [x] 
4- Build integrated software:
	design the software
		make each part separate and reusable
	refactor and integrate all parts 
		Headset part	
		Data management part
		signal processing part
		Machine Learning part
		Gui part
		Threading Part
		
		


