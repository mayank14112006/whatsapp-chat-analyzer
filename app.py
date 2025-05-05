import streamlit as st
import preprocessing,HELPER
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title('whatsapp-chat-analyzer')
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")


    df=preprocessing.preprocess(data)


    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("show analysis with respect to",user_list)
    if st.sidebar.button("Show Analysis"):

        num_messages,words,num_media_messages,num_link=HELPER.fetch_stats(selected_user,df)
        st.title("Top Stats")
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("TOTAL MESSAGES")
            st.title(num_messages)
        with col2:
            st.header("TOTAL words")
            st.title(words)
        with col3:
            st.header("TOTAL media ")
            st.title(num_media_messages)
        with col4:
            st.header("TOTAL links ")
            st.title(num_link)


        st.title("Monthly Timeline")
        timeline = HELPER.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Daily Timeline")
        daily_timeline =HELPER.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)



        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = HELPER.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = HELPER.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = HELPER.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        if selected_user=="Overall":
            st.title("Most Busy Users")
            x,new_df=HELPER.most_busy_user(df)
            fig,ax=plt.subplots()
            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        temp = df[df['user'] != 'group_notification']
        temp = temp[temp['message'] != '<Media omitted>\n']

        df_wc=HELPER.create_wordcloud(selected_user,df)
        st.title("Word Cloud")
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)



        most_common_df = HELPER.most_common_words(selected_user,df)

        fig,ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most commmon words')
        st.pyplot(fig)
        emoji_df = HELPER.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)




