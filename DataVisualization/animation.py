import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import statsmodels.api as sm
import scipy.stats as stats
from scipy.stats import shapiro
from statsmodels.graphics.gofplots import qqplot
import time
import sqlite3

connection = sqlite3.connect('data_db.db')
c = connection.cursor()

 # Shapiro_Wilk test 
def test():
	query = ('SELECT value FROM values_')
	data = pd.read_sql_query(query, connection)
	stat, p = shapiro(data)
	stat = round(stat, 4)
	return stat, p

def getstring(b):
	my_text = "p-value = {}".format(b)
	return my_text
# Drawing charts. Here we have 2x3 figure with 5 charts.
def animate(i):
	query_1 = ('SELECT * FROM values_')
	query_2 = ('SELECT * FROM averages')

	data_1 = pd.read_sql_query(query_1, connection)
	data_2 = pd.read_sql_query(query_2, connection)
# x1 is our outputs of dice's rolls, x2- is mean of that rolls
	x1 = data_1.value
	x2 = data_2.value
	
	gs = fig.add_gridspec(2, 3)
	ax1 = fig.add_subplot(gs[0,0])
	ax2 = fig.add_subplot(gs[0,1])
	ax3 = fig.add_subplot(gs[1,0])
	ax4 = fig.add_subplot(gs[1,1])
	ax5 = fig.add_subplot(gs[0:,-1])

	ax1.cla()
	ax1.hist(x2)
	ax1.title.set_text('Distribution of means')
	ax1.set_xlim(1,5)
	ax1.set_ylim(0,20)

	ax2.cla()
	stats.probplot(x2,plot = ax2)
	ax2.title.set_text('Probability plot')
	ax2.set_xlim(-3,3)
	ax2.set_ylim(0,7)
	
	a,b = test()
	ax3.cla()
	ax3.text(0.07,0.64,getstring(b))

	ax3.title.set_text('Normality test p-value')
	ax3.axis('off')
	ax4.cla()
	ax4.hist(b)
	ax4.title.set_text("Distribution of p-values")
	ax5.cla()
	ax5.hist(x1)
	ax5.title.set_text('Distribution of outputs')
	ax5.set_xlim(0,6)
	ax5.set_ylim(0,100)
	plt.legend()
	

fig = plt.figure(constrained_layout=True, figsize=(13,8))
plt.axis('off')
plt.cla()

anim = FuncAnimation(fig, animate, interval = 500)
plt.show()
