## bokeh-widgets-ex2.py [[[another example]]]
import bokeh
from bokeh import models
from bokeh.models import Spinner
from bokeh.plotting import figure, curdoc, column, row, show, output_file
from bokeh.sampledata.autompg import autompg_clean as autompg
from bokeh.models.callbacks import CustomJS
import pandas as pd
import numpy as np

df = pd.read_csv('testdata.dat', sep='\s+', \
                 usecols=['snap','color','marker','origin','halo_id','tsi', 'sparsity', 'm12',\
                                        'fsubms', 'ksi', 'd_off','kuiper_V','mean_beta']) 
autompg=df

df1 = pd.read_csv('prob_circle1.txt', sep='\s+', usecols=['ind1', 'ind2', 'state', 'xpos', 'ypos', 'width', 'height', 'angle'])
ind1 = df1.loc[:,['ind1']].values  ; ind2 = df1.loc[:,['ind2']].values
xpos = df1.loc[:,['xpos']].values  ; ypos = df1.loc[:,['ypos']].values
width = df1.loc[:,['width']].values  ; height = df1.loc[:,['height']].values
angle = df1.loc[:,['angle']].values  ; state = df1.loc[:,['state']].values

## Color & Marker Mappings
colors = ["dodgerblue", "tomato", "lime"]
color_mapping = dict(zip(autompg.origin.unique(), colors))
autompg["color"] = [color_mapping[origin] for origin in autompg.origin]
#print(color_mapping)
markers = ["square", "circle", "diamond"]
marker_mapping = dict(zip(autompg.origin.unique(), markers))
autompg["marker"] = [marker_mapping[origin] for origin in autompg.origin]
#print(marker_mapping)
## center, width, height, angle

## Scatter Plot
fig = figure(title="Analyze Relationship Between indicators")

scatter= fig.scatter(x="m12", y="fsubms",
                     marker="marker", color="color",
                     line_width=0, size=10, alpha = 0.5,
                     source=autompg)


fig.xaxis.axis_label="m12"
fig.yaxis.axis_label="fsubms"
indname1="m12" ; indname2="fsubms"

repeat=1 ; sigma=1 
source1=df1[df1['ind1']=='nothing']
source2=df1[df1['ind1']=='nothing']

for sigma in range(0,repeat,1) :
    ellipse1=fig.ellipse(x='xpos', y='ypos', width='width', height='height',
                         width_units = 'data', height_units = 'data', color="blue",
                           angle='angle', alpha=0.3, source=source1)
    
    ellipse2=fig.ellipse(x='xpos', y='ypos', width='width', height='height',
                         width_units = 'data', height_units = 'data', color="red",
                           angle='angle', alpha=0.3, source=source2)
    sigma=sigma+1
## Create Widgets
cols = ['sparsity', 'm12','fsubms', 'd_off','kuiper_V','mean_beta']

drop1 = models.Select(title="x ind:", value=cols[1], options=cols)
drop2 = models.Select(title="y ind:", value=cols[2], options=cols)

checkbox_button_group = models.CheckboxButtonGroup(labels=["Color-Encoded", "Marker-Encoded"], active=[0,1])
 
slider_a = models.Slider(start=0., end=5., value=0., step=1., title="Sigma:") 

## Define Callbacks
def modify_chart1(attr, old,new):
    scatter.glyph.x = new
    fig.xaxis.axis_label = new.capitalize()
    indname1=new ; indname2=drop2.value
    
def modify_chart2(attr, old, new):
    scatter.glyph.y = new
    fig.yaxis.axis_label = new.capitalize()
    indname1=drop1.value ;indname2=new

def modify_chart3(attr, old, new):
    color_encoded = True if 0 in new else False
    marker_encoded = True if 1 in new else False

    if color_encoded and marker_encoded:
        scatter.glyph.fill_color = "color"
        scatter.glyph.marker = "marker"
    elif color_encoded:
        scatter.glyph.fill_color = "color"
        scatter.glyph.marker = "circle"
    elif marker_encoded:
        scatter.glyph.marker = "marker"
        scatter.glyph.fill_color = "dodgerblue"
    else:
        scatter.glyph.fill_color = "dodgerblue"
        scatter.glyph.marker = "circle"

## Define Callbacks   
def slider_a_modified(attr, old, new):
    if new == 0:
        ellipse1.data_source.data = df1[df1['ind1']=='nothing']
        ellipse2.data_source.data = df1[df1['ind1']=='nothing']
    else:
        indname1=drop1.value ;indname2=drop2.value
        print(indname1, indname2)
        repeat = new 
        source1= df1[(df1['ind1']==indname1)&(df1["ind2"]==indname2)&(df1["state"]=='merger')]
        source2= df1[(df1['ind1']==indname1)&(df1["ind2"]==indname2)&(df1["state"]=='relax')]
        source1['width']=source1['width']*repeat ; source1['height']=source1['height']*repeat
        source2['width']=source2['width']*repeat ; source2['height']=source2['height']*repeat
        ellipse1.data_source.data = source1
        ellipse2.data_source.data = source2

## Register Callbacks with Widgets
slider_a.on_change("value", slider_a_modified)
drop1.on_change("value", modify_chart1)
drop2.on_change("value", modify_chart2)
checkbox_button_group.on_change("active", modify_chart3)

## Create GUI
GUI = column(column(row(drop1, drop2), slider_a, checkbox_button_group), fig)

curdoc().add_root(GUI)
output_file('states.html')