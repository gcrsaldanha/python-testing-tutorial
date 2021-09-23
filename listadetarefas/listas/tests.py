from django.test import TestCase  # TestCase do Django é um TestCase com mais funcionalidades.


class TestDummy(TestCase):
    def test_fails(self):
        self.assertEqual(1 + 1, 3)

    def test_passes(self):
        self.assertTrue(True)