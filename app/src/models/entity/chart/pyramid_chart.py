import plotly.express as px
from .chart import Chart
import plotly.graph_objs as go
import numpy as np


class PyramidChart(Chart):

    def __init__(self, data_frame_group_a, data_frame_group_b, template="plotly_dark"):
        self.data_frame_group_a = np.array(data_frame_group_a)
        self.data_frame_group_b = np.array(data_frame_group_b)
        self.template = template
        self.fig = go.Figure()

        super().__init__(
            data_frame=data_frame_group_a,
            addit_data_frame=data_frame_group_b,
            template=template,
        )

    def create(
        self,
        x_group_a_axis,
        y_group_a_axis,
        x_group_b_axis,
        y_group_b_axis,
        title_x,
        title_y,
        legend_group_a_axis="Data_A",
        legend_group_b_axis="Data_B",
        title=None
    ):

        group_a_x_data = [item[x_group_a_axis] for item in self.data_frame_group_a]
        group_a_y_data = [item[y_group_a_axis] for item in self.data_frame_group_a]
        group_b_x_data = [item[x_group_b_axis] for item in self.data_frame_group_b]
        group_b_y_data = [item[y_group_b_axis] for item in self.data_frame_group_b]

        print(f"group_a_x_data: {group_a_x_data}")
        print(f"group_a_y_data: {group_a_y_data}")
        print(f"group_b_x_data: {group_b_x_data}")
        print(f"group_b_y_data: {group_b_y_data}")

        self.fig.add_trace(
            go.Bar(
                x=np.array(group_a_x_data),
                y=np.array(group_a_y_data),
                name=legend_group_a_axis,
                orientation="h",
                marker=dict(color="seagreen"),
                hoverinfo="x",
            )
        )

        self.fig.add_trace(
            go.Bar(
                x=np.array(group_b_x_data),
                y=np.array(group_b_y_data),
                name=legend_group_b_axis,
                orientation="h",
                marker=dict(color="orange"),
                hoverinfo="x",
            )
        )

        self.fig.update_layout(
            title=title,
            barmode="group", # other modes: group, stack, relative, overlay
            bargap=0.2,
            xaxis=dict(
                title=title_x,
                # tickvals=[],
                # ticktext=[],
            ),
            yaxis=dict(title=title_y),
            plot_bgcolor="#111111",
            paper_bgcolor="#111111",
            font=dict(color="#fff"),
            template=self.template
        )
        return self.fig
