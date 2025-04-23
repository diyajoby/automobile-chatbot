import streamlit as st
from groq import Groq

# Initialize Groq client
client = Groq(api_key="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")

# Your hardcoded dataset as a string
dataset = """
Date\tDay\tSales Order (Rs)\tDelivered Orders\tRemaining Orders\tAchievement (%)\tLast Month Sales (Rs)\tStore Location\tStore Sales (Rs)\tStore Remaining (Rs)\tStore Achievement (%)\tProduct Name\tUnits Sold\tCategory\tCategory Achievement (%)\tStore Name
2023-03-20\tMon\t230000\t90\t110\t67\t1565000\tX\t699000\t73000\t91\tPlatina\t115\tCruiser\t88\tStore A
2023-03-21\tTue\t370000\t110\t90\t70\t1565000\tY\t408000\t270000\t60\tDuke 125 cc\t90\tAdventure\t65\tStore B
2023-03-22\tWed\t320000\t100\t100\t61\t1565000\tZ\t341000\t316000\t52\tPulsar 125 cc\t75\tCruiser\t88\tStore C
2023-03-23\tThu\t470000\t125\t75\t76\t1565000\tα\t201000\t405000\t33\tChetak electric\t55\tElectric\t45\tStore D
2023-03-24\tFri\t590000\t130\t70\t81\t1565000\tX\t699000\t73000\t91\tCT 125 cc\t35\tScooter\t78\tStore A
2023-03-25\tSat\t680000\t140\t60\t85\t1565000\tY\t408000\t270000\t60\tPlatina\t110\tCruiser\t88\tStore B
2023-03-26\tSun\t770000\t160\t40\t90\t1565000\tZ\t341000\t316000\t52\tDuke 125 cc\t92\tAdventure\t65\tStore C
2023-03-27\tMon\t250000\t95\t105\t63\t1565000\tα\t201000\t405000\t33\tPulsar 125 cc\t78\tCruiser\t88\tStore D
2023-03-28\tTue\t360000\t100\t100\t70\t1565000\tX\t699000\t73000\t91\tChetak electric\t50\tElectric\t45\tStore A
2023-03-29\tWed\t310000\t97\t103\t68\t1565000\tY\t408000\t270000\t60\tCT 125 cc\t40\tScooter\t78\tStore B
2023-03-30\tThu\t420000\t115\t85\t74\t1565000\tZ\t341000\t316000\t52\tPlatina\t120\tCruiser\t88\tStore C
2023-03-31\tFri\t510000\t123\t77\t79\t1565000\tα\t201000\t405000\t33\tDuke 125 cc\t88\tAdventure\t65\tStore D
2023-04-01\tSat\t620000\t135\t65\t83\t1565000\tX\t699000\t73000\t91\tPulsar 125 cc\t70\tCruiser\t88\tStore A
2023-04-02\tSun\t710000\t150\t50\t88\t1565000\tY\t408000\t270000\t60\tChetak electric\t60\tElectric\t45\tStore B
2023-04-03\tMon\t220000\t80\t120\t60\t1565000\tZ\t341000\t316000\t52\tCT 125 cc\t38\tScooter\t78\tStore C
2023-04-04\tTue\t390000\t105\t95\t71\t1565000\tα\t201000\t405000\t33\tPlatina\t112\tCruiser\t88\tStore D
2023-04-05\tWed\t300000\t90\t110\t66\t1565000\tX\t699000\t73000\t91\tDuke 125 cc\t85\tAdventure\t65\tStore A
2023-04-06\tThu\t450000\t117\t83\t75\t1565000\tY\t408000\t270000\t60\tPulsar 125 cc\t72\tCruiser\t88\tStore B
2023-04-07\tFri\t580000\t130\t70\t81\t1565000\tZ\t341000\t316000\t52\tChetak electric\t58\tElectric\t45\tStore C
2023-04-08\tSat\t670000\t142\t58\t85\t1565000\tα\t201000\t405000\t33\tCT 125 cc\t42\tScooter\t78\tStore D
"""

st.set_page_config(page_title="Automobile Sales Chatbot", page_icon="🚗")
st.title("🚗 Automobile Sales Chatbot")
st.markdown("Ask me anything about the data!")

# Session state to hold chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Chat input
user_input = st.chat_input("Ask a question about the automobile sales data...")

if user_input:
    # Show user query
    st.chat_message("user").write(user_input)

    # Construct full prompt
    full_prompt = f"""You are a professional automobile sales expert.

Here is the data:

{dataset}

Now answer this question:
{user_input}
"""

    # Streamed response
    with st.chat_message("assistant"):
        response = ""
        response_container = st.empty()

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a professional automobile sales expert."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7,
            max_completion_tokens=1024,
            top_p=1,
            stream=True,
        )

        for chunk in completion:
            delta = chunk.choices[0].delta.content
            if delta:
                response += delta
                response_container.markdown(response)

        # Save to history
        st.session_state.history.append((user_input, response))

# Show chat history
for user_msg, bot_msg in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        st.markdown(bot_msg)
