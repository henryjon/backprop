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
