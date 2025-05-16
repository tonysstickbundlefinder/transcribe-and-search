import unittest

from search import search_transcript


class TestSearchTranscript(unittest.TestCase):
    def make_segments(self, words, start=0.0, step=1.0):
        """
        Helper to create segments list from a list of words with incremental timestamps.
        """
        segments = []
        t = start
        for w in words:
            segments.append({'start': t, 'end': t + 0.5, 'text': w})
            t += step
        return segments

    def test_single_word_variants(self):
        segments = self.make_segments([
            "apple", "apples", "appley", "appleish", "applish", "banana"
        ])
        results = search_transcript(segments, ["apple"], context_window=0)
        # Should match all apple variants (5 matches) and not banana
        self.assertEqual(len(results), 5)
        # All queries should be "apple"
        self.assertTrue(all(r['query'] == "apple" for r in results))

    def test_multi_word_phrase(self):
        segments = self.make_segments(["to", "be", "or", "not", "to", "be"] )
        results = search_transcript(segments, ["to be"], context_window=0)
        # Expect two occurrences of "to be"
        self.assertEqual(len(results), 2)
        # Check start timestamps
        expected = [0.0, 4.0]
        self.assertEqual([r['timestamp_sec'] for r in results], expected)
        # Check queries
        self.assertEqual([r['query'] for r in results], ["to be", "to be"])

    def test_overlapping_phrases(self):
        segments = self.make_segments(["hello", "world", "test"])
        results = search_transcript(segments, ["hello world", "world test"], context_window=0)
        # Should match both phrases at correct positions
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['query'], "hello world")
        self.assertEqual(results[1]['query'], "world test")

if __name__ == "__main__":
    unittest.main()