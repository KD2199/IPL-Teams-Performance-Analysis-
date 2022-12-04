"""
This file used for doing the analysis of ipl teams performance
"""
import time

import numpy as np
import pandas as pd
import streamlit as st
from pandas import DataFrame
from sklearn.impute import SimpleImputer

FILE_PATH = 'ipl-data.csv'


class App:

    def __init__(self, file):
        st.markdown(f"<h1 class='header-style'>IPL Teams Performance Analysis (2008-2020)</h1>",
                    unsafe_allow_html=True)
        st.markdown(
            """
            <style>
            .header-style {
                font-size:25px;
                font-family:sans-serif;
                font-weight: bold;
                color: navy;
            }
            .data-style {
                font-size:14px;
                font-family:sans-serif;
                color: red;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        self.file = file
        self.DATA = None

    @st.cache
    def fetch_data_from_csv(self) -> pd.DataFrame:
        """
        This method used to read data from csv file
        :return: Dataframe
        """
        return pd.read_csv(self.file, index_col=False)

    def fill_missing_data(self) -> None:
        """
        This method used to fill the missing values in dataframe
        :return: None
        """
        # reading file data
        df = self.fetch_data_from_csv()

        # fill-up missing categorical data
        cat_data = df.copy()
        cat_data = cat_data.select_dtypes(include='object')
        imputer = SimpleImputer(strategy='most_frequent',
                                missing_values=np.NaN)
        imputer = imputer.fit(cat_data)
        cat_data.iloc[:, :] = imputer.transform(cat_data)

        # fill-up missing numeric data
        num_data = df.copy()
        num_data = num_data.select_dtypes(exclude='object')
        imputer = SimpleImputer(strategy='constant',
                                missing_values=np.NAN, fill_value=0
                                )
        imputer = imputer.fit(num_data)
        num_data.iloc[:, :] = imputer.transform(num_data)
        merged_df = pd.concat([cat_data, num_data], axis=1)
        self.DATA = merged_df

    @staticmethod
    def show_head_to_head_analysis(choices: list, value: str, matched_played: DataFrame) -> None:
        """
        Thsi method used to show heads to head tohead data of team
        :return:
        """
        for team in choices:
            if not team == value:
                heads = matched_played.loc[
                    ((matched_played['Team1']) == team) | ((matched_played['Team2']) == team)]
                if not heads.shape[0] == 0:
                    matched_won = heads.loc[((heads['Winner']) == value)]
                    matched_lost = heads.shape[0] - matched_won.shape[0]

                    st.markdown(
                        f"<h6>{value} VS {team} ({heads.shape[0]})</h6>",
                        unsafe_allow_html=True
                    )

                    col1, col2 = st.columns(2)
                    col1.metric(f"{value}", f"{matched_won.shape[0]}", help=f"Matches Won by {value}")
                    col2.metric(f"{team}", f"{matched_lost}", help=f"Matches Won by {team}")

                    st.bar_chart(heads['POM'].value_counts())
        st.markdown(f"<hr/>", unsafe_allow_html=True)
        return None

    def teams_analysis(self):
        """
        This method used to show the details of selected franchises.
        :return:None
        """
        tab1, tab2 = st.tabs(["Compare teams", "Compare players"])
        teams = self.DATA['Team1'].unique()
        pom = self.DATA['POM'].unique()

        tab1.markdown(f"<h5>Select your favorite teams</h5>", unsafe_allow_html=True)
        choices = tab1.multiselect('Compare performance of teams', sorted(teams), help="List of teams")

        tab2.markdown(f"<h5>Select your favorite players</h5>", unsafe_allow_html=True)
        players = tab2.multiselect('Compare performance of players', sorted(pom),
                                   help="List of players won player of the match")

        if choices:
            with st.spinner('Wait for it...'):
                time.sleep(2)
                for value in choices:
                    st.markdown(
                        f"<h1 class='header-style'>{value}</h1>",
                        unsafe_allow_html=True
                    )
                    # total of matched played by team
                    matched_played = self.DATA.loc[((self.DATA['Team1']) == value) | ((self.DATA['Team2']) == value)]
                    # total of matched won by team
                    matched_won = self.DATA.loc[((self.DATA['Winner']) == value)]
                    # total of tosses won by team
                    # tosses_won = self.DATA.loc[((self.DATA['Toss(Won)']) == value)]
                    # total super overs played by team
                    # super_overs_played = self.DATA.loc[(((self.DATA['Team1']) == value) | ((self.DATA['Team2']) == value))
                    #                                    & ((self.DATA['SuperOver']) == 'Y')]
                    # winning rate of team
                    win_rate = round(((matched_won.shape[0] / matched_played.shape[0]) * 100))

                    col1, col2, col3 = st.columns(3)
                    col1.metric("Matches Played", f"{matched_played.shape[0]}", help=f"Matches Played by {value}")
                    col2.metric("Matches Won", f"{matched_won.shape[0]}", help=f"Matches Won by {value}")
                    col3.metric("Win %", f"{win_rate} %", help=f"Win % of {value}")

                    # col3.metric("Tosses Won", f"{tosses_won.shape[0]}", help=f"Tosses Won by {value}")
                    # col4.metric("Super Overs", f"{super_overs_played.shape[0]}", help=f"Super Overs Played by {value}")

                    self.show_head_to_head_analysis(choices, value, matched_played)
        if players:
            with st.spinner('Wait for it...'):
                time.sleep(2)
                for player in players:
                    pom_won_by_player = self.DATA.loc[((self.DATA['POM']) == player)]
                    st.info(f"Player of the match won by {player} : {pom_won_by_player.shape[0]}")

        st.markdown(f"<hr/>", unsafe_allow_html=True)
        st.error(f"Created By: Karan Dave")

        return None


app = App(FILE_PATH)
app.fill_missing_data()
app.teams_analysis()





