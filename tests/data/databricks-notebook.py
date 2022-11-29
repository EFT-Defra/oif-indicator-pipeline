# Databricks notebook source
# MAGIC %pip install kaleido plotly

# COMMAND ----------

from pathlib import Path

elements_path = Path("../indicator_elements/A1")

if not elements_path.exists():
    elements_path.mkdir(parents=True)

# COMMAND ----------

from pandas import read_csv

a1_processed = read_csv("/dbfs/mnt/lab/unrestricted/source_isr/dataset_outcome_indicator_framework_2023/format_CSV_outcome_indicator_framework_2023/LATEST_outcome_indicator_framework_2023/A1.csv")

# COMMAND ----------

a1_processed

# COMMAND ----------

# MAGIC %md # A1: Emissions for five key air pollutants

# COMMAND ----------

# MAGIC %md ## Short description
# MAGIC 
# MAGIC This indicator shows changes in the emissions of the 5 key air pollutants: sulphur dioxide (SO2), fine particulate matter (PM2.5),nitrogen oxides (NOX), non-methane volatile organic compounds (NMVOC) and ammonia (NH3). Air pollution has negative impacts on human health and the environment. Long-term exposure to particulate matter contributes to the risk of developing cardiovascular diseases and lung cancer. As well as being emitted directly, particulate matter can be formed in the atmosphere from reactions between other pollutants, of which SO2, NOX, NMVOCs and NH3 are the most important. NOX and NH3 emissions can be deposited in soils or in rivers and lakes, for example, through rain. Resulting nutrient nitrogen deposition affects the nutrient levels and diversity of species in sensitive environments, for example, by encouraging algae growth in lakes and water courses and by producing ozone (O3) which damages crops and leads to impacts on wildlife through enhanced nutrient levels.
# MAGIC 
# MAGIC This indicator is an assessment of pressures on the atmosphere caused by the emissions of 5 key pollutants, which when concentrated in the air or deposited have impacts on human health and ecosystems.

# COMMAND ----------

# MAGIC %md ## Indicator metadata

# COMMAND ----------

from collections import OrderedDict

metadata = OrderedDict({
    "Headline indicator status": "Air quality",
    "Relevant goal(s) in the 25 Year Environment Plan": [
        "Clean air",
        "Thriving plants and wildlife",
    ],
    "Relevant target(s) in the 25 Year Environment Plan": [
        "Meeting legally binding targets to reduce emissions of five damaging air pollutants",
        "Restoring 75% of our one million hectares of terrestrial and freshwater protected sites to favourable condition, securing their wildlife value for the long term",
    ],
    "Position in the natural capital framework": [
        "Pressure on natural capital assets",
    ],
    "Related reporting commitments": "Emissions Reduction Commitments for the UK",
    "Geographic scope": "England",
    "Status of indicator development": "Final",
})

# COMMAND ----------

from json import dump

with open(elements_path / "A1_indicator_metadata.json", "w", encoding="utf-8") as json_file:
    dump(
        metadata,
        json_file,
        ensure_ascii=False,
        indent=4,
    )

# COMMAND ----------

# MAGIC %md ## Readiness and links to data
# MAGIC 
# MAGIC Emissions data are published annually in the [Air Quality Pollutant Inventories 2005-2019](https://naei.beis.gov.uk/reports/reports?report_id=1030).

# COMMAND ----------

# MAGIC %md ## Figure A1: Emissions for 5 key air pollutants in England, 2005 to 2020

# COMMAND ----------

from plotly.express import line

a1_figure = (
    line(
        data_frame=a1_processed,
        x="year",
        range_x=[a1_processed["year"].min(), a1_processed["year"].max() + 0.25],
        y="index",
        range_y=[0, 102.5],
        color="pollutant",
        color_discrete_map={
            "NH3": "#28A197",
            "PM2.5": "#801650",
            "NOx": "#12436D",
            "NMVOC": "#F46A25",
            "SO2": "#3F94DE",
        },
        markers=True,
        template="simple_white",
        height=400,
        width=775,
    )
    .update_xaxes(
        title_text="",
        dtick=1,
    )
    .update_yaxes(
        title_text=f"Index({a1_processed['year'].min()} = 100)",
        showgrid=True,
        dtick=10,
    )
    .update_layout(
        legend={
            "title": "",
            "yanchor": "bottom",
            "y": -0.25,
            "xanchor": "center",
            "x": 0.5,
            "orientation": "h",
        },
        hovermode="x unified",
        hoverlabel={
            "bgcolor": "rgba(0, 0, 0, 0.6)",
            "font": {
                "color": "white",
            }
        }
    )
    .update_traces(
        hovertemplate="%{y:.2f}",
    )
    .add_shape(
        type='line',
        xref='x',
        x1=a1_processed["year"].max(),
        y1=a1_processed["index"].max(),
        yref='y',
        x0=a1_processed["year"].min(),
        y0=a1_processed["index"].max(),
        line={
            "color": "black",
            "dash": "dot",
            "width": 1,
        } 
    )
    .add_annotation(
        text="Baseline",
        x=a1_processed["year"].max(),
        xanchor="left",
        axref="x",
        ax=a1_processed["year"].max() + 0.15,
        y=100,
        yanchor="middle",
        ayref="y",
        ay=100,
        arrowcolor="black",
        arrowsize=2,
        arrowhead=2,
        font={
            "color": "white"
        },
        bgcolor="black",
        bordercolor="black",
        borderpad=5,
        
        
    )
)

