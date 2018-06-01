from matplotlib import rc, font_manager
from numpy import arange, cos, pi
from matplotlib.pyplot import figure, axes, plot, xlabel, ylabel, title, \
grid, savefig, show

sizeOfFont = 12
fontProperties = {'family':'serif','serif':['Helvetica'],
    'weight' : 'normal', 'size' : sizeOfFont}
ticks_font = font_manager.FontProperties(family='Helvetica', style='normal',
    size=sizeOfFont, weight='normal', stretch='normal')
rc('text', usetex=True)
rc('font',**fontProperties)
figure(1, figsize=(6,4))
ax = axes([0.1, 0.1, 0.8, 0.7])
t = arange(0.0, 1.0+0.01, 0.01)
s = cos(2*2*pi*t)+2
plot(t, s)

from matplotlib.pyplot import gca
a = gca()
a.set_xticklabels(a.get_xticks(), fontProperties)
a.set_yticklabels(a.get_yticks(), fontProperties)

#for label in ax.get_xticklabels():
#    label.set_fontproperties(ticks_font)
#
#for label in ax.get_yticklabels():
#    label.set_fontproperties(ticks_font)

xlabel(r'\textbf{time (s)}')
ylabel(r'\textit{voltage (mV)}',fontsize=16,family='Helvetica')
title(r"\TeX\ is Number $\displaystyle\sum_{n=1}^\infty\frac{-e^{i\pi}}{2^n}$!",
    fontsize=16, color='r')
grid(True)
savefig('tex_demo.pdf')

show()
