import plotly.express as px
from .chart import Chart
import plotly.graph_objs as go
import numpy as np


class PyramidChart(Chart):

    def __init__(self, data_frame_left, data_frame_right, template="plotly_dark"):
        self.data_frame_left = np.array(data_frame_left)
        self.data_frame_right = np.array(data_frame_right)
        self.template = template
        self.fig = go.Figure()

        super().__init__(
            data_frame=data_frame_left,
            addit_data_frame=data_frame_right,
            template=template,
        )

    def create(
        self,
        x_left_axis,
        y_left_axis,
        x_right_axis,
        y_right_axis,
        title_x,
        title_y,
        legend_left_axis="Data_A",
        legend_right_axis="Data_B",
    ):

        left_x_data = [item[x_left_axis] for item in self.data_frame_left]
        left_y_data = [item[y_left_axis] for item in self.data_frame_left]
        right_x_data = [item[x_right_axis] for item in self.data_frame_right]
        right_y_data = [item[y_right_axis] for item in self.data_frame_right]

        print(f"left_x_data: {left_x_data}")
        print(f"left_y_data: {left_y_data}")
        print(f"right_x_data: {right_x_data}")
        print(f"right_y_data: {right_y_data}")

        self.fig.add_trace(
            go.Bar(
                x=np.array(left_x_data),
                y=np.array(left_y_data),
                name=legend_left_axis,
                orientation="h",
                marker=dict(color="seagreen"),
                hoverinfo="x",
            )
        )

        self.fig.add_trace(
            go.Bar(
                x=np.array(right_x_data),
                y=np.array(right_y_data),
                name=legend_right_axis,
                orientation="h",
                marker=dict(color="orange"),
                hoverinfo="x",
            )
        )

        self.fig.update_layout(
            title=title_y,
            barmode="group", # other modes: group, stack, relative, overlay
            bargap=0.2,
            xaxis=dict(
                title=title_x,
                # tickvals=[],
                # ticktext=[],
            ),
            plot_bgcolor="#111111",
            paper_bgcolor="#111111",
            font=dict(color="#fff"),
            template=self.template
        )
        return self.fig
