class PartialParse(object):
    def __init__(self, sentence):
        """Initializes this partial parse.

        Your code should initialize the following fields:
            self.stack: The current stack represented as a list with the top of the stack as the
                        last element of the list.
            self.buffer: The current buffer represented as a list with the first item on the
                         buffer as the first item of the list
            self.dependencies: The list of dependencies produced so far. Represented as a list of
                    tuples where each tuple is of the form (head, dependent).
                    Order for this list doesn't matter.

        The root token should be represented with the string "ROOT"

        Args:
            sentence: The sentence to be parsed as a list of words.
                      Your code should not modify the sentence.
        """
        # The sentence being parsed is kept for bookkeeping purposes. Do not use it in your code.
        self.sentence = sentence

        ### YOUR CODE HERE


        self.stack = ["ROOT"]
        self.buffer = self.sentence.copy()
        self.dependencies = []
        ### END YOUR CODE

    def parse_step(self, transition):
        """Performs a single parse step by applying the given transition to this partial parse

        Args:
            transition: A string that equals "S", "LA", or "RA" representing the shift, left-arc,
                        and right-arc transitions. You can assume the provided transition is a legal
                        transition.
        """
        ### YOUR CODE HERE
        #if transition == 'S':
        #    self.stack.append(self.buffer[0])
        #    self.buffer.pop(0)
        #    self.dependencies = self.dependencies
        #elif transition == 'LA':
        #    self.dependencies.append((self.stack[-1], self.stack[-2]))
        #    self.stack.pop(-2)
        #elif transition == "RA":
        #    self.dependencies.append((self.stack[-2], self.stack[-1]))
        #    self.stack.pop(-1)
        #print(transition)
        #print(type(transition))
        #print(self.stack)
        #print(self.buffer)
        if len(self.stack) == 1 and len(self.buffer) == 0:
            pass
        else:
            if transition == "S" and len(self.buffer) > 0:
                self.stack.append(self.buffer.pop(0))
            elif transition == "LA" and len(self.stack) > 1:
                dependent = self.stack.pop(-2)
                self.dependencies.append((self.stack[-1], dependent))
            elif transition == "RA" and len(self.stack) > 1:
                dependent = self.stack.pop(-1)
                self.dependencies.append((self.stack[-1], dependent))
            else:

                raise ValueError('Invalid transition {}'.format(transition))

        ### END YOUR CODE

    def parse(self, transitions):
        """Applies the provided transitions to this PartialParse

        Args:
            transitions: The list of transitions in the order they should be applied
        Returns:
            dependencies: The list of dependencies produced when parsing the sentence. Represented
                          as a list of tuples where each tuple is of the form (head, dependent)
        """
        for transition in transitions:
            self.parse_step(transition)
        return self.dependencies


def minibatch_parse(sentences, model, batch_size):
    """Parses a list of sentences in minibatches using a model.

    Args:
        sentences: A list of sentences to be parsed (each sentence is a list of words)
        model: The model that makes parsing decisions. It is assumed to have a function
               model.predict(partial_parses) that takes in a list of PartialParses as input and
               returns a list of transitions predicted for each parse. That is, after calling
                   transitions = model.predict(partial_parses)
               transitions[i] will be the next transition to apply to partial_parses[i].
        batch_size: The number of PartialParses to include in each minibatch
    Returns:
        dependencies: A list where each element is the dependencies list for a parsed sentence.
                      Ordering should be the same as in sentences (i.e., dependencies[i] should
                      contain the parse for sentences[i]).
    """

    ### YOUR CODE HERE
    #print(sentences)
    partial_parses = [PartialParse(s) for s in sentences]
    unfinished_parses = partial_parses.copy()

    #while unfinished_parses:
    #    transitions = model.predict(unfinished_parses[:batch_size])
    #    for i in range(min(batch_size, len(unfinished_parses))):
    #        unfinished_parses[i].parse_step(transitions[i])
    #    unfinished_parses = [p for p in unfinished_parses if not (len(p.stack) == 1 and len(p.buffer) == 0)]



    num_complete = len(unfinished_parses)// batch_size
    len_complete = num_complete * batch_size
    len_incomplete = len(unfinished_parses) - len_complete

    for i in range(num_complete):
        current_batch = unfinished_parses[(i * batch_size): ((i + 1)* batch_size)]
        print('current_batch  ', len(current_batch))
        while current_batch:
            print('before transition  ', current_batch)
            print([i.stack for i in current_batch])
            transitions = model.predict(current_batch)
            print(transitions)
            print(len(transitions))
            print('current  ', len(current_batch))
            check = []
            for j in range(len(current_batch)):
                print("j", j)
                print(current_batch)
                current_batch[j].parse_step(transitions[j])
                if len(current_batch[j].stack) == 1 and len(current_batch[j].buffer) == 0:
                    check.append(True)
            if len(check) == batch_size:
                break
            #current_batch = [p for p in current_batch if not (len(p.stack) == 1 and len(p.buffer) == 0)]
            #for k in range(len(current_batch)):
            #    if len(current_batch[k].stack) == 1 and len(current_batch[j].buffer) == 0:
            #        del current_batch[k]
            #        print("after deleting   ", current_batch)
            print(len(current_batch))

    last_batch = unfinished_parses[len_complete:]

    while last_batch:
        print("here is last batch")
        transitions = model.predict(last_batch)
        for k in range(len(last_batch)):
            last_batch[k].parse_step(transitions[k])
            if len(last_batch[k].stack) == 1 and len(last_batch[k].buffer) ==0:
                last_batch.pop(k)







    dependencies = [p.dependencies for p in partial_parses]





    #N = len(sentences)
    #partial_parses = [PartialParse(x) for x in sentences]
    #unfinished_parses = list(partial_parses)
    #while len(unfinished_parses) > 0:
    #    batch = unfinished_parses[:batch_size]
    #    transitions = model.predict(batch)
    #    completed = []
    #    for i, x in enumerate(transitions):
    #        batch[i].parse_step(x)
    #        if len(batch[i].buffer) == 0 and len(batch[i].stack) == 1:
    #            completed.append(i)

    #   for i in reversed(completed):
    #        unfinished_parses.pop(i)

    #dependencies = [pp.dependencies for pp in partial_parses]

    ### END YOUR CODE

    return dependencies


