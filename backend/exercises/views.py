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
        self.object = self.get_object()  # Assign the detailed object to self.object
        user_query = request.POST.get('userQuery')
        feedback = ''
        results = []
        columns = []

        try:
            parsed = sqlparse.parse(user_query)[0]
            if not parsed.get_type() == 'SELECT':
                raise ValueError("Only SELECT queries are allowed.")
        except ValueError as e:
            feedback = str(e)
        else:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(user_query)
                    columns = [col[0] for col in cursor.description] if cursor.description else []
                    results = cursor.fetchall()
            except ProgrammingError as e:
                feedback = f"Error executing the SQL query: {e}"

        context = self.get_context_data(user_query=user_query, feedback=feedback, results=results, columns=columns)
        return render(request, self.template_name, context)
    
    def fetch_results(self, cursor):
        "Fetch results in a dictionary format."
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]