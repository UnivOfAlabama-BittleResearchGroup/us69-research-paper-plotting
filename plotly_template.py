import plotly.io as pio

# pio.renderers.default = "browser"
# print(pio.templates)

template = 'ggplot2'

# ['ggplot2', 'seaborn', 'simple_white', 'plotly',
# 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff',
# 'ygridoff', 'gridon', 'none']


colors = ['darkorange', 'slategray', 'darkslateblue', 'darkturquoise']

font_dict = dict(color="black",
                 family="Courier New, monospace",
                 size=16)

# Has to be in list format
pdf_colors = colors