def test_step(name, transition, stack, buf, deps,
              ex_stack, ex_buf, ex_deps):
    """Tests that a single parse step returns the expected output"""
    pp = PartialParse([])
    pp.stack, pp.buffer, pp.dependencies = stack, buf, deps

    pp.parse_step(transition)
    stack, buf, deps = (tuple(pp.stack), tuple(pp.buffer), tuple(sorted(pp.dependencies)))
    assert stack == ex_stack, \
        "{:} test resulted in stack {:}, expected {:}".format(name, stack, ex_stack)
    assert buf == ex_buf, \
        "{:} test resulted in buffer {:}, expected {:}".format(name, buf, ex_buf)
    assert deps == ex_deps, \
        "{:} test resulted in dependency list {:}, expected {:}".format(name, deps, ex_deps)
    print("{:} test passed!".format(name))


def test_parse_step():
    """Simple tests for the PartialParse.parse_step function
    Warning: these are not exhaustive
    """
    test_step("SHIFT", "S", ["ROOT", "the"], ["cat", "sat"], [],
              ("ROOT", "the", "cat"), ("sat",), ())
    test_step("LEFT-ARC", "LA", ["ROOT", "the", "cat"], ["sat"], [],
              ("ROOT", "cat",), ("sat",), (("cat", "the"),))
    test_step("RIGHT-ARC", "RA", ["ROOT", "run", "fast"], [], [],
              ("ROOT", "run",), (), (("run", "fast"),))


def test_parse():
    """Simple tests for the PartialParse.parse function
    Warning: these are not exhaustive
    """
    sentence = ["parse", "this", "sentence"]
    dependencies = PartialParse(sentence).parse(["S", "S", "S", "LA", "RA", "RA"])
    dependencies = tuple(sorted(dependencies))
    expected = (('ROOT', 'parse'), ('parse', 'sentence'), ('sentence', 'this'))
    assert dependencies == expected,  \
        "parse test resulted in dependencies {:}, expected {:}".format(dependencies, expected)
    assert tuple(sentence) == ("parse", "this", "sentence"), \
        "parse test failed: the input sentence should not be modified"
    print("parse test passed!")


class DummyModel(object):
    """Dummy model for testing the minibatch_parse function
    First shifts everything onto the stack and then does exclusively right arcs if the first word of
    the sentence is "right", "left" if otherwise.
    """
    def predict(self, partial_parses):
        return [("RA" if pp.stack[1] is "right" else "LA") if len(pp.buffer) == 0 else "S"
                for pp in partial_parses]


def test_dependencies(name, deps, ex_deps):
    """Tests the provided dependencies match the expected dependencies"""
    deps = tuple(sorted(deps))
    assert deps == ex_deps, \
        "{:} test resulted in dependency list {:}, expected {:}".format(name, deps, ex_deps)


def test_minibatch_parse():
    """Simple tests for the minibatch_parse function
    Warning: these are not exhaustive
    """
    sentences = [["right", "arcs", "only"],
                 ["right", "arcs", "only", "again"],
                 ["left", "arcs", "only"],
                 ["left", "arcs", "only", "again"],
                 ["left", "arcs", "only", "again", "again"]]
    deps = minibatch_parse(sentences, DummyModel(), 2)
    test_dependencies("minibatch_parse", deps[0],
                      (('ROOT', 'right'), ('arcs', 'only'), ('right', 'arcs')))
    test_dependencies("minibatch_parse", deps[1],
                      (('ROOT', 'right'), ('arcs', 'only'), ('only', 'again'), ('right', 'arcs')))
    test_dependencies("minibatch_parse", deps[2],
                      (('only', 'ROOT'), ('only', 'arcs'), ('only', 'left')))
    test_dependencies("minibatch_parse", deps[3],
                      (('again', 'ROOT'), ('again', 'arcs'), ('again', 'left'), ('again', 'only')))
    print("minibatch_parse test passed!")

if __name__ == '__main__':
    test_parse_step()
    test_parse()
    test_minibatch_parse()
