import fresh_tomatoes
import media
# The below creates the movie objects that will be displayed on the site.
toy_story = media.Movie("Toy Story",
                        "http://www.impawards.com/1995/posters/toy_story_ver1_xlg.jpg",  # NOQA
                        "https://youtu.be/KYz2wyBy3kc")
avatar = media.Movie("Avatar",
                     "http://www.impawards.com/2009/posters/avatar_xlg.jpg",
                     "https://youtu.be/cRdxXPV9GNQ")
social_network = media.Movie("Social Network",
                             "http://incontention.com/wp-content/uploads/2010/06/soci.gif",  # NOQA
                             "https://youtu.be/lB95KLmpLR4")
school_of_rock = media.Movie("School of Rock",
                             "https://www.cinematerial.com/media/posters/md/pp/pp3ombpu.jpg?v=1456168941",  # NOQA
                             "https://youtu.be/XCwy6lW5Ixc")
ratatouille = media.Movie("ratatoulle",
                          "http://www.canmag.com/images/front/movies2007/ratatouilleposter5.jpg",  # NOQA
                          "https://youtu.be/c3sBBRxDAqk")
the_hunger_games = media.Movie("the hunger games",
                               "http://www.impawards.com/2012/posters/hunger_games_ver27.jpg",  # NOQA
                               "https://youtu.be/4S9a5V9ODuY")

# Places the movie objects into an array called movies.
movies = [toy_story, avatar, social_network,
          school_of_rock, ratatouille, the_hunger_games]
# Calls the open_movie_page function from the fresh_tomatoes python file.
fresh_tomatoes.open_movies_page(movies)