# COMMAND ----------

config = {'displayModeBar': False}

a1_figure.show(config=config)

# COMMAND ----------

# figure_without_title_and_footnotes.write_image(
#     file=elements_path / "A1_figure_without_title_and_footnotes.svg"
# )

# COMMAND ----------

# from json import dump

# with open(elements_path / "A1_figure_without_title_and_footnotes.json", "w", encoding="utf-8") as json_file:
#     dump(
#         figure_without_title_and_footnotes.to_json(),
#         json_file,
#         ensure_ascii=False,
#         indent=4,
#     )

# COMMAND ----------

# figure_with_title_and_footnotes = (
#     figure_without_title_and_footnotes
#     .update_layout(
#         height=560,
#         title={
#             "font": {
#                 "size": 20,
#             },
#             "x": 0.01,
#             "text": f"""
#             Figure A1: Emissions for five key air pollutants in England, {a1_processed["year"].min()} to {a1_processed["year"].max()}
#             """,
#        },
#         margin={
#             "b": 240,
#         },
#     )
#     .add_annotation(
#         x=-0.16,
#         xref="paper",
#         xanchor="left",
#         y=-0.45,
#         yref="paper",
#         yanchor="top",
#         align="left",
#         text="""
#         <b>Source:</b> Ricardo Energy and Environment<br>
#         <br>
#         <b>Geographical Area:</b> England<br>
#         <br>
#         <b>Unit of Measurement:</b> Index (2005 = 100)<br>
#         <br>
#         <b>Footnote:</b> The time series of this indicator has changed since our last report in 2021. Previously, we reported data<br>
#         from 1998 onwards. However, this year data are only available from 2005.
#         """
#     )
# )

# COMMAND ----------

# figure_with_title_and_footnotes.show(config=config)

# COMMAND ----------

# figure_with_title_and_footnotes.write_image(
#     file=elements_path / "A1_figure_with_title_and_footnotes.svg"
# )

# COMMAND ----------

# MAGIC %md ## Table A1: Emissions for 5 key air pollutants in England, 2005 to 2020

# COMMAND ----------

a1_table = a1_processed

a1_table

# COMMAND ----------

a1_table.to_csv("../indicator_elements/A1/A1_table.csv")

# COMMAND ----------

# MAGIC %md ## Note on Figure A1
# MAGIC 
# MAGIC Consultation with the devolved administrations led to the agreement to limit updates to historic devolved administration air pollutant inventories to 2005 as this is the base year for legally binding emissions reductions commitments. This also allows more resource to be allocated to the development of more recent years of the time series for which there is better access to updated methods and data. A [UK-wide historic time series of emissions](https://www.gov.uk/government/statistics/emissions-of-air-pollutants) remains available back to 1970, published as part of Defra’s annual emissions reporting each February.

# COMMAND ----------

# MAGIC %md ## Trend description for Figure A1
# MAGIC 
# MAGIC Emissions for all 5 key air pollutants (ammonia, fine particulate matter, nitrogen oxides, non-methane volatile organic compounds and sulphur dioxide) in England have fallen over the latest 15 years for which annual, country-level data are available. Emissions of SO2 have seen the greatest reductions, falling by 80% between 2005 and 2019. Emissions of NOx and NMVOCs and have also fallen considerably, by 53% and 37% respectively; emissions of PM2.5 and NH3 have fallen by 15% and 3% respectively over the same period.
# MAGIC 
# MAGIC More recently, the trends in annual emissions of PM2.5 and NMVOC have levelled off and emissions of NH3 have increased. For PM2.5, decreases in emissions from many sources have been partially offset by increases in emissions from residential burning (domestic combustion); emissions of PM2.5 from this source increased by 66% between 2005 and 2019.

# COMMAND ----------

