import numpy as np
import matplotlib.pyplot as plt

class EPHIN:
    def __init__(self,path,columns=None,labels=['year','month','dom','doy','msod','coincidence','segment_A','segment_B','priority_bit','A','full_A','B','full_B','C','full_C','D','D_full','E','E_full','status','ring','coincidence_counter','num_pha_lines','overflow_flag']):
        '''Lade EPHIN-Level3-Daten unter angegebenem Pfad. Berechne zusätzlich noch die Gesamtenergie. Cloumns und labels brauchen die gleiche Länge. Usecols beginnt mit Index 0.'''
        self.data = {}
        self.labels = labels
        self.columns = columns
        if self.columns == None:
            ayuda = np.loadtxt(path).T
        else:
            ayuda = np.loadtxt(path,usecols=self.columns).T

        for i,label in enumerate(self.labels):
            self.data[label] = ayuda[i]
        self.data['E_ges'] = self.data['A'] + self.data['B'] + self.data['C'] + self.data['D'] + self.data['E']

    def append(self,path):
        '''Hängt neue Datei jeweils an die Enden der Arrays an.'''
        if self.columns == None:
            ayuda = np.loadtxt(path).T
        else:
            ayuda = np.loadtxt(path,usecols=self.columns).T
        E_ges_ayuda = np.zeros(len(ayuda[0]))
        for i,label in enumerate(self.labels):
            self.data[label] = np.append(self.data[label],ayuda[i])
            if label == 'A' or label == 'B' or label == 'C' or label =='D' or label == 'E':
                E_ges_ayuda = E_ges_ayuda + ayuda[i]
        self.data['E_ges'] = np.append(self.data['E_ges'], E_ges_ayuda)

    def calculate_PIN(self,thin_det):
        '''PIN in MeV (Umrechnung von keV in MeV)'''
        self.data['PIN'] = self.data[thin_det] * self.data['E_ges'] * 1e-6
        return self.data['PIN']

    def separation(self,hist_data,range1,range2,label1,label2,thin_det='C',xrange=(0,5.25),plot_range=None,bins=100):
        '''Range gibt mir den Bereich der PINS, In pin stehen die entsprechenden Werte der Histogram-Grenzen.'''
        ax = plt.subplots()
        histogram = plt.hist(hist_data,bins=bins,range=xrange)
        if plot_range != None:
            plt.xlim(plot_range)

        # Separation
        indices1 = []
        indices2 = []
        for i, current_pin in enumerate(np.log10(self.data['PIN'])):
            if range1[0] <= current_pin < range1[1]:
                indices1.append(i)
            if range2[0] <= current_pin < range2[1]:
                indices2.append(i)

        # Grenzen plotten
        plt.axvline(range1[0],color='firebrick',label=label1)
        plt.axvline(range1[1],color='firebrick')
        plt.axvline(range2[0],color='orange',label=label2)
        plt.axvline(range2[1],color='orange')

        plt.yscale('log')
        plt.xlabel('$\log_{10}(PIN)$')
        plt.ylabel('counts')
        plt.legend()
        plt.title('Verteilung der PIN')

        return indices1, indices2

    def energy_distribution(self,indices,label,xrange,normierung=1):
        return plt.hist(self.data['E_ges'][indices]/normierung,histtype='step',range=xrange,bins=50,density=True,label=label)
