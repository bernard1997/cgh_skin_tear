# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 14:21:30 2025

@author: cqmsxh
"""

import streamlit as st
import pandas as pd
import datetime as datetime

# Set page configuration
st.set_page_config(
    page_title="Skin Tear Risk Assessment",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        padding: 20px;
    }
    .stButton>button {
        width: 100%;
    }
    .risk-high {
        color: #ff4b4b;
        font-weight: bold;
    }
    .risk-medium {
        color: #ffa600;
        font-weight: bold;
    }
    .risk-low {
        color: #00cc00;
        font-weight: bold;
    }
    div.row-widget.stRadio > div {
        flex-direction: row;
        align-items: center;
    }
    div.row-widget.stRadio > div > label {
        margin: 0 10px;
    }
    </style>
""", unsafe_allow_html=True)


# # Initialize session state for form data
# if 'form_data' not in st.session_state:
#     st.session_state.form_data = pd.DataFrame(
#         columns=['case_no', 'assessment_date', 'risk_factors', 'risk_category']
#     )

def calculate_risk_category(risk_factors_dict):
    """
    Calculate risk category based on specific conditions:
    - No risk factors = No Risk
    - Impaired visual OR Impaired mobility OR ADL-dependent OR Extreme age OR Previous skin tear = High Risk
    - All other cases = At Risk
    """
    # Convert 'Yes' to True and 'No' to False
    bool_factors = {k: (v == 'Yes') for k, v in risk_factors_dict.items()}
    
    # Count total risk factors
    total_risks = sum(1 for value in bool_factors.values() if value)
    
    if total_risks == 0:
        return "No Risk"
    elif (bool_factors['q5'] or 
          bool_factors['q9'] or 
          bool_factors['q10'] or
          bool_factors['q12'] or
          bool_factors['q14']):
        return "High Risk"
    else:
        return "At Risk"

