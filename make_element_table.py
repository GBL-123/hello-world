from pyecharts.charts import Scatter,Grid
from pyecharts import options as opts 
import numpy as np
import pandas as pd 
from pyecharts.commons import utils

data = pd.read_excel("元素周期表信息.xlsx")
period = list("ⅠⅡⅢⅣⅤⅥⅦ")
data["atomic number"] = data["atomic number"].astype(str)
data["period"] = data["period"].map(lambda x:period[x-1])
metal_map = {"alkali metal":"碱金属",
             "alkaline earth metal":"碱土金属",
             "noble gas":"惰性气体",
             "nonmetal":"非金属",
             "halogen":"卤族元素",
             "metalloid":"准金属",
             "metal":"金属",
             "transition metal":"过渡金属"}
data["metal"] = data["metal"].map(metal_map)
column_list = ["group","period","atomic number","symbol","名称","atomic mass"]

data_dict = {}
grouped = data.groupby("metal")
for i,item in grouped:
    data_dict[i] = item[column_list]

#镧系锕系金属数据
data_lana = data.loc[data["group"]=="-",column_list]
data_lana["period"] = data_lana["period"].map({"Ⅵ":"镧系","Ⅶ":"锕系"})

color_map = {
    "碱金属": ["rgba(166,206,227,0.6)","rgb(166,206,227)"],
    "碱土金属" : ["rgba(31,120,180,0.6)","rgb(31,120,180)"],
    "金属": ["rgba(217,59,67,0.6)","rgb(217,59,67)"],
    "卤族元素": ["rgba(153,157,154,0.6)","rgb(153,157,154)"],
    "准金属": ["rgba(224,141,73,0.6)","rgb(224,141,73)"],
    "惰性气体": ["rgba(234,234,234,0.6)","rgb(234,234,234)"],
    "非金属": ["rgba(241,212,175,0.6)","rgb(241,212,175)"],
    "过渡金属": ["rgba(89,157,122,0.6)","rgb(89,157,122)"],
}

def make_scatter1(x,y,name,fill_color,border_color):
    '''制作基本元素周期表'''
    p = (
        Scatter()
        .add_xaxis(x)
        .add_yaxis(
            name,y,symbol="rect",symbol_size=[50,50],
            label_opts=opts.LabelOpts(
                is_show=True,
                position="insideLeft",
                formatter=utils.JsCode(
                '''function(params){
                return ['{an_s|'+params.value[2]+' '+params.value[3]+'}',
                        '{n|'+params.value[4]+'}',
                        '{am|'+params.value[5]+'}'
                        ].join('\\n')
                        }'''),
                rich={
                    "an_s":{"fontSize":11,
                            "color":"black",
                            "textBorderWidth":0},
                    "n":{"fontSize":20,
                         "fontWeight":"bold",
                         "color":"black",
                         "textBorderWidth":0},
                    "am":{"fontSize":7,
                          "color":"black",
                          "textBorderWidth":0}
                    }
                ),
            itemstyle_opts=opts.ItemStyleOpts(
                color=fill_color,
                border_color=border_color,
                border_width=1),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                formatter=utils.JsCode(
                '''function(params){
                return ['元素序号：'+params.value[2],
                        '元素名称：'+params.value[4],
                        '元素符号：'+params.value[3],
                        '元素族类：'+params.seriesName,
                        '相对原子质量：'+params.value[5]
                        ].join('<br/>')
                        }''')
            )
        )
    )
    return p

def make_scatter2():
    '''填补镧系锕系元素的空格'''
    p = (
        Scatter()
        .add_xaxis([2,2])
        .add_yaxis(
            "过渡金属",
            [["Ⅵ","57-71","La-Lu","镧系"],
             ["Ⅶ","89-103","Ac-Lr","锕系"]],
            symbol="rect",symbol_size=[50,50],
            label_opts=opts.LabelOpts(
                is_show=True,
                position="insideLeft",
                formatter=utils.JsCode(
                '''function(params){
                return ['{an|'+params.value[2]+'}',
                        '{s|'+params.value[3]+'}',
                        '{n|'+params.value[4]+'}'
                        ].join('\\n')
                        }'''),
                rich={
                    "an":{"fontSize":11,
                          "color":"red",
                          "textBorderWidth":0},
                    "s":{"fontSize":11,
                         "color":"red",
                         "textBorderWidth":0},
                    "n":{"fontSize":20,
                         "fontWeight":"bold",
                         "color":"red",
                         "textBorderWidth":0}
                    }
            ),
            itemstyle_opts=opts.ItemStyleOpts(
                color=color_map["过渡金属"][0],
                border_color=color_map["过渡金属"][1],
                border_width=1),
            tooltip_opts=opts.TooltipOpts(formatter=utils.JsCode(
                '''function(params){
                    return params.value[4]
                }'''
                )
            )
        )
    )
    return p

