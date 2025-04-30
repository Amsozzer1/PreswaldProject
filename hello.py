from preswald import text, plotly, connect, get_df, table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

THEME_COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'positive': '#2ca02c',
    'negative': '#d62728',
    'neutral': '#7f7f7f',
    'background': '#f8f9fa'
}

CHART_TEMPLATE = 'plotly_white'
GENDER_COLORS = {"Male": THEME_COLORS['primary'], "Female": THEME_COLORS['secondary']}

text("# Student Performance Analysis Dashboard")
text("An analysis of factors influencing academic performance based on data from 1,000 students.")

df = pd.read_csv('/home/ahmed/Apply/my_project/data/student_habits_performance.csv')

def create_kpi_section():
    total_students = len(df)
    avg_score = df['exam_score'].mean()
    max_score = df['exam_score'].max()
    pass_rate = len(df[df['exam_score'] >= 60]) / total_students * 100
    
    text("## Key Performance Indicators")
    text(f"Total Students: {total_students}")
    text(f"Average Exam Score: {avg_score:.1f}")
    text(f"Maximum Score: {max_score:.1f}")
    text(f"Pass Rate: {pass_rate:.1f}%")

def create_demographics():
    text("## Student Demographics")
    
    demographics_fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "pie"}, {"type": "histogram"}]],
        subplot_titles=("Gender Distribution", "Age Distribution")
    )
    
    gender_counts = df['gender'].value_counts()
    demographics_fig.add_trace(
        go.Pie(
            labels=gender_counts.index, 
            values=gender_counts.values,
            marker=dict(colors=[GENDER_COLORS["Male"], GENDER_COLORS["Female"]]),
            textinfo='percent+label',
            hole=0.4,
        ),
        row=1, col=1
    )
    
    demographics_fig.add_trace(
        go.Histogram(
            x=df['age'],
            marker=dict(color=THEME_COLORS['primary'], opacity=0.7),
            nbinsx=10,
        ),
        row=1, col=2
    )
    
    demographics_fig.update_layout(
        height=400,
        template=CHART_TEMPLATE,
        showlegend=False,
        margin=dict(t=50, b=30, l=30, r=30),
        font=dict(family="Arial, Helvetica, sans-serif")
    )
    
    demographics_fig.update_xaxes(title_text="Age", row=1, col=2)
    demographics_fig.update_yaxes(title_text="Number of Students", row=1, col=2)
    
    plotly(demographics_fig)

def create_academic_performance():
    text("## Academic Performance Distribution")
    
    score_fig = go.Figure()
    score_fig.add_trace(go.Histogram(
        x=df['exam_score'],
        marker=dict(color=THEME_COLORS['primary'], opacity=0.7),
        nbinsx=20,
        name="Score Distribution"
    ))
    
    score_fig.add_vline(
        x=df['exam_score'].mean(), 
        line=dict(dash="dash", color=THEME_COLORS['secondary']),
        annotation=dict(text="Mean", font=dict(size=12), bgcolor="white")
    )
    
    score_fig.add_vline(
        x=df['exam_score'].median(), 
        line=dict(dash="dot", color=THEME_COLORS['neutral']),
        annotation=dict(text="Median", font=dict(size=12), bgcolor="white")
    )
    
    score_fig.update_layout(
        title=None,
        xaxis_title="Exam Score",
        yaxis_title="Number of Students",
        template=CHART_TEMPLATE,
        showlegend=False,
        font=dict(family="Arial, Helvetica, sans-serif"),
        margin=dict(l=40, r=40, t=20, b=40)
    )
    
    plotly(score_fig)
    
    text(f"Mean Score: {df['exam_score'].mean():.2f}")
    text(f"Median Score: {df['exam_score'].median():.2f}")
    text(f"Standard Deviation: {df['exam_score'].std():.2f}")

