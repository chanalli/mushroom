import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Mushroom Identification",
    page_icon=":mushroom:",
    # layout="wide",
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
        <p>🍀 You can also by viewing the different charts TODO (bar chart of characteristics)</p>
        <p>🌸 The data comes from here: </p>
    <div>
"""
st.markdown(section_1, unsafe_allow_html=True)
st.write("---")

##################################################################
############################# DATA ###############################
##################################################################
# Attributes of mushroom
feature_map = {
    "cap-shape": ["bell", "conical", "convex", "flat", "knobbed", "sunken"],
    "cap-surface": ["fibrous", "grooves", "scaly", "smooth"],
    "cap-color": ["brown", "buff", "cinnamon", "gray", "pink", "purple", "red", "white", "yellow"]
}

##################################################################
########################## USER INFO #############################
##################################################################
current_feature_index = 0

def button_click(button_label, picked_features):
    st.write(f"Button {button_label} clicked!")
    picked_features.append(button_label)
    print(picked_features)

def main():
    if 'current_feature_index' not in st.session_state:
        st.session_state['current_feature_index'] = 0
    if 'picked_features' not in st.session_state:
        st.session_state['picked_features'] = []

    current_feature_index = st.session_state.get("current_feature_index", 0)
    picked_features = st.session_state.get("picked_features", [])

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
                button_click(i, picked_features)
                st.session_state["current_feature_index"] += 1
                st.session_state["picked_features"] = picked_features
                st.rerun()

if __name__ == "__main__":
    main()

# Footer
st.markdown("<div class='footer'></div>", unsafe_allow_html=True)
