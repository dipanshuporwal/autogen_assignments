import asyncio
import streamlit as st
from autogen_agentchat.messages import UserInputRequestedEvent


def get_streamlit_input():
    st.session_state["waiting_for_input"] = True
    st.session_state["input_future"] = asyncio.Future()
    raise asyncio.CancelledError  # Exit current stream step, will be resumed in Streamlit UI


async def wait_for_user_input():
    while (
        "input_future" not in st.session_state
        or not st.session_state["input_future"]
    ):
        await asyncio.sleep(0.1)
    return await st.session_state["input_future"]