def main():
    st.title("Skin Tear Risk Assessment")

    # Patient Information
    st.subheader("Patient Information")
    col1, col2 = st.columns(2)
    with col1:
        case_no = st.text_input("Case Number")
    with col2:
        assessment_date = st.date_input("Assessment Date", format="DD/MM/YYYY")

    # Risk Factors Assessment
    st.subheader("Risk Factors Assessment")
    
    # General Health
    st.markdown("##### General Health")
    col1, col2 = st.columns(2)
    with col1:
        chronic_disease = st.radio("Chronic/critical disease", options=['Yes', 'No'], index=None)
        impaired_cognitive = st.radio("Impaired cognitive", options=['Yes', 'No'], index=None)
        impaired_visual = st.radio("Impaired visual", options=['Yes', 'No'], index=None)
        impaired_nutrition = st.radio("Impaired nutrition", options=['Yes', 'No'], index=None)
    with col2:
        polypharmacy = st.radio("Polypharmacy", options=['Yes', 'No'], index=None)
        impaired_sensory = st.radio("Impaired sensory", options=['Yes', 'No'], index=None)
        impaired_auditory = st.radio("Impaired auditory", options=['Yes', 'No'], index=None)

    # Mobility
    st.markdown("##### Mobility")
    col1, col2 = st.columns(2)
    with col1:
        history_falls = st.radio("History of falls", options=['Yes', 'No'], index=None)
        adl_dependent = st.radio("ADL-dependent", options=['Yes', 'No'], index=None)
    with col2:
        impaired_mobility = st.radio("Impaired mobility", options=['Yes', 'No'], index=None)
        mechanical_trauma = st.radio("Mechanical trauma", options=['Yes', 'No'], index=None)

    # Skin Assessment
    st.markdown("##### Skin")
    col1, col2 = st.columns(2)
    with col1:
        extreme_age = st.radio("Extremes of age (>= 85 years old)", options=['Yes', 'No'], index=None)
        previous_skin_tear = st.radio("Previous skin tear", options=['Yes', 'No'], index=None)
    with col2:
        fragile_skin = st.radio("Fragile skin", options=['Yes', 'No'], index=None)

    # Submit button
    if st.button("Submit Assessment"):
        if not case_no:
            st.error("Please enter a Case Number")
        elif None in [chronic_disease, polypharmacy, impaired_cognitive, impaired_sensory,
                    impaired_visual, impaired_auditory, impaired_nutrition, history_falls,
                    impaired_mobility, adl_dependent, mechanical_trauma, extreme_age,
                    fragile_skin, previous_skin_tear]:
            st.error("Please answer all risk factor questions")
        else:
            # Collect all risk factors in a dictionary
            risk_factors = {
                'q1': chronic_disease,
                'q2': polypharmacy,
                'q3': impaired_cognitive,
                'q4': impaired_sensory,
                'q5': impaired_visual,
                'q6': impaired_auditory,
                'q7': impaired_nutrition,
                'q8': history_falls,
                'q9': impaired_mobility,
                'q10': adl_dependent,
                'q11': mechanical_trauma,
                'q12': extreme_age,
                'q13': fragile_skin,
                'q14': previous_skin_tear
            }
            
            # Calculate risk category
            risk_category = calculate_risk_category(risk_factors)
            
            # # Count total 'Yes' responses
            # total_yes = sum(1 for value in risk_factors.values() if value == 'Yes')
            
            # # Save to session state
            # new_data = pd.DataFrame({
            #     'case_no': [case_no],
            #     'assessment_date': [assessment_date],
            #     'risk_factors': [total_yes],
            #     'risk_category': [risk_category]
            # })
            
            # st.session_state.form_data = pd.concat(
            #     [st.session_state.form_data, new_data],
            #     ignore_index=True
            # )
            
            # Set form_submitted to True
            st.session_state.form_submitted = True

            # Show results
            st.success("Assessment submitted successfully!")
            
            st.markdown("### Assessment Results")
            st.markdown(f"**Case Number:** {case_no}")
            st.markdown(f"**Assessment Date:** {assessment_date.strftime('%d/%m/%Y')}")
            
            # Display risk category with appropriate styling
            if risk_category == "High Risk":
                st.markdown(f'<p class="risk-high">Risk Category: {risk_category}</p>', unsafe_allow_html=True)
                st.markdown("")
                st.markdown("""
                ##### Objective data:
                Patient is at high risk for skin tear
                """)
                st.markdown("")
                st.markdown("""
                ##### Nursing problem list:
                Risk for Impaired skin integrity
                """)
                st.markdown("")
                st.markdown("""
                ##### Plan:
                To prevent skin break down
                """)
                st.markdown("")
                st.markdown("""
                ##### Intervention:
                """)
                st.markdown("""Continue skin assessment""")
                st.markdown("""Identify change of skin condition""")
                st.markdown("""Inform team Dr and family member""")
                st.markdown("""Re-apply the wrist tag at lower risk area""")
                st.markdown("""Implement Skin Tear Prevention Care Bundle""")
                st.markdown("""Skin care education to caregiver""")
                st.markdown("")
                st.markdown("""
                ##### Evaluation:
                Indicate patient's skin condition at the end of the shift
                """)
            elif risk_category == "At Risk":
                st.markdown(f'<p class="risk-medium">Risk Category: {risk_category}</p>', unsafe_allow_html=True)
                st.markdown("")
                st.markdown("""
                ##### Objective data:
                Patient is at risk for skin tear
                """)
                st.markdown("")
                st.markdown("""
                ##### Nursing problem list:
                Risk for Impaired skin integrity
                """)
                st.markdown("")
                st.markdown("""
                ##### Plan:
                To prevent skin break down
                """)
                st.markdown("")
                st.markdown("""
                ##### Intervention:
                """)
                st.markdown("""Continue skin assessment""")
                st.markdown("""Identify change of skin condition""")
                st.markdown("""Inform team Dr and family member""")
                st.markdown("""Re-apply the wrist tag at lower risk area""")
                st.markdown("""Implement Skin Tear Prevention Care Bundle""")
                st.markdown("""Skin care education to caregiver""")
                st.markdown("")
                st.markdown("""
                ##### Evaluation:
                Indicate patient's skin condition at the end of the shift
                """)
            else:
                st.markdown(f'<p class="risk-low">Risk Category: {risk_category}</p>', unsafe_allow_html=True)
                st.markdown("")
                st.markdown("""
                ###### Objective data:
                Patient has no risk for skin tear  
                """)
                st.markdown("")
                st.markdown("""
                ###### Nursing problem list:
                N.A.
                """)
                st.markdown("")
                st.markdown("""
                ###### Note:
                Upon admission/transfer in, if patient has no risk for skin tear, indicate the date of assessment and finding in special mention.
                """)

if __name__ == "__main__":
    main()
