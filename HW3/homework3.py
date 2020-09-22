import copy
import time


class Predicate:
    sign = None
    name = None
    arguments_list = None
    variable_list = None
    constants_list = None

    def __init__(self):
        self.sign = 0
        self.name = ""
        self.arguments_list = []
        self.variable_list = []
        self.constants_list = []

    def __eq__(self, other):
        return self.sign == other.sign and self.name == other.name and self.arguments_list == other.arguments_list

    def display(self):
        print("********************************")
        print("sign: ", self.sign)
        print("name: ", self.name)
        print("arguments: ", self.arguments_list)
        print("variable_list: ", self.variable_list)
        print("constants_list: ", self.constants_list)


def negate_predicate(predicate):
    predicate_copy = copy.deepcopy(predicate)
    return change_sign(predicate_copy)


def get_all_sentence_nums_with_negated_predicate(negated_predicate):
    to_search = ""
    if negated_predicate.sign == -1:
        to_search = "~"
    to_search += negated_predicate.name
    if to_search in predicate_name_to_sentence_dict:
        return predicate_name_to_sentence_dict[to_search]
    # if query predicate not in kb
    return None


def substitute_new(unified_sent, substitution):
    for key, value in substitution.items():
        for pred in unified_sent:
            for i in range(0, len(pred.arguments_list)):
                if pred.arguments_list[i] == key:
                    substitute_with = value
                    if is_var(substitute_with):
                        pred.variable_list[i] = substitute_with
                        pred.constants_list[i] = None
                    else:
                        pred.variable_list[i] = None
                        pred.constants_list[i] = substitute_with
                    pred.arguments_list[i] = substitute_with


def get_sign_name_from_predicate(predicate):
    str = ""
    if predicate.sign == -1:
        str += "~"
    comma_seperated_args = ",".join(predicate.arguments_list)
    str += predicate.name + "(" + comma_seperated_args + ")"
    return str


def construct_str_from_unified_sent(unified_sent):
    list_of_unique_pred_obj = []
    list_of_unique_pred_str = []
    for pred in unified_sent:
        str = get_sign_name_from_predicate(pred)
        if str not in list_of_unique_pred_str:
            list_of_unique_pred_str.append(str)
            list_of_unique_pred_obj.append(pred)

    non_duplicate_str = " | ".join(list_of_unique_pred_str)
    return non_duplicate_str, list_of_unique_pred_obj


def is_loop_detected(unified_sent):
    return unified_sent in derived_sentences


def add_unified_sent_to_kb(rule, str_rule, counter):
    if str_rule not in derived_sentences:
        standardize_var(rule, counter)
        kb_copy.append(rule)
        counter += 1
        fill_predicate_name_to_sentence_dict(rule, kb_copy)