def create_study_analysis():
    text("## Study Habits Impact Analysis")
    
    study_fig = px.scatter(
        df, 
        x='study_hours_per_day', 
        y='exam_score',
        color='gender',
        color_discrete_map=GENDER_COLORS,
        size='attendance_percentage',
        size_max=15,
        hover_data=['age', 'sleep_hours'],
        opacity=0.75,
        labels={
            'study_hours_per_day': 'Study Hours Per Day',
            'exam_score': 'Exam Score',
            'attendance_percentage': 'Attendance %'
        }
    )
    
    x = df['study_hours_per_day']
    y = df['exam_score']
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    
    study_fig.add_trace(
        go.Scatter(
            x=np.sort(x.unique()),
            y=p(np.sort(x.unique())),
            mode='lines',
            name='Trend',
            line=dict(color=THEME_COLORS['neutral'], width=2, dash='dash')
        )
    )
    
    study_corr = df['study_hours_per_day'].corr(df['exam_score'])
    
    study_fig.update_layout(
        title=f"Study Hours vs. Exam Score (Correlation: {study_corr:.3f})",
        xaxis_title="Study Hours Per Day",
        yaxis_title="Exam Score",
        template=CHART_TEMPLATE,
        legend_title="Gender",
        font=dict(family="Arial, Helvetica, sans-serif"),
        margin=dict(l=40, r=40, t=50, b=40)
    )
    
    plotly(study_fig)
    
    study_groups = df.groupby(df['study_hours_per_day'].round())['exam_score'].mean().reset_index()
    study_groups.columns = ['Study Hours (Rounded)', 'Average Exam Score']
    
    study_bar_fig = px.bar(
        study_groups, 
        x='Study Hours (Rounded)',
        y='Average Exam Score',
        text_auto='.1f',
        color='Average Exam Score',
        color_continuous_scale='Blues',
        labels={
            'Study Hours (Rounded)': 'Study Hours Per Day',
            'Average Exam Score': 'Average Exam Score'
        }
    )
    
    study_bar_fig.update_traces(textposition='outside')
    study_bar_fig.update_layout(
        title="Average Exam Score by Study Hours",
        xaxis_title="Study Hours Per Day",
        yaxis_title="Average Exam Score",
        template=CHART_TEMPLATE,
        font=dict(family="Arial, Helvetica, sans-serif"),
        margin=dict(l=40, r=40, t=50, b=40),
        coloraxis_showscale=False
    )
    
    plotly(study_bar_fig)
    
    text("As study hours increase, there is a clear positive trend in exam scores, highlighting the importance of dedicated study time in academic success.")

