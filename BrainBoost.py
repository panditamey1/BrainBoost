# Import libraries
import pandas as pd
import streamlit as st
from random import choice
import pyperclip
from streamlit_extras.add_vertical_space import add_vertical_space
st.set_page_config(page_title="BrainBoost",page_icon="🧠")

js = '''
<script>
    var body = window.parent.document.querySelector(".main");
    console.log(body);
    body.scrollTop = 0;
</script>
'''
# Cod used to scroll to the top of the page
# simply add st.components.v1.html(js) when you need to use it

def take_test(type):
    st.session_state["test"] = type
    st.session_state["page"] = "options"
    st.rerun()
    
# Create a df of the questions that will be in the test
def choose_question(q,t,d,m):
    # All questions in the csv file
    if st.session_state["test"] == "demo":
        all_questions = pd.DataFrame(st.session_state["demo_questions"])
    else:
        all_questions = pd.DataFrame(st.session_state["upload_questions"])

    # Questions that meet the riquirement to be in the test, complete table with all columns and possible answers 
    all_test_questions = all_questions[(all_questions["DIFFICULTY"].isin(d)) & (all_questions["TOPIC"].isin(t))].copy()
    st.session_state["all_test_questions"] = all_test_questions
    
    # Single column table with no duplicates, just a list of the questions that will be in the test
    unique_test_questions = all_test_questions["QUESTION"].drop_duplicates().sample(frac=1).reset_index(drop=True).head(q).copy()
    st.session_state["unique_test_questions"] = unique_test_questions

    # List of questions that will be in the test with all columns and rows
    test_questions = all_test_questions[all_test_questions["QUESTION"].isin(unique_test_questions)].sample(frac=1).reset_index(drop=True).copy()
    
    # Same list as before but sorted so the correct answer stays at the top
    test_questions = test_questions.sort_values(by=["QUESTION","CORRECT ANSWER"],ascending=[True,False]).reset_index(drop=True).copy()
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
        st.session_state["page"] = "test"
        st.rerun()

def page_header():
    st.title("BrainBoost 🧠🚀")
    st.markdown("Created with 😭 and 🩷 by [Rodrigo Ferreira](https://www.linkedin.com/in/rodrigoavf/)")

def main():
    def page_top():
        st.components.v1.html(js)

    if "page" not in st.session_state:
        st.session_state["page"] = "home"
        st.session_state["test"] = "demo"
        st.session_state["demo_questions"] = pd.read_csv("demo_questions.csv",delimiter=";",encoding="utf-8")
        st.session_state["correct_text"] = ["Correct!", "Yes!", "Right!", "Spot on!", "Absolutely!"]
        st.session_state["wrong_text"] = ["Wrong!", "Nope!", "Incorrect!", "Try again!", "Not quite!"]
        st.session_state["correct_emoji"] = ["👍", "🎉", "👌", "🌟", "👏"]
        st.session_state["wrong_emoji"] = ["❌", "😞", "👎", "😭", "😢"]

    if st.session_state["test"] == "demo":
        questions = pd.DataFrame(st.session_state["demo_questions"])
    else:
        questions = pd.DataFrame(st.session_state["upload_questions"])

    questions.columns = [column.upper() for column in questions.columns]

    if st.session_state["page"] == "home":
        page_header()
        with st.empty().container():
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
                    You will be be able to choose how many possible answers __BrainBoost__ 🧠 should display for each question.

                    #### :red[CORRECT ANSWER]
                    A boolean that tells if the answer is the correct one for the question or not.

                    #### :red[TOPIC]
                    The topic the question is about.

                    #### :red[DIFFICULTY]
                    How difficult the question is, should ideally be either EASY, MEDIUM or HARD.
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
                    1. Use the prompt below in __ChatGPT__ to get a few questions formatted as __BrainBoost__ 🧠 expects
                    2. :red[Amend the prompt as needed], specially where the text is ---like this--- or simply remove the ---
                        - There are only 2 places where that happens
                            - ---Data Mining---
                            - ---10---
                    3. Ask ChatGPT for more questions without repeating the previous ones, so you get a larger set of questions
                    4. Save all the responses together in a CSV file enconding 'UTF-8' and upload to __BrainBoost__ 🧠
                    """
                )
                add_vertical_space(1)
                gpt_prompt = """Create a csv table with 5 columns QUESTION, ANSWERS, CORRECT ANSWER, TOPIC, DIFFICULTY
