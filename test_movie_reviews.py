"""Regression checks for the movie review lab."""

import contextlib
import io
import subprocess
import sys
import unittest
from pathlib import Path

import movie_reviews as board


class MovieReviewTests(unittest.TestCase):
    """Check public behavior and security-related changes."""

    def setUp(self):
        board.movies.clear()
        board.add_movie("First", "Drama", 2021)
        board.add_movie("Second", "Comedy", 2022)

    def tearDown(self):
        board.movies.clear()

    def test_rating_boundaries_reviews_and_rejection(self):
        self.assertTrue(board.rate_movie("First", 1, "Low"))
        self.assertTrue(board.rate_movie("First", 5))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertFalse(board.rate_movie("First", 0, "Invalid"))
            self.assertFalse(board.rate_movie("First", 6, "Invalid"))
        self.assertIn("Rating must be between 1 and 5", output.getvalue())
        self.assertEqual(board.movies["First"]["ratings"], [1, 5])
        self.assertEqual(board.movies["First"]["reviews"], ["Low"])
        self.assertEqual(board.movies["Second"]["ratings"], [])

    def test_average_and_unrated_movies(self):
        self.assertEqual(board.average_rating("First"), 0.0)
        for stars in (4, 4, 5):
            board.rate_movie("First", stars)
        self.assertEqual(board.average_rating("First"), 4.3)

    def test_rankings_counts_and_stable_ties(self):
        board.add_movie("Third", "Action", 2023)
        board.rate_movie("First", 4)
        board.rate_movie("Second", 5)
        board.rate_movie("Third", 4)
        self.assertEqual(board.top_movies(), ["Second", "First"])
        self.assertEqual(board.top_movies(0), [])
        self.assertEqual(board.top_movies(10), ["Second", "First", "Third"])

    def test_featured_movie_is_registered(self):
        for _ in range(20):
            self.assertIn(board.pick_featured(), {"First", "Second"})

    def test_review_identifier_is_stable_and_unambiguous(self):
        identifier = board.review_id("Film", "Great")
        self.assertEqual(identifier, board.review_id("Film", "Great"))
        self.assertRegex(identifier, r"^[0-9a-f]{64}$")
        self.assertNotEqual(identifier, board.review_id("Film", "Poor"))
        self.assertNotEqual(board.review_id("ab", "c"),
                            board.review_id("a", "bc"))
        self.assertNotEqual(board.review_id("Film", "café"),
                            board.review_id("Film", "cafe"))

    def test_display_and_loopback_address(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            board.print_all_reviews()
        self.assertEqual(output.getvalue(), "1 First 0.0\n2 Second 0.0\n")
        self.assertEqual(board.stream_address(), "127.0.0.1:8000")

    def test_import_has_no_demo_side_effects(self):
        result = subprocess.run(
            [sys.executable, "-c",
             "import movie_reviews; print(len(movie_reviews.movies))"],
            cwd=Path(__file__).parent,
            capture_output=True, text=True, check=True,
        )
        self.assertEqual(result.stdout, "0\n")
        self.assertEqual(result.stderr, "")

    def test_demo_preserves_ratings_rankings_and_genres(self):
        board.movies.clear()
        with contextlib.redirect_stdout(io.StringIO()) as output:
            board.main()
        lines = output.getvalue().splitlines()
        self.assertEqual(lines[:5], [
            "Rating must be between 1 and 5, got 6",
            "1 The Long Road 4.5",
            "2 Laugh Track 2.0",
            "3 Star Drift 4.0",
            "Top movies: ['The Long Road', 'Star Drift']",
        ])
        self.assertIn(lines[5].removeprefix("Featured today: "), board.movies)
        self.assertRegex(lines[6], r"^Review id: [0-9a-f]{64}$")
        self.assertEqual(lines[7], "Streaming from 127.0.0.1:8000")
        self.assertEqual(lines[8], "Genres: ['Comedy', 'Drama', 'Sci-Fi']")


if __name__ == "__main__":
    unittest.main()
