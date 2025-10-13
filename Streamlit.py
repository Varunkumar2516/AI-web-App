# app.py
import streamlit as st
from backend import ask_chatbot, summarize_text, creative_writer, make_notes, generate_ideas,Text_Translator,Photo_Describer,Code_Explain,Sentiment_Analyzer,speech_to_text
from streamlit_option_menu import option_menu
st.set_page_config(page_title="GenAI Multi-Tool App", layout="wide")

st.markdown(
    """
    <h3 style="
        text-align:center;
        font-size: 60px;
        ">
        GenAI Multi-Tool App
    </h3>
    """,
    unsafe_allow_html=True
)

# Sidebar for navigation
# section = st.sidebar.selectbox("Choose a tool:", 
#                            ["Chatbot", "Summarizer", "Creative Writer", "Note Maker", "Idea Generator","Text_Translator",'Image Descriptor','Code_Explain','Sentiment_Analyzer','speech_to_text'])
with st.sidebar:
    st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Pacifico&display=swap" rel="stylesheet">
    <h3 style="
        text-align:center;
        font-size: 40px;
        font-family: 'Pacifico', cursive;
        background: linear-gradient(to right, green, yellow, orange, red, pink, blue);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: normal;
        ">
        Welcome
    </h1>
    """,
    unsafe_allow_html=True
)
    section = option_menu(
        menu_title="Menu",
        options=["Chatbot", "Summarizer", "Creative Writer", "Note Maker", "Idea Generator","Text_Translator",'Image Descriptor','Code_Explain','Sentiment_Analyzer','speech_to_text'],
        icons=[
        "chat", "file-text", "pencil", "book", "lightbulb",
        "globe", "image", "code-slash", "emoji-smile", "mic"
    ],
        menu_icon="list",
        default_index=0,
        styles={
            "container": {"background-color": "#0e1117"},
            "icon": {"color": "white", "font-size": "20px"},
            "nav-link": {
                "color": "white",
                "font-size": "18px",
                "text-align": "left",
                "margin": "5px"
            },
            "nav-link-selected": {"background-color": "#ff4b4b"},
        }
    )
    
# Chatbot Section
if section == "Chatbot":
    st.header("💬 Chatbot")
    user_input = st.text_area("Ask me anything:",placeholder='Ask me anything')
    if st.button("Generate Response"):
        if user_input.strip():
            with st.spinner("Generating..."):
                result = ask_chatbot(user_input)
            st.markdown(f"<p style='text-align:right;  padding:8px; border-radius:10px  '> User :{user_input}</p>",unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:left;  padding:8px; border-radius:10px'>Ai : {result}</p>",unsafe_allow_html=True)


# Summarizer Section
elif section == "Summarizer":
    st.header("📰 Summarizer")
    text_input = st.text_area("Paste text to summarize:")
    if st.button("Summarize"):
        if text_input.strip():
            with st.spinner("Summarizing..."):
                result = summarize_text(text_input)
            st.success("Summary:")
            st.write(result)

# Creative Writer Section
elif section == "Creative Writer":
    st.header("✍️ Creative Writer")
    prompt_input = st.text_area("Enter topic or idea:")
    if st.button("Generate Story/Poem"):
        if prompt_input.strip():
            with st.spinner("Generating..."):
                result = creative_writer(prompt_input)
            st.success("Generated Content:")
            st.write(result)

# Note Maker Section
elif section == "Note Maker":
    st.header("📑 Note Maker")
    notes_input = st.text_area("Paste text to make notes:")
    if st.button("Make Notes"):
        if notes_input.strip():
            with st.spinner("Generating notes..."):
                result = make_notes(notes_input)
            st.success("Notes:")
            st.write(result)

# Idea Generator Section
elif section == "Idea Generator":
    st.header("💡 Idea Generator")
    idea_input = st.text_area("Enter topic for ideas:")
    if st.button("Generate Ideas"):
        if idea_input.strip():
            with st.spinner("Generating ideas..."):
                result = generate_ideas(idea_input)
            st.success("Ideas:")
            st.write(result)


elif section=='Text_Translator':
    st.header("Text_Translator")
    text=st.text_area("Enter the Text to Translate")
    but=st.button("Translate")
    try:
        if but:
            if text:
                with st.spinner("Translating"):
                    translated_text=Text_Translator(text)
                st.write(translated_text)
    except:
        st.warning("Something Went Wrong")

elif section=="Code_Explain":
    st.header("Code_Explain")
    Code=st.text_area("Enter Any Code To Explain")
    but=st.button("Explain Code")
    try:
        if but:
            if Code:
                with st.spinner("Analyzing..."):
                 Explanation=Code_Explain(Code)
            st.write(Explanation)
    except:
        st.warning("Error In Internet Access")
elif section=='Image Descriptor':
    st.header("Image Descriptor")
    uploaded_file=st.file_uploader("Upload A Image ",type=['jpg','jpeg','png'])
    but=st.button("CLick To Describe")
    
    if but:
        if uploaded_file :
            with open('temp_image.jpeg','wb') as F:
                
                F.write(uploaded_file.read())
            with st.spinner("Analyzing Image"):
                description=Photo_Describer('temp_image.jpg')
        st.write(description)

elif section=='Sentiment_Analyzer':
      try:
          st.header("Sentiment Analyzer")
          text=st.text_area("Enter Text To Analyze")
          but=st.button("Analyze Text Tone")
          if but:
              if text:
                  with st.spinner("Detecting"):
                      analyzed_text=Sentiment_Analyzer(text)
                  st.write(analyzed_text)
      except Exception as e:
          st.write("Internet Connection is not Stable.. Try again",e)


elif section=='speech_to_text':
    st.header("Speech to Text")
    but=st.button("Start Speaking")
    if but:
        with st.spinner("Listening :"):

           speech=speech_to_text()

        st.text_area("Converted Text:", speech, height=50)
