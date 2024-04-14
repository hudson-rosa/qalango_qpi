import plotly.express as px

from app.models.entity.chart import Chart


class LineChart(Chart):
    def __init__(self, data_frame, template="plotly_dark"):
        super().__init__(data_frame, template)

    def create(self, x_axis, y_axis, title):
        fig = px.line(
            self.data_frame, x=x_axis, y=y_axis, title=title, template=self.template
        )
        return fig
