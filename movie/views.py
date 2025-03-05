from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
import base64
from collections import Counter


from .models import Movie
# Create your views here.

def home(request):
    # return HttpResponse('<h1>Welcome to Home Page</h1>')
    # return render(request, 'home.html', {'name':'Esteban Romero'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies':movies})

def about(request):
    # return HttpResponse('<h1>Welcome to About page</h1>')
    return render(request, 'about.html', {'name':'Esteban Romero'})
def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email':email})


def statistics_view(request):
    matplotlib.use('Agg')
    # Obtener todas las películas
    all_movies = Movie.objects.all()
    # Crear un diccionario para almacenar la cantidad de películas por año
    movie_counts_by_year = {}
    # Filtrar las películas por año y contar la cantidad de películas por año
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1

    # Ancho de las barras
    bar_width = 0.5
    # Posiciones de las barras
    bar_positions = range(len(movie_counts_by_year))

    # Crear la gráfica de barras
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')

    # Personalizar la gráfica
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)

    # Ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)

    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    # Gráfica 2: Cantidad de películas por género (solo el primer género)
    genre_counts = Counter()
    for movie in all_movies:
        if movie.genre:  # Verifica que tenga género
            first_genre = movie.genre.split(",")[0].strip()  # Toma solo el primer género
            genre_counts[first_genre] += 1

    plt.clf()
    plt.figure(figsize=(10, 5))
    plt.bar(genre_counts.keys(), genre_counts.values(), color='lightcoral', edgecolor='black')
    plt.title('Movies per Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic_genres = base64.b64encode(image_png).decode('utf-8')

    # Renderizar la plantilla con ambas imágenes
    return render(request, 'statistics.html', {
        'graphic': graphic,
        'graphic_genres': graphic_genres
    })