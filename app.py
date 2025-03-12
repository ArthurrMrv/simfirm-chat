import streamlit as st
import requests
from mistralai import Mistral
api_key = "2sKCAviNHHwjObwbZKFygdLRJTITyPCx"
model = "mistral-large-latest"

def main():
    # Set the title of the app
    st.title("SimFirm Helper")
    
    p_type_list = ('Get a plan of action for next round', 'Get a stratgic summary of the current round')
    p_type_nb = st.radio(
    'Which action would you like to perform',
    p_type_list
)
    
    # Add two text input fields
    text1 = st.text_input("Summary of previous rounds (optionnal)")
    text2 = st.text_input("Current round situation")
    
    # Add a button
    if st.button("Combine Texts and Send to Mistral"):
        if text2:
            if not text1:
                text1 = ""
                
            prompt = get_prompt(p_type_list.index(p_type_nb) + 1, text2, text1)
            
            client = Mistral(api_key=api_key)

            chat_response = client.chat.complete(
                model= model,
                messages = [
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ]
            )
            
            response = chat_response.choices[0].message.content
            
            st.title("Answer")
            st.write(response)
        else:
            st.write("Please enter both chunks of text.")
            
def get_prompt(p_type, round_info, hist_context = ""):
    
    if p_type == 1:
        instructions = """Based on the above context, please perform the following:
1. Situation Analysis: Identify the key strategic opportunities and risks based on the current financial, market, and operational context.
2. Strategic Decision-Making: Outline your decisions for market expansion, product focus, and operational improvements, ensuring a balance between profitability and ESG responsibilities.
3. Rationale: Provide clear reasoning for each decision, incorporating insights from historical performance, current market trends, and sustainability considerations.
4. Action Plan: Detail a concise action plan that addresses immediate challenges and outlines steps for long-term growth and market positioning.
"""
    elif p_type == 2:
        instructions = """Based on the above context, please perform the following:
Based on the above context, please perform the following:
1. Situation Analysis: Identify the key strategic opportunities and risks based on the current financial, market, and operational context.
2. Action Plan: Detail a concise action plan that addresses immediate challenges and outlines steps for long-term growth and market positioning.
3. Strategic Plan : Provide your output detailing the current situation. Presenting with bullet points in detail (1) Analysis of the different markets & products (2) Analysis of the Key Success Factors (3) Strategic Objectives (4) Your implementation Plan"""
    else:
        raise ValueError("Invalid prompt type. Please choose 1 (decision making) or 2 (round summary).")
    
    return """
    SIMFIRM SIMULATION - STRATEGIC DECISION-MAKING PROMPT
INTRODUCTION
You are a participant in a high-fidelity SimFirm simulation powered by Cesim—a global leader in online business simulation games. These simulations are designed to enhance your strategic decision-making, critical thinking, and holistic business acumen across disciplines such as marketing, finance, strategy, and sustainability. In this environment, you are expected to balance financial performance with responsible management and ESG principles.
CONTEXT: Pillsens - Strategic Decision-Making Overview
Company Overview
* Heritage & Leadership: Founded in 1865 by Erik & Anni Pillsen, built on a legacy of research-driven medicine.
* Market Focus: Strong domestic presence in Finland with a dual focus on OTC and prescription drugs.
* Current Leadership: CEO Katrine Pillsen (appointed one year ago) is focused on streamlining operations and improving profitability.
* Expansion Plans: Intent to enter the French and U.S. markets when conditions become favorable.
Financial Position
* Recent Performance: Experiencing poor financial performance with high leverage and low profitability.
* Operational Challenges: Internal inefficiencies and sensitivity to exchange rate fluctuations pose challenges for foreign market entry.
Market Landscape
* Domestic (Finland):
    * Stable market share amid rising competition.
    * Low price elasticity; price cuts have minimal impact on demand.
    * Strong reputation for high quality remains a key customer driver.
* International (France & USA):
    * Large, competitive markets; more price-sensitive consumer bases compared to Finland.
    * The U.S. market for painkillers and antioxidants is particularly expansive, while the French market may mirror similar dynamics.
    * Emerging demand in the antioxidant segment, albeit with uncertain long-term viability.
Marketing & Product Strategies
* Marketing:
    * OTC drug demand is significantly driven by advertising.
    * In Finland, maintain market presence through retailer incentives; in France and the USA, focus on expanding retail availability with strong branding and customer care.
    * Antioxidants require dynamic marketing efforts due to their responsiveness and evolving scientific discourse.
* Product Lines:
    * Painkillers:
        * Globally steady demand with targeted expansion in the U.S. and France.
        * Domestic market shows limited growth with emerging competition.
    * Antioxidants:
        * Production launch scheduled in two years.
        * Market shows growth potential, but scientific opinions and media influence demand variability.
        * Continuous product innovation is essential to maintain market relevance.
Production & Logistics
* Current Setup:
    * Painkillers are produced exclusively in Finland.
* Future Prospects:
    * Consider establishing production in the Midwestern USA to support antioxidants (and potentially painkillers).
    * In France, production is not local due to legal restrictions; reliance on exports from Finland or the USA is necessary.
* Transportation:
    * Domestic: Primarily truck cargo.
    * International: A combination of truck and maritime shipping—with maritime being more sustainable as electric truck technology evolves.
* Efficiency & Sustainability:
    * Painkiller production is efficient; improvements in antioxidant production could further reduce costs and environmental impact.
Economic & Sustainability Considerations
* Economic Outlook:
    * The U.S. shows a faster but unstable recovery, while Europe's recovery is slower despite ECB efforts.
* Sustainability:
    * Increasing consumer emphasis on ESG factors affects purchasing decisions.
    * A third-party sustainability score can enhance brand perception and customer appeal, especially when linked with certification options.
Decision-Making & Investment
* Unit Measures:
    * Sales, production, and wholesale are measured in 1,000-tablet units.
* Investment:
    * Expansion of production capacity occurs in increments of 10,000 units.

HISTORICAL CONTEXT
{}

CURRENT OBJECTIVES
{}

INSTRUCTIONS
{}""".format(hist_context, round_info, instructions)

if __name__ == "__main__":
    main()