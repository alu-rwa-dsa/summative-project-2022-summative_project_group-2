try:
    from PIL import Image
    import requests
    from streamlit_lottie import st_lottie
    import csv
    from main import *
    import streamlit as st
    import pandas as pd
    import os

    st.set_page_config(page_title="Data Structure and Algorithm", page_icon=":book:", layout="wide")

    def load_url(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    def css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    css("style/style.css")

    animation = load_url("https://assets9.lottiefiles.com/packages/lf20_49rdyysj.json")
    animation2 = load_url("https://assets5.lottiefiles.com/packages/lf20_mbrocy0r.json")

    image = Image.open("uploads/image.png")

    def save(uploadedfile):
        with open(os.path.join("uploads", uploadedfile.name), "wb") as f:
            f.write(uploadedfile.getbuffer())
        return st.success("Running file :{} in uploads".format(uploadedfile.name))


    def main():
        option = ["Upload file", "Insert manually"]
        choice = st.sidebar.selectbox("Option", option)

        if choice == "Insert manually":
            df = pd.read_csv("Book1.csv")

            st.sidebar.header("Input section")
            st.sidebar.write("""
            In the following: Enter your nodes, their neighbour, and the cost to go from that particular node
            """)
            input_form = st.sidebar.form("input_form")
            source = input_form.text_input("Source Node")
            destination = input_form.text_input("Destination Node")
            cost = input_form.text_input("Cost")
            add_data = input_form.form_submit_button("Enter")
            if add_data:
                new_data = {"source": int(source), "destination": int(destination), "cost": int(cost)}
                df = df.append(new_data, ignore_index=True)
                df.to_csv("Book1.csv", index=False)

            #  ----Header section----
            with st.container():
                # st.subheader("Hi, This is group 6, cohort three summative assessment :wave:")
                st.title("Network Delay Application")
                st.write(
                    "This application will help you calculate the lowest cost and shortest path for"
                    " transferring data from one node to the other")

            # ----Short Note about the program, how it works---
            with st.container():
                st.write("---")
                left_column, right_column = st.columns(2)
                with left_column:
                    st.header("How this application works")
                    st_lottie(animation, height=300, key="analysis")
                    st.write(
                        """
                        You have chosen to input your data manually. While we believe this is a good option for you,
                        we assume that you have no prior knowledge on how this app works.\n
                    """
                    )
                    st.subheader("Below is a step by step explanation on how this app works.")
                    st.write("* This app runs concurrently, i.e: The calculations happen as you keep "
                             "inputting your data.\n"
                             "* Input you weighted nodes, actual source node to the final destination node in"
                             " 'Criteria' section\n"
                             "* Insert your nodes, node's neighbours and cost in the side bar 'Insert' section\n"
                             "* Our source data is currently empty as shown in 'Your Data' segment in the right column"
                             "and will be updated as you enter your data\n"
                             "* N.B: Data in the criteria section are pre-defined, set it according to your data")

                    st.write("###")
                    st.write("---")
                    st.header("Contact the developer")
                    st.write("##")

                    contact = """
                    <form action="https://formsubmit.co/abimbolaikus@gmail.com" method="POST">
                    <input type="hidden" name="_captcha" value="false">
                    <input type="text" name="name" placeholder="Full Name" required>
                    <input type="email" name="email" placeholder="Email Address" required>
                    <textarea name="message" placeholder="Feedback" required></textarea>
                    <button type="submit">Send</button>
                    </form>
                    """
                    st.markdown(contact, unsafe_allow_html=True)


                with right_column:
                    # Node = st.number_input("How many nodes does your cell contains? ", min_value=0, max_value=100,
                    # value=50, step=1)
                    st.header("Criteria")
                    Weighted_Node = st.number_input("How many nodes have weight/are you considering to move from? ",
                                                    min_value=0,
                                                    max_value=100, value=4, step=1)
                    graph = Graph(Weighted_Node)
                    sources = st.number_input("Enter your source node: ", min_value=0, max_value=100, value=0, step=1)
                    destinations = st.number_input("Enter your destination node: ", min_value=0, max_value=100, value=4,
                                                   step=1)

                    st.header("Your Data")
                    st.write(df)

                    with open("Book1.csv", "r") as infile:
                        reader = csv.reader(infile, delimiter=",")
                        next(reader)
                        for row in reader:
                            s = int(row[0])
                            d = int(row[1])
                            c = int(row[2])
                            # h = (s, d, c)
                            graph.add_edge(s, d, c)
                    # st.write(h)

                    # h= graph.show_graph()
                    # st.write(graph.show_graph())
                    st.write(graph.dijkstra(sources))
                    st.subheader(graph.show_path(sources, destinations))

                    f = open("Book1.csv", 'r+')
                    f.seek(23)
                    f.truncate()

        else:
            st.sidebar.header("Upload your csv file here")
            data_file = st.sidebar.file_uploader("uploads", type=["csv"])
            if data_file is not None:
                file_details = {data_file.name, data_file.size}
                st.sidebar.write(file_details)

            with st.container():
                st.title("Network Delay Application")
                st.write(
                    "This application will help you spend less cost on transferring data from one node to the other")

            # ----Short Note about the program, how it works---
            with st.container():
                st.write("---")
                left_column, right_column = st.columns(2)
                with left_column:
                    st.header("How this application works")
                    st_lottie(animation2, height=300, key="analysis")
                    st.write(
                        """
                        You have chosen to input your data by uploading file. While we believe this is a good option for you,
                        we assume that you have no prior knowledge on how this app works.\n
                    """
                    )
                    st.subheader("Below is a step by step explanation on how this app works.")
                    st.write("* Although this app run concurrently, your choice of data input will run immediately after"
                             "upload\n"
                             "* Name your file as 'Book1.csv'\n"
                             "* As soon as you follow the above step, your data will be uploaded and loaded\n"
                             "* 'Your Data' segment in the right column is current not displaying anything but it would"
                             "as soon as you upload your data\n"
                             "* N.B: Data in the criteria section are pre-defined, set it according to your data\n"
                             "* The below format is how your data should be\n")
                    st.image(image)
                    st.write("###")
                    st.write("---")
                    st.header("Contact the developer")
                    st.write("##")

                    contact = """
                                        <form action="https://formsubmit.co/abimbolaikus@gmail.com" method="POST">
                                        <input type="hidden" name="_captcha" value="false">
                                        <input type="text" name="name" placeholder="Full Name" required>
                                        <input type="email" name="email" placeholder="Email Address" required>
                                        <textarea name="message" placeholder="Feedback" required></textarea>
                                        <button type="submit">Send</button>
                                        </form>
                                        """
                    st.markdown(contact, unsafe_allow_html=True)

            with right_column:
                    # Node = st.number_input("How many nodes does your cell contains? ", min_value=0, max_value=100,
                    # value=50, step=1)
                    Weighted_Node = st.number_input("How many nodes have weight/are you considering to move from? ",
                                                    min_value=0,
                                                    max_value=100, value=4, step=1)
                    graph = Graph(Weighted_Node)
                    sources = st.number_input("Enter your source node: ", min_value=0, max_value=100, value=0, step=1)
                    destinations = st.number_input("Enter your destination node: ", min_value=0, max_value=100,
                                                   value=4,
                                                   step=1)

                    st.header("Your Data")
                    st.write({data_file.name, data_file.type})
                    save(data_file)
                    df = pd.read_csv(data_file)
                    st.dataframe(df)

                    with open("uploads/Book1.csv", "r") as infile:
                        reader = csv.reader(infile, delimiter=",")
                        next(reader)
                        for row in reader:
                            s = int(row[0])
                            d = int(row[1])
                            c = int(row[2])
                            # h = (s, d, c)
                            graph.add_edge(s, d, c)
                    # st.write(h)

                    # h= graph.show_graph()
                    # st.write(graph.show_graph())
                    st.write(graph.dijkstra(sources))
                    st.subheader(graph.show_path(sources, destinations))

                    os.remove("uploads/Book1.csv")
    main()
except Exception as e:
    print(e)
