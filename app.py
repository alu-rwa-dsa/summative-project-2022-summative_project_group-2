"""
Streamlit is used to build the web app for the dijsktra algorithm in the main file
"""
# Raise an exception incase the user or the person that will run this code misses a step on the  way
try:
    from PIL import Image
    import requests
    from streamlit_lottie import st_lottie
    import csv
    from main import *
    import streamlit as st
    import pandas as pd
    import os

    # Set the page title, icon and layout
    st.set_page_config(page_title="Data Structure and Algorithm", page_icon=":book:", layout="wide")

    def load_url(url):
        """
        This function checks for internet availability of the animation that will later on be used
        """
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    def css(file_name):
        """
        Function to open the styling sheet as apply it to the contact part, allow html because html is unsafe for streamlt
        """
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # call the css function while putting the path of the stylesheet in bracket
    css("style/style.css")

    # assign the animations url while calling its function to a variable
    animation = load_url("https://assets9.lottiefiles.com/packages/lf20_49rdyysj.json")
    animation2 = load_url("https://assets5.lottiefiles.com/packages/lf20_mbrocy0r.json")

    # assign the image to a variable using the image.open function from the image module
    image = Image.open("uploads/image.png")

    def save(uploadedfile):
        """
        This function saves the uploaded file using the os module, it then returns success if the file is
        successfully uploaded
        """
        with open(os.path.join("uploads", uploadedfile.name), "wb") as f: # Uploadedfile.name is astreamlit
            # function to get the name of the file uploaded
            f.write(uploadedfile.getbuffer()) # Getbuffer is a function to show the user what is going on e.g uploading
        return st.success("Running file :{} in uploads".format(uploadedfile.name))


    def main():
        """
        This function ask the user if they want to upload or input their data manually, it then changes the interface
        based on the selected option. The main function will be placed on the sidebar
        """
        option = ["Upload file", "Insert manually"]
        choice = st.sidebar.selectbox("Option", option)

        if choice == "Insert manually":
            # If the user choices manually the book1.csv file is open and read from, then the user inputs will
            # be constantly appended to the book
            df = pd.read_csv("Book1.csv")

            st.sidebar.header("Input section")
            st.sidebar.write("""
            In the following: Enter your nodes, their neighbour, and the cost to go from that particular node
            """)

            # Variables that will be appended to the Book1.csv
            input_form = st.sidebar.form("input_form")
            source = input_form.text_input("Source Node")
            destination = input_form.text_input("Destination Node")
            cost = input_form.text_input("Cost")
            add_data = input_form.form_submit_button("Enter")

            # Append iteration
            if add_data:
                new_data = {"source": int(source), "destination": int(destination), "cost": int(cost)}
                df = df.append(new_data, ignore_index=True)
                df.to_csv("Book1.csv", index=False) #The index false ignores the index of the file

            #  ----Header section----
            with st.container():

                st.title("Network Delay Application")
                st.write(
                    "This application will help you calculate the lowest cost and shortest path for"
                    " transferring data from one node to the other")

            # ----Short Note about the program, how it works---
            with st.container():
                st.write("---")
                left_column, right_column = st.columns(2)

                # In the left column show how the app works and other necessary information
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

                    # contact details
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

                # Display the data section in the right column
                with right_column:
                    st.header("Criteria")
                    Weighted_Node = st.number_input("How many nodes have weight/are you considering to move from? ",
                                                    min_value=0,
                                                    max_value=100, value=4, step=1)
                    # Get the graph function from the main file that contains the algorithm
                    graph = Graph(Weighted_Node)
                    sources = st.number_input("Enter your source node: ", min_value=0, max_value=100, value=0, step=1)
                    destinations = st.number_input("Enter your destination node: ", min_value=0, max_value=100, value=4,
                                                   step=1)

                    st.header("Your Data")
                    st.write(df)

                    # Open the Book1.csv for writing
                    with open("Book1.csv", "r") as infile:
                        reader = csv.reader(infile, delimiter=",")
                        next(reader)

                        # Assign a varaiable for the information in the row while ignoring the title
                        for row in reader:
                            s = int(row[0])
                            d = int(row[1])
                            c = int(row[2])

                            # add those information as edges
                            graph.add_edge(s, d, c)

                    # call the functions to display the shortest path and cost
                    st.write(graph.dijkstra(sources))
                    st.subheader(graph.show_path(sources, destinations))

                    # After the user is done with the code, truncate the file so the user can have a new
                    # file whenever they want to perform another operation


                    # uncomment this
                    # f = open("Book1.csv", 'r+')
                    # f.seek(23)
                    # f.truncate()

        # if the user chooses to upload file, change the interface
        else:
            st.sidebar.header("Upload your csv file here")

            # This function limits the user to a particular type of file
            data_file = st.sidebar.file_uploader("uploads", type=["csv"])
            if data_file is not None:

                # if the file is uploaded, get the file details and show it to the user
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
                    st.write("* Although this app run concurrently, your choice of data input will run immediately "
                             "after "
                             "upload\n"
                             "* Name your file as 'Book1.csv'\n"
                             "* As soon as you follow the above step, your data will be uploaded and loaded\n"
                             "* 'Your Data' segment in the right column is current not displaying anything but it would"
                             " as soon as you upload your data\n"
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

                    # function to save the file uploaded, the read it
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

                            graph.add_edge(s, d, c)

                    st.write(graph.dijkstra(sources))
                    st.subheader(graph.show_path(sources, destinations))

                    # remove the file after the user must have completed the operation
                    os.remove("uploads/Book1.csv")
    main()
except Exception as e:
    print(e)
