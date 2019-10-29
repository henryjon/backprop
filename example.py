import pprint

import tensorlib as t

pp = pprint.PrettyPrinter(compact=True)

x1 = t.Variable("x1")
x2 = t.Variable("x2")


# o3 = x1 ** 2 * x2 + x2
o1 = t.Multiply(x1, x2, "o1")
o2 = t.Multiply(x1, o1, "o2")
o3 = t.Add(x2, o2, "o3")


for a, b in [(2, 1), (3, 2)]:
    o3.clear()

    x1.set_value(a)
    x2.set_value(b)

    o3.forward_calc()
    o3.backward_calc()

    print()
    pp.pprint(o3.graph_data())
    print()
    print(x1)
    print(x2)


# {'a-name': 'add-o3',
#  'b-value': 5,
#  'd-deps': [(1, {'a-name': 'x2', 'b-value': 1}),
#             (1,
#              {'a-name': 'mult-o2',
#               'b-value': 4,
#               'd-deps': [(2, {'a-name': 'x1', 'b-value': 2}),
#                          (2,
#                           {'a-name': 'mult-o1',
#                            'b-value': 2,
#                            'd-deps': [(2, {'a-name': 'x1', 'b-value': 2}),
#                                       (4,
#                                        {'a-name': 'x2', 'b-value': 1})]})]})]}

# {'name': 'x1', 'value': 2, 'grad': 4}
# {'name': 'x2', 'value': 1, 'grad': 5}

# {'a-name': 'add-o3',
#  'b-value': 20,
#  'd-deps': [(1, {'a-name': 'x2', 'b-value': 2}),
#             (1,
#              {'a-name': 'mult-o2',
#               'b-value': 18,
#               'd-deps': [(6, {'a-name': 'x1', 'b-value': 3}),
#                          (3,
#                           {'a-name': 'mult-o1',
#                            'b-value': 6,
#                            'd-deps': [(6, {'a-name': 'x1', 'b-value': 3}),
#                                       (9,
#                                        {'a-name': 'x2', 'b-value': 2})]})]})]}

# {'name': 'x1', 'value': 3, 'grad': 12}
# {'name': 'x2', 'value': 2, 'grad': 10}