def create_lifestyle_analysis():
    text("## Lifestyle Factors Analysis")
    
    lifestyle_fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Sleep Hours vs. Exam Score", 
            "Social Media Hours vs. Exam Score",
            "Mental Health Rating vs. Exam Score",
            "Part-time Job Impact"
        ),
        vertical_spacing=0.12,
        horizontal_spacing=0.08
    )
    
    # Sleep Hours
    lifestyle_fig.add_trace(
        go.Scatter(
            x=df['sleep_hours'],
            y=df['exam_score'],
            mode='markers',
            marker=dict(
                color=df['sleep_hours'],
                colorscale='Blues',
                size=8,
                opacity=0.7,
                showscale=False
            ),
            name="Sleep Hours"
        ),
        row=1, col=1
    )
    
    # Add trend line for sleep
    x_sleep = df['sleep_hours']
    y = df['exam_score']
    z_sleep = np.polyfit(x_sleep, y, 1)
    p_sleep = np.poly1d(z_sleep)
    lifestyle_fig.add_trace(
        go.Scatter(
            x=[x_sleep.min(), x_sleep.max()],
            y=[p_sleep(x_sleep.min()), p_sleep(x_sleep.max())],
            mode='lines',
            line=dict(color=THEME_COLORS['neutral'], width=2, dash='dash'),
            showlegend=False
        ),
        row=1, col=1
    )
    
    # Social Media Hours
    lifestyle_fig.add_trace(
        go.Scatter(
            x=df['social_media_hours'],
            y=df['exam_score'],
            mode='markers',
            marker=dict(
                color=df['social_media_hours'],
                colorscale='Reds',
                size=8,
                opacity=0.7,
                showscale=False
            ),
            name="Social Media"
        ),
        row=1, col=2
    )
    
    # Add trend line for social media
    x_social = df['social_media_hours']
    z_social = np.polyfit(x_social, y, 1)
    p_social = np.poly1d(z_social)
    lifestyle_fig.add_trace(
        go.Scatter(
            x=[x_social.min(), x_social.max()],
            y=[p_social(x_social.min()), p_social(x_social.max())],
            mode='lines',
            line=dict(color=THEME_COLORS['neutral'], width=2, dash='dash'),
            showlegend=False
        ),
        row=1, col=2
    )
    
    # Mental Health Rating
    mental_health_groups = df.groupby('mental_health_rating')['exam_score'].mean().reset_index()
    lifestyle_fig.add_trace(
        go.Bar(
            x=mental_health_groups['mental_health_rating'],
            y=mental_health_groups['exam_score'],
            marker_color=THEME_COLORS['positive'],
            name="Mental Health"
        ),
        row=2, col=1
    )
    
    # Part-time Job Impact
    job_groups = df.groupby('part_time_job')['exam_score'].mean().reset_index()
    lifestyle_fig.add_trace(
        go.Bar(
            x=job_groups['part_time_job'],
            y=job_groups['exam_score'],
            marker_color=[THEME_COLORS['primary'], THEME_COLORS['secondary']],
            text=job_groups['exam_score'].round(1),
            textposition='outside',
            name="Part-time Job"
        ),
        row=2, col=2
    )
    
    # Update axes
    lifestyle_fig.update_xaxes(title_text="Sleep Hours", row=1, col=1)
    lifestyle_fig.update_yaxes(title_text="Exam Score", row=1, col=1)
    
    lifestyle_fig.update_xaxes(title_text="Social Media Hours", row=1, col=2)
    lifestyle_fig.update_yaxes(title_text="Exam Score", row=1, col=2)
    
    lifestyle_fig.update_xaxes(title_text="Mental Health Rating (1-10)", row=2, col=1)
    lifestyle_fig.update_yaxes(title_text="Average Exam Score", row=2, col=1)
    
    lifestyle_fig.update_xaxes(title_text="Has Part-time Job", row=2, col=2)
    lifestyle_fig.update_yaxes(title_text="Average Exam Score", row=2, col=2)
    
    # Update layout
    lifestyle_fig.update_layout(
        height=800,
        template=CHART_TEMPLATE,
        showlegend=False,
        font=dict(family="Arial, Helvetica, sans-serif"),
        margin=dict(t=60, b=40, l=40, r=40)
    )
    
    plotly(lifestyle_fig)
    
    sleep_corr = df['sleep_hours'].corr(df['exam_score'])
    social_corr = df['social_media_hours'].corr(df['exam_score'])
    mental_corr = df['mental_health_rating'].corr(df['exam_score'])
    
    text("Key Lifestyle Correlations:")
    text(f"• Sleep Hours: {sleep_corr:.3f}")
    text(f"• Social Media Hours: {social_corr:.3f}")
    text(f"• Mental Health Rating: {mental_corr:.3f}")

