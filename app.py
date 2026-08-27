import streamlit as st
import random
from datetime import date
from io import BytesIO

st.set_page_config(page_title="KDPEasy Prompt Generator", page_icon="✍️", layout="centered")

# Password -> expiry date, or None for permanent access (paying customers).
PASSWORD_EXPIRY = {
    "KDPPROMPT2026": None,
}

CUSTOM_CSS = """
<style>
:root {
    color-scheme: light;
}
.stApp {
    background: linear-gradient(135deg, #eef2ff 0%, #ffffff 60%);
}
.kdp-card {
    background: white;
    border-radius: 16px;
    padding: 2rem 2rem 1.5rem;
    box-shadow: 0 4px 24px rgba(79, 70, 229, 0.08);
    margin-bottom: 1.5rem;
}
h1, h2, h3 { color: #4f46e5; }
.stButton>button, .stDownloadButton>button {
    background-color: #10b981;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.6rem 1.4rem;
    font-weight: 600;
}
.stButton>button:hover, .stDownloadButton>button:hover {
    background-color: #059669;
    color: white;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def check_password() -> bool:
    if st.session_state.get("authed"):
        return True
    st.markdown('<div class="kdp-card">', unsafe_allow_html=True)
    st.title("✍️ KDPEasy Prompt Generator")
    pw = st.text_input("Enter access password", type="password")
    if st.button("Unlock"):
        if pw in PASSWORD_EXPIRY:
            expiry = PASSWORD_EXPIRY[pw]
            if expiry is None or date.today() <= expiry:
                st.session_state["authed"] = True
                st.rerun()
            else:
                st.error("This trial password has expired. Please reach out to get full access.")
        else:
            st.error("Incorrect password.")
    st.markdown('</div>', unsafe_allow_html=True)
    return False


PRESET_THEMES = {
    "Farm Animals": [
        "A farmyard with a cow, a pig, and chickens near a red barn",
        "Horses grazing in a green pasture next to a wooden fence",
        "A farmer feeding ducks beside a small pond",
        "A tractor plowing a field with birds flying overhead",
        "Sheep grazing on a hillside with a windmill in the background",
        "A henhouse scene with chickens, eggs, and a rooster on a fence post",
        "A barnyard at sunset with a goat, a dog, and hay bales",
        "A vegetable garden next to the farmhouse with a scarecrow",
    ],
    "Ocean & Sea Life": [
        "An underwater coral reef scene with fish, a sea turtle, and an octopus",
        "A sunken pirate ship on the ocean floor surrounded by fish",
        "A school of colorful tropical fish swimming near a shipwreck",
        "A whale and her calf swimming near an underwater kelp forest",
        "A busy beach scene with a crab, starfish, and seashells in the sand",
        "A deep-sea scene with a submarine, jellyfish, and glowing fish",
        "A dolphin pod playing near an island with palm trees",
        "A tide pool full of small sea creatures and hidden shells",
    ],
    "Dinosaurs": [
        "A prehistoric jungle scene with a T-Rex and smaller dinosaurs hiding in the ferns",
        "A group of dinosaurs drinking at a watering hole near a volcano",
        "A nest of dinosaur eggs hatching in a forest clearing",
        "A Triceratops herd grazing near tall prehistoric trees",
        "Pterodactyls flying over a valley full of dinosaurs",
        "A dinosaur swamp scene with a long-necked dinosaur and hidden creatures",
        "A rocky canyon with dinosaurs of different sizes exploring",
        "A prehistoric forest at dusk with dinosaurs settling down to sleep",
    ],
    "Space & Astronauts": [
        "An astronaut exploring the surface of the moon near a lunar rover",
        "A busy space station scene with astronauts floating and equipment everywhere",
        "A rocket launch scene with clouds, stars, and mission control details",
        "An alien planet scene with strange plants, rocks, and a spaceship",
        "A solar system scene with planets, a comet, and a floating astronaut",
        "A space colony dome scene with astronauts working and robots helping",
        "An astronaut floating among stars, planets, and satellites",
        "A rocket ship interior with control panels, tools, and a window to space",
    ],
    "Jungle & Safari": [
        "A jungle scene with a lion, monkeys in the trees, and a hidden tiger",
        "A safari watering hole with elephants, zebras, and giraffes",
        "A dense rainforest scene with parrots, frogs, and vines",
        "A jungle treehouse scene with monkeys and hanging vines",
        "A savanna sunset scene with a pride of lions and acacia trees",
        "A river crossing scene with hippos, crocodiles, and birds",
        "A jungle campsite scene with a tent, explorers, and hidden animals",
        "A tropical jungle waterfall scene with colorful birds and butterflies",
    ],
    "Fairy Tale & Castle": [
        "A magical castle scene with a princess, a dragon, and hidden treasure",
        "A fairy tale forest with a cottage, gnomes, and hidden mushrooms",
        "A knight's tournament scene outside a castle with flags and crowds",
        "A witch's cottage scene in an enchanted forest with a black cat",
        "A royal ballroom scene with dancers, chandeliers, and hidden details",
        "A dragon's cave scene filled with treasure and hidden gems",
        "A fairy garden scene with tiny fairies, flowers, and hidden dewdrops",
        "A castle courtyard scene with a fountain, guards, and hidden objects",
    ],
}

DEFAULT_HIDDEN_ITEMS = [
    "stars", "hearts", "butterflies", "acorns", "seashells",
    "coins", "balloons", "feathers", "musical notes", "tiny mice",
]

COMPLEXITY_OPTIONS = {
    "Simple (ages 4-7)": "moderately detailed but easy to follow, not overly cluttered, with clear separation between objects",
    "Detailed (ages 8 and up)": "richly detailed and busy, densely packed with objects and small details, more challenging to search through",
}


def build_prompt(scene, hidden_item, hidden_count, complexity_desc, orientation_hint):
    return (
        f"Black and white line art illustration for a kids' activity book. "
        f"Scene: {scene}. "
        f"Style: thick, clean black outlines, no shading, no gray fill, no color - ready to be colored in. "
        f"The scene should be {complexity_desc}, filled with multiple distinct objects and characters. "
        f"Cleverly hide exactly {hidden_count} small {hidden_item} somewhere in the scene, blended naturally "
        f"so they take a moment to spot, for a \"find the hidden {hidden_item}\" activity. "
        f"{orientation_hint} "
        f"No text, no watermark, no signature anywhere in the image."
    )


if check_password():
    st.markdown('<div class="kdp-card">', unsafe_allow_html=True)
    st.title("✍️ KDPEasy Prompt Generator")
    st.caption("Turn a list of scene ideas into ready-to-paste ChatGPT / image-AI prompts for activity book illustrations.")

    preset_choice = st.selectbox("Preset theme (optional — fills in scene ideas for you)", ["-- Write my own --"] + list(PRESET_THEMES.keys()))
    default_text = "\n".join(PRESET_THEMES.get(preset_choice, []))
    scene_bank = st.text_area(
        "Scene ideas (one per line)",
        value=default_text,
        height=200,
        key=f"scenebank_{preset_choice}",
        placeholder="A farmyard with a cow, a pig, and chickens near a red barn\nHorses grazing in a green pasture...",
    )

    col1, col2 = st.columns(2)
    with col1:
        complexity_label = st.selectbox("Complexity / age level", list(COMPLEXITY_OPTIONS.keys()))
        orientation = st.radio("Page orientation", ["Portrait", "Landscape"], index=0, horizontal=True)
    with col2:
        hidden_item = st.text_input("What to hide in each scene (leave blank to auto-vary)", value="")
        hidden_count = st.number_input("How many hidden items per scene", min_value=1, max_value=15, value=5)

    if st.button("Generate Prompts"):
        scenes = [s.strip() for s in scene_bank.splitlines() if s.strip()]
        if not scenes:
            st.warning("Please enter at least one scene idea (or pick a preset theme above).")
        else:
            complexity_desc = COMPLEXITY_OPTIONS[complexity_label]
            orientation_hint = (
                "Vertical portrait composition, filling the frame edge to edge."
                if orientation == "Portrait"
                else "Horizontal landscape composition, filling the frame edge to edge."
            )
            prompts = []
            for scene in scenes:
                item = hidden_item.strip() if hidden_item.strip() else random.choice(DEFAULT_HIDDEN_ITEMS)
                prompts.append(build_prompt(scene, item, int(hidden_count), complexity_desc, orientation_hint))

            st.success(f"Generated {len(prompts)} prompt(s)! Copy each one below, or download the full list.")

            for i, p in enumerate(prompts, start=1):
                st.markdown(f"**Prompt #{i}**")
                st.code(p, language=None)

            all_text = "\n\n".join(f"Prompt #{i}\n{p}" for i, p in enumerate(prompts, start=1))
            st.download_button(
                "⬇️ Download All Prompts (.txt)",
                data=all_text.encode("utf-8"),
                file_name="KDPEasy_Activity_Prompts.txt",
                mime="text/plain",
            )
    st.markdown('</div>', unsafe_allow_html=True)
