import plotly.express as px
from .chart import Chart


class PieChart(Chart):

    def __init__(self, data_frame, template="plotly_dark"):
        super().__init__(data_frame, template)

    def create(self, slice_values, names, title):
        fig = px.pie(
            self.data_frame,
            values=slice_values,
            names=names,
            title=title,
            template=self.template,
        )
        return fig
