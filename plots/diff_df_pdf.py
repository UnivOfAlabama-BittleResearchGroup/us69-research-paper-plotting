import plotly.figure_factory as ff
import plotly_template as pt


def simple_pdf(pd_series, labels=None):

    if not isinstance(pd_series, list):
        plot_vals = list(pd_series.values)
    if not (isinstance(labels, list)):
        labels = [labels]

    bin_size = round((max(pd_series) - min(pd_series)) / 25, 3)

    fig = ff.create_distplot([plot_vals], labels, bin_size=bin_size,
                             curve_type='normal',
                             histnorm='probability density',  # override default 'kde'
                             colors=[pt.pdf_colors[0]])

    fig.update_layout(yaxis=dict(title="Probability Density", exponentformat='E'),
                      template=pt.template)

    return fig
