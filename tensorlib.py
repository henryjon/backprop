class Node:
    def __init__(self, name):
        self.name = name
        self.value = None


class Variable(Node):
    def __init__(self, name):
        super().__init__(name)
        self.grad = 0

    def clear(self):
        self.value = None
        self.grad = 0

    def set_value(self, value):
        self.value = value

    def forward_calc(self):
        pass

    def backward_calc(self, v):
        self.grad += v

    def graph_data(self):
        return {"a-name": self.name, "b-value": self.value}

    def __str__(self):
        return str({"name": self.name, "value": self.value, "grad": self.grad})


class Operation(Node):
    def __init__(self, name, forward, dependents, dependent_weights_fn):
        super().__init__(name)

        self.weights = None

        self.forward = forward
        self.dependent_weights_fn = dependent_weights_fn
        self.dependents = dependents

    def clear(self):
        self.value = None
        self.weights = None

        for d in self.dependents:
            d.clear()

    def forward_calc(self):

        for d in self.dependents:
            d.forward_calc()

        self.value = self.forward(*[d.value for d in self.dependents])

    def backward_calc(self, w=1):

        self.weights = self.dependent_weights_fn(w, self.dependents)

        for d, w in zip(self.dependents, self.weights):
            d.backward_calc(w)

    def graph_data(self):
        return {
            "a-name": self.name,
            "b-value": self.value,
            "d-deps": list(
                zip(self.weights, [d.graph_data() for d in self.dependents])
            ),
        }


class Add(Operation):
    def __init__(self, t1, t2, name):
        super().__init__(
            forward=lambda x1, x2: x1 + x2,
            dependents=[t1, t2],
            dependent_weights_fn=lambda w, deps: [w, w],
            name=f"add-{name}",
        )


class Multiply(Operation):
    def __init__(self, t1, t2, name):
        super().__init__(
            forward=lambda x1, x2: x1 * x2,
            dependents=[t1, t2],
            dependent_weights_fn=lambda v, deps: [
                v * x.value for x in [deps[1], deps[0]]
            ],
            name=f"mult-{name}",
        )