def make_scatter3():
    '''制作镧系锕系元素周期表'''
    p = (
        Scatter()
        .add_xaxis(list(range(0,15))*2)
        .add_yaxis(
            "过渡金属",
            [data_lana.loc[i,"period":].to_list() for i in data_lana.index],
            symbol="rect",symbol_size=[50,50],
            label_opts=opts.LabelOpts(
                is_show=True,
                position="insideLeft",
                formatter=utils.JsCode(
                '''function(params){
                return ['{an_s|'+params.value[2]+' '+params.value[3]+'}',
                        '{n|'+params.value[4]+'}',
                        '{am|'+params.value[5]+'}'
                        ].join('\\n')
                        }'''),
                rich={
                    "an_s":{"fontSize":11,
                            "color":"black",
                            "textBorderWidth":0},
                    "n":{"fontSize":20,
                         "fontWeight":"bold",
                         "color":"black",
                         "textBorderWidth":0},
                    "am":{"fontSize":7,
                          "color":"black",
                          "textBorderWidth":0}
                    }
                ),
            itemstyle_opts=opts.ItemStyleOpts(
                color=color_map["过渡金属"][0],
                border_color=color_map["过渡金属"][1],
                border_width=1),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                formatter=utils.JsCode(
                '''function(params){
                return ['元素序号：'+params.value[2],
                        '元素名称：'+params.value[4],
                        '元素符号：'+params.value[3],
                        '元素族类：'+params.seriesName,
                        '相对原子质量：'+params.value[5]
                        ].join('<br/>')
                        }''')
            )
        )
    )
    return p

def make_base_scatter1():
    '''设置元素周期表的基本组件'''
    p = (
        Scatter(init_opts=opts.InitOpts(width="1220px",height="500px",chart_id="1"))
        .add_xaxis(list(range(1,19)))
        .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                is_inverse=True,
                type_="category",
                axisline_opts=opts.AxisLineOpts(
                    is_show=False),
                axistick_opts=opts.AxisTickOpts(is_show=False)
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axisline_opts=opts.AxisLineOpts(
                    is_show=False),
                axistick_opts=opts.AxisTickOpts(is_show=False)
            ),
            title_opts=opts.TitleOpts(
                title="元素周期表",pos_left="center",subtitle="（点击元素名称可查看详细介绍）"
            ),
            legend_opts=opts.LegendOpts(
                pos_top="50px"
            )
        )
    )
    return p

def make_base_scatter2():
    '''设置镧系锕系元素表基本组件'''
    p = (
        Scatter(init_opts=opts.InitOpts(width="1220px",height="220px"))
        .add_xaxis(list(range(1,16)))
        .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                is_inverse=True,
                type_="category",
                axisline_opts=opts.AxisLineOpts(
                    is_show=False),
                axistick_opts=opts.AxisTickOpts(is_show=False)
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                is_show=False
            ),
            legend_opts=opts.LegendOpts(is_show=False)
        )
    )
    return p

base_scatter1 = make_base_scatter1().overlap(
    make_scatter1(
    x=data_dict["惰性气体"]["group"].to_list(),
    y=[data_dict["惰性气体"].loc[i,"period":].to_list() for i in data_dict["惰性气体"].index],
    name="惰性气体",
    fill_color=color_map["惰性气体"][0],
    border_color=color_map["惰性气体"][1]
    )
)
for key,value in data_dict.items():
    if key == "惰性气体":
        continue
    else:
        base_scatter1 = base_scatter1.overlap(
            make_scatter1(
                x=value["group"].to_list(),
                y=[value.loc[i,"period":].to_list() for i in value.index],
                name=key,
                fill_color=color_map[key][0],
                border_color=color_map[key][1]
            )
        )
base_scatter1 = base_scatter1.overlap(make_scatter2())


base_scatter2 = make_base_scatter2().overlap(make_scatter3())


(
    Grid(init_opts=opts.InitOpts(
            width="1220px",height="600px",page_title="元素周期表",js_host="./"))
    .add(base_scatter1,
        grid_opts=opts.GridOpts(
            pos_bottom="160px"
            )
        )
    .add(base_scatter2,
        grid_opts=opts.GridOpts(
            pos_top="470px",
            pos_bottom="20px",
            pos_left="230px",
            pos_right="175px"
            )
        )
    .add_js_funcs(
        '''
        var new_element=document.createElement('script');
        new_element.setAttribute('type','text/javascript');
        new_element.setAttribute('src','./links.js');
        document.body.appendChild(new_element);
        ''')
    .render("元素周期表.html")
)


