#!/usr/bin/python3
"""
Unit tests for the HackerNews API wrapper.
"""

import unittest

import hnapi


class TestHnApi(unittest.TestCase):
    """
    Unit tests for the HackerNews API wrapper.
    """

    def test_normalized_top_items_valid(self):
        """
        Test a perfectly valid case.
        """
        # Arrange
        item = {
            "id": 1,
            "title": "Foo",
            "url": "http://foo.bar",
            "score": 42,
            "descendants": 1337,
            "by": "Baz"
        }
        items = [item] * 20

        num_items = 10
        output_keys = ["title", "uri", "points", "comments", "rank"]

        # Act
        results = hnapi.get_normalized_top_items(num_items, items)

        # Assert
        self.assertEqual(num_items, len(results))
        for rank, result in enumerate(results, start=1):
            # Check all attributes are in the output
            for key in output_keys:
                self.assertIn(key, result)

            # Check length restrictions for the title and username
            title_len = len(result["title"])
            self.assertTrue(title_len > 0 and
                            title_len <= hnapi.MAX_TITLE_LENGTH)

            author_len = len(result["author"])
            self.assertTrue(author_len > 0 and
                            author_len <= hnapi.MAX_USERNAME_LENGTH)

            # Check fields value
            self.assertEqual(item["title"], result["title"])
            self.assertEqual(item["url"], result["uri"])
            self.assertEqual(item["score"], result["points"])
            self.assertEqual(item["descendants"], result["comments"])
            self.assertEqual(item["by"], result["author"])
            self.assertEqual(rank, result["rank"])

    def test_normalized_top_items_truncated_title(self):
        """
        Test when the title is too long.
        """
        # Arrange
        item = {
            "id": 1,
            "title": "Foo" * hnapi.MAX_TITLE_LENGTH,
            "url": "http://foo.bar",
            "score": 42,
            "descendants": 1337,
            "by": "Baz"
        }
        items = [item]

        num_items = 1
        output_keys = ["title", "uri", "points", "comments", "rank"]

        # Act
        results = hnapi.get_normalized_top_items(num_items, items)

        # Assert
        self.assertEqual(num_items, len(results))
        for rank, result in enumerate(results, start=1):
            # Check all attributes are in the output
            for key in output_keys:
                self.assertIn(key, result)

            # Check length restrictions for the title and username
            title_len = len(result["title"])
            self.assertTrue(title_len > 0 and
                            title_len <= hnapi.MAX_TITLE_LENGTH)

            author_len = len(result["author"])
            self.assertTrue(author_len > 0 and
                            author_len <= hnapi.MAX_USERNAME_LENGTH)

            # Check fields value
            self.assertNotEqual(item["title"], result["title"])
            self.assertEqual(item["title"][:hnapi.MAX_TITLE_LENGTH],
                             result["title"])
            self.assertEqual(item["url"], result["uri"])
            self.assertEqual(item["score"], result["points"])
            self.assertEqual(item["descendants"], result["comments"])
            self.assertEqual(item["by"], result["author"])
            self.assertEqual(rank, result["rank"])

    def test_normalized_top_items_truncated_author(self):
        """
        Test when the author's username is too long.
        """
        # Arrange
        item = {
            "id": 1,
            "title": "Foo",
            "url": "http://foo.bar",
            "score": 42,
            "descendants": 1337,
            "by": "Baz" * hnapi.MAX_USERNAME_LENGTH
        }
        items = [item]

        num_items = 1
        output_keys = ["title", "uri", "points", "comments", "rank"]

        # Act
        results = hnapi.get_normalized_top_items(num_items, items)

        # Assert
        self.assertEqual(num_items, len(results))
        for rank, result in enumerate(results, start=1):
            # Check all attributes are in the output
            for key in output_keys:
                self.assertIn(key, result)

            # Check length restrictions for the title and username
            title_len = len(result["title"])
            self.assertTrue(title_len > 0 and
                            title_len <= hnapi.MAX_TITLE_LENGTH)

            author_len = len(result["author"])
            self.assertTrue(author_len > 0 and
                            author_len <= hnapi.MAX_USERNAME_LENGTH)

            # Check fields value
            self.assertEqual(item["title"], result["title"])
            self.assertEqual(item["url"], result["uri"])
            self.assertEqual(item["score"], result["points"])
            self.assertEqual(item["descendants"], result["comments"])
            self.assertEqual(item["by"][:hnapi.MAX_USERNAME_LENGTH],
                             result["author"])
            self.assertEqual(rank, result["rank"])

    def test_normalized_top_items_invalid_score(self):
        """
        Test when the number of points is invalid.
        """
        # Arrange
        item = {
            "id": 1,
            "title": "Foo",
            "url": "http://foo.bar",
            "score": -42,
            "descendants": 1337,
            "by": "Baz"
        }
        items = [item]

        num_items = 1
        output_keys = ["title", "uri", "points", "comments", "rank"]

        # Act
        results = hnapi.get_normalized_top_items(num_items, items)

        # Assert
        self.assertEqual(num_items, len(results))
        for rank, result in enumerate(results, start=1):
            # Check all attributes are in the output
            for key in output_keys:
                self.assertIn(key, result)

            # Check length restrictions for the title and username
            title_len = len(result["title"])
            self.assertTrue(title_len > 0 and
                            title_len <= hnapi.MAX_TITLE_LENGTH)

            author_len = len(result["author"])
            self.assertTrue(author_len > 0 and
                            author_len <= hnapi.MAX_USERNAME_LENGTH)

            # Check fields value
            self.assertEqual(item["title"], result["title"])
            self.assertEqual(item["url"], result["uri"])
            self.assertNotEqual(item["score"], result["points"])
            self.assertEqual(0, result["points"])
            self.assertEqual(item["descendants"], result["comments"])
            self.assertEqual(item["by"], result["author"])
            self.assertEqual(rank, result["rank"])

    def test_normalized_top_items_invalid_comments(self):
        """
        Test when the number of comments is invalid.
        """
        # Arrange
        item = {
            "id": 1,
            "title": "Foo",
            "url": "http://foo.bar",
            "score": 42,
            "descendants": -1337,
            "by": "Baz"
        }
        items = [item]

        num_items = 1
        output_keys = ["title", "uri", "points", "comments", "rank"]

        # Act
        results = hnapi.get_normalized_top_items(num_items, items)

        # Assert
        self.assertEqual(num_items, len(results))
        for rank, result in enumerate(results, start=1):
            # Check all attributes are in the output
            for key in output_keys:
                self.assertIn(key, result)

            # Check length restrictions for the title and username
            title_len = len(result["title"])
            self.assertTrue(title_len > 0 and
                            title_len <= hnapi.MAX_TITLE_LENGTH)

            author_len = len(result["author"])
            self.assertTrue(author_len > 0 and
                            author_len <= hnapi.MAX_USERNAME_LENGTH)

            # Check fields value
            self.assertEqual(item["title"], result["title"])
            self.assertEqual(item["url"], result["uri"])
            self.assertEqual(item["score"], result["points"])
            self.assertNotEqual(item["descendants"], result["comments"])
            self.assertEqual(0, result["comments"])
            self.assertEqual(item["by"], result["author"])
            self.assertEqual(rank, result["rank"])

    def test_normalized_top_items_malformed_url(self):
        """
        Test when the URL is malformed.
        """
        # Arrange
        item = {
            "id": 1,
            "title": "Foo",
            "url": "http://foo:-1/bar",
            "score": 42,
            "descendants": 1337,
            "by": "Baz"
        }
        items = [item]

        num_items = 1
        output_keys = ["title", "uri", "points", "comments", "rank"]

        # Act
        results = hnapi.get_normalized_top_items(num_items, items)

        # Assert
        self.assertEqual(num_items, len(results))
        for rank, result in enumerate(results, start=1):
            # Check all attributes are in the output
            for key in output_keys:
                self.assertIn(key, result)

            # Check length restrictions for the title and username
            title_len = len(result["title"])
            self.assertTrue(title_len > 0 and
                            title_len <= hnapi.MAX_TITLE_LENGTH)

            author_len = len(result["author"])
            self.assertTrue(author_len > 0 and
                            author_len <= hnapi.MAX_USERNAME_LENGTH)

            # Check fields value
            self.assertEqual(item["title"], result["title"])
            self.assertNotEqual(item["url"], result["uri"])
            self.assertEqual(item["score"], result["points"])
            self.assertEqual(item["descendants"], result["comments"])
            self.assertEqual(item["by"], result["author"])
            self.assertEqual(rank, result["rank"])

    def test_normalized_top_items_error(self):
        """
        Test when the URL is malformed.
        """
        # Arrange
        items = [None]
        num_items = 1

        # Act
        results = hnapi.get_normalized_top_items(num_items, items)

        # Assert
        self.assertNotEqual(num_items, len(results))
