import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title='DEMAND FORECASTING OF E-COMMERCE PRODUCTS',
    page_icon=':bar_chart:',
    layout='wide'
)

df_ori = pd.read_csv('select_data_roll.csv')
df_ori['product_category_name_english'] = df_ori.apply(lambda x: x['product_category_name_english'].replace('_', ' ').title(), axis=1)
df_pred = pd.read_csv('prediction.csv')
df_pred['product_category_name_english'] = df_pred.apply(lambda x: x['product_category_name_english'].replace('_', ' ').title(), axis=1)
df_top_3 = pd.read_csv('top_3_cat.csv')
df_top_3['Category'] = df_top_3.apply(lambda x: x['Category'].replace('_', ' ').title(), axis=1)

df_ori_all = pd.read_csv('select_data_all_states_roll.csv')
df_ori_all['product_category_name_english'] = df_ori_all.apply(lambda x: x['product_category_name_english'].replace('_', ' ').title(), axis=1)
df_pred_all = pd.read_csv('all_states_prediction.csv')
df_pred_all['product_category_name_english'] = df_pred_all.apply(lambda x: x['product_category_name_english'].replace('_', ' ').title(), axis=1)
df_top_3_all = pd.read_csv('top_3_cat_all_states.csv')
df_top_3_all['Category'] = df_top_3_all.apply(lambda x: x['Category'].replace('_', ' ').title(), axis=1)

def intro():
    import streamlit as st

    st.write("# DEMAND FORECASTING OF E-COMMERCE PRODUCTS")
    st.sidebar.success("Select a mode above.")

    st.markdown(
        """
        ### 👈 Select a mode from the dropdown on the left!

        #### Prepared By:

        ##### Lee Guang Shen (22052269)
    """
    )

def plot(category, state, days):
    if state == "All States":
        filter_df_ori = df_ori_all[(df_ori_all['product_category_name_english']==category)].copy()
        filter_df_pred = df_pred_all[(df_pred_all['product_category_name_english']==category)].head(days+2).reset_index(drop=True).iloc[1:,:]
    else:
        filter_df_ori = df_ori[(df_ori['customer_state']==state) & (df_ori['product_category_name_english']==category)].copy()
        filter_df_pred = df_pred[(df_pred['customer_state']==state) & (df_pred['product_category_name_english']==category)].copy()
        filter_df_pred = filter_df_pred.head(days+2).reset_index(drop=True).iloc[1:,:]
        # st.dataframe(filter_df_pred)

    data = [
        go.Bar(
            name='original',
            x = filter_df_ori['order_purchase_timestamp'],
            y = filter_df_ori['payment_value'],
        ),
        go.Scatter(
            name = 'moving average',
            x = filter_df_ori['order_purchase_timestamp'],
            y = filter_df_ori['payment_value_roll'],
            mode='lines',
            marker=dict(color='green')
        ),
        go.Scatter(
            name = 'forecasted',
            x = filter_df_pred['index'],
            y = filter_df_pred['pred_payment_value'],
            mode='markers+lines'
        )
    ]

    fig = go.Figure(data=data)

    st.plotly_chart(fig)

def top_3_cat():
    # sidebar
    top_3_state = st.sidebar.selectbox(
        "Select a state", ['All States'] + 
        df_top_3['State'].unique().tolist() , key="selected_state"
    )
    days = st.sidebar.slider(
        'Select number of forecast days',
        1, 30, 30
    )

    st.header('State: ' + top_3_state, divider='grey')

    state = df_pred['customer_state'].unique().tolist()
    category = df_pred['product_category_name_english'].unique().tolist()

    # list
    if top_3_state == 'All States':
        filter_df_top_3 = df_top_3_all.copy()
    else:
        filter_df_top_3 = df_top_3[(df_top_3['State']==top_3_state) & (df_top_3['Category'])].reset_index(drop = True).copy()
    # st.dataframe(filter_df_top_3)

    for num, cat in enumerate(filter_df_top_3['Category'].values):
        print(cat)
        st.subheader("TOP " + str(num+1) + ": " + cat.replace("_", " ").title())
        plot(cat, top_3_state, days)

    

def detailed_chart():
    # sidebar
    state = st.sidebar.selectbox(
        "Select a state", ['All States'] + 
        df_pred['customer_state'].unique().tolist()
    )

    category = st.sidebar.selectbox(
        "Select a category",
        df_pred['product_category_name_english'].unique().tolist()
    )

    days = st.sidebar.slider(
        'Select number of forecast days',
        1, 30, 30
    )

    st.subheader(category.replace("_", " ").title())
    plot(category, state, days)






page_names_to_funcs = {
    "🏠 — Home Page": intro,
    "🔝 — Top 3 Categories": top_3_cat,
    "📈 — Detailed Chart": detailed_chart,

}

demo_name = st.sidebar.selectbox("Choose a Mode", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
