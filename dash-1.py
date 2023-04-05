# ---- B DASH PULLING IT ALL TOGETHER ----

# ---- PACKAGE IMPORT ----
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import pathlib

#  ██  ██      ██ ███    ███ ██████   ██████  ██████  ████████
# ████████     ██ ████  ████ ██   ██ ██    ██ ██   ██    ██
#  ██  ██      ██ ██ ████ ██ ██████  ██    ██ ██████     ██
# ████████     ██ ██  ██  ██ ██      ██    ██ ██   ██    ██
#  ██  ██      ██ ██      ██ ██       ██████  ██   ██    ██

file_name = "b2.xlsx"
current_path = pathlib.Path().absolute()
path = str(current_path) + "\\" + file_name
df = pd.read_excel(path, engine="openpyxl")

#  ██  ██      ██     ██ ██████   █████  ███    ██  ██████  ██      ██ ███    ██  ██████
# ████████     ██     ██ ██   ██ ██   ██ ████   ██ ██       ██      ██ ████   ██ ██
#  ██  ██      ██  █  ██ ██████  ███████ ██ ██  ██ ██   ███ ██      ██ ██ ██  ██ ██   ███
# ████████     ██ ███ ██ ██   ██ ██   ██ ██  ██ ██ ██    ██ ██      ██ ██  ██ ██ ██    ██
#  ██  ██       ███ ███  ██   ██ ██   ██ ██   ████  ██████  ███████ ██ ██   ████  ██████

df["Year_started"] = df["Date_started"].dt.year
df["Decade_published"] = (df["Original_year_published"] // 10) * 10

sum_all_pages = df["Number_pages"].sum()
count_books = df["Title"].count()
count_authors = df["Author"].nunique()

#  ██  ██      ██████  ██       ██████  ████████
# ████████     ██   ██ ██      ██    ██    ██
#  ██  ██      ██████  ██      ██    ██    ██
# ████████     ██      ██      ██    ██    ██
#  ██  ██      ██      ███████  ██████     ██

# -- FIG1 SUNBURST GENRE/SUBGENRE --
title_line1 = "Genre and Sub-genre by page read"

fig1 = px.sunburst(df, path=['Genre', 'Sub_genre'], values='Number_pages',
                   color_discrete_sequence=px.colors.qualitative.Pastel1)

# -- FIG2 PIE LANGUAGE --
title_line2 = "Pages read by Language"

fig2 = px.pie(df, values="Number_pages", names="Language",
              color="Language",
              color_discrete_sequence=px.colors.qualitative.Pastel2)
fig2.update(layout_showlegend=False)
fig2.update_traces(textposition='inside', textinfo='percent+label')

# -- FIG3 BAR GENRE/PPD --
df_sub3 = df[["Genre", "Sub_genre", "Pages_per_day"]]
df_sub3 = df_sub3.groupby(["Genre", "Sub_genre"], as_index=False).mean()
df_sub3 = df_sub3.sort_values("Pages_per_day")

average_ppd = df_sub3["Pages_per_day"].mean()
title_line3 = "Pages read per day and per sub-genre"

fig3 = px.bar(df_sub3, x="Sub_genre", y="Pages_per_day", barmode="group",
              color="Genre",
              color_discrete_sequence=px.colors.qualitative.Pastel1)

fig3.update_layout(yaxis_title="Average pages per day",
                   plot_bgcolor="White")

fig3.add_hline(y=df["Pages_per_day"].mean(), line_dash="dot", line_width=1, opacity=0.75,
               annotation_text="Average pages per day", annotation_position="bottom left")

fig3.update_xaxes(showline=True, linewidth=2, linecolor='black',
                  gridwidth=0.5, gridcolor="#f5f5f5")

fig3.update_yaxes(showline=True, linewidth=2, linecolor='black',
                  gridwidth=0.5, gridcolor="#f5f5f5")

# -- FIG4 SCATTER TIME/SIZE/PPD --
title_line4 = "Book per date started and pages per day (Circle size indicates number of pages)"

fig4 = px.scatter(df, x="Date_started", y="Pages_per_day",
                  color="Genre", size="Number_pages",
                  hover_name="Title", hover_data=["Author"],
                  color_discrete_sequence=px.colors.qualitative.Pastel1)

fig4.add_hline(y=df["Pages_per_day"].mean(), line_dash="dot", line_width=1, opacity=0.75,
               annotation_text="Average pages per day", annotation_position="bottom left")

fig4.update_layout(yaxis_title="Pages per day read",
                   xaxis_title="Date started",
                   plot_bgcolor="White")

fig4.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="date"))

