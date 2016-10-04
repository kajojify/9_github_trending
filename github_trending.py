import requests
from datetime import datetime, timedelta


def get_trending_repositories(top_size):
    """С помощью github api производит поиск всех репозиториев, созданных
     за последнюю неделю. Упорядочивает их по убыванию количества звёзд(stars).
     Возвращает список, элементами которого являются словари с информацией о
     репозитории."""

    github_url = "https://api.github.com/search/repositories"
    user_datetime = datetime.now()
    github_datetime = user_datetime - timedelta(days=7)
    # github_datetime - время, которое было неделю назад
    github_datetime_string = github_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    payload = {'q': 'created:>='+github_datetime_string,
               'sort': 'stars', 'order': 'desc', 'per_page': top_size}
    # payload['q'] - запрос к github api
    github_response = requests.get(github_url, params=payload)
    github_data = github_response.json()['items']
    trending_repositories = list()
    for repo in github_data:
        trending_repositories.append({'repo_owner': repo['owner']['login'],
                                      'repo_name': repo['name'],
                                      'url': repo['html_url'],
                                      'issues_number': repo["open_issues_count"]}
                                     )
    return trending_repositories


if __name__ == '__main__':
    trending_repositories = get_trending_repositories(20)
    print("Список репозиториев, созданных за последнюю неделю \""
          "и упорядоченных по убыванию количества звёзд(stars):")
    print("{:<10}{:<20}{:<35}{:^50}{:<20}\n".format("№", "Имя владельца",
                                                    "Название репозитория",
                                                    "Ссылка", "Количество issues"))
    for repo_number, repo in enumerate(trending_repositories):
        print("{:<10}{:<20}{:<35}{:<60}{:<5}".format(repo_number+1,
                                                     repo['repo_owner'],
                                                     repo['repo_name'],
                                                     repo['url'],
                                                     repo['issues_number']))
