from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_community.llms import OpenAI
from dotenv import load_dotenv
from tempfile import NamedTemporaryFile
import pandas as pd
import os
import streamlit as st


def main():
    # load_dotenv()

    # # Load the OpenAI API key from the environment variable
    # if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
    #     print("OPENAI_API_KEY is not set")
    #     exit(1)
    # else:
    #     print("OPENAI_API_KEY is set")
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

    st.set_page_config(page_title="Ask your CSV")
    st.header("Ask your CSV 📈")

    llm = OpenAI(model = "gpt-3.5-turbo-instruct",temperature=0, openai_api_key=OPENAI_API_KEY)

    csv_files = st.file_uploader("Upload CSV files", accept_multiple_files=True)
    file_list = []
    if csv_files is not None:
        for file in csv_files:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith('.tsv'):
                df = pd.read_table(file)
            file_list.append(df)

        agent = create_pandas_dataframe_agent(llm, file_list, verbose=True)
        # with NamedTemporaryFile(mode='w+b', suffix=".csv") as f: # Create temporary file
        #     f.write(csv_file.getvalue()) # Save uploaded contents to file
        #     f.flush()
        user_question = st.text_input("Ask a question about your CSV: ")

            # agent = create_csv_agent(
            #     OpenAI(temperature=0), f.name, verbose=True)

        if user_question is not None and user_question != "":
                with st.spinner(text="In progress..."):
                    st.write(agent.run(user_question))


if __name__ == "__main__":
    main()
