import unittest
from serialize import serialize
from unserialize import unserialize


class TestSerializeMethods(unittest.TestCase):
    def test_string(self):
        self.assertEqual(serialize("乗"), '"乗"')

    def test_string_encoding(self):
        self.assertEqual(serialize("乗", "gbk"), '"乗\\"')

    def test_bool(self):
        self.assertEqual(serialize(True), "true")
        self.assertEqual(serialize(False), "false")

    def test_number(self):
        self.assertEqual(serialize(0.1), "0.1")
        self.assertEqual(serialize(100), "100")

    def test_list(self):
        self.assertEqual(serialize([1]), "{1}")

    def test_list_multiple(self):
        self.assertEqual(serialize([1, 0.2, "3", True]), '{1,0.2,"3",true}')

    def test_list_indent(self):
        self.assertEqual(
            serialize([1, 2, "3"], indent="  "), '{\n  1,\n  2,\n  "3",\n}'
        )

    def test_nested_list(self):
        self.assertEqual(serialize([1, 2, "3", [4]]), '{1,2,"3",{4}}')

    def test_nested_list_indent(self):
        self.assertEqual(
            serialize([1, 2, "3", [4]], indent="  "),
            '{\n  1,\n  2,\n  "3",\n  {\n    4,\n  },\n}',
        )

    def test_dict(self):
        self.assertEqual(serialize({1: 1, 2: 2, "3": "3"}), '{1,2,["3"]="3"}')

    def test_dict_indent(self):
        self.assertEqual(
            serialize({1: 1, 2: 2, "3": "3"}, indent="  "),
            '{\n  1,\n  2,\n  ["3"] = "3",\n}',
        )

    def test_nested_dict(self):
        self.assertEqual(
            serialize({1: 1, 2: 2, "3": {3: "3"}}), '{1,2,["3"]={[3]="3"}}'
        )

    def test_nested_dict_indent(self):
        self.assertEqual(
            serialize({1: 1, 2: 2, "3": {3: "3"}}, indent="  "),
            '{\n  1,\n  2,\n  ["3"] = {\n    [3] = "3",\n  },\n}',
        )


if __name__ == "__main__":
    unittest.main()
