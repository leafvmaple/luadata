import unittest
from serialize import serialize
from unserialize import unserialize


class TestSerializeMethods(unittest.TestCase):
    def test_string(self):
        self.assertEqual(serialize("str"), '"str"')

    def test_string_encoding(self):
        self.assertEqual(serialize("乗"), '"乗"')
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


class TestUnserializeMethods(unittest.TestCase):
    def test_string(self):
        with self.assertRaises(Exception):
            unserialize('"str')
        self.assertEqual(unserialize('"str"'), tuple(["str"]))

    def test_string_encoding(self):
        with self.assertRaises(Exception):
            unserialize('"乗\\"')
        self.assertEqual(unserialize('"乗"'), tuple(["乗"]))

        with self.assertRaises(Exception):
            unserialize('"乗"', "gbk")
        self.assertEqual(unserialize('"乗\\"', "gbk"), tuple(["乗"]))

    def test_bool(self):
        with self.assertRaises(Exception):
            unserialize("True")
        with self.assertRaises(Exception):
            unserialize("true1")
        self.assertEqual(unserialize("true"), tuple([True]))
        self.assertEqual(unserialize("false"), tuple([False]))

    def test_number(self):
        with self.assertRaises(Exception):
            unserialize("1..")
        with self.assertRaises(Exception):
            unserialize("..1")
        with self.assertRaises(Exception):
            unserialize("1.1.")
        self.assertEqual(unserialize(".1"), tuple([0.1]))
        self.assertEqual(unserialize("0.1"), tuple([0.1]))
        self.assertEqual(unserialize("100"), tuple([100]))
        self.assertEqual(unserialize("100."), tuple([100]))

    def test_list(self):
        with self.assertRaises(Exception):
            unserialize("{1")
        with self.assertRaises(Exception):
            unserialize("{1}}")
        with self.assertRaises(Exception):
            unserialize("{1,,}")
        self.assertEqual(unserialize("{}"), tuple([[]]))
        self.assertEqual(unserialize("{ }"), tuple([[]]))
        self.assertEqual(unserialize("{1}"), tuple([[1]]))
        self.assertEqual(unserialize("{1 }"), tuple([[1]]))
        self.assertEqual(unserialize("{ 1}"), tuple([[1]]))
        self.assertEqual(unserialize("{1,}"), tuple([[1]]))
        self.assertEqual(unserialize("{1, }"), tuple([[1]]))
        self.assertEqual(unserialize("{1 , }"), tuple([[1]]))

    def test_list_multiple(self):
        self.assertEqual(unserialize('{1,0.2,"3",true}'), tuple([[1, 0.2, "3", True]]))

    def test_list_indent(self):
        self.assertEqual(unserialize('{\n  1,\n  2,\n  "3",\n}'), tuple([[1, 2, "3"]]))

    def test_nested_list(self):
        self.assertEqual(unserialize('{1,2,"3",{4}}'), tuple([[1, 2, "3", [4]]]))

    def test_nested_list_indent(self):
        self.assertEqual(
            unserialize('{\n  1,\n  2,\n  "3",\n  {\n    4,\n  },\n}'),
            tuple([[1, 2, "3", [4]]]),
        )

    def test_dict(self):
        self.assertEqual(
            unserialize('{1,2,["3"]="3"}'), tuple([{1: 1, 2: 2, "3": "3"}])
        )

    def test_dict_indent(self):
        self.assertEqual(
            unserialize('{\n  1,\n  2,\n  ["3"] = "3",\n}'),
            tuple([{1: 1, 2: 2, "3": "3"}]),
        )

    def test_nested_dict(self):
        self.assertEqual(
            unserialize('{1,2,["3"]={[3]="3"}}'),
            tuple([{1: 1, 2: 2, "3": {3: "3"}}]),
        )

    def test_nested_dict_indent(self):
        self.assertEqual(
            unserialize('{\n  1,\n  2,\n  ["3"] = {\n    [3] = "3",\n  },\n}'),
            tuple([{1: 1, 2: 2, "3": {3: "3"}}]),
        )


if __name__ == "__main__":
    unittest.main()
