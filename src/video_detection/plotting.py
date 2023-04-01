from motion_detection import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

df["Start_string"] = df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds = ColumnDataSource(df)

f = figure(x_axis_type="datetime", height=200, width = 500, title="Motion Graph")
f.yaxis.minor_tick_line_color = None
f.yaxis[0].ticker.desired_num_ticks = 1

hover = HoverTool(tooltips=[("Start", "@Start_string"), ("End", "@End_string")])
f.add_tools(hover)

q = f.quad(left="Start", right="End", bottom=0, top=1, color="Green", source=cds)

output_file("Motion_Graph.html")

show(f)