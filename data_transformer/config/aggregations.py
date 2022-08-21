aggregations = [
    {'name': 'freq_in_title', 'column': 'word_in_title', 'greater_then_zero': False, 'agg_type': 'avg'},
    {'name': 'freq_in_text', 'column': 'word_in_text', 'greater_then_zero': False, 'agg_type': 'avg'},
    {'name': 'count_in_title', 'column': 'word_in_title', 'greater_then_zero': True, 'agg_type': 'count'},
    {'name': 'count_in_text', 'column': 'word_in_text', 'greater_then_zero': True, 'agg_type': 'count'},
    {'name': 'part_in_title', 'column': 'word_in_title_found', 'greater_then_zero': False, 'agg_type': 'avg'},
    {'name': 'part_in_text', 'column': 'word_in_text_found', 'greater_then_zero': False, 'agg_type': 'avg'}]
