import os
from dotenv import load_dotenv
load_dotenv()

from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from langchain_community.document_loaders import PyPDFLoader

search_tool = None

## Fixed Blood Test Report Tool
class BloodTestReportInput(BaseModel):
    path: str = Field(default='data/sample.pdf', description="Path of the pdf file to read")

class BloodTestReportTool(BaseTool):
    name: str = "read_blood_test_report"
    description: str = "Tool to read data from a blood test report PDF file. Always provide the file path."
    args_schema: Type[BaseModel] = BloodTestReportInput

    def _run(self, path: str, **kwargs) -> str:
        """Read and process blood test report PDF"""
        
        # Validate path
        if not path:
            return "[ERROR] No file path provided"
            
        if not os.path.exists(path):
            return f"[ERROR] File not found at path: {path}"
            
        if not path.lower().endswith('.pdf'):
            return f"[ERROR] File must be a PDF: {path}"
            
        try:
            print(f"Reading PDF from: {path}")
            
            # Load the PDF
            loader = PyPDFLoader(file_path=path)
            docs = loader.load()
            
            if not docs:
                return "[ERROR] PDF file appears to be empty or corrupted"

            full_report = ""
            for i, doc in enumerate(docs):
                content = doc.page_content.strip()
                if content:  # Only add non-empty content
                    # Clean formatting
                    content = content.replace('\n\n', '\n')
                    content = content.replace('\t', ' ')
                    # Remove excessive whitespace
                    content = ' '.join(content.split())
                    full_report += f"Page {i+1}:\n{content}\n\n"

            if not full_report.strip():
                return "[ERROR] No readable content found in PDF"

            # Truncate if too long but preserve important content
            max_chars = 2000
            if len(full_report) > max_chars:
                full_report = full_report[:max_chars] + "\n\n... [Content truncated for processing]"

            return full_report

        except Exception as e:
            error_msg = f"[ERROR] Failed to read PDF: {str(e)}"
            print(error_msg)
            return error_msg

# Create tool instance
blood_test_tool = BloodTestReportTool()

## Nutrition Analysis Tool (kept as reference but not used in main flow)
class NutritionTool:
    @staticmethod
    def analyze_nutrition_tool(blood_report_data):
        """Analyze blood report for nutritional insights"""
        if not blood_report_data or blood_report_data.startswith("[ERROR]"):
            return "Unable to analyze nutrition due to data reading error."
            
        try:
            # Process and analyze the blood report data
            processed_data = blood_report_data.lower()
            nutrition_recommendations = []

            if "vitamin d" in processed_data or "25-oh" in processed_data:
                nutrition_recommendations.append(
                    "Vitamin D: Consider increasing sun exposure and consuming fortified foods like cereals or dairy alternatives."
                )

            if "b12" in processed_data or "cobalamin" in processed_data:
                nutrition_recommendations.append(
                    "B12: Include more B12-rich foods such as eggs, fish, dairy products, or fortified plant-based alternatives."
                )

            if "iron" in processed_data or "ferritin" in processed_data:
                nutrition_recommendations.append(
                    "Iron: Eat iron-rich foods like lean red meat, spinach, lentils, and pair with vitamin C-rich foods for better absorption."
                )

            if "cholesterol" in processed_data:
                nutrition_recommendations.append(
                    "Cholesterol: Add more soluble fiber (oats, legumes), heart-healthy fats (avocados), and reduce processed foods."
                )

            if "glucose" in processed_data or "hba1c" in processed_data:
                nutrition_recommendations.append(
                    "Blood Sugar: Focus on complex carbohydrates, reduce added sugars, and maintain regular meal timing."
                )

            if "calcium" in processed_data:
                nutrition_recommendations.append(
                    "Calcium: Boost intake with dairy, sesame seeds, leafy greens, or calcium-fortified beverages."
                )

            if not nutrition_recommendations:
                nutrition_recommendations.append(
                    "No specific nutrient issues detected. Maintain a balanced diet with fruits, vegetables, lean proteins, and healthy fats."
                )

            return "\n".join(nutrition_recommendations)
            
        except Exception as e:
            return f"Error analyzing nutrition data: {str(e)}"

## Exercise Planning Tool (kept as reference but not used in main flow)
class ExerciseTool:
    @staticmethod
    def create_exercise_plan_tool(blood_report_data):
        """Create exercise plan based on blood report"""
        if not blood_report_data or blood_report_data.startswith("[ERROR]"):
            return "Unable to create exercise plan due to data reading error."
            
        try:
            exercise_recommendations = []
            data_lower = blood_report_data.lower()

            if "cholesterol" in data_lower or "ldl" in data_lower:
                exercise_recommendations.append(
                    "Cholesterol Management: Incorporate moderate cardio (cycling, swimming) for 150+ minutes weekly."
                )

            if "glucose" in data_lower or "diabetes" in data_lower:
                exercise_recommendations.append(
                    "Blood Sugar Control: Alternate between aerobic sessions and resistance training 3-4 times weekly."
                )

            if "blood pressure" in data_lower or "hypertension" in data_lower:
                exercise_recommendations.append(
                    "Blood Pressure: Focus on low-impact cardio like walking or swimming, 30 minutes most days."
                )

            if "vitamin d" in data_lower:
                exercise_recommendations.append(
                    "Vitamin D: Prioritize outdoor activities like hiking or walking during morning hours."
                )

            if "iron" in data_lower or "anemia" in data_lower:
                exercise_recommendations.append(
                    "Iron/Anemia: Start with low-impact activities like walking or gentle yoga, gradually increase intensity."
                )

            if not exercise_recommendations:
                exercise_recommendations.append(
                    "General Fitness: Combine 150 minutes moderate cardio with strength training twice weekly."
                )

            exercise_recommendations.append(
                "Important: Consult your healthcare provider before beginning any new fitness program."
            )

            return "\n".join(exercise_recommendations)
            
        except Exception as e:
            return f"Error creating exercise plan: {str(e)}"

# Create tool instances
nutrition_tool = NutritionTool()
exercise_tool = ExerciseTool()