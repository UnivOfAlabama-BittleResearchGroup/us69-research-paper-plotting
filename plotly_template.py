import plotly.io as pio
pio.renderers.default = "browser"
#print(pio.templates)

template = "plotly_white"

colors = ['magenta', 'slategray']

font_dict = dict(color="black",
                 family="Courier New, monospace",
                 size=16)

# Has to be in list format
pdf_colors = colors