Do not make anything diferente than this structure.

TOPIC:
All rows should be: ---Data Mining---

DIFFICULTY:
The difficulty of the question, should be either EASY, MEDIUM or HARD

QUESTION:
Should have a list of questions that should be repeated as there are going to be multiple answers to choose from. Do not enumerate the questions.

ANSWER:
List of answers to choose from, only one is the correct answer to the question. Do not enumerate them nor ad letters to identify them.

CORRECT ANSWER
A Boolean that tells if the answer is the correct one for the question or not.

Populate the table with multiple choice questions on the TOPIC defined earlier.
Each question must have ---10--- answers being only one of them correct.
Use ; as the delimiter.

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
What is the primary goal of data mining?;To calculate mathematical constants like Pi;FALSE;Data Mining;EASY"""

                if st.button(label="Copy prompt to clipboard 📋",type="primary"):
                    pyperclip.copy(gpt_prompt)
                    st.success(body="Prompt copied to the clipboard! 😉")
                st.session_state["code"] = st.code(gpt_prompt,language="html")
            
            col1, col2, col3 = st.columns([3,1,1])
            with col1:
                upload_file = st.file_uploader(label="",label_visibility="collapsed",type="csv")

            if upload_file != None:
                st.session_state["upload_questions"] = pd.read_csv(upload_file,delimiter=";",encoding="utf-8")
                take_test("real")

            st.subheader("Or...")
            st.write("You can take our sample test")
            col1, col2, col3 = st.columns([3,1,1])
            with col1:
                if st.button(label="Take sample test",type="primary",use_container_width=True):
                    take_test("demo")

    elif st.session_state["page"] == "options":
        page_header()
        with st.empty().container():
            if "num_questions" not in st.session_state:
                st.session_state["num_questions"] = questions["QUESTION"].nunique()

            total_questions = questions["QUESTION"].nunique()
            topics = questions["TOPIC"].drop_duplicates()
            difficulty = questions["DIFFICULTY"].drop_duplicates()

            st.write("## How would you like to be tested?")

            test_topics = st.multiselect("Topic",topics,default=topics)
            test_difficulty = st.multiselect("Difficulty",difficulty,default=difficulty)
            max_q_count = st.slider(label="Maximun number of answers to choose from",min_value=2,max_value=10,value=5)
            total_questions = questions[(questions["TOPIC"].isin(test_topics)) & (questions["DIFFICULTY"].isin(test_difficulty))]["QUESTION"].nunique()
            if total_questions < 2:
                st.error("The options you chose leave you with less than 2 questions, please change your settings",icon="🚨")
                test_questions = []
            else:
                test_questions = st.slider(label="Total number of questions",min_value=1,max_value=total_questions,value=total_questions)

                st.write(
                    f"""
                    ### Your test
                    Your test will be composed of :red[ {str(test_questions)} questions] on :red[ {str(test_topics)} ]
                    with difficulty level :red[ {str(test_difficulty)} ].
                    Each question will have a maximum of :red[ {str(max_q_count)} ] options of answers
                    """
                )

            add_vertical_space(2)
            col1, col2, col3, col4 = st.columns([1,2,2,1])
            with col2:
                if st.button(label="Restart BrainBoost 🧠", use_container_width=True, type="primary"):
                    del st.session_state["page"]
                    try:
                        del st.session_state["final_test"]
                    except:
                        pass
                    try:
                        del st.session_state["test"]
                    except:
                        pass
                    try:
                        del st.session_state["upload_questions"]
                    except:
                        pass
                    st.rerun()

            with col3:
                if st.button(label="Start test 🚀",type="primary",use_container_width=True):
                    check_options(test_questions,test_topics,test_difficulty,max_q_count)

        page_top()

    elif st.session_state["page"] == "test":
        with st.empty().container():
            page_header()

            final_test = st.session_state["final_test"]
            unique_test_questions = st.session_state["unique_test_questions"]
            
            # For checking if the dataframes are correct, not to be displayed to the user
            if 1 == 0:
                st.write("all_test_questions")
                st.data_editor(st.session_state["all_test_questions"])

                st.write("unique_test_questions")
                st.dataframe(st.session_state["unique_test_questions"])
                
                st.write("test_questions")
                st.dataframe(st.session_state["test_questions"])

                st.write("final_test")
                st.dataframe(st.session_state["final_test"])

            st.write("#### Display options")
            col1, col2 = st.columns(2)
            with col1:
                st.toggle(label=":red[Evaluate my answer as I answer]",key="toggle_check")
                st.toggle(label=":red[Display correct answer as I answer]",key="toggle_answer")
            with col2:
                st.toggle(label=":red[Display question's topic]",key="toggle_topic")
                st.toggle(label=":red[Display question's difficulty]",key="toggle_difficulty")
            st.divider()

            for question in unique_test_questions:
                # Question header
                st.write("##### ", question)

                # Question info (toggles)
                if st.session_state["toggle_topic"]:
                    q_topic = final_test.loc[final_test[(final_test["QUESTION"]==question) & final_test["CORRECT ANSWER"] == True].index[0],"TOPIC"]
                    q_topic = f"Topic __:blue[{q_topic}]__"
                else:
                    q_topic = ""
                
                if st.session_state["toggle_difficulty"]:
                    q_difficulty = final_test.loc[final_test[(final_test["QUESTION"]==question) & final_test["CORRECT ANSWER"] == True].index[0],"DIFFICULTY"]
                    if q_difficulty == "EASY":
                        q_difficulty =  f"Difficulty __:green[ {q_difficulty} ]__"
                    elif q_difficulty == "MEDIUM":
                        q_difficulty = f"Difficulty __:orange[ {q_difficulty} ]__"
                    else:
                        q_difficulty = f"Difficulty __:red[ {q_difficulty} ]__"
                else:
                    q_difficulty = ""
                
                if (q_topic != "") & (q_difficulty != ""):
                    st.write(q_topic,"‎ ‎ ‎ | ‎ ‎ ‎",q_difficulty)
                else:
                    st.write(q_topic,q_difficulty)
                
                # Answers choice
                st.radio(label="",options=final_test[final_test["QUESTION"] == question]["ANSWER"],label_visibility="collapsed",key=question,index=None)
                
                correct_answer = final_test.loc[final_test[(final_test["QUESTION"]==question) & final_test["CORRECT ANSWER"] == True].index[0],"ANSWER"]
                if st.session_state["toggle_check"] & (st.session_state[question] != None):
                    if correct_answer == st.session_state[question]:
                        st.success(body=choice(st.session_state["correct_text"]), icon=choice(st.session_state["correct_emoji"]))
                    else:
                        st.error(body=choice(st.session_state["wrong_text"]),icon=choice(st.session_state["wrong_emoji"]))

                if st.session_state["toggle_answer"] & (st.session_state[question] != None):
                    if correct_answer != st.session_state[question]:
                        st.write("The correct answer is: __:green[", correct_answer, "]__")
                st.divider()
            
            # Score count
            st.session_state["score"] = 0
            for question in unique_test_questions:
                if final_test.loc[final_test[(final_test["QUESTION"]==question) & final_test["CORRECT ANSWER"] == True].index[0],"ANSWER"] == st.session_state[question]:
                    st.session_state["score"] += 1
            
            # Expander with the test result
            with st.expander(label="Check your answers"):
                final_score = round(st.session_state["score"]/unique_test_questions.count(),2)*100
                st.write("Out of :red[",str(unique_test_questions.count()),"] questions you got :red[",str(st.session_state["score"]), "] correct answers")
                st.write("Your score is: ", ":red[" if final_score < 60 else ":green[",str(final_score),"%]")

            add_vertical_space(2)
            col1, col2, col3, col4 = st.columns([1,2,2,1])
            # Button to retake test
            with col2:
                if st.button(label="Retake test", use_container_width=True, type="primary"):
                    st.session_state["page"] = "options"
                    st.rerun()

            # Button to restart BrainBoost
            with col3:
                if st.button(label="Restart BrainBoost 🧠", use_container_width=True, type="primary"):
                    del st.session_state["page"]
                    del st.session_state["final_test"]
                    del st.session_state["test"]
                    try:
                        del st.session_state["upload_questions"]
                    except:
                        pass
                    st.rerun()

        page_top()

if __name__ == "__main__":
    main()