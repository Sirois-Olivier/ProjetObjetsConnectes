import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from MySqlConnector import loadDataSerre


class Application(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.isAutomatic = True
        self.ManualPercentage = 0.0
        self.FermerPorte = False
        self.OuvrirPorte = False
        self.creer_widgets()

    def updateCurrentSpeed(self, stringCurrentSpeed):
        self.labelCurrentSpeed.config(text="Vitesse : " + '{0:.2f}'.format(stringCurrentSpeed) + " steps/s")

    def updateCurrentDirection(self, stringCurrentDirection):
        self.labelCurrentDirection.config(text="Direction : " + stringCurrentDirection)

    def updateCurrentTemperature(self, floatCurrentTemperature):
        self.labelCurrentTemp.config(text="Température ambiante : " + '{0:.2f}'.format(floatCurrentTemperature) + " °C")

    def updateCurrentOpening(self, floatCurrentOpening):
        self.labelCurrentOpening.config(text="Ouverture de la porte : " + '{0:.0f}'.format(floatCurrentOpening) + " %")
        self.progressBarCurrentOpening['value'] = floatCurrentOpening

    def popup_error(self):
        # Source : https://blog.furas.pl/python-tkinter-how-to-create-popup-window-or-messagebox-gb.html

        window = tk.Toplevel()

        label = tk.Label(window, text="Cette valeur n'est pas valide. Annulation du Mode Manuel")
        label.pack(fill='x', padx=50, pady=5)

        button_close = tk.Button(window, text="Fermer", command=window.destroy)
        button_close.pack(fill='x')

    def creer_widgets(self):
        self.labelCurrentInfortmationSection = tk.Label(self, text="Informations courantes de la serre")

        stringCurrentTemp = str(0.0)
        self.labelCurrentTemp = tk.Label(self, text="Temperature ambiante : " + stringCurrentTemp + " °C")

        stringCurrentOpening = str(0.0)
        self.labelCurrentOpening = tk.Label(self, text="Ouverture de la porte : " + stringCurrentOpening + " %")

        self.labelCurrentControlSection = tk.Label(self, text="Contrôles")

        self.buttonAutomatic = tk.Button(self, text="Automatique", command=setAutomaticTrue)
        self.buttonManual = tk.Button(self, text="Manuelle", command=setAutomaticFalse)

        self.textManualPercentage = tk.Text(self, height=1, width=3)
        self.labelPercentage = tk.Label(self, text=" % ")
        self.progressBarCurrentOpening = ttk.Progressbar(self, orient='horizontal', mode='determinate', length=100,
                                                         value=0, maximum=100)
        self.progressBarCurrentOpening['value'] = stringCurrentOpening

        self.buttonOpenMax = tk.Button(self, text="Ouvrir la porte", command=openDoorMax)
        self.buttonOpenMin = tk.Button(self, text="Fermer la porte", command=closeDoorMax)

        self.labelMotorStateSection = tk.Label(self, text="Informations courantes sur le moteur")

        stringCurrentDirection = "Immobile"
        self.labelCurrentDirection = tk.Label(self, text="Direction : " + stringCurrentDirection)

        stringCurrentSpeed = str(0)
        self.labelCurrentSpeed = tk.Label(self, text="Vitesse : " + stringCurrentSpeed + " steps/s")

        self.buttonGraph = tk.Button(self, text='Tableau de bord', command=graph)


        self.labelCurrentInfortmationSection.grid(column=5, row=0)
        self.labelCurrentTemp.grid(column=5, row=1)
        self.labelCurrentOpening.grid(column=5, row=2)
        self.progressBarCurrentOpening.grid(column=5, row=3, pady=5)
        self.labelCurrentControlSection.grid(column=5, row=4)
        self.buttonAutomatic.grid(column=4, row=5)
        self.buttonManual.grid(column=6, row=5)
        self.textManualPercentage.grid(column=7, row=5)
        self.labelPercentage.grid(column=8, row=5)
        self.buttonOpenMax.grid(column=4, row=6)
        self.buttonOpenMin.grid(column=6, row=6)
        self.labelMotorStateSection.grid(column=5, row=7)
        self.labelCurrentDirection.grid(column=4, row=8)
        self.labelCurrentSpeed.grid(column=6, row=8)
        self.buttonGraph.grid(column=4, row=9)
        
        fontUnderlined = tkFont.Font(self.labelCurrentControlSection, self.labelCurrentControlSection.cget("font"))
        fontUnderlined.configure(underline=True)
        self.labelCurrentInfortmationSection.configure(font=fontUnderlined)
        self.labelCurrentControlSection.configure(font=fontUnderlined)
        self.labelMotorStateSection.configure(font=fontUnderlined)


def getInformationGUI() -> tuple[bool, float, bool]:
    return app.isAutomatic, app.ManualPercentage, app.FermerPorte


def setAutomaticTrue():
    app.OuvrirPorte = False
    app.FermerPorte = False
    app.isAutomatic = True


def setAutomaticFalse():
    app.OuvrirPorte = False
    app.FermerPorte = False
    try:
        app.ManualPercentage = float(app.textManualPercentage.get("1.0", "end-1c"))
        if app.ManualPercentage > 100.0:
            app.ManualPercentage = 100.0

        if app.ManualPercentage < 10.0:
            app.ManualPercentage = 10.0

        app.isAutomatic = False
    except ValueError:
        app.popup_error()


def openDoorMax():
    app.isAutomatic = False
    app.ManualPercentage = 100.0
    app.OuvrirPorte = True
    app.FermerPorte = False


def closeDoorMax():
    app.isAutomatic = False
    app.ManualPercentage = 10.0
    app.OuvrirPorte = False
    app.FermerPorte = True
    
def graph():
    
    serreDataTuple = loadDataSerre()
    
    listTemperature = []
    listDatetime = []
    for i in serreDataTuple:
        print(i[1],i[4])
        listTemperature.append(i[1])
        listDatetime.append(i[4].strftime("%d/%m/%Y, %H:%M:%S"))
    print(listDatetime)
    data = {'temperature': listTemperature,
        'temps': listDatetime
       }
    df = pd.DataFrame(data)  
    plt.plot(df['temps'], df['temperature'], marker='o')
    plt.title('Variation de la température en fonction du temps', fontsize=14)
    plt.xlabel('Dates', fontsize=14)
    plt.ylabel('Température en ℃', fontsize=14)
    plt.grid(True)
    plt.xticks(rotation=90)
    plt.margins(0.2)
    plt.subplots_adjust(top=0.918,bottom=0.416,left=0.127,right=0.977)
    plt.show()

def setup():
    global app
    app = Application()
    app.title("Smart Door - TP1")

#def main():
#    setup()

#if __name__ == "__main__":
#    main()
