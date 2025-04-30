from haive.haive.toolkits.chucknorris_toolkit import (
    get_available_categories,
    get_random_joke,
    get_random_joke_by_category,
    search_jokes,
)


def test_get_random_joke():
    joke = get_random_joke()
    assert joke.id
    assert joke.value
    assert "Chuck Norris" in joke.value


def test_get_available_categories():
    categories = get_available_categories()
    assert isinstance(categories, list)
    assert "dev" in categories  # One of the default categories


def test_get_joke_by_category():
    categories = get_available_categories()
    joke = get_random_joke_by_category(categories[0])
    assert joke.id
    assert joke.value


def test_search_jokes():
    jokes = search_jokes("code")
    assert isinstance(jokes, list)
    if jokes:
        assert "Chuck Norris" in jokes[0].value
