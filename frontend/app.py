
import streamlit as st
import requests
import time

st.set_page_config(page_title="♠ Poker Win Simulator", layout="centered")
st.title("♠ Poker Win Probability Simulator")
st.markdown("Use Monte Carlo simulation to estimate your win rate in a Texas Hold'em hand.")

# Input form
with st.form("poker_form"):
    hole_input = st.text_input("🃏 Your Hole Cards (e.g. As, Kd)", "As, Kd")
    board_input = st.text_input("🃏 Community Cards (e.g. 7h, Ts, 2d)", "7h, Ts, 2d")
    sim_button = st.form_submit_button("🔥 Simulate")

if sim_button:
    hole = [card.strip() for card in hole_input.split(",") if card.strip()]
    board = [card.strip() for card in board_input.split(",") if card.strip()]

    # 💳 Show the inputted cards visually
    def display_card_row(cards, title):
        st.markdown(f"### {title}")
        cols = st.columns(len(cards) if cards else 1)
        for i, card in enumerate(cards):
            url = f"https://deckofcardsapi.com/static/img/{card.upper()}.png"
            try:
                cols[i].image(url, width=100)
            except:
                cols[i].error(f"Invalid card: {card}")

    display_card_row(hole, "🧾 Your Hand")
    display_card_row(board, "🧾 Community Cards")

    # 🎲 Simulate via backend
    payload = {"hole": hole, "board": board}

    with st.spinner("Simulating... 🧠"):
        time.sleep(0.5)  # just for effect
        try:
            res = requests.post("http://localhost:8000/simulate", json=payload)
            result = res.json()

            if "win_rate" in result:
                st.success(f"✅ Estimated Win Rate: **{result['win_rate']}%**")
                st.info(f"🤝 Tie Rate: **{result['tie_rate']}%**")

                # Pie chart visualization
                st.markdown("### 📊 Outcome Breakdown")
                st.plotly_chart({
                    "data": [{
                        "values": [result["win_rate"], result["tie_rate"], round(100 - result["win_rate"] - result["tie_rate"], 2)],
                        "labels": ["Win", "Tie", "Loss"],
                        "type": "pie"
                    }],
                    "layout": {"height": 400}
                })
            else:
                st.error(f"❌ Error: {result.get('error', 'Invalid input')}")
        except Exception as e:
            st.error("❌ Could not connect to backend. Is FastAPI running?")