def unify_new(predicate, sent_pred_index, query):
    sentence_num = sent_pred_index[0]
    predicate_num = sent_pred_index[1]
    predicate_to_compare = kb_copy[sentence_num][predicate_num]

    predicate_copy = copy.deepcopy(predicate)
    predicate_to_compare_copy = copy.deepcopy(predicate_to_compare)

    substitution = {}
    for i in range(0, len(predicate_copy.arguments_list)):
        pred1_arg = predicate_copy.arguments_list[i]
        pred2_arg = predicate_to_compare_copy.arguments_list[i]

        # both are constants, check for equality
        if pred1_arg == predicate_copy.constants_list[i] and pred2_arg == predicate_to_compare_copy.constants_list[i]:
            if pred1_arg != pred2_arg:
                return False, None
        # one is constant and one is variable
        elif pred1_arg == predicate_copy.constants_list[i] and pred2_arg == predicate_to_compare_copy.variable_list[i]:
            substitution[pred2_arg] = pred1_arg
            for i in range(0, len(predicate_copy.arguments_list)):
                if predicate_copy.arguments_list[i] == pred2_arg:
                    predicate_copy.arguments_list[i] = pred1_arg
                    predicate_copy.variable_list[i] = None
                    predicate_copy.constants_list[i] = pred1_arg

            for i in range(0, len(predicate_to_compare_copy.arguments_list)):
                if predicate_to_compare_copy.arguments_list[i] == pred2_arg:
                    predicate_to_compare_copy.arguments_list[i] = pred1_arg
                    predicate_to_compare_copy.variable_list[i] = None
                    predicate_to_compare_copy.constants_list[i] = pred1_arg

        elif pred1_arg == predicate_copy.variable_list[i] and pred2_arg == predicate_to_compare_copy.constants_list[i]:
            substitution[pred1_arg] = pred2_arg
            for i in range(0, len(predicate_copy.arguments_list)):
                if predicate_copy.arguments_list[i] == pred1_arg:
                    predicate_copy.arguments_list[i] = pred2_arg
                    predicate_copy.variable_list[i] = None
                    predicate_copy.constants_list[i] = pred2_arg

            for i in range(0, len(predicate_to_compare_copy.arguments_list)):
                if predicate_to_compare_copy.arguments_list[i] == pred1_arg:
                    predicate_to_compare_copy.arguments_list[i] = pred2_arg
                    predicate_to_compare_copy.variable_list[i] = None
                    predicate_to_compare_copy.constants_list[i] = pred2_arg

        # both are variables
        elif pred1_arg == predicate_copy.variable_list[i] and pred2_arg == predicate_to_compare_copy.variable_list[i]:
            substitution[pred1_arg] = pred2_arg
            for i in range(0, len(predicate_copy.arguments_list)):
                if predicate_copy.arguments_list[i] == pred1_arg:
                    predicate_copy.arguments_list[i] = pred2_arg
                    predicate_copy.variable_list[i] = pred2_arg
                    predicate_copy.constants_list[i] = None

            for i in range(0, len(predicate_to_compare_copy.arguments_list)):
                if predicate_to_compare_copy.arguments_list[i] == pred1_arg:
                    predicate_to_compare_copy.arguments_list[i] = pred2_arg
                    predicate_to_compare_copy.variable_list[i] = pred2_arg
                    predicate_to_compare_copy.constants_list[i] = None

    alpha = copy.deepcopy(query)
    alpha.remove(predicate)

    gamma = copy.deepcopy(kb_copy[sentence_num])
    gamma.remove(predicate_to_compare)

    unified_sent = alpha + gamma
    # print("substitution: ", substitution)
    substitute_new(unified_sent, substitution)
    return True, unified_sent


def is_query_true(query):
    if time.time() > threshold:
        # print("*******TIME LIMIT EXCEEDED*****")
        return False

    for predicate in query:
        negated_predicate = negate_predicate(predicate)
        sent_nums = get_all_sentence_nums_with_negated_predicate(negated_predicate)
        if not sent_nums:
            continue
        for sent_pred_index in sent_nums:
            is_unifyable, unified_sentence = unify_new(predicate, sent_pred_index, query)
            if not is_unifyable:
                continue
            if len(unified_sentence) == 0:
                return True
            str_unified_sent, unified_sentence = construct_str_from_unified_sent(unified_sentence)
            add_unified_sent_to_kb(unified_sentence, str_unified_sent, counter)

            if is_loop_detected(str_unified_sent):
                continue
            derived_sentences.append(str_unified_sent)
            value = is_query_true(unified_sentence)
            if value:
                return True
    return False


def parse_to_predicate(atomic_sentence):
    split_query = atomic_sentence.split("(")
    p = Predicate()
    if "~" in split_query[0]:
        p.sign = -1
        p.name = split_query[0].split("~")[1]
    else:
        p.sign = 0
        p.name = split_query[0]

    split_arg_list = split_query[1].strip(")").split(",")
    arg_list = []
    for arg in split_arg_list:
        arg_list.append(arg.lstrip().rstrip())

    for arg in arg_list:
        arg = arg.lstrip().rstrip()
        if is_var(arg):
            p.variable_list.append(arg)
        else:
            p.variable_list.append(None)
        if is_constant(arg):
            p.constants_list.append(arg)
        else:
            p.constants_list.append(None)
    p.arguments_list = arg_list
    return p


def change_sign(predicate):
    if predicate.sign == 0:
        predicate.sign = -1
    else:
        predicate.sign = 0
    return predicate


def is_atomic(sentence_in_kb):
    return '=>' not in sentence_in_kb and '&' not in sentence_in_kb


def is_and_separated_sentence(sentence_in_kb):
    return '=>' not in sentence_in_kb and '&' in sentence_in_kb


