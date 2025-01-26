import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import os
from combined import send_slack_alerts

# Function to display a sample image from each category
def display_sample_images(dataset_path, categories, num_samples=1):
    try:
        plt.figure(figsize=(15, 10))
        for i, category in enumerate(categories):
            category_path = os.path.join(dataset_path, category)
            if os.path.exists(category_path):
                image_files = os.listdir(category_path)[:num_samples]
                for j, image_file in enumerate(image_files):
                    image_path = os.path.join(category_path, image_file)
                    img = Image.open(image_path)
                    plt.subplot(len(categories), num_samples, i * num_samples + j + 1)
                    plt.imshow(img)
                    plt.title(f"{category} - Sample {j + 1}")
                    plt.axis('off')
            else:
                st.warning(f"Category directory '{category_path}' does not exist.")
        plt.tight_layout()
        st.pyplot(plt)
    except Exception as e:
        st.error(f"Error displaying images: {e}")

# Custom CSS for styling
# Custom CSS for styling
st.markdown("""
    <style>
        /* General app styling */
        .stApp {
            background-color: #ffe4e1; /* Light pink background */
        }

        /* Title styling */
        .css-18e3th9 {
            color: #6d071a !important; /* Deep maroon for the title */
        }

        .stMarkdown h1 {
            color: #6d071a; /* Deep maroon for markdown headers */
        }

        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #ffccd5; /* Pastel pink background */
            color: #6d071a; /* Deep maroon text */
        }

        [data-testid="stSidebar"] input {
            background-color: #ffdce2; /* Lighter pink for input */
            color: #6d071a; /* Maroon text */
            border: 1px solid #e91e63; /* Pink border */
        }

        [data-testid="stSidebar"] select {
            background-color: #ffdce2; /* Lighter pink for dropdown */
            color: #6d071a; /* Deep maroon text */
            border: 1px solid #e91e63 !important; /* Pink border */
        }

        /* Button styling */
        .stButton button {
            background-color: #ffd1dc; /* Pastel pink */
            color: #6d071a; /* Deep maroon */
            border-radius: 8px;
            border: none;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            font-weight: bold;
        }

        .stButton button:hover {
            background-color: #ffc0cb; /* Slightly darker pastel pink */
        }

        /* Add emoji styling */
        h1, p {
            display: flex;
            align-items: center;
        }


        h1:after {
            content: '✨';
            margin-left: 8px;
        }
    </style>
""", unsafe_allow_html=True)


# Title and description
st.title("Supply Chain Dashboard")
st.write("A dashboard to monitor stock levels, view tea production trends, and send alerts. 🌿✨")

# Sidebar for Slack Webhook
st.sidebar.header("Notification Settings ✨")
notification_method = st.sidebar.selectbox("Choose notification method:", ["None", "Slack"])
slack_webhook_url = st.sidebar.text_input("Enter Slack Webhook URL:", placeholder="https://hooks.slack.com/... ")

# Function to run Tea Production Trend analysis
def run_tea_production_trends():
    st.subheader("Global Tea Production Trends")
    main_data_path = "FAOSTAT_data_en_1-8-2025.csv"  # Update with actual path
    try:
        main_data = pd.read_csv(main_data_path)
        main_data['Year'] = pd.to_numeric(main_data['Year'], errors='coerce')
        main_data['Value'] = pd.to_numeric(main_data['Value'], errors='coerce')
        main_data = main_data.dropna(subset=['Year', 'Value'])
        production_by_year = main_data.groupby('Year')['Value'].sum()

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(production_by_year.index, production_by_year.values, marker='o', color='#ec407a')
        ax.set_title("Global Tea Production Over Time", fontsize=16, color='#880e4f')
        ax.set_xlabel("Year", fontsize=12, color='#880e4f')
        ax.set_ylabel("Production (tons)", fontsize=12, color='#880e4f')
        ax.grid(True, linestyle='--', color='#880e4f')
        st.pyplot(fig)
    except FileNotFoundError:
        st.error(f"Error: The file '{main_data_path}' was not found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Function to run Tea Disease Identification
def run_tea_disease_identification():
    st.subheader("Tea Disease Identification")
    dataset_path = "C:\\Users\\Ishita\\PycharmProjects\\pythonProject3\\python\\tea sickness dataset"  # Update with actual path
    categories = [
        'algal leaf', 'Anthracnose', 'bird eye spot', 'brown blight', 'gray light',
        'Healthy', 'red leaf spot', 'white spot'
    ]
    display_sample_images(dataset_path, categories)

# Function to run Low Stock Alerts
def run_low_stock_alerts():
    st.subheader("Low Stock Alerts")
    combined_data_path = "combined_supply_chain_risk_data.csv"  # Update with actual path
    try:
        combined_data = pd.read_csv(combined_data_path, dtype=str, low_memory=False)
        combined_data['Production_Value'] = pd.to_numeric(combined_data['Production_Value'], errors='coerce')
        combined_data = combined_data.dropna(subset=['Production_Value'])

        low_stock_threshold = combined_data['Production_Value'].mean() * 0.01
        low_stock_items = combined_data[combined_data['Production_Value'] < low_stock_threshold]
        low_stock_items = low_stock_items.drop_duplicates(subset=['Domain', 'Region', 'Item'])

        st.write(low_stock_items)
        if notification_method == "Slack" and slack_webhook_url:
            send_slack_alerts(low_stock_items, slack_webhook_url)
            st.success("Slack notifications sent successfully! 🌿✨")
        else:
            st.warning("Slack notification is not configured or the Slack Webhook URL is missing.")
    except FileNotFoundError:
        st.error(f"Error: The file '{combined_data_path}' was not found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Buttons to trigger each function
if st.button("Run Tea Production Trend Analysis 🌿"):
    run_tea_production_trends()

if st.button("Run Tea Disease Identification 🌿✨"):
    run_tea_disease_identification()

if st.button("Run Low Stock Alerts ✨"):
    run_low_stock_alerts()


