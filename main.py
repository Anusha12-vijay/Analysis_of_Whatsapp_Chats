import streamlit as st
import preprocess
import help
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Pick a file to Analyse")

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocess.preprocess(data)

    #st.dataframe(df)

    #unique users

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis for", user_list)

    if st.sidebar.button("Show Analysis"):
        number_of_messages, words, num_media_messages, num_links = help.fetch_the_statistics(selected_user,df)

        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)



        with col1:
            st.markdown("### Total Messages")
            st.markdown(f"## {number_of_messages}")

        with col2:
            st.markdown("### Total Words")
            st.markdown(f"## {words}")

        with col3:
            st.markdown("### Media Shared")
            st.markdown(f"## {num_media_messages}")

        with col4:
            st.markdown("### Links Shared")
            st.markdown(f"## {num_links}")

        #monthly timeline
        st.title("Monthly Timeline")
        timeline = help.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='red')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = help.daily_timeline(selected_user, df)  # Correct function used
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='pink')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Active Day")
            active_day =help.week_activity_map(selected_user, df)
            fig, ax =plt.subplots()
            ax.bar(active_day.index, active_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Active Month")
            active_month = help.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(active_month.index, active_month.values, color = 'orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)




        #finding the most active user in the group

    if selected_user == 'Overall':
        st.title('Most Busy Users')
        x, new_df = help.fetch_active_users(df)
        fig, ax = plt.subplots()
        col1, col2 = st.columns(2)

        with col1:
            ax.bar(x.index, x.values, color='green')  # Corrected this line
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.dataframe(new_df)


    #Wordcloud
    st.title("WordCloud")
    df_wc = help.create_wordcloud(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)


    #most common words

    most_common_df = help.most_common_words(selected_user, df)

    fig, ax = plt.subplots()

    ax.barh(most_common_df[0], most_common_df[1])
    plt.xticks(rotation = 'vertical')


    st.title('Most Common Words')
    st.pyplot(fig)

    # emoji analysis
    emoji_df = help.emoji_helper(selected_user, df)
    st.title("Emoji Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig, ax = plt.subplots()
        ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
        st.pyplot(fig)