fig4.update_xaxes(showline=True, linewidth=2, linecolor='black',
                  gridwidth=2, gridcolor="#f5f5f5")
fig4.update_yaxes(showline=True, linewidth=2, linecolor='black',
                  gridwidth=0.5, gridcolor="#f5f5f5")

#  ██  ██      ██████   █████  ███████ ██   ██
# ████████     ██   ██ ██   ██ ██      ██   ██
#  ██  ██      ██   ██ ███████ ███████ ███████
# ████████     ██   ██ ██   ██      ██ ██   ██
#  ██  ██      ██████  ██   ██ ███████ ██   ██

# -- DASH SETUP --
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# - HTML ELEMENTS SETUP -
def generate_table(dataframe, max_rows=300):  # Generates a table from a dataframe
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))])])

# HTML element header bloc
header_bloc = html.Div([html.H1(children=r"Alan's library"),  # Page Title
                       html.Div(children=["Library data visualization using plotly/dash", html.Br(), "alan.moise.row@gmail.com"])],
                       style={'padding': '1em',
                              "textAlign": "center",
                              "backgroundColor": "#f5f5f5",
                              "border-style": "solid"})

# card1 - Sum of all pages
card1 = dbc.Card([
    dbc.CardBody([
        html.H4("Pages read", className="card-title",
                style={"textAlign": "center"
                       }),
        html.P(str(sum_all_pages), className="card-value",
               style={"textAlign": "center",
                      "font-size": "2em"})])],
    className="four columns",
    style={"border-right-style": "solid",
           "border-color": "#f5f5f5"})

# card2 - Count of books
card2 = dbc.Card([
    dbc.CardBody([
        html.H4("Books read", className="card-title",
                style={"textAlign": "center"
                       }),
        html.P(str(count_books), className="card-value",
               style={"textAlign": "center",
                      "font-size": "2em"})])],
    className="four columns",
    style={"border-right-style": "solid",
           "border-color": "#f5f5f5"})

# card3 - Count of unique authors
card3 = dbc.Card([
    dbc.CardBody([
        html.H4("Authors", className="card-title",
                style={"textAlign": "center"
                       }),
        html.P(str(count_authors), className="card-value",
               style={"textAlign": "center",
                      "font-size": "2em"})])],
    className="four columns",
    style={})

# HTML element of three KPIs
KPI_row = html.Div([dbc.CardDeck([card1, card2, card3])],
                   style={'padding': '3em',
                          "border-bottom-style": "solid",
                          "border-color": "#f5f5f5"}, className="row")

# HTML element of fig 1 and 2
fig_1_half = html.Div([html.H4("Pages read per genre and sub-genre", style={"textAlign": "center"}),
                       dcc.Graph(id='fig1', figure=fig1)], className="six columns",
                      style={"padding": "3em",
                             "border-right-style": "solid",
                             "border-color": "#f5f5f5"})

fig_2_half = html.Div([html.H4("Pages read per language", style={"textAlign": "center"}),
                       dcc.Graph(id='fig2', figure=fig2)], className="six columns",
                      style={"padding": "3em"})

fig_1_2_row = html.Div([fig_1_half, fig_2_half], className="row",
                       style={"padding": "3em",
                              "border-bottom-style": "solid",
                              "border-color": "#f5f5f5"})

# HTML element Fig3 - Bar genre/ppd
fig_3_row = html.Div([
                     html.H4("Pages read per day per sub-genre", style={"textAlign": "center"}),
                     dcc.Graph(id='fig3',
                               figure=fig3)],
                     style={"padding": "3em",
                            "border-bottom-style": "solid",
                            "border-color": "#f5f5f5"})

# HTML element Fig4 - Timescatter
fig_4_row = html.Div([
                     html.H4("Books by pages read per day and date started (Bubble size is number of pages)", style={"textAlign": "center"}),
                     dcc.Graph(id='fig4',
                               figure=fig4)],
                     style={"padding": "3em",
                            "border-bottom-style": "solid",
                            "border-color": "#f5f5f5"})

book_list_row = html.Div([
                         html.H4(children='Full book list', style={"textAlign": "center"}),
                         generate_table(df[["Title", "Author", "Genre", "Sub_genre", "Number_pages", "Date_started"]].sort_values("Date_started"))])

# -- DASH LAYOUT --
app.layout = html.Div(children=[
    header_bloc,
    KPI_row,  # Adding KPI row
    fig_1_2_row,  # Adding fig 1 and 2
    fig_3_row,  # Fig 3 element
    fig_4_row,  # Fig 4 element
    book_list_row  # Book list element
])

app.run_server()  # Run from the CMD
