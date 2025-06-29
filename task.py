from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent

from agents import doctor, verifier,nutritionist,exercise_specialist
from tools import search_tool, blood_test_tool
## Creating a task to help solve user's query
verification = Task(
    description=(
        "Read and validate the blood test report PDF file. "
        "IMPORTANT: Use the blood test tool with the exact file path provided in the crew inputs. "
        "The file path will be available as {file_path} in the crew inputs. "
        "Verify if it's a valid blood test report by checking for common biomarkers. "
        "User query context: {query}"
    ),
    expected_output=(
        "Document validation result including:\n"
        "- Whether the document is valid (Valid/Invalid/Uncertain)\n"
        "- Key biomarkers identified\n"
        "- Any formatting issues found\n"
        "- Raw report data for next agents"
    ),
    agent=verifier,
    tools=[blood_test_tool]
)
help_patients = Task(
    description=("Thoroughly analyze the user's blood test data provided in the query: {query}. "
        "Identify any abnormal markers and explain their clinical relevance in clear, medically accurate terms. "
        "If needed, reference trusted medical knowledge or databases to support your interpretation."),

    expected_output=(
        "Provide a detailed medical interpretation of the blood report, including:\n"
        "- Explanation of abnormal values\n"
        "- Potential underlying health conditions\n"
        "- Recommendations for next steps (e.g., further testing, physician consultation)\n"
        "- Clear and concise medical terminology appropriate for patient understanding"
    ),

    agent=doctor,
    tools=[blood_test_tool],
    context=[verification]
)

## Creating a nutrition analysis task
nutrition_analysis = Task(
    description=(
        "Analyze the user's blood test report to identify any possible nutritional deficiencies, imbalances, or diet-related concerns.\n"
        "Focus on interpreting markers like Vitamin D, B12, iron, glucose, cholesterol, and calcium.\n"
        "Based on your analysis, recommend appropriate dietary changes, nutrient-rich foods, and supplements if needed.\n"
        "Tailor your advice to support the user’s long-term health goals based on the provided report and query: {query}."
    ),
    expected_output=(
        "Deliver a clear nutrition guide that includes:\n"
        "- Identified nutritional issues based on blood markers\n"
        "- Specific food and diet recommendations (e.g., iron-rich foods)\n"
        "- Optional supplement suggestions with dosage hints\n"
        "- Brief reasoning behind each suggestion\n"
        "- Easy-to-follow tips that align with evidence-based dietary guidance"
    ),
    agent=nutritionist,
    context=[help_patients]
)

## Creating an exercise planning task
exercise_planning = Task(
    description=(
        "Develop a customized exercise plan based on the user's blood report and health status described in {query}.\n"
        "Pay attention to cardiovascular, metabolic, and musculoskeletal indicators like glucose, cholesterol, hemoglobin, and vitamin D.\n"
        "Design a fitness routine that is safe, sustainable, and supportive of the user's health goals. Consider limitations such as anemia, hypertension, or high glucose levels."
    ),
    expected_output=(
        "Provide a comprehensive workout plan that includes:\n"
        "- Weekly schedule (types of exercises, durations, intensity levels)\n"
        "- Exercise types: cardio, strength, flexibility, balance\n"
        "- Any required precautions or modifications (e.g., anemia-related fatigue)\n"
        "- Guidelines for progression and recovery\n"
        "- Motivational or lifestyle tips to support adherence"
    ),
    agent=exercise_specialist,
    context=[help_patients, nutrition_analysis]
)
