import numpy as np
from sklearn.neighbors import NearestNeighbors

class MovieRecommendationAI:
    def __init__(self):
        # База данных фильмов и их характеристик
        self.movies = {
            'Матрица': [1, 1, 0, 1, 0],  # [фантастика, боевик, комедия, драма, ужасы]
            'Мальчишник в Вегасе': [0, 0, 1, 0, 0],
            'Начало': [1, 1, 0, 1, 0],
            'Одноклассники': [0, 0, 1, 1, 0],
            'Звёздные войны': [1, 1, 0, 0, 0],
            'Паранормальное явление': [0, 0, 0, 0, 1],
            'Крепкий орешек': [0, 1, 0, 1, 0],
            'Супергерои': [0, 0, 1, 0, 0]
        }
        
        # Обучаем модель на наших данных
        self.model = NearestNeighbors(n_neighbors=2, metric='cosine')
        movie_features = list(self.movies.values())
        self.model.fit(movie_features)
        
        self.movie_names = list(self.movies.keys())
    
    def learn_from_feedback(self, liked_movie, recommended_movie, liked=True):
        """Агент учится на основе обратной связи"""
        if liked:
            # Увеличиваем вес характеристик понравившегося фильма
            for movie in [liked_movie, recommended_movie]:
                if movie in self.movies:
                    self.movies[movie] = [x + 0.1 for x in self.movies[movie]]
            print(f"✅ Запомнил, что вам нравятся фильмы типа '{liked_movie}'")
        else:
            # Уменьшаем сходство между этими фильмами
            print(f"❌ Учту, что '{liked_movie}' и '{recommended_movie}' не похожи")
    
    def recommend(self, liked_movie):
        """ИИ рекомендает фильм на основе схожести"""
        if liked_movie not in self.movies:
            return "Не знаю этот фильм"
        
        # Находим ближайших соседей
        movie_index = self.movie_names.index(liked_movie)
        distances, indices = self.model.kneighbors([self.movies[liked_movie]])
        
        # Исключаем сам фильм из рекомендаций
        for idx in indices[0]:
            if idx != movie_index:
                recommended = self.movie_names[idx]
                return recommended
        
        return "Не могу найти рекомендацию"
    
    def interact(self):
        """Интерактивный режим работы агента"""
        print("🎬 ИИ-помощник по рекомендации фильмов")
        print("Доступные фильмы:", ", ".join(self.movies.keys()))
        
        while True:
            liked = input("\nКакой фильм вам понравился? (или 'стоп'): ")
            if liked.lower() == 'стоп':
                break
                
            recommendation = self.recommend(liked)
            if recommendation in self.movies:
                print(f"📽 На основе вашего выбора '{liked}' рекомендую: {recommendation}")
                
                feedback = input("Понравилась рекомендация? (да/нет): ")
                if feedback.lower() == 'да':
                    self.learn_from_feedback(liked, recommendation, liked=True)
                else:
                    self.learn_from_feedback(liked, recommendation, liked=False)
            else:
                print(recommendation)

# Запуск ИИ-агента
if __name__ == "__main__":
    ai = MovieRecommendationAI()
    ai.interact()