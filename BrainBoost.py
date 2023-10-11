# Import libraries
import pandas as pd
import streamlit as st
from random import choice
from streamlit_extras.add_vertical_space import add_vertical_space
st.set_page_config(page_title="BrainBoost",page_icon="🧠")

def take_test(type):
    st.session_state["test"] = type

# Create a df of the questions that will be in the test
def choose_question(q,t,d,m):
    # All questions in the csv file
    all_questions = pd.DataFrame(st.session_state["questions"])

    # Questions that meet the riquirement to be in the test, complete table with all columns and possible answers 
    all_test_questions = all_questions[(all_questions["DIFFICULTY"].isin(d)) & (all_questions["TOPIC"].isin(t))]
    st.session_state["all_test_questions"] = all_test_questions
    
    # Single column table with no duplicates, just a list of the questions that will be in the test
    unique_test_questions = all_questions["QUESTION"].drop_duplicates().sample(frac=1).reset_index(drop=True).head(q)
    st.session_state["unique_test_questions"] = unique_test_questions

    # List of questions that will be in the test with all columns and rows
    test_questions = all_test_questions[all_test_questions["QUESTION"].isin(unique_test_questions)].sample(frac=1).reset_index(drop=True)
    
    # Same list as before but sorted so the correct answer stays at the top
    test_questions = test_questions.sort_values(by=["QUESTION","CORRECT ANSWER"],ascending=[True,False]).reset_index(drop=True)
    st.session_state["test_questions"] = test_questions

    # Create an empty dataframe with the same structue as test_questions
    final_test = test_questions.iloc[:0]

    # Build the questions and possible answers that will be in the test
    for question in unique_test_questions:
        q_count = (test_questions["QUESTION"] == question).sum()

        possible_answers = test_questions[test_questions["QUESTION"] == question].head(min(q_count,m))
        final_test = pd.concat([final_test,possible_answers])
    
    # Randomize the order of the questions and answers
    final_test = final_test.sample(frac=1).reset_index(drop=True)

    st.session_state["final_test"] = final_test


def check_options(q,t,d,m):
    if len(t) == 0:
        st.warning(body="You must choose at least one topic",icon="⚠️")
    elif len(d) == 0:
        st.warning(body="You must choose at least one difficulty",icon="⚠️")
    else:
        choose_question(q,t,d,m)


