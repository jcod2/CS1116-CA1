def pop_choices(query):
    '''
    function - return list from db column query
    :param - db query
    :return - list of the data in each db cell 
    '''
    '''
    choices = [("")]
    for item in query:
        if item[0] != "":
            choices.append(item[0])
    '''
    choices = [i[0] for i in query if i[0] != ""]
    choices.insert(0, "")
    
    return choices