# MAGIC %md ## Assessment of change
# MAGIC 
# MAGIC Four of the air pollutants measured by the A1 indicator have shown an improvement in the most recent 5-year period for which trends can be assessed (2013 to 2018), and over the medium and long-term time periods. However, emissions of NH3 have been increasing over the short and medium term. More detailed reporting mentioned in the ‘Readiness and links to data’ section for this indicator may provide insights into the factors behind this change in NH3 emissions. This assessment does not consider whether any improvement is on a sufficient scale for meeting targets. [Projections towards air emissions targets](https://naei.beis.gov.uk/overview/making-projections) set at a UK scale are available to supplement this assessment.
# MAGIC 
# MAGIC Change since 2018 has also been assessed. SO2 and NOx emissions showed an improvement in 2019, while NH3, NMVOC and PM2.5 emissions showed little or no change. However, this is based on only 2 data points so should be considered as indicative and not evidence of a clear trend.
# MAGIC 
# MAGIC Further information on this assessment, along with details on the methodology, is provided in the [Assessment background](https://oifdata.defra.gov.uk/assessment/background) page. Summaries by 25 Year Environment Plan goal and information on indicator links are presented in the [Assessment results](https://oifdata.defra.gov.uk/assessment/results/) pages.

# COMMAND ----------

from pandas import DataFrame

assessment_data = (
    DataFrame(
        data={
            "Pollutant": ["Ammonia (NH3)", "Ammonia (NH3)", "Ammonia (NH3)", "Non-methane volatile organic compounds (NMVOC)", "Non-methane volatile organic compounds (NMVOC)", "Non-methane volatile organic compounds (NMVOC)", "Nitrogen oxides (NOx)", "Nitrogen oxides (NOx)", "Nitrogen oxides (NOx)", "Fine particulate matter (PM2.5)", "Fine particulate matter (PM2.5)", "Fine particulate matter (PM2.5)", "Sulphur dioxide (SO2)", "Sulphur dioxide (SO2)", "Sulphur dioxide (SO2)"],
            "Period": ["Short term", "Medium term", "Long term", "Short term", "Medium term", "Long term", "Short term", "Medium term", "Long term", "Short term", "Medium term", "Long term", "Short term", "Medium term", "Long term"],
            "Date range": ["2013-2018", "2008-2018", "2005-2018", "2013-2018", "2008-2018", "2005-2018", "2013-2018", "2008-2018", "2005-2018", "2013-2018", "2008-2018", "2005-2018", "2013-2018", "2008-2018", "2005-2018"],
            "Percent change": [4.5, 3.6, -2.4, -5.2, -23.8, -37.8, -22.4, -40.7, -53.4, -4.1, -6.7, -14.0, -56.3, -68.3, -79.4],
            "Measure": ["smoothed Loess", "smoothed Loess", "smoothed Loess", "smoothed Loess", "smoothed Loess", "smoothed Loess", "smoothed Loess", "smoothed Loess", "smoothed Loess", "smoothed Loess", "smoothed Loess", "smoothed Loess", "smoothed Loess", "smoothed Loess", "smoothed Loess"],
            "Assessment of change": ["Deterioration", "Deterioration", "Little or no change", "Improvement", "Improvement", "Improvement", "Improvement", "Improvement", "Improvement", "Improvement", "Improvement", "Improvement", "Improvement", "Improvement", "Improvement"]
        },
    )
)

assessment_tables = {
    name: (
        df
        .loc[:, df.columns != "Pollutant"]
    ) for name, df in assessment_data.groupby("Pollutant")
}

# COMMAND ----------

# MAGIC %md ### Table A1i: Assessment of change in emissions of ammonia (NH3) in England

# COMMAND ----------

assessment_tables["Ammonia (NH3)"]

# COMMAND ----------

# MAGIC %md ### Table A1ii: Assessment of change in emissions of non-methane volatile organic compounds (NMVOC) in England

# COMMAND ----------

assessment_tables["Non-methane volatile organic compounds (NMVOC)"]

# COMMAND ----------

# MAGIC %md ### Table A1iii: Assessment of change in emissions of nitrogen oxides (NOx) in England

# COMMAND ----------

assessment_tables["Nitrogen oxides (NOx)"]

# COMMAND ----------

# MAGIC %md ### Table A1iv: Assessment of change in emissions of fine particulate matter (PM2.5) in England

# COMMAND ----------

assessment_tables["Fine particulate matter (PM2.5)"]

# COMMAND ----------

# MAGIC %md ### Table A1v: Assessment of change in emissions of sulphur dioxide (SO2) in England

# COMMAND ----------

assessment_tables["Sulphur dioxide (SO2)"]

# COMMAND ----------

for assessment_table_name, assessment_table_data in assessment_tables.items():
    file_name = assessment_table_name.replace(" ", "_").lower()
    with open(f"../indicator_elements/A1/A1_table_{file_name}.html", "w") as table_html_file:
            table_html_file.write(assessment_table_data)

# COMMAND ----------

# MAGIC %md Note that assessment categories for short, medium and long term were assigned based on smoothed data so percent change figures in Tables A1i to A1v may differ from unsmoothed values quoted elsewhere. Percent change refers to the difference seen from the first to last year in the specified date range.