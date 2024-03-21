from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.db import connection
from django.db.utils import ProgrammingError
import sqlparse
from .models import Exercise

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
        feedback = ''
        feedback_type = 'danger'  # default to red for errors or mismatches
        columns = []

        # Try parsing the user's query to ensure it's a SELECT statement
        try:
            parsed = sqlparse.parse(user_query)[0]
            if not parsed.get_type() == 'SELECT':
                raise ValueError("Only SELECT queries are allowed.")
            # Execute user query and fetch results
            user_results, columns = self.execute_and_fetch(user_query)
            # Assuming direct result set comparison is needed
            # Execute solution query and fetch results for comparison
            solution_results, _ = self.execute_and_fetch(solution_query)
            # Simplified comparison: Check if user results match the solution's results
            if sorted(user_results) == sorted(solution_results):
                feedback = "Your query's results match the expected solution."
                feedback_type = 'success'
            else:
                feedback = "The query results do not match the expected solution."
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