def is_var(arg):
    return (len(arg) == 1 and arg.islower()) or (len(arg) > 1 and arg[0].islower())


def is_constant(arg):
    return (len(arg) == 1 and arg.isupper()) or (len(arg) > 1 and arg[0].isupper())


def standardize_var(rule, sent_num):
    for pred in rule:
        arg_list = pred.arguments_list
        var_list = pred.variable_list
        for i in range(0, len(arg_list)):
            if is_var(arg_list[i]):
                var_str = arg_list[i]
                if var_str[len(arg_list[i]) - 1].isdigit():
                    var_str = var_str[0:len(arg_list[i]) - 1]
                standardized_var = var_str + str(sent_num)
                var_list[i] = standardized_var
                arg_list[i] = standardized_var


# returns list of predicates in cnf version of given sentence
def parse_kb(sentence_in_kb):
    rule_list = []

    if is_atomic(sentence_in_kb):
        rule = []
        rule.append(parse_to_predicate(sentence_in_kb))
        rule_list.append(rule)

    elif is_and_separated_sentence(sentence_in_kb):
        split_sent = sentence_in_kb.split("&")
        for s in split_sent:
            rule = []
            rule.append(parse_to_predicate(s.lstrip().rstrip()))
            rule_list.append(rule)
    else:
        rule = []
        premise, conclusion = sentence_in_kb.split("=>")[0].lstrip().rstrip(), sentence_in_kb.split("=>")[
            1].lstrip().rstrip()
        split_premises = premise.split("&")
        for atomic_sent in split_premises:
            rule.append(change_sign(parse_to_predicate(atomic_sent.lstrip().rstrip())))
        rule.append(parse_to_predicate(conclusion))
        rule_list.append(rule)
    return rule_list


def write_to_output(answer_list):
    with open("output.txt", "w") as f:
        output_str = ""
        for ans in answer_list:
            if ans:
                output_str += "TRUE\n"
            else:
                output_str += "FALSE\n"
        output_str = output_str.rstrip("\n")
        f.write(output_str)


queries = []
kb_str = []
kb = []
kb_copy = []
predicate_name_to_sentence_dict = {}
derived_sentences = []
counter = 0
start_time = 0
threshold = 0
with open("input.txt") as f:
    no_of_queries = int(f.readline().strip("\n"))
    for i in range(0, no_of_queries):
        query_str = f.readline().strip("\n")
        queries.append(parse_to_predicate(query_str))

    no_of_statements_in_kb = int(f.readline().strip("\n"))
    for i in range(0, no_of_statements_in_kb):
        kb_str.append(f.readline().strip("\n"))

for sentence in kb_str:
    rule_list = parse_kb(sentence)
    for rule in rule_list:
        kb.append(rule)

for rule in kb:
    standardize_var(rule, kb.index(rule))


def fill_predicate_name_to_sentence_dict(rule, knowledge_base):
    for predicate in rule:
        if predicate.sign == -1:
            predicate_sign_name = "~" + predicate.name
        else:
            predicate_sign_name = predicate.name
        if predicate_sign_name not in predicate_name_to_sentence_dict:
            predicate_name_to_sentence_dict[predicate_sign_name] = [(knowledge_base.index(rule), rule.index(predicate))]
        else:
            predicate_name_to_sentence_dict[predicate_sign_name].append(
                (knowledge_base.index(rule), rule.index(predicate)))


# find if query is true or false
answer_list = []
for query in queries:
    kb_copy = copy.deepcopy(kb)

    for rule in kb_copy:
        fill_predicate_name_to_sentence_dict(rule, kb_copy)

    counter = len(kb_copy)
    negated_query = negate_predicate(query)
    new_rule = [negated_query]
    add_unified_sent_to_kb(new_rule, query, counter)

    derived_sentences.append(get_sign_name_from_predicate(negated_query))

    start_time = time.time()
    threshold = start_time + 30
    try:
        ans = is_query_true([negated_query])
        answer_list.append(ans)
    except:
        # print("******* reached recurssion depth *******")
        answer_list.append(False)

    derived_sentences.clear()
    kb_copy.clear()
    predicate_name_to_sentence_dict.clear()
    # print("over")

write_to_output(answer_list)
