import unittest
from langtree.core import Prompt, render_prompt

# Assuming the previous definitions are here

class TestRenderPrompt(unittest.TestCase):

    def test_render_with_no_substitution(self):
        self.assertEqual(render_prompt("Hello, world!"), "Hello, world!")

    def test_render_with_one_substitution(self):
        self.assertEqual(render_prompt("Hello, {{name}}!", name="Alice"), "Hello, Alice!")

    def test_render_with_multiple_substitutions(self):
        self.assertEqual(render_prompt("{{greeting}}, {{name}}!", greeting="Hi", name="Bob"), "Hi, Bob!")

    def test_render_with_no_template(self):
        self.assertIsNone(render_prompt(None, name="Charlie"))

    def test_render_with_special_characters(self):
        self.assertEqual(render_prompt("Hello, {{name}}!", name="Alice (from Wonderland)"), "Hello, Alice (from Wonderland)!")

class TestPrompt(unittest.TestCase):

    def test_call_with_substitution(self):
        prompt = Prompt("Hello, {{name}}!")
        self.assertEqual(prompt(name="David"), "Hello, David!")

    def test_add_with_string(self):
        prompt1 = Prompt("Hello, ")
        prompt2 = prompt1 + "world!"
        self.assertEqual(prompt2.template, "Hello, world!")

    def test_add_with_another_prompt(self):
        prompt1 = Prompt("Hello, ")
        prompt2 = Prompt("{{name}}!")
        prompt3 = prompt1 + prompt2
        self.assertEqual(prompt3.template, "Hello, {{name}}!")
        self.assertEqual(prompt3(name="Edward"), "Hello, Edward!")

    def test_add_with_non_string_raises_type_error(self):
        prompt = Prompt("Hello, ")
        with self.assertRaises(TypeError):
            prompt + 123

if __name__ == '__main__':
    unittest.main()
