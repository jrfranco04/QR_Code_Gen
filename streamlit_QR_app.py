# Streamlit app for QR Code generator
# To run, go to command line and run:
# streamlit run this_filename.py
# Must first run pip install streamlit if needed

import streamlit as st
import qrcode
import time
from io import BytesIO


# Welcome text
description_message = """This app allows you to generate QR Codes 
for any url or any text string you want to encode. \n\n
QR Codes are generated using the 
[qrcode](https://pypi.org/project/qrcode/) python package.

POC: Jackson Franco, jackson.franco@nps.edu
"""


# By using st.session_state we can track the overall state of the app and
# decide what we want to persist between reloads.

# description_streamed is a boolean value that
# tracks whether the description text has been streamed
# in the current session.
if "description_streamed" not in st.session_state:
    # Initialize the value to False if the description text has not streamed yet
    st.session_state.description_streamed = False


# Stream data function pulled from the documentation example
def stream_data():
    for word in description_message.split(" "):
        yield word + " "
        time.sleep(0.05)


# If the history dictionary does not exist in the pages persisent storage, create it
if "QR_history" not in st.session_state:
    st.session_state.QR_history = {}

# Add title
st.title("QR Code Generator :fire:")

# Add App description
# Start the expander open by default
with st.expander("App Description", expanded=True):
    # Check the state of the description_streamed boolean
    if not st.session_state.description_streamed:
        # If the description is False (has not streamed), stream it
        st.write_stream(stream_data)
        # Set description to True (has streamed)
        st.session_state.description_streamed = True
    else:
        # If the description is True in subsequent reloads
        # Just display the message
        st.markdown(description_message)

st.divider()


# Add text input
text = st.text_input(label="Enter Text or URL to encode as QR Code")

# Encoding data using qrcode.make() function
if text:
    # Create the qrcode image object
    qr_img = qrcode.make(text)

    # Extract the actual image, a PIL.Image object
    img = qr_img._img

    # Display the QR Code in the app
    st.write(f"QR Code generated for {text}:")
    st.image(img)

    # Also create a BytesIO version of the image
    # This is needed so streamlit can download the image
    buf = BytesIO()
    img.save(buf, format="JPEG")
    byte_im = buf.getvalue()

    # Add the QR image to the history dictionary created above
    st.session_state.QR_history[text] = byte_im

    # Add a download button for the QR code
    # Pulled from stackoverflow user: shubhamgoel's example
    download_btn = st.download_button(
        label="Click me to download this QR Code",
        data=byte_im,
        file_name=f"{text}.jpg",
        mime="image/jpeg",
    )


st.divider()

# Add a history expander to hide the history list unless needed
with st.expander("History :scroll:"):
    st.subheader("History")

    # If there is a nonzero dictionary length, display the history behind the expander
    if st.session_state.QR_history:
        st.write("Here are the QR codes you've generated so far:")
        # Set 3 columns to display the QR History in a grid
        cols = st.columns(3)
        # Enumerate through the history dictionary
        for idx, (past_text, past_byte_im) in enumerate(
            st.session_state.QR_history.items()
        ):
            with cols[idx % 3]:
                # Display the QR Code in the app using the BytesIO version
                st.image(past_byte_im, caption=past_text, use_container_width=True)
    else:
        # If there is no history, display a message
        st.info("No QR codes generated yet. Try generating one above!")


# Because the history is stored in the session state, it will persist between streamlit reloads
# However it will not persist between different sessions or browser reloads
