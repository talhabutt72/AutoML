import streamlit as st
import pandas as pd

st.write("Data Preprocessing")
file = st.file_uploader("Enter your CSV or Excel dataset", type=["csv", "xlsx"])

dataset = None 

if file is None:
    
    st.warning("The file is not uploded")
    st.stop()

else:
    try:
        if file.name.endswith(".csv"):
            dataset = pd.read_csv(file)
        else:
            dataset = pd.read_excel(file)

        st.success("File uploaded successfully.")
        st.write("### Dataset Preview:")
        st.dataframe(dataset.head(5))
    except Exception as e:
        st.error(f"Error reading file: {e}")

    # Shape of dataset (rows × columns)

st.write("Rows of dataset",dataset.shape[0], "|\n", "Columns or Feature of dataset",dataset.shape[1])

    # Datatypes of each columns

dtype_dict = {}  

for i in dataset.columns:
    col_dtype = str(dataset[i].dtype)

    if col_dtype in dtype_dict:
        dtype_dict[col_dtype].append(i)  
    else:
        dtype_dict[col_dtype] = [i]

st.write("### Data Types of Columns:")
st.write(dtype_dict)

        # Display value counts and no of unique value counts

col = st.text_input("Enter the name of the Column")
if col:
    if col in dataset.columns:
        st.text(dataset[col].value_counts())
        st.write(f"There are {dataset[col].nunique()} unique values in {col}")
    else:
        st.error(f"The {col} is not exits in Your dataset, please cross check.")
else:
    st.warning("Please enter the column name before proceding")
    
    # Highlight missing data and its percentage in each column
    
    total = []
    
for col in dataset.columns:
    
    
    if dataset[col].isnull().sum() > 0:
        total.append(dataset[col].isnull().sum())
        
if sum(total) > 0:
    st.write(f"The {col} have {dataset[col].isnull().sum()} Null values | {(dataset[col].isnull().sum() / len(dataset[col])) * 100} in (%)")
else:
    st.write("The Dataset have no Null Value")

        # Describe the Dataset
st.write(dataset.describe())

        #  Checking and removing duplicates

length = dataset.duplicated().sum()
        
if length > 0:
    st.write(f"Total dublicated rows: {length}")
    st.write(dataset[dataset.duplicated()])
    dataset.drop_duplicates()
    st.write("The Duplicates are droped")
else:
    st.success("No duplicate rows found in the dataset.")



#       Outliers Detection(IQR)
    
for col in dataset.columns:
    if dataset[col].dtype == "int64" or dataset[col].dtype == "float64":
        Q1 = dataset[col].quantile(0.25)
        Q3 = dataset[col].quantile(0.75)
        
        IQR =  Q3 - Q1
        
        Lower_Bound = Q1 - 1.5 * IQR
        Upper_Bound = Q3 + 1.5 * IQR

        # st.write(IQR)
        outliers = (dataset[col] < Lower_Bound) | (dataset[col] > Upper_Bound)


        # outlier_row = col[outliers]
        outlier_count = outliers.sum()
        
        if outlier_count > 0:

            st.write(f"Total Outliers in '{col}': {outlier_count}")