def create_correlation_analysis():
    text("## Key Factors Correlation Analysis")
    
    correlation_factors = [
        'study_hours_per_day', 'sleep_hours', 'attendance_percentage', 
        'social_media_hours', 'netflix_hours', 'mental_health_rating', 
        'exercise_frequency', 'age'
    ]
    
    correlations = []
    for factor in correlation_factors:
        corr = df[factor].corr(df['exam_score'])
        correlations.append({
            'Factor': factor.replace('_', ' ').title(),
            'Correlation': corr,
            'Direction': 'Positive' if corr >= 0 else 'Negative'
        })
    
    corr_df = pd.DataFrame(correlations)
    corr_df = corr_df.sort_values('Correlation', ascending=False)
    
    corr_fig = px.bar(
        corr_df, 
        y='Factor', 
        x='Correlation',
        color='Direction',
        color_discrete_map={'Positive': THEME_COLORS['positive'], 'Negative': THEME_COLORS['negative']},
        orientation='h',
        text='Correlation',
        labels={
            'Factor': 'Student Factor',
            'Correlation': 'Correlation with Exam Score'
        }
    )
    
    corr_fig.update_layout(
        xaxis=dict(
            title='Correlation Coefficient',
            gridcolor='#EEEEEE',
            range=[-1, 1],
            zeroline=True,
            zerolinecolor=THEME_COLORS['neutral'],
            zerolinewidth=1
        ),
        yaxis=dict(title='Factor', autorange="reversed"),
        template=CHART_TEMPLATE,
        legend_title="Direction",
        font=dict(family="Arial, Helvetica, sans-serif"),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    corr_fig.update_traces(
        texttemplate='%{text:.3f}',
        textposition='outside'
    )
    
    plotly(corr_fig)

def create_comparative_analysis():
    text("## Comparative Analysis: High vs. Low Performers")
    
    high_performers = df[df['exam_score'] > 90]
    middle_performers = df[(df['exam_score'] >= 50) & (df['exam_score'] <= 90)]
    low_performers = df[df['exam_score'] < 50]
    
    comparative_data = []
    
    for factor in ['study_hours_per_day', 'sleep_hours', 'attendance_percentage', 
                  'social_media_hours', 'mental_health_rating', 'exercise_frequency']:
        comparative_data.append({
            'Factor': factor.replace('_', ' ').title(),
            'High Performers': high_performers[factor].mean(),
            'Middle Performers': middle_performers[factor].mean(),
            'Low Performers': low_performers[factor].mean()
        })
    
    comp_df = pd.DataFrame(comparative_data)
    
    # Reshape for plotting
    plot_df = pd.melt(
        comp_df, 
        id_vars=['Factor'], 
        value_vars=['High Performers', 'Middle Performers', 'Low Performers'],
        var_name='Performance Group', 
        value_name='Average Value'
    )
    
    comp_fig = px.bar(
        plot_df,
        x='Factor',
        y='Average Value',
        color='Performance Group',
        barmode='group',
        color_discrete_map={
            'High Performers': THEME_COLORS['positive'],
            'Middle Performers': THEME_COLORS['neutral'],
            'Low Performers': THEME_COLORS['negative']
        },
        labels={'Average Value': 'Average Value'}
    )
    
    comp_fig.update_layout(
        title="Comparison of Factors by Performance Level",
        xaxis_title=None,
        yaxis_title="Average Value",
        template=CHART_TEMPLATE,
        legend_title="Performance Group",
        font=dict(family="Arial, Helvetica, sans-serif"),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    plotly(comp_fig)
    
    text("Insights from Comparative Analysis:")
    text("• High performers average nearly 3x more study hours than low performers")
    text("• Mental health ratings show a consistent increase with performance level")
    text("• High performers have significantly better attendance records")
    text("• Social media usage is inversely related to performance")

def create_data_explorer():
    text("## Data Explorer")
    text("Sample of student records from the dataset:")
    table(df.head(10))

def create_recommendations():
    text("## Recommendations for Academic Success")
    text("Based on our data analysis, we recommend the following strategies to improve academic performance:")
    text("1. **Dedicate Consistent Study Time:** 4+ hours of daily study strongly correlates with top performance")
    text("2. **Prioritize Mental Wellbeing:** Higher mental health ratings show significant positive impact")
    text("3. **Maintain Regular Attendance:** Attendance percentage is a key predictor of success")
    text("4. **Manage Digital Distractions:** Limit social media and streaming consumption")
    text("5. **Ensure Adequate Sleep:** Balanced sleep patterns support better academic outcomes")

def main():
    create_kpi_section()
    create_demographics()
    create_academic_performance()
    create_study_analysis()
    create_lifestyle_analysis()
    create_correlation_analysis()
    create_comparative_analysis()
    create_data_explorer()
    create_recommendations()
    

main()