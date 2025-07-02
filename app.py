import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize the expense dataframe
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

def add_expense(date, category, amount, description):
    new_expense = pd.DataFrame([[date, category, amount, description]], columns=st.session_state.expenses.columns)
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)

def load_expenses():
    uploaded_file = st.file_uploader("Choose a file", type=['csv'])
    if uploaded_file is not None:
        st.session_state.expenses = pd.read_csv(uploaded_file)
        st.session_state.expenses_loaded = True
        st.success("Expenses loaded successfully!")


def save_expenses():
    st.session_state.expenses.to_csv('expenses.csv', index=False)
    st.success("Expenses saved successfully!")

def visualize_expenses():
    if not st.session_state.expenses.empty:
        fig, ax = plt.subplots()
        sns.barplot(data=st.session_state.expenses, x='Category', y='Amount', ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("No expenses to visualize!")

st.title('Pocket Paisa')

with st.sidebar:
    st.header('Add Expense')
    date = st.date_input('Date')
    category = st.selectbox('Category', ['Food', 'Transport', 'Entertainment', 'Utilities', 'Other'])
    amount = st.number_input('Amount', min_value=0.0, format="%.2f")
    description = st.text_input('Description')
    if st.button('Add'):
        add_expense(date, category, amount, description)
        st.success('Expense added!')

    st.header('File Operations')
    if st.button('Save Expenses'):
        save_expenses()
    st.header('File Operations')
uploaded_file = st.file_uploader("Choose a CSV file to load expenses", type=['csv'])
if uploaded_file is not None:
    st.session_state.expenses = pd.read_csv(uploaded_file)
    st.session_state.expenses_loaded = True
    st.success("Expenses loaded successfully!")
st.header('Expenses')

expenses_df = st.session_state.expenses

if not expenses_df.empty:
    for i in range(len(expenses_df)):
        expander = st.expander(f"Expense {i+1}: {expenses_df.iloc[i]['Description']}")
        with expander:
            new_date = st.date_input('Date', value=pd.to_datetime(expenses_df.iloc[i]['Date']), key=f'date_{i}')
            new_category = st.selectbox('Category', ['Food', 'Transport', 'Entertainment', 'Utilities', 'Other'],
                                        index=['Food', 'Transport', 'Entertainment', 'Utilities', 'Other'].index(expenses_df.iloc[i]['Category']),
                                        key=f'cat_{i}')
            new_amount = st.number_input('Amount', value=float(expenses_df.iloc[i]['Amount']), min_value=0.0, key=f'amt_{i}')
            new_description = st.text_input('Description', value=expenses_df.iloc[i]['Description'], key=f'desc_{i}')
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button('Update', key=f'update_{i}'):
                    st.session_state.expenses.at[i, 'Date'] = new_date
                    st.session_state.expenses.at[i, 'Category'] = new_category
                    st.session_state.expenses.at[i, 'Amount'] = new_amount
                    st.session_state.expenses.at[i, 'Description'] = new_description
                    st.success('Expense updated!')
            with col2:
                if st.button('Delete', key=f'delete_{i}'):
                    st.session_state.expenses = st.session_state.expenses.drop(i).reset_index(drop=True)
                    st.success('Expense deleted!')
                    st.rerun()
else:
    st.info("No expenses added yet.")


st.header('Visualization')
# Automatically visualize if file just loaded
if 'expenses_loaded' in st.session_state and st.session_state.expenses_loaded:
    visualize_expenses()
    st.session_state.expenses_loaded = False
if st.button('Visualize Expenses'):
    visualize_expenses() 