def main():
    st.title("BrainBoost 🧠🚀")
    st.markdown("Created with 😭 and 🩷 by [Rodrigo Ferreira](https://www.linkedin.com/in/rodrigoavf/)")

    if "placeholder" not in st.session_state:
        st.session_state["placeholder"] = st.empty()
        st.session_state["questions"] = pd.read_csv("data_mining_demo.csv",delimiter=";",encoding="utf-8")
        st.session_state["correct_text"] = ["Correct!", "Yes!", "Right!", "Spot on!", "Absolutely!"]
        st.session_state["wrong_text"] = ["Wrong!", "Nope!", "Incorrect!", "Try again!", "Not quite!"]
        st.session_state["correct_emoji"] = ["👍", "🎉", "👌", "🌟", "👏"]
        st.session_state["wrong_emoji"] = ["❌", "😞", "👎", "😭", "😢"]

    questions = pd.DataFrame(st.session_state["questions"])
    placeholder = st.session_state["placeholder"].container()

    if "test" not in st.session_state:
        with placeholder:
            st.write(
                """
                ## Study any topic with multiple choice questions
                You can choose to upload your own set of questions to be tested on
                """
            )
            with st.expander(label="How should the file I upload look like?"):
                st.write(
                    """
                    You should create a CSV file with encondig 'UTF-8' and the following 5 columns \n
                    ###### :red[Useful tip:]
                    :red[At the end] of this section you can copy a :red[ChatGPT promtp] to help you creat your CSV file. \n

                    #### :red[QUESTION]
                    Should have a list of questions that should be repeated as there are going to be multiple answers to choose from. Do not enumerate the questions.
                    
                    #### :red[ANSWERS]
                    List of answers to choose from, only one is the correct answer to the question. Do not enumerate them nor ad letters to identify them. \n
                    You can have as many answers to choose from as you wish, but only one option should be the correct one. \n
                    You will be be able to choose how many possible answers BrainBoost should display for each question.

                    #### :red[CORRECT ANSWER]
                    A boolean that tells if the answer is the correct one for the question or not.

                    #### :red[TOPIC]
                    The topic the question is about.

                    #### :red[DIFFICULTY]
                    How difficult the question is, it should be either EASY, MEDIUM or HARD.
                    """
                )
                add_vertical_space(1)
                st.write(
                    """
                    #### Your CSV file should look like this
                    """
                )
                st.download_button(label="Download CSV model",data=questions.to_csv(encoding="utf-8"),file_name="data_mining_demo.csv",type="primary")
                st.dataframe(questions,hide_index=True,use_container_width=True)

                st.write(
                    """
                    #### :red[ChatGPT Prompt]
                    - Use the prompt below in __ChatGPT__ to get a few questions formatted as BrainBoost expects
                    - :red[Amend the prompt as needed], specially where the text is ---like this---
                       - There are only 3 places where that happens
                            - ---Data Mining---
                            - ---either EASY, MEDIUM or HARD---
                            - ---10---
                    - Save the response in a CSV file enconding 'UTF-8' and upload to BrainBoost
                    """
                )
                add_vertical_space(1)
                st.write("Prompt starts below")
                st.code("""
                    Create a csv table with 5 columns QUESTION, ANSWERS, CORRECT ANSWER, TOPIC, DIFFICULTY
                    Do not make anything diferente than this structure.

                    TOPIC:
                    All rows should be: ---Data Mining---

                    DIFFICULTY:
                    The difficulty of the question, should be ---either EASY, MEDIUM or HARD---

                    QUESTION:
                    Should have a list of questions that should be repeated as there are going to be multiple answers to choose from. Do not enumerate the questions.

                    ANSWER:
                    List of answers to choose from, only one is the correct answer to the question. Do not enumerate them nor ad letters to identify them.

                    CORRECT ANSWER
                    A Boolean that tells if the answer is the correct one for the question or not.

                    Populate the table with multiple choice questions on the TOPIC defined earlier.
                    Each question must have ---10--- answers being only one of them correct.

                    Here is an example of how the table should look like:
                    QUESTION;ANSWER;CORRECT ANSWER;TOPIC;DIFFICULTY
                    What is the primary goal of data mining?;To build a database of all available data;FALSE;Data Mining;EASY
                    What is the primary goal of data mining?;To extract and transform data into reports;FALSE;Data Mining;EASY
                    What is the primary goal of data mining?;To predict future trends and behaviors;TRUE;Data Mining;EASY
                    What is the primary goal of data mining?;To store data in a secure and encrypted format;FALSE;Data Mining;EASY
                    What is the primary goal of data mining?;To create data visualizations and charts;FALSE;Data Mining;EASY
                    What is the primary goal of data mining?;To perform real-time data analysis;FALSE;Data Mining;EASY
                    What is the primary goal of data mining?;To automate data entry tasks;FALSE;Data Mining;EASY
                    What is the primary goal of data mining?;To generate random data samples;FALSE;Data Mining;EASY
                    What is the primary goal of data mining?;To design database schemas;FALSE;Data Mining;EASY
                    What is the primary goal of data mining?;To calculate mathematical constants like Pi;FALSE;Data Mining;EASY
                """,language="html")
            st.button(label="Upload set of questions",type="primary")

            st.subheader("Or...")
            st.write("You can take our sample test on Data Mining")
            st.button(label="Take sample test",type="primary", on_click=take_test("demo"))
    elif "final_test" not in st.session_state:
        if "num_questions" not in st.session_state:
            st.session_state["num_questions"] = questions["QUESTION"].nunique()

        total_questions = questions["QUESTION"].nunique()
        topics = questions["TOPIC"].drop_duplicates()
        difficulty = questions["DIFFICULTY"].drop_duplicates()

        with placeholder:
            st.write("## How would you like to be tested?")
            col1, col2 = st.columns(2)
            with col1:
                test_question = st.slider(label="Total number of questions",min_value=1,max_value=total_questions,value=total_questions)
                test_topics = st.multiselect("Topic",topics,default=topics)
                test_difficulty = st.multiselect("Topic",difficulty,default=difficulty)
                max_q_count = st.slider(label="Total number of questions",min_value=2,max_value=10,value=5)
            with col2:
                
                st.write("Your test will be composed of :red[", str(test_question), "] questions")
                add_vertical_space(3)
                st.write("The topic of the questions will be :red[", str(test_topics), "]")
                add_vertical_space(3)
                st.write("The difficulty of the questions will be :red[", str(test_difficulty), "]")
                add_vertical_space(3)
                st.write("Each question will have a maximum of :red[", str(max_q_count), "] options of answers")

            add_vertical_space(2)
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.button("START TEST",type="primary",use_container_width=True):
                    check_options(test_question,test_topics,test_difficulty,max_q_count)
                    st.rerun()

    elif "test_results" not in st.session_state:
        final_test = st.session_state["final_test"]
        unique_test_questions = st.session_state["unique_test_questions"]

        st.toggle(label=":red[Display correct answer as I answer]",key="toggle")
        add_vertical_space(1)

        for question in unique_test_questions:
            st.write("##### ", question)
            st.radio(label="",options=final_test[final_test["QUESTION"] == question]["ANSWER"],label_visibility="collapsed",key=question,index=None)
            
            if st.session_state["toggle"] & (st.session_state[question] != None):
                correct_answer = final_test.loc[final_test[(final_test["QUESTION"]==question) & final_test["CORRECT ANSWER"] == True].index[0],"ANSWER"]
                if correct_answer == st.session_state[question]:
                    st.success(body=choice(st.session_state["correct_text"]), icon=choice(st.session_state["correct_emoji"]))
                else:
                    st.error(body=choice(st.session_state["wrong_text"]),icon=choice(st.session_state["wrong_emoji"]))
                    st.write("The correct answer is: __:green[", correct_answer, "]__")
            add_vertical_space(2)
            
        st.session_state["score"] = 0
        for question in unique_test_questions:
            if final_test.loc[final_test[(final_test["QUESTION"]==question) & final_test["CORRECT ANSWER"] == True].index[0],"ANSWER"] == st.session_state[question]:
                st.session_state["score"] += 1

        
        
        with st.expander(label="Check your answers"):
            st.write("Out of ",unique_test_questions.count()," questions you got ",st.session_state["score"], " correct answers")

if __name__ == "__main__":
    main()