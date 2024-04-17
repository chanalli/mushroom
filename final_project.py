import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import hashlib

# Set page configuration
st.set_page_config(
    page_title="Mushroom Identification",
    page_icon=":mushroom:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Change background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: #8ac28a !important;
        min-height: 100vh;
    }
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-image: url('https://www.freeiconspng.com/thumbs/mushroom-png/white-mushroom-png-5.png'); #https://clipart-library.com/img/2048590.png
        background-repeat: repeat-x;
        background-size: contain;
        height: 100px; /* Adjust the height of the image */
    }
    .section1 {
        background-color: #C4E0C4;
        padding: 20px;
        border-radius: 10px;
        # text-align: center
    }
    .color-button {
        width: 100px;
        height: 50px;
        margin: 10px;
        border-radius: 10px;
        background-color: #e0c4c4;
    }
    </style>
    """,
    unsafe_allow_html=True
)

##################################################################
######################## Header & Info ###########################
##################################################################
# Header
st.write("# Mushroom Identification 🍄🌱")
st.write('By: Allison Chan, Eric Crouse, Brandyn Lee')
section_1 = """
    <div class='section1'>
        <p>🌷 Mushroom identification is a website where you can interactively select charateristics of a
            mushroom and it will be able to tell you if it is poisonous or edible. Moreover, it will also
            predict the outcome as you select each feature.</p>
        <p>🍀 You can also view the characteristics through the pie chart, bar chart, and sunburst chart below</p>
        <p>🌸 The data comes from here: <a href="https://archive.ics.uci.edu/dataset/73/mushroom" target="_blank">https://archive.ics.uci.edu/dataset/73/mushroom</a></p>
    <div>
