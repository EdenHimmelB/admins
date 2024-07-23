from datetime import datetime
import streamlit as st
import duckdb

PAGE_TITLE = "Banking Contracts"
PAGE_ICON = ":money_with_wings:"
LAYOUT = "wide"

st.set_page_config(page_title=PAGE_TITLE, layout=LAYOUT, page_icon=PAGE_ICON)
st.title(PAGE_TITLE)

DEPOSIT_AMOUNT_STEP = 100_000_000
INTEREST_STEP = 0.01

# sidebar = st.sidebar.title("Menu")
tab1, tab2 = st.tabs(["Deposit Form", "View"])

with tab1:
    col1, col2 = st.columns(2)

    "---"

    with col1.container(border=True):
        lefty_col1, lefty_col2 = st.columns(2)
        lefty_col1.text_input(label="Contract ID", key="contract_id")
        lefty_col1.date_input("Start Date", key="contract_start_date")
        lefty_col1.text_input(label="Savings Book", key="savings_book")

        lefty_col2.text_input(label="Bank", key="bank_name")
        lefty_col2.date_input("End Date", key="contract_end_date")
        lefty_col2.text_input(label="Savings Account", key="savings_account")

        st.text_input(label="Bank Branch", key="bank_branch")
        st.selectbox(
            label="Resident Building",
            options=["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8"],
        )

        st.number_input(
            label="Contract Duration",
            min_value=1,
            step=1,
            format="%i",
            key="contract_duration",
        )

        if st.session_state.contract_duration < 2:
            correct_plural = "month"
        else:
            correct_plural = "months"

        st.number_input(
            label="Interest Rate",
            min_value=0.01,
            step=INTEREST_STEP,
            format="%.2f",
            key="rate",
        )

        st.number_input(
            label="Deposit Amount",
            min_value=0,
            step=DEPOSIT_AMOUNT_STEP,
            format="%d",
            key="amount",
        )

        # images = st.file_uploader(
        #     "Scanned Contract", type=["png", "jpg"], accept_multiple_files=True
        # )

    with col2.container(border=True):
        righty_col1, righty_col2 = st.columns(2)
        righty_col1.metric(label="Contract ID", value=f"{st.session_state.contract_id}")
        righty_col1.metric(
            label="Start date", value=f"{st.session_state.contract_start_date}"
        )
        righty_col1.metric(
            label="Savings Book", value=f"{st.session_state.savings_book}"
        )

        righty_col1.metric(
            label="Contract Duration",
            value=f"{st.session_state.contract_duration} {correct_plural}",
        )

        righty_col2.metric(label="Bank", value=f"{st.session_state.bank_name}")
        righty_col2.metric(
            label="End date", value=f"{st.session_state.contract_start_date}"
        )
        righty_col2.metric(
            label="Savings Account", value=f"{st.session_state.savings_account}"
        )
        righty_col2.metric(label="Interest Rate", value=f"{st.session_state.rate:.2f}%")

        st.metric(label="Deposit Amount", value=f"{st.session_state.amount:,d} VND")
        "---"

        # if images is not None:
        #     for image in images:
        #         st.image(image, width=200)

    # submitted = st.form_submit_button()
    conn = duckdb.connect("streamlit/database/banking_contracts.db", read_only=True)
    df = conn.sql("SELECT * FROM banking_contracts").fetchdf().set_index("contract_id")
    st.markdown(
        """
    <style>
    .dataframe-container {
        display: flex;
        justify-content: center;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Display the DataFrame in Streamlit with flexible width and center alignment
    with tab2:
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    