"""Compound interest calculator page component for Streamlit Hello App."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_hello_app.components import get_plotly_dark_theme


def calculate_compound_interest(principal: float, rate: float, time: float, 
                               compounding_frequency: int = 12) -> tuple:
    """
    Calculate compound interest and related values.
    
    Args:
        principal: Initial amount (P)
        rate: Annual interest rate as decimal (r)
        time: Time in years (t)
        compounding_frequency: Number of times interest compounds per year (n)
    
    Returns:
        Tuple of (final_amount, total_interest, yearly_breakdown)
    """
    # Calculate final amount using compound interest formula
    # A = P(1 + r/n)^(nt)
    final_amount = principal * (1 + rate / compounding_frequency) ** (compounding_frequency * time)
    total_interest = final_amount - principal
    
    # Calculate yearly breakdown
    yearly_breakdown = []
    current_principal = principal
    
    for year in range(1, int(time) + 1):
        yearly_amount = current_principal * (1 + rate / compounding_frequency) ** compounding_frequency
        yearly_interest = yearly_amount - current_principal
        yearly_breakdown.append({
            'Year': year,
            'Principal': round(current_principal, 2),
            'Interest': round(yearly_interest, 2),
            'Total': round(yearly_amount, 2)
        })
        current_principal = yearly_amount
    
    # Add final year if time is not a whole number
    if time > int(time):
        remaining_time = time - int(time)
        yearly_amount = current_principal * (1 + rate / compounding_frequency) ** (compounding_frequency * remaining_time)
        yearly_interest = yearly_amount - current_principal
        yearly_breakdown.append({
            'Year': f"{int(time)}.5",
            'Principal': round(current_principal, 2),
            'Interest': round(yearly_interest, 2),
            'Total': round(yearly_amount, 2)
        })
    
    return round(final_amount, 2), round(total_interest, 2), yearly_breakdown


def render_compound_interest_calculator() -> None:
    """Render the compound interest calculator page."""
    st.header("💰 Compound Interest Calculator")
    
    st.markdown("""
    Calculate how your investments grow over time with compound interest. 
    Compound interest is the interest calculated on the initial principal and the accumulated interest of previous periods.
    """)
    
    # Input section
    st.subheader("📝 Investment Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        principal = st.number_input(
            "Initial Amount ($)",
            min_value=0.0,
            value=10000.0,
            step=100.0,
            help="The initial amount of money you're investing"
        )
        
        annual_rate = st.number_input(
            "Annual Interest Rate (%)",
            min_value=0.0,
            max_value=100.0,
            value=7.0,
            step=0.1,
            help="Annual interest rate as a percentage"
        )
        
        time_period = st.number_input(
            "Time Period (years)",
            min_value=0.0,
            value=10.0,
            step=0.5,
            help="Number of years to invest"
        )
    
    with col2:
        compounding_freq = st.selectbox(
            "Compounding Frequency",
            options=[
                (1, "Annually"),
                (2, "Semi-annually"),
                (4, "Quarterly"),
                (12, "Monthly"),
                (52, "Weekly"),
                (365, "Daily")
            ],
            format_func=lambda x: x[1],
            index=3,  # Default to monthly
            help="How often interest is compounded"
        )[0]
        
        monthly_contribution = st.number_input(
            "Monthly Contribution ($)",
            min_value=0.0,
            value=0.0,
            step=50.0,
            help="Additional amount to add each month (optional)"
        )
    
    # Calculate results
    if st.button("Calculate", type="primary"):
        if principal > 0 and annual_rate >= 0 and time_period > 0:
            # Convert percentage to decimal
            rate_decimal = annual_rate / 100
            
            # Calculate compound interest
            final_amount, total_interest, yearly_breakdown = calculate_compound_interest(
                principal, rate_decimal, time_period, compounding_freq
            )
            
            # Display results
            st.subheader("📊 Results")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="Initial Investment",
                    value=f"${principal:,.2f}",
                    help="Your starting amount"
                )
            
            with col2:
                st.metric(
                    label="Final Amount",
                    value=f"${final_amount:,.2f}",
                    delta=f"${total_interest:,.2f}",
                    help="Total amount after compound interest"
                )
            
            with col3:
                st.metric(
                    label="Total Interest Earned",
                    value=f"${total_interest:,.2f}",
                    delta=f"{((final_amount / principal - 1) * 100):.1f}%",
                    help="Total interest earned over the time period"
                )
            
            # Create visualizations
            st.subheader("📈 Investment Growth Visualization")
            
            # Prepare data for charts
            years = [item['Year'] for item in yearly_breakdown]
            principals = [item['Principal'] for item in yearly_breakdown]
            interests = [item['Interest'] for item in yearly_breakdown]
            totals = [item['Total'] for item in yearly_breakdown]
            
            # Create growth chart
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                # Line chart showing growth over time
                theme_config = get_plotly_dark_theme()
                
                fig_line = go.Figure()
                fig_line.add_trace(go.Scatter(
                    x=years,
                    y=totals,
                    mode='lines+markers',
                    name='Total Value',
                    line=dict(color='#4ECDC4', width=3),
                    marker=dict(size=8)
                ))
                
                fig_line.update_layout(
                    title="Investment Growth Over Time",
                    xaxis_title="Year",
                    yaxis_title="Amount ($)",
                    **theme_config["layout"]
                )
                
                st.plotly_chart(fig_line, config={'displayModeBar': False})
            
            with chart_col2:
                # Pie chart showing principal vs interest
                theme_config = get_plotly_dark_theme()
                
                fig_pie = go.Figure(data=[go.Pie(
                    labels=['Initial Principal', 'Interest Earned'],
                    values=[principal, total_interest],
                    marker_colors=['#FF6B6B', '#4ECDC4'],
                    textinfo='label+percent+value'
                )])
                
                fig_pie.update_layout(
                    title="Composition of Final Amount",
                    **theme_config["layout"]
                )
                
                st.plotly_chart(fig_pie, config={'displayModeBar': False})
            
            # Yearly breakdown table
            st.subheader("📋 Year-by-Year Breakdown")
            
            # Create DataFrame for the table
            breakdown_df = pd.DataFrame(yearly_breakdown)
            
            # Format the DataFrame for better display
            breakdown_df['Principal'] = breakdown_df['Principal'].apply(lambda x: f"${x:,.2f}")
            breakdown_df['Interest'] = breakdown_df['Interest'].apply(lambda x: f"${x:,.2f}")
            breakdown_df['Total'] = breakdown_df['Total'].apply(lambda x: f"${x:,.2f}")
            
            st.dataframe(
                breakdown_df,
                width='stretch',
                hide_index=True
            )
            
            # Summary insights
            st.subheader("💡 Key Insights")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.info(f"""
                **Compound Interest Impact:**
                - Your money grew by **{((final_amount / principal - 1) * 100):.1f}%** over {time_period} years
                - Interest earned represents **{(total_interest / final_amount * 100):.1f}%** of your final amount
                - Average annual return: **{(((final_amount / principal) ** (1/time_period) - 1) * 100):.1f}%**
                """)
            
            with col2:
                st.success(f"""
                **Time Value of Money:**
                - Every dollar invested today becomes **${final_amount/principal:.2f}** in {time_period} years
                - The power of compounding: Interest on interest effect
                - Your money worked for you for {time_period * 12:.0f} months
                """)
            
            # Download results
            st.subheader("💾 Download Results")
            
            # Create downloadable CSV
            csv_data = breakdown_df.copy()
            csv_data['Year'] = csv_data['Year'].astype(str)
            csv_data['Principal'] = csv_data['Principal'].str.replace('$', '').str.replace(',', '').astype(float)
            csv_data['Interest'] = csv_data['Interest'].str.replace('$', '').str.replace(',', '').astype(float)
            csv_data['Total'] = csv_data['Total'].str.replace('$', '').str.replace(',', '').astype(float)
            
            csv = csv_data.to_csv(index=False)
            
            st.download_button(
                label="📥 Download Yearly Breakdown as CSV",
                data=csv,
                file_name=f"compound_interest_breakdown_{time_period}yrs_{annual_rate}pct.csv",
                mime="text/csv"
            )
            
        else:
            st.error("Please enter valid values for all fields.")
    
    # Educational content
    st.markdown("---")
    st.subheader("🎓 Understanding Compound Interest")
    
    with st.expander("What is Compound Interest?"):
        st.markdown("""
        **Compound interest** is the interest calculated on the initial principal and the accumulated interest of previous periods.
        
        **Formula:** A = P(1 + r/n)^(nt)
        
        Where:
        - A = Final amount
        - P = Principal amount
        - r = Annual interest rate (as decimal)
        - n = Number of times interest compounds per year
        - t = Time in years
        
        **Key Benefits:**
        - Interest earns interest (the "snowball effect")
        - Time is your greatest ally
        - Small amounts can grow significantly over long periods
        """)
    
    with st.expander("Tips for Maximizing Compound Interest"):
        st.markdown("""
        **Start Early:** The earlier you start investing, the more time compound interest has to work.
        
        **Consistent Contributions:** Regular monthly contributions accelerate growth.
        
        **Higher Interest Rates:** Even small increases in interest rates can make significant differences over time.
        
        **Reinvest Dividends:** Don't withdraw interest - let it compound.
        
        **Long-term Perspective:** Compound interest works best over long time horizons.
        """)
    
    with st.expander("Common Compounding Frequencies"):
        st.markdown("""
        - **Daily (365 times/year):** Most frequent, highest growth
        - **Weekly (52 times/year):** Very frequent compounding
        - **Monthly (12 times/year):** Common for savings accounts
        - **Quarterly (4 times/year):** Common for bonds and CDs
        - **Semi-annually (2 times/year):** Some bonds and savings products
        - **Annually (1 time/year):** Least frequent, lowest growth
        """)
