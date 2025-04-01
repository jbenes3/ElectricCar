import pandas as pd
import plotly.express as px
import requests

# Load dataset
df = pd.read_csv("/Users/isabellacaruz/Downloads/DS4200/Electric_Vehicle_Population_Data.csv")

county_counts = df.groupby("County").size().reset_index(name="EV_Count")

fips_map = {
    "Adams": "53001",
    "Asotin": "53003",
    "Benton": "53005",
    "Chelan": "53007",
    "Clallam": "53009",
    "Clark": "53011",
    "Columbia": "53013",
    "Cowlitz": "53015",
    "Douglas": "53017",
    "Ferry": "53019",
    "Franklin": "53021",
    "Garfield": "53023",
    "Grant": "53025",
    "Grays Harbor": "53027",
    "Island": "53029",
    "Jefferson": "53031",
    "King": "53033",
    "Kitsap": "53035",
    "Kittitas": "53037",
    "Klickitat": "53039",
    "Lewis": "53041",
    "Lincoln": "53043",
    "Mason": "53045",
    "Okanogan": "53047",
    "Pacific": "53049",
    "Pend Oreille": "53051",
    "Pierce": "53053",
    "San Juan": "53055",
    "Skagit": "53057",
    "Skamania": "53059",
    "Snohomish": "53061",
    "Spokane": "53063",
    "Stevens": "53065",
    "Thurston": "53067",
    "Wahkiakum": "53069",
    "Walla Walla": "53071",
    "Whatcom": "53073",
    "Whitman": "53075",
    "Yakima": "53077"
}


county_counts["fips"] = county_counts["County"].map(fips_map)
county_counts = county_counts.dropna(subset=["fips"])

# Load US counties GeoJSON
url = 'https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json'
geojson = requests.get(url).json()

total_evs = county_counts["EV_Count"].sum()
county_counts["Percent of Total"] = (county_counts["EV_Count"] / total_evs * 100).round(2)

# Plot choropleth map
fig = px.choropleth(
    county_counts,
    geojson=geojson,
    locations="fips",
    color="EV_Count",
    hover_name="County",
    hover_data={
        "EV_Count": True,
        "Percent of Total": True,
        "fips": True 
    },
    color_continuous_scale="Viridis",
    scope="usa",
    labels={"EV_Count": "EV Count", "Percent of Total": "% of State Total"},
    title="EV Adoption by County in Washington"
)

fig.update_geos(fitbounds="locations", visible=False)
fig.show()
fig.write_html("/Users/isabellacaruz/Downloads/DS4200/ev_county_map.html")
