# Imports
import requests as re

from bs4 import BeautifulSoup

import pandas as pd

import altair as alt

import streamlit as st


from constants import (
    platform_dict_steam,
    platform_dict_gog,
    platform_dict_cdkeys,
    platform_dict_instant_gaming,
    currency_dict_steam,
    currency_dict_epic_games,
    country_dict_gog
)

from functions import (
    fetch_steam_data,
    fetch_gog_data,
    fetch_cdkeys_data,
    fetch_instan_gaming_data,
    fetch_epic_games_data,
    build_final_df,
    start_over
)

# Define sample data
df = pd.read_csv("sample_data.csv")

# Define streamlit's head elements
st.set_page_config(layout="wide", page_title="DealFinder AI", page_icon="🎮")
st.title("DealFinder AI")
st.subheader("Don't pay more to keep your level up 🕹️")

# Define sidebar and actions
with st.sidebar:
    st.image("logo.png")
    st.caption("Input the game or DLC you want and we will find the best deal for you")
    game_title = st.text_input("Game title", placeholder="Game title", key='game_title')
    platform = st.selectbox(
        "Select a platform",
        (
            "Windows",
            "MacOS",
            "Linux",
            "Switch",
            "Playstation 4",
            "Playstation 5",
            "Xbox One",
            "Xbox Series X/S",
            "GeForce Now",
        ),
        key='platform'
    )
    currency = st.selectbox("Select a currency", ("USD", "EUR"), key='currency')

    if st.button("Let's hook you up"):

        with st.spinner("Wait for it..."):
            try:
                df_steam = fetch_steam_data(
                    game_title,
                    currency,
                    platform,
                    platform_dict_steam,
                    currency_dict_steam,
                    re,
                    BeautifulSoup,
                    pd,
                )
            except Exception as e:
                st.warning("No answer from Steam", icon="⚠️")
                df_steam = pd.DataFrame()

            try:
                df_gog = fetch_gog_data(
                    game_title,
                    currency,
                    platform,
                    platform_dict_gog,
                    re,
                    pd,
                    country_dict_gog
            )

            except Exception as e:
                st.warning("No answer from GOG", icon="⚠️")
                df_gog = pd.DataFrame()
            
            try:
                df_cd_keys = fetch_cdkeys_data(
                    game_title,
                    currency,
                    re,
                    pd,
                )
            except:
                st.warning("No answer from CDKeys", icon="⚠️")
                df_cd_keys = pd.DataFrame()

            try:
                df_instant_gaming = fetch_instan_gaming_data(
                    game_title,
                    currency,
                    platform,
                    re,
                    pd,
                    BeautifulSoup,
                    platform_dict_instant_gaming,
                )
            except:
                st.warning("No answer from Instant-Gaming", icon="⚠️")
                df_instant_gaming = pd.DataFrame()

            try:
                df_epic_games = fetch_epic_games_data(
                    re,
                    pd,
                    game_title,
                    currency_dict_steam,
                    currency,
                )
            except:
                st.warning("No answer from Epic Games", icon="⚠️")
                df_epic_games = pd.DataFrame()

            try:
                df = build_final_df(
                    df_steam, df_gog, df_cd_keys, df_instant_gaming, df_epic_games, pd
                )
                st.success("Done!")
            except Exception as e:
                st.error("Offers lits couldn't be generated", icon="⚠️")
                st.info(e)

    # if st.button("Start over"):
    #     st.session_state['game_title'] = 'Reset'
    def reset_game_title():
        st.session_state.game_title = ''
        st.session_state.currency = 'USD'
        st.session_state.platform = 'Windows'
        

    if st.button('Reset Game Title', on_click=reset_game_title):
        st.info("You are all set to search again")

# Define main container for visualizations
with st.container():

    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Max price", value=df["price"].max())
        with col2:
            st.metric(label="Min price", value=df["price"].min())
        with col3:
            st.metric(label="Mean price", value=round(df["price"].mean(), 2))

    with st.container():
        col3, col4 = st.columns([4, 1])
        with col3:
            columns_to_display = ["image", "title", "price", "vendor", "link"]

            st.dataframe(
                df[columns_to_display].sort_values("price"),
                column_config={
                    "image": st.column_config.ImageColumn("Thumbnail"),
                    "title": "Game or DLC title",
                    "price": st.column_config.NumberColumn(
                        "Price",
                        help="Game or DLC price in the selected currency",
                        format="%.2f",
                    ),
                    "vendor": "Item's vendor",
                    "link": st.column_config.LinkColumn("Item's URL"),
                },
                hide_index=True,
                use_container_width=True,
                height=500,
            )
        with col4:

            grouped_data = df.groupby("vendor")["price"].mean().reset_index()
            color_scale = alt.Scale(domain=['CDKeys', 'Epic Games', 'GOG', 'Instant-Gaming', 'Steam'], range=['#58468d', '#303034', '#ab3aaf', '#ff5400', '#1b2838'])
            chart = alt.Chart(grouped_data).mark_bar().encode(
                x=alt.X("vendor:N", title='Vendor', sort=alt.EncodingSortField(field="price", order="ascending")),
                y=alt.Y("price:Q", title=f'Mean price in {currency}'),
                color=alt.Color('vendor:N', scale=color_scale, title='Vendor', legend=None)
            ).interactive()

            st.write("Prices behavior by vendor")
            st.altair_chart(chart)