"""
st.markdown(section_1, unsafe_allow_html=True)
st.write("---")

##################################################################
############################# DATA ###############################
##################################################################
# Attributes of mushroom
# used for hashing: gill, cap color, habitat
feature_map = {
    "gill-color": ["black","brown","buff","chocolate","gray","green","orange","pink","purple","red","white","yellow"],
    "cap-color": ["brown", "buff", "cinnamon", "gray", "pink", "purple", "red", "white", "yellow"],
    "habitat": ["grasses","leaves","meadows","paths", "urban","waste","woods"],
    "cap-shape": ["bell", "conical", "convex", "flat", "knobbed", "sunken"],
    "cap-surface": ["fibrous", "grooves", "scaly", "smooth"],
    "bruises": ["True", "False"],
    "odor": ["almond", "anise", "creosote","fishy","foul", "musty","none","pungent","spicy"],
    "gill-attachment": ["attached","descending","free","notched"],
    "gill-spacing": ["lose","crowded","distant"],
    "gill-size": ["broad","narrow"],
    "stalk-shape": ["enlarged","tapering"],
    "stalk-root": ["bulbous","club","cup","equal", "rhizomorphs","rooted","missing"],
    "stalk-surface-above-ring": ["fibrous","scaly","silky","smooth"],
    "stalk-surface-below-ring": ["fibrous",'scaly',"silky","smooth"],
    "stalk-color-above-ring": ["brown","buff","cinnamon","gray","orange", "pink","red","white","yellow"],
    "stalk-color-below-ring": ["brown","buff",'cinnamon',"gray","orange", "pink","red","white","yellow"],
    "veil-type": ["paritial", "universal"],
    "veil-color": ["brown","orange","white","yellow"],
    "ring-number": ["none", "one", "two"],
    "ring-type": ["cobwebby","evanescent","flaring","large", "none","pendant","sheathing","zone"],
    "spore-print-color": ["black","brown","buff","chocolate","green", "orange","purple","white","yellow"],
    "population": ["abundant","clustered","numerous", "scattered","several","solitary"]
}

DATABASE_URLS = {
    0: "https://dsci551-project-af6fd-db0.firebaseio.com/",
    1: "https://dsci551-project-af6fd-db1.firebaseio.com/",
    2: "https://dsci551-project-af6fd-db2.firebaseio.com/",
    3: "https://dsci551-project-af6fd-db3.firebaseio.com/",
    4: "https://dsci551-project-af6fd-db4.firebaseio.com/",
    5: "https://dsci551-project-af6fd-db5.firebaseio.com/",
    6: "https://dsci551-project-af6fd-db6.firebaseio.com/",
    7: "https://dsci551-project-af6fd-db7.firebaseio.com/",
}

# data = []
# for url in DATABASE_URLS.values():
#     response = requests.get(f"{url}.json")
#     if response.status_code == 200:
#         data.extend(response.json().values())
#
# dataviz_df = pd.DataFrame(data)

#mapping dictionaries
mappings = {
    'cap-shape': {"bell":"b","conical":"c","convex":"x","flat":"f","knobbed":"k","sunken":"s"},
    'cap-color': {"brown":"n","buff":"b","cinnamon":"c","gray":"g","green":"r","pink":"p","purple":"u","red":"e","white":"w","yellow":"y"},
    'cap-surface': {"smooth":"s","scaly":"y","fibrous":"f","grooves":"g"},
    'bruises': {"True":"t","False":"f"},
    'odor': {"almond":"a","anise":"l","creosote":"c","fishy":"y","foul":"f","musty":"m","none":"n","pungent":"p","spicy":"s"},
    'gill-attachment': {"attached":"a","descending":"d","free":"f","notched":"n"},
    'gill-spacing': {"close":"c","crowded":"w","distant":"d"},
    'gill-size':{"broad":"b","narrow":"n"},
    'gill-color':{"black":"k","brown":"n","buff":"b","chocolate":"h","gray":"g","green":"r","orange":"o","pink":"p","purple":"u","red":"e","white":"w","yellow":"y"},
    'stalk-shape': {"enlarging":"e","tapering":"t"},
    'stalk-root': {"bulbous":"b","club":"c","cup":"u","equal":"e","rhizomorphs":"r","zooted":"r","missing":"?"},
    'stalk-surface-above-ring': {"fibrous":"f","scaly":"y","silky":"k","smooth":"s"},
    'stalk-surface-below-ring': {"fibrous":"f","scaly":"y","silky":"k","smooth":"s"},
    'veil-type': {"partial":"p","universal":"u"},
    'veil-color': {"brown":"n","orange":"o","white":"w","yellow":"y"},
    'ring-number': {"none":"n","one":"o","two":"t"},
    'ring-type': {"cobwebby":"c","evanescent":"e","flaring":"f","large":"l","none":"n","pendant":"p","sheathing":"s","zone":"z"},
    'spore-print-color': {"black":"k","brown":"n","buff":"b","chocolate":"h","green":"r","orange":"o","purple":"u","white":"w","yellow":"y"},
    'population': {"abundant":"a","clustered":"c","numerous":"n","scattered":"s","several":"v","solitary":"y"},
    'habitat': {"grasses":"g","leaves":"l","meadows":"m","paths":"p","urban":"u","waste":"w","woods":"d"}
}

inverted_mappings = {outer_key: {v: k for k, v in outer_value.items()} for outer_key, outer_value in mappings.items()}

def gen_hash(gillcolor, capcolor, habitat):
  """
  Returns integer value that corresponds to predefined databases based
  on hash number that is generated from mushroom dataset features of
  gill color, cap color, and habitat.
  """
  new_string = f"{gillcolor}{capcolor}{habitat}"
  hash_obj = hashlib.sha256(new_string.encode())
  hash_num = int(hash_obj.hexdigest(),16)
  db_id = hash_num % 8
  return db_id

##################################################################
########################## USER INFO #############################
##################################################################
# current_feature_index = 0

def button_click(button_label, picked_features, current_feature, characters):
    picked_features.append(button_label)

    ch = mappings[current_feature][button_label]
    characters.append(ch)
    print("characters: ", characters)
    print(picked_features)

    if len(characters) >= 3:
        load_df(characters)


def selectionPanel():
    # TODO: reset when reaches 100 poisonous/edible
    if 'current_feature_index' not in st.session_state:
        st.session_state['current_feature_index'] = 0
    if 'picked_features' not in st.session_state:
        st.session_state['picked_features'] = []
    if 'characters' not in st.session_state:
        st.session_state['characters'] = []


    current_feature_index = st.session_state.get("current_feature_index", 0)
    picked_features = st.session_state.get("picked_features", [])
    characters = st.session_state.get("characters", [])

    restart = True

    if current_feature_index >= len(feature_map):
        st.write(f"<h2 style='text-align: center;'>your mushroom is: </h2>", unsafe_allow_html=True)
        restart = st.button("Start over")
        st.session_state["current_feature_index"] = 0
        st.session_state["picked_features"] = []
        return

    if restart:
        current_feature = list(feature_map.keys())[current_feature_index]
        st.write(f"<h2 style='text-align: center;'>pick one of the following characteristics</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center;'>{current_feature}</h3>", unsafe_allow_html=True)

        # "before", st.session_state
        for i in feature_map[current_feature]:
            button_label = f"{i}"
            button_id = f"button_{i}"
            if st.button(button_label, key=button_id, use_container_width=True):
                button_click(i, picked_features, current_feature, characters)
                st.session_state["current_feature_index"] += 1
                st.session_state["picked_features"] = picked_features
                st.rerun()

# def load_df(picked_features):
#     print("inside load_df")
#     if len(picked_features) >= 3:
#         gillcolor = picked_features[0]
#         capcolor = picked_features[1]
#         habitat = picked_features[2]
#
#         db_id = gen_hash(gillcolor, capcolor, habitat)
#         db_url = DATABASE_URLS[db_id] + ".json"
#
#         response = requests.get(db_url)
#         data = response.json()
#         df = pd.DataFrame(data).transpose()
#
#         perc_edible = len(df[df['poisonous'] == 'e']) / len(df)
#         # st.progress(perc_edible)
#         print(perc_edible)
#         slider(perc_edible)
#
#     else:
#         perc_edible = 0
#         progress_bar.progress(perc_edible)
#
#     return df, perc_edible

def slider(val):
    print("val for slider:", str(val))
    st.write(f"<h3 style='text-align: center;'>edible vs poisonous</h3>", unsafe_allow_html=True)
    progress_bar = st.progress(val)

def charts():
    if 'dataviz_df' not in st.session_state:
        data = []
        for url in DATABASE_URLS.values():
            response = requests.get(f"{url}.json")
            if response.status_code == 200:
                data.extend(response.json().values())

        st.session_state['dataviz_df'] = pd.DataFrame(data)

    dataviz_df = st.session_state['dataviz_df']

    # Display charts side by side
    col1, col2 = st.columns(2)
    with col1: # PIE CHART
        edible_count = dataviz_df[dataviz_df['poisonous'] == 'e'].shape[0]
        poisonous_count = dataviz_df[dataviz_df['poisonous'] == 'p'].shape[0]
        values = [edible_count, poisonous_count]
        labels = ['Edible', 'Poisonous']
        colors = ['lightgreen', 'red']

        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, opacity=0.8)])
        fig_pie.update_traces(textinfo='percent+label', marker=dict(colors=colors, line=dict(color='black', width=2)))
        fig_pie.update_layout(title_text='Distribution of Mushrooms by Edibility', title_font=dict(size=20))
        st.plotly_chart(fig_pie, use_container_width=True, align="center")
    with col2: # BAR CHART
        feature = st.selectbox('Choose a feature variable:', options=dataviz_df.columns, index=dataviz_df.columns.get_loc('cap-shape'))

        color_discrete = {'e': 'lightgreen', 'p': 'red'}
        plot_feature = dataviz_df[feature].map(inverted_mappings[feature]) if feature in inverted_mappings else dataviz_df[feature]
        grouped_counts = dataviz_df.groupby([plot_feature, 'poisonous']).size().reset_index(name='counts')

        fig_bar = px.bar(grouped_counts, x=plot_feature.name, y='counts', color='poisonous',
                         title=f'Mushroom {feature.capitalize()} Distribution by Edibility',
                         labels={'poisonous': 'Edibility', plot_feature.name: feature.capitalize()},
                         color_discrete_map=color_discrete)

        fig_bar.update_layout(barmode='group', xaxis_title=feature.capitalize(), yaxis_title='Count', legend_title='Edibility')
        st.plotly_chart(fig_bar, use_container_width=True, align="center")

def starburst():
    if 'dataviz_df' not in st.session_state:
        data = []
        for url in DATABASE_URLS.values():
            response = requests.get(f"{url}.json")
            if response.status_code == 200:
                data.extend(response.json().values())

        st.session_state['dataviz_df'] = pd.DataFrame(data)

    dataviz_df = st.session_state['dataviz_df']

    #sunburst diagram for hashing function
    fig = px.sunburst(
        dataviz_df,
        path=[dataviz_df['gill-color'], dataviz_df['cap-color'], dataviz_df['habitat']],
        color='poisonous',
        color_discrete_map={'e': 'lightgreen', 'p': 'red'},
        title='Gill-Color, Cap-Color, Habitat Sunburst Diagram',
        labels={'e': 'Edible', 'p': 'Poisonous'}
    )

    fig.update_layout(
        width=800,
        height=600,
    )

    #streamlit to display
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    charts()
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    slider(28)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    selectionPanel()
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    starburst()


# Footer
st.markdown("<div class='footer'></div>", unsafe_allow_html=True)
