import google.generativeai as genai
import os
from dotenv import load_dotenv
from sqlglot import parse_one, diff  # Import SqlGlot
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.db import connection
from django.db.utils import ProgrammingError
import sqlparse

from .models import Exercise 

load_dotenv()  # Load environment variables 
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

def compare_results_precise(user_query, solution_query, user_results, solution_results):
    """
    Compares query results and structure (AST) ensuring both data and 
    filtering logic match exactly.
    """

    if len(user_results) != len(solution_results):
        return False  # Mismatch if lengths differ

    # Data Match Check (unchanged from your original version)
    if not all(user_row == solution_row 
               for user_row, solution_row in zip(user_results, solution_results)):
        return False

    # Parse Queries into ASTs
    user_ast = parse_one(user_query)
    solution_ast = parse_one(solution_query)

    # Calculate AST Diff
    transformations = diff(user_ast, solution_ast)  

    # Check if all transformations are 'Keep'
    return all(transformation.get('type') == 'keep' for transformation in transformations)

class ExerciseListView(ListView):
    model = Exercise
    template_name = 'exercises/exercise_list.html'
    context_object_name = 'exercises'

    def get_queryset(self):
        queryset = super().get_queryset()
        difficulty = self.request.GET.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        return queryset

class ExerciseDetailView(DetailView):
    model = Exercise
    template_name = 'exercises/exercise_detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_query = request.POST.get('userQuery')
        solution_query = self.object.solution
        excercise = self.object.description
        feedback = ''
        feedback_type = 'danger'  # default to red for errors or mismatches
        columns = []


        # Try parsing the user's query to ensure it's a SELECT statement
        try:
            parsed = sqlparse.parse(user_query)[0]
            if not parsed.get_type() == 'SELECT':
                raise ValueError("Only SELECT queries are allowed.")

            print("Executing User Query:", user_query)
            # Execute user query and fetch results
            user_results, columns = self.execute_and_fetch(user_query)

            # Assuming direct result set comparison is needed
            # Execute solution query and fetch results for comparison
            solution_results, _ = self.execute_and_fetch(solution_query)

            print("*** User Results ***")
            print(user_results)  # Adjust the number if needed 
            print("*** Solution Results ***")
            print(solution_results) 

            exercise = excercise

            # Simplified comparison: Check if user results match the solution's results
            if compare_results_precise(user_query, self.object.solution, user_results, solution_results):
                feedback = "Your query's results match the expected solution."
                feedback_type = 'success'
            else:
                # AST Generation with SqlGlot
                user_ast = parse_one(user_query)
                solution_ast = parse_one(solution_query)
                # Calculate AST Diff
                transformations = diff(user_ast, solution_ast)
                # Construct a prompt based on the transformations 
                prompt = f"""{exercise}
                User Query: {user_query}
                Solution Query: {solution_query}
                **Task:**  
                Identify the specific changes needed in the User Query to make it produce the exact same output as the Solution Query.  Analyze the User Query, Solution Query, and the provided AST Diff to pinpoint these required modifications. 
                **Output Format:**
                Provide the missing elements in a clear, step-by-step format. Focus on:
                * Additional clauses that need to be added (e.g., WHERE, JOIN)
                * Changes to existing clauses
                * Columns that need to be added or removed from the SELECT statement
                Do Not provide the solution query only the steps needed to match the solution. Add an empty line between each step you provide.
                AST Diff: {transformations}""" 



                response = model.generate_content(prompt)

                # Process Gemini's response 
                gemini_feedback = response.text 

                # Integrate Gemini's feedback 
                feedback = f"Your query has some differences from the expected solution. Here are some suggestions: {gemini_feedback}" 

        except ValueError as e:
            feedback = str(e)
        except ProgrammingError as e:
            feedback = f"Error executing the SQL query: {e}"

        context = self.get_context_data(
            object=self.object,
            user_query=user_query,
            feedback=feedback,
            feedback_type=feedback_type,
            results=user_results if 'user_results' in locals() else [],
            columns=columns
        )
        return render(request, self.template_name, context)

    def execute_and_fetch(self, query):
        "Execute a query and fetch results in a dictionary format."
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description] if cursor.description else []
            results = cursor.fetchall()
            return results, columns 
